from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone
import json, time, tempfile, shutil, hashlib, sys
from .common import PHASE,REPO,P02,P04,load,write,stable_id,iso,config,parse_dt
from .acquisition_planner import build_plan
from .context_cache import inspect_entry,store_source,cache_state
from .freshness_authority import classify_observation
from .kernel_health import evaluate as health_eval

# P02 remains the only acquisition/parser/observation authority.
from AD_V3_PHASE_02_TOTAL_LIVE_DATA_OBSERVABILITY_FABRIC.runtime import executor as p02_executor
from AD_V3_PHASE_02_TOTAL_LIVE_DATA_OBSERVABILITY_FABRIC.runtime.http_client import PublicHttpClient as OriginalHttpClient, FetchResult

_EXT={'html':['.html','.txt'],'json':['.json','.txt'],'csv':['.csv','.txt'],'xml':['.xml','.txt'],'txt':['.txt','.csv'],'pdf':['.pdf']}
_CT={'html':'text/html','json':'application/json','csv':'text/csv','xml':'application/xml','txt':'text/plain','pdf':'application/pdf'}

def _fixture_body(fixture_dir,source):
    if not fixture_dir: return None
    base=Path(fixture_dir)
    for ext in _EXT.get(source.get('format'),['.txt','.html','.json','.csv','.xml','.pdf']):
        p=base/(source['source_id']+ext)
        if p.exists():
            b=p.read_bytes(); return b,_CT.get(source.get('format'),'application/octet-stream'),p
    return None

class _KernelHttpClient:
    def __init__(self, policy, *, source_map, cache_hits, cache_root, cache_policy, as_of_utc, mode, fixture_network_dir=None):
        self.delegate=OriginalHttpClient(policy); self.source_map=source_map; self.cache_hits=cache_hits; self.cache_root=cache_root; self.cache_policy=cache_policy; self.as_of=as_of_utc; self.mode=mode; self.fixture_network_dir=fixture_network_dir
    def fetch(self,source_id,url,method='GET',data=None,headers=None):
        started=time.monotonic(); source=self.source_map[source_id]
        if source_id in self.cache_hits:
            entry=self.cache_hits[source_id]['entry']; body_path=Path(self.cache_hits[source_id]['body_path']); body=body_path.read_bytes()
            return FetchResult(source_id,'p07-cache://'+source_id+'/'+entry['raw_sha256'],'SUCCESS',200,_CT.get(source.get('format'),'application/octet-stream'),body,None,iso(),hashlib.sha256(body).hexdigest(),int((time.monotonic()-started)*1000))
        fx=_fixture_body(self.fixture_network_dir,source)
        if fx:
            body,ctype,p=fx
            return FetchResult(source_id,'fixture-network://'+p.name,'SUCCESS',200,ctype,body,None,iso(),hashlib.sha256(body).hexdigest(),int((time.monotonic()-started)*1000))
        if self.mode=='CACHE_ONLY':
            return FetchResult(source_id,'p07-offline://'+source_id,'FETCH_FAILED',None,None,None,'P07_CACHE_ONLY_MISS',iso(),None,int((time.monotonic()-started)*1000))
        return self.delegate.fetch(source_id,url,method=method,data=data,headers=headers)


def _load_previous_control_room(output_root=None):
    p=Path(output_root) if output_root else P04/'artifacts'
    f=p/'latest'/'latest_control_room.json'
    try: return load(f) if f.exists() else None
    except Exception: return None

def _rewrite_current_observations(data_root,acquisition_run_id,annotations):
    p=Path(data_root)/'observations'/'gold_fact_observations.jsonl'
    if not p.exists(): return
    out=[]
    for line in p.read_text(encoding='utf-8-sig').splitlines():
        if not line.strip(): continue
        o=json.loads(line)
        if o.get('acquisition_run_id')==acquisition_run_id and o.get('fact_id') in annotations:
            meta=dict(o.get('metadata') or {}); meta['p07_kernel']=annotations[o['fact_id']]; o['metadata']=meta
        out.append(json.dumps(o,ensure_ascii=False,separators=(',',':')))
    tmp=p.with_suffix('.tmp'); tmp.write_text('\n'.join(out)+'\n',encoding='utf-8'); tmp.replace(p)

def _source_health(attempt,source):
    if source.get('collector_type')=='GAP_ONLY':
        ac=(source.get('access_class') or '').upper()
        if 'PRIVATE' in ac: return 'PRIVATE_GAP'
        if 'PAID' in ac or 'LICENSE' in ac: return 'PAID_GAP'
        return 'PROVIDER_GAP'
    if not attempt: return 'UNAVAILABLE'
    if str(attempt.get('url') or '').startswith('p07-cache://'): return 'HEALTHY_CACHE'
    st=attempt.get('status')
    if st in ('SUCCESS','STATIC_RESOLVED','FIXTURE_SUCCESS'): return 'HEALTHY'
    err=str(attempt.get('error') or '')
    if 'NOT_PUBLISHED' in err: return 'NOT_PUBLISHED'
    if 'PARSE' in err: return 'PARSER_FAILURE'
    return 'TRANSIENT_FAILURE' if attempt.get('attempted') else 'UNAVAILABLE'

def _governed_coverage(p02_receipt,health,plan,run_id):
    adm=health['overall_analysis_admission']; mapped={'ALLOW':'PASS','DEGRADED_ALLOW':'DEGRADED','BLOCK':'BLOCKED'}[adm]
    blockers=[]
    if mapped=='BLOCKED':
        blockers=[{'fact_id':fid,'state':'P07_CRITICAL_LIVE_UNAVAILABLE'} for fid in config('gold_kernel_policy.json').get('market_anchor_blocking_cluster') or [] if fid in health.get('live_kernel_unfresh_fact_ids',[])]
    return {
      **p02_receipt,
      'record_type':'AD_V3_P07_GOVERNED_COVERAGE_RECEIPT','phase':'AD-V3-P07',
      'receipt_id':stable_id('P07COV',{'p02':p02_receipt.get('receipt_id'),'plan':plan.get('plan_id'),'health':health}),
      'p02_original_receipt_id':p02_receipt.get('receipt_id'),'p02_original_analysis_admission':p02_receipt.get('analysis_admission'),
      'analysis_admission':mapped,'analysis_may_start':bool(health.get('analysis_may_start')),
      'failed_blocking_facts':blockers,'unattempted_blocking_facts':[],
      'p07_kernel':{'run_id':run_id,'plan_id':plan.get('plan_id'),'mode':plan.get('mode'),'horizon':plan.get('horizon'),'health':health,'knowledge_universe_preserved':True,'p02_acquisition_authority_preserved':True},
      'hard_note':'P07 governs operational admission by critical live freshness; P02 original coverage remains preserved and auditable. P07 has no Direction or trade-permission authority.'
    }

def run_kernel(repo_root=None,horizon=None,mode='NORMAL',as_of_utc=None,data_root_override=None,output_root_override=None,fixture_network_dir=None):
    start=time.monotonic(); repo=Path(repo_root) if repo_root else REPO; mode=mode.upper(); asof=as_of_utc or iso(); horizon=horizon or config('gold_kernel_policy.json')['default_horizon']
    data=Path(data_root_override) if data_root_override else P02/'artifacts'/'live_store'; out=Path(output_root_override) if output_root_override else PHASE/'artifacts'
    run_id=stable_id('P07RUN',{'as_of':asof,'horizon':horizon,'mode':mode,'data':str(data),'nonce':time.time_ns()}); rd=out/'runs'/run_id; rd.mkdir(parents=True,exist_ok=False)
    previous=_load_previous_control_room()
    plan_started=time.monotonic(); plan=build_plan(horizon,mode,asof,out/'context_cache',previous); planning_ms=int((time.monotonic()-plan_started)*1000); write(rd/'acquisition_plan.json',plan)
    sr=load(P02/'config/source_contract_registry.json'); smap={s['source_id']:s for s in sr['sources']}; cache_policy=config('context_cache_policy.json')
    cache_hits={}
    for row in plan['sources']:
        if row['action']=='CONTEXT_REUSE':
            chk=inspect_entry(smap[row['source_id']],asof,cache_policy,out/'context_cache')
            if chk['status']=='HIT': cache_hits[row['source_id']]=chk
    cache_lookup_ms=0
    ClientOrig=p02_executor.PublicHttpClient
    class ClientFactory:
        def __init__(self,policy):
            self.inner=_KernelHttpClient(policy,source_map=smap,cache_hits=cache_hits,cache_root=out/'context_cache',cache_policy=cache_policy,as_of_utc=asof,mode=mode,fixture_network_dir=fixture_network_dir)
        def fetch(self,*a,**k): return self.inner.fetch(*a,**k)
    p02_executor.PublicHttpClient=ClientFactory
    acq_start=time.monotonic()
    try:
        result=p02_executor.execute(P02,config('gold_kernel_policy.json').get('p02_snapshot_horizon','ALL'),asof,str(data),None,False)
    finally:
        p02_executor.PublicHttpClient=ClientOrig
    network_acquisition_ms=int((time.monotonic()-acq_start)*1000)
    p02_receipt=result['coverage_receipt']; observations=result['observations']; attempts={a['source_id']:a for a in p02_receipt.get('source_attempts') or []}
    # Refresh cache only from genuinely refreshed context sources, never from cache reuse.
    fact_tier={x['fact_id']:x['operational_tier'] for x in plan['facts']}; source_action={x['source_id']:x['action'] for x in plan['sources']}
    for row in plan['sources']:
        sid=row['source_id']; action=row['action']; a=attempts.get(sid)
        if action in ('CONTEXT_REFRESH','ESCALATION_FETCH') and a and a.get('status')=='SUCCESS' and not str(a.get('url') or '').startswith('p07-cache://'):
            store_source(smap[sid],a,observations,cache_policy,out/'context_cache')
    fresh_policy=config('freshness_authority_policy.json'); freshness_rows=[]; annotations={}
    for o in observations:
        fid=o['fact_id']; sid=o.get('source_id'); src=smap.get(sid,{})
        action=source_action.get(sid,'NON_NETWORK')
        fr=classify_observation(o,src,fact_tier.get(fid,'CONTEXT_CACHE'),action,horizon,asof,fresh_policy)
        row={'fact_id':fid,'source_id':sid,'operational_tier':fact_tier.get(fid,'CONTEXT_CACHE'),'source_action':action,'freshness_state':fr['state'],'economic_time_quality':fr.get('economic_time_quality'),'freshness_reason':fr.get('reason'),'economic_marker':({k:v for k,v in (fr.get('economic_marker') or {}).items() if k!='dt'} or None),'cache_reused':action=='CONTEXT_REUSE'}
        freshness_rows.append(row); annotations[fid]=row
    _rewrite_current_observations(data,p02_receipt['acquisition_run_id'],annotations)
    validation_started=time.monotonic(); health=health_eval(plan,observations,p02_receipt,freshness_rows); validation_ms=int((time.monotonic()-validation_started)*1000)
    governed=_governed_coverage(p02_receipt,health,plan,run_id); governed_path=write(rd/'governed_coverage.json',governed)
    write(rd/'p02_coverage_original.json',p02_receipt); write(rd/'freshness_decisions.json',{'record_type':'AD_V3_P07_FRESHNESS_DECISIONS','rows':freshness_rows}); write(rd/'kernel_health.json',health)
    action_counts=plan.get('counts',{}).get('source_actions',{}); cache_hit_count=int(action_counts.get('CONTEXT_REUSE',0)); ext_network=sum(1 for sid,a in attempts.items() if source_action.get(sid) in ('LIVE_FETCH','CONTEXT_REFRESH','ESCALATION_FETCH') and a.get('attempted') and smap.get(sid,{}).get('collector_type') not in ('STATIC','GAP_ONLY','DERIVED_SOURCE') and not str(a.get('url') or '').startswith(('p07-cache://','p07-offline://')))
    source_health=[{'source_id':sid,'health':_source_health(attempts.get(sid),smap[sid]),'action':source_action.get(sid)} for sid in sorted(smap) if sid in source_action]
    total_ms=int((time.monotonic()-start)*1000)
    receipt={
      'record_type':'AD_V3_P07_KERNEL_RUN_RECEIPT','schema_version':'1.0.0','phase':'AD-V3-P07','version':'3.7.0-live-intraday-gold-kernel','run_id':run_id,'generated_at_utc':iso(),'subject':'XAUUSD','horizon':horizon,'mode':mode,
      'plan_id':plan['plan_id'],'p02_acquisition_run_id':p02_receipt.get('acquisition_run_id'),'p02_receipt_id':p02_receipt.get('receipt_id'),'governed_coverage_receipt_id':governed.get('receipt_id'),'governed_coverage_path':str(governed_path),
      'universe':{'gold_facts':plan['fact_universe_count'],'p02_observations':len(observations),'full_current_snapshot':len(observations)==plan['fact_universe_count']},
      'kernel_health':health,'performance':{'planning_ms':planning_ms,'cache_lookup_ms':cache_lookup_ms,'network_acquisition_ms':network_acquisition_ms,'validation_ms':validation_ms,'total_p07_ms':total_ms,'network_requests':ext_network,'cache_hits':cache_hit_count,'cache_misses':int(action_counts.get('CONTEXT_REFRESH',0)+action_counts.get('CACHE_MISS',0)),'context_reused':cache_hit_count,'context_refreshed':int(action_counts.get('CONTEXT_REFRESH',0)),'escalation_attempts':int(action_counts.get('ESCALATION_FETCH',0))},
      'source_action_counts':action_counts,'source_health':source_health,'known_provider_gap_facts':p02_receipt.get('provider_gap_facts') or [],'known_private_gap_facts':p02_receipt.get('private_unobservable_facts') or [],'known_paid_gap_facts':p02_receipt.get('paid_only_facts') or [],
      'cache_state':cache_state(sr,cache_policy,asof,out/'context_cache'),'escalation':plan.get('escalation'),
      'p02_original_admission':p02_receipt.get('analysis_admission'),'analysis_admission':governed.get('analysis_admission'),'analysis_may_start':governed.get('analysis_may_start'),
      'direction_authority':False,'trade_permission_authority':False,'production_promotion_performed':False
    }
    write(rd/'kernel_run_receipt.json',receipt); latest=out/'latest'; latest.mkdir(parents=True,exist_ok=True); write(latest/'latest_kernel_receipt.json',receipt); write(latest/'latest_acquisition_plan.json',plan); write(latest/'latest_kernel_health.json',health); write(latest/'latest_governed_coverage.json',governed)
    return receipt
