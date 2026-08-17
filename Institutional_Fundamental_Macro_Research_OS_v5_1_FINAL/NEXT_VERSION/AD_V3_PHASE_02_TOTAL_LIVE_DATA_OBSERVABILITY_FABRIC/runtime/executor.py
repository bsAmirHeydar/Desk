from __future__ import annotations
import json, os, pathlib, hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from .common import iso, load_json, write_json, append_jsonl, stable_id
from .planner import build_plan
from .http_client import PublicHttpClient
from . import extractors

SUCCESS_STATES={"OBSERVED_CURRENT","OBSERVED_DELAYED","LATEST_VALID","RELEASE_NOT_DUE","PUBLIC_PROXY","MODEL_DERIVED"}
FAIL_STATES={"FETCH_FAILED","PARSE_FAILED","UNKNOWN_TRUE","STALE"}
GAP_STATES={"PAID_ONLY","PRIVATE_UNOBSERVABLE"}


def _source_map(reg): return {x['source_id']:x for x in reg['sources']}
def _fact_map(reg): return {x['fact_id']:x for x in reg['contracts']}

def _format_endpoint(source, as_of):
    ep=source.get('machine_endpoint') or source.get('canonical_url') or ''
    try:
        dt=datetime.fromisoformat(as_of.replace('Z','+00:00'))
    except Exception:
        dt=datetime.now(timezone.utc)
    repl={'yyyymm':dt.strftime('%Y%m'),'yyyy':dt.strftime('%Y'),'mm':dt.strftime('%m'),'yyyymmdd':dt.strftime('%Y%m%d')}
    for k,v in repl.items(): ep=ep.replace('{'+k+'}',v)
    return ep

def _request_parts(source, as_of):
    endpoint=_format_endpoint(source,as_of)
    method=str(source.get('request_method') or 'GET').upper()
    headers=dict(source.get('request_headers') or {})
    body=None
    if source.get('request_json') is not None:
        body=json.dumps(source.get('request_json'),separators=(',',':')).encode('utf-8')
        headers.setdefault('Content-Type','application/json')
        headers.setdefault('Accept','application/json')
    elif source.get('request_body') is not None:
        rb=source.get('request_body')
        body=(rb.encode('utf-8') if isinstance(rb,str) else bytes(rb))
    return endpoint,method,headers,body

def _request_signature(source, as_of):
    endpoint,method,headers,body=_request_parts(source,as_of)
    payload={
      'endpoint':endpoint,'method':method,
      'headers':{str(k).lower():str(v) for k,v in sorted(headers.items())},
      'body_sha256':hashlib.sha256(body).hexdigest() if body is not None else None
    }
    return json.dumps(payload,sort_keys=True,separators=(',',':'))

def _fact_stub(fact, state, source_id, retrieved, value=None, warnings=None, directness=None):
    seed={'fact_id':fact['fact_id'],'source_id':source_id,'retrieved_at':retrieved,'state':state,'value':value}
    return {
      'record_type':'AD_V3_P02_FACT_OBSERVATION','observation_id':stable_id('P02OBS',seed),'phase':'AD-V3-P02','subject':'XAUUSD',
      'fact_id':fact['fact_id'],'source_id':source_id,'epistemic_state':state,'value_type':'OBJECT' if isinstance(value,dict) else 'TEXT' if isinstance(value,str) else 'NONE',
      'value':value,'unit':None,'reference_period':None,'event_time':None,'published_at':None,'first_seen_at':retrieved,'retrieved_at':retrieved,
      'revision_number':0,'supersedes_observation_id':None,'directness':directness or fact.get('directness','UNKNOWN'),'provenance_ref':None,'raw_sha256':None,
      'metadata':{},'warnings':warnings or []
    }

def _extract(fact, source, body, retrieved, raw_hash, ctype):
    t=source.get('collector_type')
    if t=='TREASURY_XML_NOMINAL': return extractors.treasury_observation(fact,source,body,retrieved,raw_hash,real=False)
    if t=='TREASURY_XML_REAL': return extractors.treasury_observation(fact,source,body,retrieved,raw_hash,real=True)
    if t=='NYFED_SOFR_JSON': return extractors.nyfed_sofr_observation(fact,source,body,retrieved,raw_hash)
    if t=='FED_H10_HTML': return extractors.fed_h10_observation(fact,source,body,retrieved,raw_hash)
    if t=='FED_H10_DAILY_INDEX_HTML': return extractors.fed_h10_daily_index_observation(fact,source,body,retrieved,raw_hash)
    if t=='BLS_API_JSON': return extractors.bls_api_observation(fact,source,body,retrieved,raw_hash)
    if t=='FRED_CSV_LATEST': return extractors.fred_csv_observation(fact,source,body,retrieved,raw_hash)
    if t=='RBI_INR_HTML': return extractors.rbi_inr_observation(fact,source,body,retrieved,raw_hash)
    if t=='CENSUS_RETAIL_SALES_HTML': return extractors.census_retail_sales_observation(fact,source,body,retrieved,raw_hash)
    if t=='FED_H10_INR_HTML': return extractors.fed_h10_inr_observation(fact,source,body,retrieved,raw_hash)
    if t=='PIB_GOLD_DUTY_HTML': return extractors.pib_gold_duty_observation(fact,source,body,retrieved,raw_hash)
    if t=='WGC_SGE_WITHDRAWALS_HTML': return extractors.wgc_sge_withdrawals_observation(fact,source,body,retrieved,raw_hash)
    if t=='WGC_GOLD_PRICE_HTML': return extractors.wgc_gold_price_observation(fact,source,body,retrieved,raw_hash)
    if t=='GOLDPRICEDEV_XAU_JSON': return extractors.goldpricedev_xau_observation(fact,source,body,retrieved,raw_hash)
    if t=='CME_GOLD_QUOTES_JSON': return extractors.cme_gold_quotes_observation(fact,source,body,retrieved,raw_hash)
    if t=='CME_FEDFUNDS_QUOTES_JSON': return extractors.cme_fedfunds_quotes_observation(fact,source,body,retrieved,raw_hash)
    if t=='RAW_PUBLIC_PDF_PROXY': return extractors.raw_public_pdf_proxy_observation(fact,source,body,retrieved,raw_hash)
    if t=='CFTC_DISAGG_TXT': return extractors.cftc_observation(fact,source,body,retrieved,raw_hash)
    return extractors.generic_observation(fact,source,body,retrieved,raw_hash,ctype)

def _read_fixture(fixture_dir, source):
    if not fixture_dir: return None
    base=pathlib.Path(fixture_dir)
    exts={'html':['.html','.txt'], 'json':['.json','.txt'], 'csv':['.csv','.txt'], 'xml':['.xml','.txt'], 'txt':['.txt','.csv'], 'pdf':['.pdf']}
    choices=exts.get(source.get('format'),['.txt','.html','.json','.csv','.xml'])
    for ext in choices:
        p=base/(source['source_id']+ext)
        if p.exists():
            body=p.read_bytes(); return {'ok':True,'status_code':200,'body':body,'content_type':{'html':'text/html','json':'application/json','csv':'text/csv','xml':'application/xml','pdf':'application/pdf'}.get(source.get('format'),'text/plain'),'url':'fixture://'+p.name,'error':None,'sha256':hashlib.sha256(body).hexdigest()}
    return None

def _attempt_source(source, policy, as_of, fixture_dir=None, no_network=False, client=None):
    retrieved=iso()
    if source.get('collector_type') in ('GAP_ONLY','DERIVED_SOURCE'):
        return {'source_id':source['source_id'],'attempted':False,'retrieved_at':retrieved,'status':'NON_NETWORK_CONTRACT','ok':False,'error':None,'body':None,'sha256':None,'url':source.get('machine_endpoint') or source.get('canonical_url'),'content_type':''}
    if source.get('collector_type')=='STATIC':
        return {'source_id':source['source_id'],'attempted':True,'retrieved_at':retrieved,'status':'STATIC_RESOLVED','ok':True,'error':None,'body':b'STATIC_CALENDAR_CONTRACT','sha256':hashlib.sha256(b'STATIC_CALENDAR_CONTRACT').hexdigest(),'url':source.get('canonical_url'),'content_type':'text/plain'}
    fx=_read_fixture(fixture_dir,source)
    if fx:
        return {'source_id':source['source_id'],'attempted':True,'retrieved_at':retrieved,'status':'FIXTURE_SUCCESS',**fx}
    if no_network:
        return {'source_id':source['source_id'],'attempted':False,'retrieved_at':retrieved,'status':'NETWORK_DISABLED','ok':False,'error':'network disabled','body':None,'sha256':None,'url':_format_endpoint(source,as_of),'content_type':''}
    if not client: client=PublicHttpClient(policy)
    endpoint,method,headers,body=_request_parts(source,as_of)
    r=client.fetch(source['source_id'],endpoint,method=method,data=body,headers=headers)
    ok=(r.status=='SUCCESS' and r.body is not None)
    return {
      'source_id':source['source_id'],'attempted':True,'retrieved_at':r.retrieved_at or retrieved,
      'status':r.status,'ok':ok,'error':r.error,'body':r.body,'sha256':r.sha256,
      'url':r.url or endpoint,'content_type':r.content_type or '','status_code':r.http_status,
      'elapsed_ms':r.elapsed_ms
    }

def _persist_raw(source_attempt, data_root):
    if not data_root or not source_attempt.get('ok') or source_attempt.get('body') is None: return None
    d=pathlib.Path(data_root)/'raw'/source_attempt['source_id']; d.mkdir(parents=True,exist_ok=True)
    ext='.bin'
    ct=(source_attempt.get('content_type') or '').lower()
    if 'json' in ct: ext='.json'
    elif 'html' in ct: ext='.html'
    elif 'xml' in ct: ext='.xml'
    elif 'csv' in ct: ext='.csv'
    elif 'pdf' in ct: ext='.pdf'
    p=d/(source_attempt['retrieved_at'].replace(':','').replace('-','')+'_'+source_attempt['sha256'][:12]+ext)
    if not p.exists(): p.write_bytes(source_attempt['body'])
    return str(p)

def _derive_fact(fact, observations, retrieved):
    by={o['fact_id']:o for o in observations if o.get('epistemic_state') in SUCCESS_STATES}
    deps=fact.get('dependencies',[])
    have=[d for d in deps if d in by]
    missing=[d for d in deps if d not in by]
    # Strict derived numeric cases.
    fid=fact['fact_id']
    if fid in ('US_5Y_BREAKEVEN','US_10Y_BREAKEVEN'):
        years='5Y' if '5Y' in fid else '10Y'
        nom=by.get(f'UST_{years}_NOMINAL_YIELD'); real=by.get(f'UST_{years}_REAL_YIELD')
        if nom and real and isinstance(nom.get('value'),(int,float)) and isinstance(real.get('value'),(int,float)):
            o=_fact_stub(fact,'MODEL_DERIVED','DERIVED_DEPENDENCIES',retrieved,nom['value']-real['value'],directness='DERIVED')
            o['value_type']='NUMBER'; o['unit']='percent'; o['metadata']={'dependencies':[nom['observation_id'],real['observation_id']],'formula':'nominal-real'}; return o
    if fid=='US_5Y5Y_FORWARD_INFLATION':
        b5=by.get('US_5Y_BREAKEVEN'); b10=by.get('US_10Y_BREAKEVEN')
        if b5 and b10 and isinstance(b5.get('value'),(int,float)) and isinstance(b10.get('value'),(int,float)):
            try:
                v=((((1+b10['value']/100.0)**10)/((1+b5['value']/100.0)**5))**(1/5)-1)*100.0
                o=_fact_stub(fact,'MODEL_DERIVED','DERIVED_DEPENDENCIES',retrieved,v,directness='DERIVED')
                o['value_type']='NUMBER'; o['unit']='percent'; o['metadata']={'dependencies':[b5['observation_id'],b10['observation_id']],'formula':'((1+BE10)^10/(1+BE5)^5)^(1/5)-1'}; return o
            except Exception:
                pass
    state='MODEL_DERIVED' if deps and not missing else 'UNKNOWN_TRUE'
    val={'dependencies':deps,'available_dependencies':have,'missing_dependencies':missing,'semantic_derivation_deferred_to_p03':True}
    return _fact_stub(fact,state,'DERIVED_DEPENDENCIES',retrieved,val,warnings=([] if state=='MODEL_DERIVED' else ['DERIVATION_DEPENDENCIES_INCOMPLETE']),directness='DERIVED')

def _apply_lineage(observations, data_root, smap):
    if not data_root: return observations
    log=pathlib.Path(data_root)/'observations'/'gold_fact_observations.jsonl'
    previous=[]
    if log.exists():
        for line in log.read_text(encoding='utf-8',errors='ignore').splitlines():
            try: previous.append(json.loads(line))
            except Exception: pass
    latest={}
    for o in previous:
        latest[(o.get('fact_id'),o.get('source_id'))]=o
    for o in observations:
        prev=latest.get((o.get('fact_id'),o.get('source_id')))
        if not prev: continue
        if o.get('raw_sha256') and o.get('raw_sha256')==prev.get('raw_sha256'):
            o['first_seen_at']=prev.get('first_seen_at') or prev.get('retrieved_at') or o['first_seen_at']
            o['revision_number']=prev.get('revision_number',0)
            o['supersedes_observation_id']=prev.get('supersedes_observation_id')
            src=smap.get(o.get('source_id'),{})
            cad=(src.get('cadence') or '').upper()
            if o.get('epistemic_state') in ('OBSERVED_CURRENT','OBSERVED_DELAYED') and cad not in ('REALTIME','INTRADAY','EVENT'):
                o['epistemic_state']='LATEST_VALID'
                o.setdefault('warnings',[]).append('UNCHANGED_RAW_SNAPSHOT_CARRIED_AS_LATEST_VALID')
        elif o.get('raw_sha256') and prev.get('raw_sha256'):
            o['revision_number']=int(prev.get('revision_number',0))+1
            o['supersedes_observation_id']=prev.get('observation_id')
    return observations

def execute(phase_root:str|pathlib.Path, horizon='ALL', as_of_utc=None, data_root=None, fixture_dir=None, no_network=False):
    root=pathlib.Path(phase_root); as_of=as_of_utc or iso(); run_started_at=iso(); retrieved=run_started_at
    facts=load_json(root/'config/fact_acquisition_registry.json'); sources=load_json(root/'config/source_contract_registry.json'); policy=load_json(root/'config/acquisition_policy.json')
    fmap=_fact_map(facts); smap=_source_map(sources); plan=build_plan(facts,sources,horizon,as_of)
    acquisition_run_id=stable_id('P02RUN',{'plan_id':plan['plan_id'],'as_of':as_of,'horizon':horizon,'started_at':run_started_at})
    source_attempts={}; client=PublicHttpClient(policy)
    planned=list(plan['source_ids_to_attempt'])
    # Fixtures intentionally execute per source contract. Live network mode deduplicates identical endpoints.
    if fixture_dir or no_network:
        for sid in planned:
            a=_attempt_source(smap[sid],policy,as_of,fixture_dir,no_network,client); raw_path=_persist_raw(a,data_root); a['raw_path']=raw_path; source_attempts[sid]=a
    else:
        groups={}
        for sid in planned:
            src=smap[sid]
            if src.get('collector_type') in ('STATIC','GAP_ONLY','DERIVED_SOURCE'):
                key='__'+sid
            else:
                key=_request_signature(src,as_of) if policy.get('deduplicate_identical_endpoints',True) else '__'+sid
            groups.setdefault(key,[]).append(sid)
        def one(key,sids):
            rep=sids[0]; return key,sids,_attempt_source(smap[rep],policy,as_of,None,False,PublicHttpClient(policy))
        with ThreadPoolExecutor(max_workers=int(policy.get('max_concurrent_requests',6))) as pool:
            futs={pool.submit(one,k,v):(k,v) for k,v in groups.items()}
            for fut in as_completed(futs):
                group_key,group_sids=futs[fut]
                try:
                    key,sids,base=fut.result()
                except Exception as e:
                    # A network-adapter/runtime exception must become explicit coverage failure,
                    # never terminate the whole acquisition before the fail-closed gate can run.
                    sids=group_sids
                    rep=sids[0]
                    src=smap[rep]
                    base={
                      'source_id':rep,'attempted':True,'retrieved_at':iso(),
                      'status':'FETCH_FAILED','ok':False,
                      'error':'NETWORK_WORKER_EXCEPTION:'+type(e).__name__+':'+str(e),
                      'body':None,'sha256':None,'url':_format_endpoint(src,as_of),
                      'content_type':'','status_code':None,'elapsed_ms':None
                    }
                for sid in sids:
                    a=dict(base); a['source_id']=sid; raw_path=_persist_raw(a,data_root); a['raw_path']=raw_path; source_attempts[sid]=a
    observations=[]
    # Direct/static/gap observations first.
    for item in plan['fact_items']:
        if not item['applicable']: continue
        fact=fmap[item['fact_id']]; mode=fact['acquisition_mode']
        if mode in ('DERIVED_FROM_FACTS','DERIVED_FROM_STORE','CALENDAR_DERIVED'): continue
        if mode=='PRIVATE_GAP': observations.append(_fact_stub(fact,'PRIVATE_UNOBSERVABLE','PRIVATE_GAP',retrieved,warnings=['INTENTIONALLY_UNOBSERVABLE_PUBLICLY'])); continue
        if mode in ('PAID_GAP','LICENSED_GAP'): observations.append(_fact_stub(fact,'PAID_ONLY',fact['source_ids'][0],retrieved,warnings=['PAID_OR_LICENSED_GAP_NOT_PROXY_FILLED'])); continue
        if mode=='PROVIDER_GAP': observations.append(_fact_stub(fact,'UNKNOWN_TRUE',fact['source_ids'][0],retrieved,warnings=['PUBLIC_OR_PROVIDER_GAP_NO_CANONICAL_FREE_DIRECT_SOURCE'])); continue
        if mode=='STATIC_KNOWLEDGE': observations.append(_fact_stub(fact,'LATEST_VALID','STATIC_KNOWLEDGE',retrieved,{'knowledge_state':'CANONICAL_P01'},directness='STATIC')); continue
        candidates=[]
        for sid in fact['source_ids']:
            src=smap[sid]; a=source_attempts.get(sid)
            if a and a.get('attempted') and a.get('ok'):
                try: candidates.append(_extract(fact,src,a['body'],a['retrieved_at'],a['sha256'],a.get('content_type','')))
                except Exception as e: candidates.append(_fact_stub(fact,'PARSE_FAILED',sid,retrieved,warnings=['EXTRACTOR_EXCEPTION:'+type(e).__name__]))
            elif a and a.get('attempted'):
                candidates.append(_fact_stub(fact,'FETCH_FAILED',sid,retrieved,warnings=[a.get('error') or 'FETCH_FAILED']))
            elif item['must_attempt']:
                candidates.append(_fact_stub(fact,'UNKNOWN_TRUE',sid,retrieved,warnings=['SOURCE_NOT_ATTEMPTED']))
        if not candidates:
            observations.append(_fact_stub(fact,'UNKNOWN_TRUE',fact['source_ids'][0] if fact['source_ids'] else 'NONE',retrieved,warnings=['NO_ACQUISITION_RESULT']))
        else:
            # Prefer direct successful evidence; retain one canonical observation per fact plus all-source metadata.
            best=next((x for x in candidates if x['epistemic_state'] in SUCCESS_STATES),candidates[0]); best['metadata']=dict(best.get('metadata') or {}); best['metadata']['candidate_source_states']=[{'source_id':x['source_id'],'state':x['epistemic_state']} for x in candidates]; observations.append(best)
    # Derived second pass.
    for item in plan['fact_items']:
        if not item['applicable']: continue
        fact=fmap[item['fact_id']]
        if fact['acquisition_mode'] in ('DERIVED_FROM_FACTS','DERIVED_FROM_STORE','CALENDAR_DERIVED'):
            observations.append(_derive_fact(fact,observations,retrieved))
    observations=_apply_lineage(observations,data_root,smap)
    # Bind every observation to this exact acquisition run. P03 must never infer
    # current-run membership from a receipt timestamp alone.
    for o in observations:
        o['acquisition_run_id']=acquisition_run_id
    observation_cutoff_utc=max([o.get('retrieved_at') or run_started_at for o in observations] or [run_started_at])
    # Coverage gate.
    obs_by={o['fact_id']:o for o in observations}
    mandatory=[x for x in plan['fact_items'] if x['applicable'] and x['must_attempt']]
    unattempted=[]; failures=[]
    for item in mandatory:
        fact=fmap[item['fact_id']]
        actual=[source_attempts.get(s) for s in fact['source_ids'] if s in source_attempts]
        if not any(a and a.get('attempted') for a in actual): unattempted.append(fact['fact_id'])
        o=obs_by.get(fact['fact_id'])
        if item['block_on_failure'] and (not o or o.get('epistemic_state') in FAIL_STATES): failures.append({'fact_id':fact['fact_id'],'state':o.get('epistemic_state') if o else 'MISSING'})
    private_gaps=[o['fact_id'] for o in observations if o['epistemic_state']=='PRIVATE_UNOBSERVABLE']; paid_gaps=[o['fact_id'] for o in observations if o['epistemic_state']=='PAID_ONLY']
    public_provider_gaps=[o['fact_id'] for o in observations if o['epistemic_state']=='UNKNOWN_TRUE' and 'PUBLIC_OR_PROVIDER_GAP_NO_CANONICAL_FREE_DIRECT_SOURCE' in o.get('warnings',[])]
    blocked=bool(unattempted or failures)
    degraded=(not blocked) and bool(private_gaps or paid_gaps or public_provider_gaps or any(o['epistemic_state'] in ('PUBLIC_PROXY','UNKNOWN_TRUE') for o in observations))
    run_state='BLOCKED' if blocked else ('DEGRADED' if degraded else 'PASS')
    attempted_ids=[s for s,a in source_attempts.items() if a.get('attempted')]
    run_completed_at=iso()
    receipt={
      'record_type':'AD_V3_P02_COVERAGE_RECEIPT','receipt_id':stable_id('P02COV',{'plan_id':plan['plan_id'],'acquisition_run_id':acquisition_run_id,'completed_at':run_completed_at}),'phase':'AD-V3-P02','subject':'XAUUSD','as_of_utc':as_of,'generated_at_utc':run_completed_at,'horizon':horizon,
      'acquisition_run_id':acquisition_run_id,'acquisition_started_at_utc':run_started_at,'acquisition_completed_at_utc':run_completed_at,'observation_cutoff_utc':observation_cutoff_utc,
      'analysis_admission':run_state,'analysis_may_start':not blocked,'direction_authority_granted':False,'trade_permission_authority_granted':False,
      'fact_counts':{'p01_total':facts['contract_count'],'applicable':sum(1 for x in plan['fact_items'] if x['applicable']),'mandatory_attempt':len(mandatory),'observations':len(observations),'private_gaps':len(private_gaps),'paid_gaps':len(paid_gaps),'provider_gaps':len(public_provider_gaps),'unattempted_blocking':len(unattempted),'failed_blocking':len(failures)},
      'source_counts':{'planned_unique':len(plan['source_ids_to_attempt']),'attempted_unique':len(attempted_ids),'unique_endpoints':len({(a.get('url') or a.get('source_id')) for a in source_attempts.values()}),'deduplicated':True},
      'unattempted_blocking_facts':unattempted,'failed_blocking_facts':failures,'private_unobservable_facts':private_gaps,'paid_only_facts':paid_gaps,'provider_gap_facts':public_provider_gaps,
      'zero_silent_omission':len(obs_by)==sum(1 for x in plan['fact_items'] if x['applicable']),'source_attempts':[ {k:v for k,v in a.items() if k!='body'} for a in source_attempts.values() ],
      'observability_completeness_cap_applies':bool(private_gaps or paid_gaps or public_provider_gaps),'hard_note':'P02 acquisition coverage is not Direction and cannot produce trade permission.'
    }
    if data_root:
        dr=pathlib.Path(data_root); (dr/'receipts').mkdir(parents=True,exist_ok=True); (dr/'observations').mkdir(parents=True,exist_ok=True); (dr/'plans').mkdir(parents=True,exist_ok=True)
        plan_out=dict(plan); plan_out['acquisition_run_id']=acquisition_run_id; plan_out['acquisition_started_at_utc']=run_started_at
        write_json(dr/'plans'/(plan['plan_id']+'.json'),plan_out)
        # Atomic handoff discipline: persist the complete observation set first,
        # then publish the coverage receipt last. A visible receipt therefore
        # certifies that the run's observation log has already been appended.
        for o in observations: append_jsonl(dr/'observations'/'gold_fact_observations.jsonl',o)
        write_json(dr/'receipts'/(receipt['receipt_id']+'.json'),receipt)
    return {'plan':plan,'observations':observations,'coverage_receipt':receipt}
