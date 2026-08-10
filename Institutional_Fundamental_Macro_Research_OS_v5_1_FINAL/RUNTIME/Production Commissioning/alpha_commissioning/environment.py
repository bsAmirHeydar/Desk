from pathlib import Path
import os, re, sys, json, subprocess
from .util import load_json,dump_json,now,data_root,add_runtime_paths,host_command_json,current_certification_surface
from .openai_api import OpenAIResponsesClient, output_text, web_sources

SECRET_RE=re.compile(r'\bsk-[A-Za-z0-9_-]{20,}\b')

def _r4(v):
    add_runtime_paths(v)
    from alpha_certification.preflight import run
    return run(v)

def doctor(vault_root):
    v=Path(vault_root).resolve();c=v/'RUNTIME'/'Production Commissioning';checks=[];errors=[]
    try:
        rm=load_json(v/'RUNTIME'/'RUNTIME_MANIFEST.json');checks += [('scientific_v213',rm.get('scientific_stack')=='V21.3.0'),('runtime_r4',rm.get('runtime_version')=='R4.0.0'),('commissioning_c1',rm.get('commissioning',{}).get('version')=='C1.0.0'),('authority_none',rm.get('authority',{}).get('direction')=='NONE' and rm.get('authority',{}).get('permission')=='NONE'),('block_only',rm.get('operational_execution',{}).get('authority')=='BLOCK_ONLY')]
    except Exception as e:errors.append('runtime manifest: '+str(e))
    try:
        pack=load_json(v/'RUNTIME'/'R2 Prompt Execution OS'/'config'/'prompt_pack.json');checks.append(('prompt_pack_1_1',pack.get('version')=='ALPHALAB_PROMPT_PACK_1.1.0'))
    except Exception as e:errors.append('prompt pack: '+str(e))
    try:
        src=load_json(v/'100 Six-Market D2 Fact Books and Production Shadow Engine'/'config'/'d2_source_registry.json');pol=load_json(c/'config'/'source_domain_policy.json');ids={x['source_id'] for x in src['sources']};mapped=set(pol['sources']);missing=sorted(ids-mapped);checks.append(('all_57_source_contracts_commissioned',len(ids)==57 and not missing));
        if missing:errors.append('unmapped source ids: '+','.join(missing))
    except Exception as e:errors.append('source policy: '+str(e))
    try:
        ok=True
        for pid in ['W30_TEMPORAL','W31_FUNDAMENTAL','W32_EXPECTATIONS_POLICY_REGIME','W33_NARRATIVE_REFLEXIVITY_CONSUMPTION','W34_POSITIONING','W35_ACTUAL_FLOW','W36_FUNDING_PLUMBING','W37_MECHANICS_CAPACITY_VOL']:
            m=load_json(v/'RUNTIME'/'R2 Prompt Execution OS'/'prompt_registry'/pid/'manifest.json')
            ok=ok and 'decision_evidence_pack' in m.get('required_inputs',[]) and 'evidence_integrity_receipt' in m.get('required_inputs',[])
        checks.append(('s3_substantive_evidence_transport',ok))
    except Exception as e:errors.append('evidence transport: '+str(e))
    try:
        ctx=(v/'RUNTIME'/'R2 Prompt Execution OS'/'alpha_prompt_runtime'/'context.py').read_text(encoding='utf-8');checks.append(('dynamic_selected_paths_hash_pinned','selected_paths' in ctx and 'canonical_context_hashes' in ctx and 'retrieval-plan path escaped vault' in ctx))
    except Exception as e:errors.append('context compiler: '+str(e))
    try:
        mb=load_json(c/'config'/'model_bindings.json');checks.append(('no_silent_model_downgrade',mb.get('automatic_model_downgrade') is False and all(x.get('model')=='gpt-5.6-sol' for x in mb['profiles'].values())))
    except Exception as e:errors.append('model bindings: '+str(e))
    try:
        repo=v.parent;templates=c/'wrappers';pairs=[('AlphaLab.ps1',repo/'AlphaLab.ps1'),('AlphaLab_Commission.ps1',repo/'AlphaLab_Commission.ps1')];ok=all(dst.is_file() and (templates/name).read_bytes()==dst.read_bytes() for name,dst in pairs);checks.append(('root_launchers_match_certified_templates',ok))
    except Exception as e:errors.append('root launcher integrity: '+str(e))
    # secret scan: only strong key-shaped tokens, not environment variable names.
    found=[]
    for p in v.rglob('*'):
        if not p.is_file() or p.suffix.lower() not in ('.md','.txt','.json','.yaml','.yml','.py','.ps1','.csv'):continue
        try:t=p.read_text(encoding='utf-8',errors='ignore')
        except Exception:continue
        if SECRET_RE.search(t):found.append(str(p.relative_to(v)))
    checks.append(('no_api_secret_in_vault',not found));
    if found:errors.append('secret-like tokens in: '+','.join(found[:10]))
    dr=data_root(v)
    try:dr.mkdir(parents=True,exist_ok=True);test=dr/'commissioning'/'.write_test';test.parent.mkdir(parents=True,exist_ok=True);test.write_text('ok',encoding='ascii');test.unlink();checks.append(('data_root_writable',True))
    except Exception as e:checks.append(('data_root_writable',False));errors.append(str(e))
    # R4 full offline remains authoritative after commissioning changes.
    try:r4=_r4(v);checks.append(('r4_full_preflight',r4.get('status')=='PASS'))
    except Exception as e:r4={'status':'FAIL','errors':[str(e)]};checks.append(('r4_full_preflight',False));errors.append('r4: '+str(e))
    failed=[n for n,ok in checks if not ok];errors+=failed
    return {'schema_version':'1.0.0','status':'PASS' if not errors else 'FAIL','classification':'C1_INSTALLED_OFFLINE_VALIDATED' if not errors else 'NOT_COMMISSIONED','checks':[{'name':n,'pass':bool(ok)} for n,ok in checks],'api_key_present':bool(os.environ.get('OPENAI_API_KEY')),'data_root':str(dr),'r4_status':r4.get('status'),'errors':errors,'created_at_utc':now()}

def certify(vault_root):
    v=Path(vault_root).resolve();dr=data_root(v);d=doctor(v);checks=list(d['checks']);errors=list(d.get('errors') or [])
    if d['status']!='PASS':
        out={'schema_version':'1.0.0','status':'FAIL','classification':'NOT_CERTIFIED','checks':checks,'errors':errors,'created_at_utc':now()};dump_json(dr/'commissioning'/'environment_receipt.json',out);return out
    if not os.environ.get('OPENAI_API_KEY'):
        out={'schema_version':'1.0.0','status':'FAIL','classification':'NOT_CERTIFIED','checks':checks+[{'name':'openai_api_key_present','pass':False}],'errors':['OPENAI_API_KEY is not set in the current environment'],'created_at_utc':now()};dump_json(dr/'commissioning'/'environment_receipt.json',out);return out
    surface=current_certification_surface(v)
    cfg=load_json(v/'RUNTIME'/'Production Commissioning'/'config'/'model_bindings.json');client=OpenAIResponsesClient(timeout=600,max_attempts=2);hp=cfg['health_profile'];model_receipt={};web_receipt={}
    try:
        schema={'type':'object','required':['ok'],'properties':{'ok':{'type':'boolean'}},'additionalProperties':False}
        resp=client.create({'model':hp['model'],'reasoning':hp['reasoning'],'store':False,'input':'Return {"ok":true}. This is an Alpha Lab production environment capability attestation.','max_output_tokens':200,'text':{'format':{'type':'json_schema','name':'alphalab_health','strict':True,'schema':schema}}})
        txt=output_text(resp);obj=json.loads(txt);ok=obj.get('ok') is True and bool(resp.get('id')) and bool(resp.get('model'));checks.append({'name':'openai_gpt_5_6_sol_responses_health','pass':ok});
        if not ok:errors.append('model health response invalid')
        model_receipt={'response_id':resp.get('id'),'configured_model':hp['model'],'returned_model':resp.get('model'),'status':resp.get('status'),'reasoning_requested':hp['reasoning'],'usage':resp.get('usage'),'store':False}
    except Exception as e:checks.append({'name':'openai_gpt_5_6_sol_responses_health','pass':False});errors.append('model health: '+str(e))
    try:
        resp=client.create({'model':hp['model'],'reasoning':{'mode':'pro','effort':'high','context':'current_turn'},'store':False,'tools':[{'type':'web_search','filters':{'allowed_domains':['developers.openai.com']},'search_context_size':'low'}],'tool_choice':'required','include':['web_search_call.action.sources'],'input':'Find the OpenAI API documentation page for web search and return its title in one sentence.','max_output_tokens':500})
        src=web_sources(resp);ok=bool(src) and all('developers.openai.com' in (x.get('url') or '') for x in src);checks.append({'name':'openai_web_search_domain_filter_health','pass':ok});
        if not ok:errors.append('web search did not return domain-filtered source evidence')
        web_receipt={'response_id':resp.get('id'),'returned_model':resp.get('model'),'sources':src,'usage':resp.get('usage'),'store':False}
    except Exception as e:checks.append({'name':'openai_web_search_domain_filter_health','pass':False});errors.append('web search health: '+str(e))
    status='PASS' if not errors and all(x.get('pass') for x in checks) else 'FAIL';out={'schema_version':'1.0.0','status':status,'classification':'ENVIRONMENT_CERTIFIED' if status=='PASS' else 'NOT_CERTIFIED','checks':checks,'model_receipt':model_receipt,'web_search_receipt':web_receipt,'source_scope_note':'Licensed/subscription/private feeds are not claimed connected by this environment attestation.','data_root':str(dr),'certification_surface_fingerprint':surface,'created_at_utc':now(),'errors':errors};dump_json(dr/'commissioning'/'environment_receipt.json',out);return out
