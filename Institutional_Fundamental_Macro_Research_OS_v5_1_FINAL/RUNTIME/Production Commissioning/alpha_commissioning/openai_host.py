from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import urlparse
import json, os, sys, traceback, hashlib
from .util import load_json, now, sha256_obj, add_runtime_paths, ensure_inside
from .openai_api import OpenAIResponsesClient, OpenAIAPIError, output_text, web_sources

class CommissionedHostError(RuntimeError):
    def __init__(self,msg,category='PERMANENT_ERROR'):
        super().__init__(msg);self.category=category

def _infer_vault(req):
    env=os.environ.get('ALPHALAB_VAULT_ROOT')
    if env:
        p=Path(env).resolve()
        if (p/'CURRENT_PRODUCTION_MANIFEST.json').is_file():return p
    candidates=[]
    ap=(req.get('prompt') or {}).get('absolute_path')
    if ap:candidates.append(Path(ap).resolve())
    for c in (req.get('context') or {}).get('canonical_context') or []:
        if c.get('absolute_path'):candidates.append(Path(c['absolute_path']).resolve())
    for p in candidates:
        for q in [p,*p.parents]:
            if (q/'CURRENT_PRODUCTION_MANIFEST.json').is_file():return q
    raise CommissionedHostError('cannot infer Alpha Lab vault root','CONFIGURATION')

def _read_ref(vault,item,key='absolute_path'):
    p=item.get(key)
    if not p: return item.get('text') or ''
    q=ensure_inside(vault,p)
    if not q.is_file():raise CommissionedHostError('referenced context file missing: '+str(q),'PERMANENT_ERROR')
    return q.read_text(encoding='utf-8',errors='replace')

def _json_parse(s):
    t=s.strip()
    if t.startswith('```'):
        lines=t.splitlines()
        if lines and lines[0].startswith('```'):lines=lines[1:]
        if lines and lines[-1].strip()=='```':lines=lines[:-1]
        t='\n'.join(lines).strip()
    return json.loads(t)

def _transport_schema(expected_names):
    return {
      'type':'object','required':['status','artifacts'],
      'properties':{
        'status':{'enum':['PRESENT','NOT_APPLICABLE','UNAVAILABLE','UNDETERMINED','ESCALATE','FAILED']},
        'reason':{'type':['string','null']},
        'artifacts':{'type':'object'}
      },
      'additionalProperties':False
    }

def _validate_process(vault,inv,body):
    errs=[]
    if body.get('status')=='PRESENT':
        arts=body.get('artifacts') or {}
        expected={x['logical_name']:x for x in inv['output_contract']['schemas']}
        for name in expected:
            if name not in arts:errs.append('missing artifact '+name)
        for name in arts:
            if name not in expected:errs.append('unexpected artifact '+name)
        add_runtime_paths(vault)
        try:from alpha_prompt_runtime.validation import validate_json_schema
        except Exception as e:return ['local schema validator unavailable: '+str(e)]
        for name,cfg in expected.items():
            if name not in arts:continue
            try:validate_json_schema(vault,cfg['schema_ref'],arts[name])
            except Exception as e:errs.append(name+': '+str(e))
    return errs

def _usage(resp):
    u=resp.get('usage') or {}
    return u.get('input_tokens'),u.get('output_tokens')

def _process(vault,req,cfg,client):
    profile_name=req.get('model_profile')
    profile=cfg['profiles'].get(profile_name)
    if not profile:raise CommissionedHostError('uncommissioned model profile: '+str(profile_name),'CONFIGURATION')
    prompt=_read_ref(vault,req.get('prompt') or {})
    ctx=req.get('context') or {}
    canon=[]
    for item in ctx.get('canonical_context') or []:
        canon.append({'path':item.get('path'),'sha256':item.get('sha256'),'content':_read_ref(vault,item)})
    material={
      'run_id':req.get('run_id'),'process_id':req.get('process_id'),'analysis_cutoff_utc':ctx.get('analysis_cutoff_utc'),
      'prompt_pack_version':ctx.get('prompt_pack_version'),'typed_input_artifacts':ctx.get('input_artifacts') or [],
      'canonical_context':canon,'runtime_evidence_snapshots':ctx.get('runtime_evidence_snapshots') or [],
      'expected_outputs':req.get('output_contract',{}).get('expected_outputs') or [],
      'output_schemas':req.get('output_contract',{}).get('schemas') or []
    }
    preamble=(
      'You are a stateless execution worker inside Alpha Lab. Execute ONLY the supplied process contract. '
      'The supplied typed artifacts and hash-pinned canonical context are the entire authorized information set. '
      'Do not use web search, outside knowledge as evidence, free conversation memory, future information, or hidden assumptions. '
      'Preserve epistemic classes: unavailable/unknown is not zero, proxy is not direct fact, inference is not observed fact. '
      'Respect the process authority exactly. Return a JSON object with status, optional reason, and artifacts. '
      'For PRESENT, include every expected artifact and no unexpected artifact. Every artifact must satisfy its supplied JSON schema. '
      'Do not wrap JSON in markdown.'
    )
    user='PROCESS PROMPT:\n'+prompt+'\n\nAUTHORIZED MATERIAL:\n'+json.dumps(material,ensure_ascii=False,separators=(',',':'))
    nbytes=len(user.encode('utf-8'))
    limit=int(cfg['context_policy']['max_materialized_input_bytes'])
    if nbytes>limit:raise CommissionedHostError('CONTEXT_BUDGET_EXCEEDED_NO_TRUNCATION bytes=%d limit=%d'%(nbytes,limit),'PERMANENT_ERROR')
    expected=[x['logical_name'] for x in req.get('output_contract',{}).get('schemas') or []]
    base={
      'model':profile['model'],'reasoning':profile['reasoning'],'store':False,'instructions':preamble,'input':user,
      'max_output_tokens':int(cfg['output_policy']['max_output_tokens']),
      'text':{'verbosity':profile.get('text_verbosity','high'),'format':{'type':'json_schema','name':'alphalab_process_transport','strict':False,'schema':_transport_schema(expected)}}
    }
    previous=None;validation=[];resp=None;body=None
    max_rep=int(cfg['output_policy'].get('schema_repair_attempts',1))
    for repair in range(max_rep+1):
        payload=dict(base)
        if repair:
            payload['input']=user+'\n\nSCHEMA REPAIR ONLY. The prior output failed local validation. Do not change the evidence set or retrieve anything new. Repair the JSON to satisfy the exact supplied schemas.\nVALIDATION ERRORS:\n'+json.dumps(validation,ensure_ascii=False)+'\nPRIOR OUTPUT:\n'+json.dumps(previous,ensure_ascii=False)
        resp=client.create(payload)
        if resp.get('status') not in (None,'completed'):
            raise CommissionedHostError('OpenAI response not completed: '+str(resp.get('status')),'TRANSIENT_ERROR')
        txt=output_text(resp)
        try:body=_json_parse(txt)
        except Exception as e:
            validation=['response is not valid JSON: '+str(e)];previous={'raw_output':txt[-12000:]}
            if repair>=max_rep:raise CommissionedHostError(validation[0],'FORMAT_INVALID')
            continue
        if not isinstance(body,dict):validation=['process response is not an object'];previous=body
        else:validation=_validate_process(vault,req,body);previous=body
        if not validation:break
        if repair>=max_rep:raise CommissionedHostError('SCHEMA_VALIDATION_FAILED: '+' | '.join(validation)[:8000],'SCHEMA_REPAIRABLE')
    process_output={
      'schema_version':'1.0.0','run_id':req['run_id'],'process_id':req['process_id'],
      'process_version':req['output_contract']['process_version'],'status':body['status'],'reason':body.get('reason'),
      'artifacts':body.get('artifacts') or {},'completed_at_utc':now()
    }
    it,ot=_usage(resp)
    return {'status':'OK','process_output':process_output,'host_receipt':{'provider':'OPENAI','model':resp.get('model') or profile['model'],'model_version':resp.get('model') or profile['model'],'request_id':resp.get('id'),'input_tokens':it,'output_tokens':ot,'temperature':None,'seed':None,'tool_profile':'NO_TOOLS_MODEL_PROCESS','configured_model':profile['model'],'reasoning':profile['reasoning'],'schema_repair_count':repair,'store':False}}

def _domain_allowed(url,domains):
    try:h=(urlparse(url).hostname or '').lower().rstrip('.')
    except Exception:return False
    for d in domains:
        x=d.lower().lstrip('www.').rstrip('.')
        hh=h[4:] if h.startswith('www.') else h
        if hh==x or hh.endswith('.'+x):return True
    return False

def _iso_leq(a,b):
    try:
        da=datetime.fromisoformat(str(a).replace('Z','+00:00')).astimezone(timezone.utc)
        db=datetime.fromisoformat(str(b).replace('Z','+00:00')).astimezone(timezone.utc)
        return da<=db
    except Exception:return False

def _retrieval_schema():
    return {'type':'object','required':['found','summary','facts','publication_time','event_time','reference_time','effective_time','vintage_id','vintage_is_official_archive','primary_url'],
      'properties':{'found':{'type':'boolean'},'summary':{'type':'string'},'facts':{'type':'array','items':{'type':'object'}},'publication_time':{'type':['string','null']},'event_time':{'type':['string','null']},'reference_time':{'type':['string','null']},'effective_time':{'type':['string','null']},'vintage_id':{'type':['string','null']},'vintage_is_official_archive':{'type':'boolean'},'primary_url':{'type':['string','null']}},'additionalProperties':False}

def _retrieve(vault,req,cfg,source_policy,client):
    contracts=req.get('source_contracts') or []
    sid=(contracts[0].get('source_id') if contracts else None) or ((req.get('requirements') or [{}])[0].get('source_id'))
    pol=source_policy['sources'].get(sid)
    if not pol:return {'status':'UNAVAILABLE','snapshots':[],'unavailable_reason':'SOURCE_NOT_COMMISSIONED'}
    if pol['access_mode'] in ('SUBSCRIPTION_UNBOUND','LICENSED_UNBOUND'):
        return {'status':'UNAVAILABLE','snapshots':[],'unavailable_reason':pol['access_mode']}
    domains=pol.get('allowed_domains') or []
    if not domains:return {'status':'UNAVAILABLE','snapshots':[],'unavailable_reason':'NO_ALLOWED_DOMAINS'}
    r=(req.get('requirements') or [{}])[0];mode=str(req.get('run_mode') or 'LIVE').upper();cut=req.get('analysis_cutoff_utc')
    historical=mode not in ('LIVE','SHADOW_LIVE')
    contract=contracts[0] if contracts else {'source_id':sid}
    if historical:
        ask=('Find an OFFICIAL archived/vintage publication on the allowed source domain that was published no later than the analysis cutoff. '
             'Use only an explicit archive/vintage identity and explicit source dates; do not infer a historical value from a current page. If those conditions cannot be proven, found=false.')
    else:
        ask=('Find the most recent source-supported information currently available on the allowed domains that is directly relevant to this source contract and requirement. '
             'Extract only explicit facts. Do not invent timestamps, values, direction, or missing fields. If decision-useful source material is not found, found=false.')
    prompt={'source_id':sid,'instrument':req.get('instrument') or r.get('instrument'),'analysis_cutoff_utc':cut,'run_mode':mode,'requirement':r,'source_contract':contract,'rule':ask}
    rp=cfg['retrieval_profile']
    payload={'model':rp['model'],'reasoning':rp['reasoning'],'store':False,
      'tools':[{'type':'web_search','filters':{'allowed_domains':domains},'search_context_size':rp.get('search_context_size','high'),'return_token_budget':rp.get('return_token_budget','unlimited')}],
      'tool_choice':rp.get('tool_choice','required'),'include':['web_search_call.action.sources'],
      'instructions':'You are Alpha Lab evidence retrieval, not market cognition. Search only the allowed domains. Return source-supported extraction, not an investment conclusion. Never turn proxy/context into direct evidence. Never invent publication/vintage clocks. For historical mode fail closed unless an official archive/vintage and its date are explicit.',
      'input':json.dumps(prompt,ensure_ascii=False),
      'max_output_tokens':12000,
      'text':{'verbosity':'high','format':{'type':'json_schema','name':'alphalab_evidence_extraction','strict':False,'schema':_retrieval_schema()}}}
    resp=client.create(payload);txt=output_text(resp)
    try:ex=_json_parse(txt)
    except Exception as e:raise CommissionedHostError('retrieval output JSON invalid: '+str(e),'FORMAT_INVALID')
    if not isinstance(ex,dict) or not ex.get('found'):return {'status':'UNAVAILABLE','snapshots':[],'unavailable_reason':'NO_ADMISSIBLE_SOURCE_MATERIAL'}
    sources=[s for s in web_sources(resp) if _domain_allowed(s.get('url',''),domains)]
    primary=ex.get('primary_url')
    if primary and _domain_allowed(primary,domains):
        if not any(s.get('url')==primary for s in sources):sources.insert(0,{'url':primary,'title':'primary'})
    if not sources:return {'status':'UNAVAILABLE','snapshots':[],'unavailable_reason':'NO_DOMAIN_VALIDATED_SOURCE_URL'}
    retrieved=now()
    if historical:
        if not ex.get('vintage_is_official_archive') or not ex.get('vintage_id') or not ex.get('publication_time') or not cut or not _iso_leq(ex['publication_time'],cut):
            return {'status':'UNAVAILABLE','snapshots':[],'unavailable_reason':'HISTORICAL_STRICT_ARCHIVE_NOT_PROVEN'}
        vi='OFFICIAL_VINTAGE_ARCHIVE';first=ex['publication_time'];vintage=str(ex['vintage_id'])
    else:
        vi='ORIGINAL_CAPTURE';first=retrieved;vintage='OPENAI_WEB_CAPTURE_'+str(resp.get('id') or hashlib.sha256(txt.encode()).hexdigest()[:16])
    raw={'schema_version':'1.0.0','source_id':sid,'requirement_id':r.get('requirement_id'),'extraction':ex,'validated_web_sources':sources,'openai_response_id':resp.get('id'),'openai_model':resp.get('model'),'analysis_cutoff_utc':cut,'run_mode':mode,'domain_allowlist':domains}
    content=json.dumps(raw,ensure_ascii=False,sort_keys=True)
    snapshot_id='SNP_C1_'+hashlib.sha256((sid+'|'+str(r.get('requirement_id'))+'|'+content).encode('utf-8')).hexdigest()[:20].upper()
    snap={'schema_version':'1.0.0','snapshot_id':snapshot_id,'requirement_id':r.get('requirement_id'),'source_id':sid,'source_uri':sources[0]['url'],'media_type':'application/json','content':content,'content_encoding':'UTF8_TEXT','publication_time':ex.get('publication_time'),'first_available_time':first,'retrieved_at':retrieved,'ingested_at':retrieved,'event_time':ex.get('event_time'),'reference_time':ex.get('reference_time'),'effective_time':ex.get('effective_time'),'vintage_id':vintage,'vintage_integrity':vi,'superseded_at':None,'metadata':{'adapter':'OPENAI_WEB_SEARCH_C1','response_id':resp.get('id'),'response_model':resp.get('model'),'allowed_domains':domains,'access_mode':pol['access_mode']}}
    return {'status':'OK','snapshots':[snap],'host_receipt':{'provider':'OPENAI','model':resp.get('model') or rp['model'],'model_version':resp.get('model') or rp['model'],'request_id':resp.get('id'),'tool_profile':'WEB_SEARCH_DOMAIN_FILTERED','store':False}}

def handle(req):
    vault=_infer_vault(req);croot=vault/'RUNTIME'/'Production Commissioning';cfg=load_json(croot/'config'/'model_bindings.json');sp=load_json(croot/'config'/'source_domain_policy.json')
    client=OpenAIResponsesClient(timeout=int(os.environ.get('ALPHALAB_OPENAI_TIMEOUT','3600')),max_attempts=int(os.environ.get('ALPHALAB_OPENAI_HTTP_ATTEMPTS','3')))
    op=req.get('operation')
    if op=='MODEL_PROCESS':return _process(vault,req,cfg,client)
    if op=='EVIDENCE_RETRIEVAL':return _retrieve(vault,req,cfg,sp,client)
    raise CommissionedHostError('unsupported commissioned host operation: '+str(op),'CONFIGURATION')

def main(argv=None):
    a=list(argv or sys.argv[1:])
    if len(a)!=2:
        print('usage: openai_host.py REQUEST.json RESPONSE.json',file=sys.stderr);return 2
    reqp=Path(a[0]);rspp=Path(a[1])
    try:
        req=json.loads(reqp.read_text(encoding='utf-8'));out=handle(req);rspp.parent.mkdir(parents=True,exist_ok=True);rspp.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');return 0
    except (OpenAIAPIError,CommissionedHostError) as e:
        cat=getattr(e,'category','PERMANENT_ERROR');out={'status':'ERROR','error':str(e),'error_category':cat};rspp.parent.mkdir(parents=True,exist_ok=True);rspp.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');print(str(e),file=sys.stderr);return 0
    except Exception as e:
        out={'status':'ERROR','error':str(e),'error_category':'PERMANENT_ERROR'};rspp.parent.mkdir(parents=True,exist_ok=True);rspp.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');traceback.print_exc();return 0
if __name__=='__main__':raise SystemExit(main())
