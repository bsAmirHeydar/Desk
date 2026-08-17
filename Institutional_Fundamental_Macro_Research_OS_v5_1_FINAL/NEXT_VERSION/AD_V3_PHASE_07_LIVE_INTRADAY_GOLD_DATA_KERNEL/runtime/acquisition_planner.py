from __future__ import annotations
from collections import defaultdict, Counter
from .common import P02,load,stable_id,iso,config
from .context_cache import inspect_entry


def _fact_tier(fact,sources,kernel_policy,horizon):
    mode=fact.get('acquisition_mode')
    if mode in set(kernel_policy.get('gap_acquisition_modes') or []): return 'ESCALATION'
    if fact.get('fact_id') in set(kernel_policy.get('session_live_fact_overrides') or []) and horizon=='SESSION_1_6H': return 'LIVE_KERNEL'
    if mode in set(kernel_policy.get('non_network_acquisition_modes') or []): return 'CONTEXT_CACHE'
    live_cad=set(kernel_policy.get('live_source_cadences') or [])
    if any((sources.get(s) or {}).get('cadence') in live_cad for s in fact.get('source_ids') or []): return 'LIVE_KERNEL'
    return 'CONTEXT_CACHE'

def build_plan(horizon=None,mode='NORMAL',as_of_utc=None,cache_root=None,previous_control_room=None):
    kernel=config('gold_kernel_policy.json'); freshness=config('freshness_authority_policy.json'); cache_policy=config('context_cache_policy.json'); escalation_policy=config('escalation_policy.json')
    horizon=horizon or kernel['default_horizon']; mode=mode.upper()
    if mode not in set(kernel['acquisition_modes']): raise ValueError('UNKNOWN_P07_MODE:'+mode)
    fr=load(P02/'config/fact_acquisition_registry.json'); sr=load(P02/'config/source_contract_registry.json')
    sources={s['source_id']:s for s in sr['sources']}
    from .escalation_planner import evaluate
    escalation=evaluate(previous_control_room,escalation_policy)
    escalation_facts=set(escalation.get('eligible_fact_ids') or [])
    facts=[]; source_to_facts=defaultdict(list)
    for f in fr['contracts']:
        active=horizon in (f.get('active_horizons') or [])
        tier=_fact_tier(f,sources,kernel,horizon)
        row={'fact_id':f['fact_id'],'family':f.get('family'),'role':f.get('default_role'),'active_for_horizon':active,'operational_tier':tier,'criticality':'IMPORTANT_NONBLOCKING' if f['fact_id'] in set(kernel.get('important_nonblocking_live_facts') or []) else 'STANDARD','acquisition_mode':f.get('acquisition_mode'),'source_ids':list(f.get('source_ids') or []),'reason':'SESSION_LIVE_OR_EVENT' if tier=='LIVE_KERNEL' else ('KNOWN_GAP_OR_SPECIALIST' if tier=='ESCALATION' else 'STRUCTURAL_OR_SLOW_CONTEXT')}
        facts.append(row)
        for sid in f.get('source_ids') or []: source_to_facts[sid].append(row)
    live_cad=set(kernel.get('live_source_cadences') or [])
    gap_modes=set(kernel.get('gap_acquisition_modes') or [])
    source_rows=[]
    planned=set()
    # P02 ALL-horizon planner is the source of truth for which sources would be attempted.
    from AD_V3_PHASE_02_TOTAL_LIVE_DATA_OBSERVABILITY_FABRIC.runtime.planner import build_plan as p02_build
    p02_plan=p02_build(fr,sr,kernel.get('p02_snapshot_horizon','ALL'),as_of_utc or iso())
    planned=set(p02_plan.get('source_ids_to_attempt') or [])
    for sid in sorted(planned):
        s=sources[sid]; refs=source_to_facts.get(sid,[]); ref_tiers={x['operational_tier'] for x in refs}
        networkable=s.get('collector_type') not in ('GAP_ONLY','DERIVED_SOURCE','STATIC')
        cache_check=inspect_entry(s,as_of_utc or iso(),cache_policy,cache_root)
        escalation_selected=bool(escalation.get('triggered') and any(x['fact_id'] in escalation_facts for x in refs))
        if not networkable:
            action='KNOWN_GAP' if s.get('collector_type')=='GAP_ONLY' else 'NON_NETWORK'
            reason='NON_NETWORK_SOURCE_CONTRACT'
        elif mode=='FULL_REFRESH':
            action='LIVE_FETCH' if s.get('cadence') in live_cad else 'CONTEXT_REFRESH'; reason='FULL_REFRESH_MODE'
        elif mode=='CACHE_ONLY':
            action='CONTEXT_REUSE' if cache_check['status']=='HIT' else 'CACHE_MISS'; reason=cache_check.get('reason')
        elif escalation_selected:
            action='ESCALATION_FETCH'; reason='CONDITIONAL_ESCALATION_TRIGGERED'
        elif s.get('cadence') in live_cad:
            action='LIVE_FETCH'; reason='LIVE_OR_EVENT_CADENCE'
        elif cache_check['status']=='HIT':
            action='CONTEXT_REUSE'; reason='VALID_CONTEXT_CACHE'
        else:
            action='CONTEXT_REFRESH'; reason=cache_check.get('reason') or 'CACHE_NOT_VALID'
        source_rows.append({'source_id':sid,'cadence':s.get('cadence'),'publication_lag':s.get('publication_lag'),'collector_type':s.get('collector_type'),'referenced_fact_count':len(refs),'referenced_tiers':sorted(ref_tiers),'action':action,'reason':reason,'cache_status':cache_check.get('status'),'cache_reason':cache_check.get('reason'),'escalation_selected':escalation_selected})
    fc=Counter(x['operational_tier'] for x in facts); sc=Counter(x['action'] for x in source_rows)
    seed={'horizon':horizon,'mode':mode,'facts':[x['fact_id'] for x in facts],'sources':[(x['source_id'],x['action']) for x in source_rows],'as_of':as_of_utc}
    return {'record_type':'AD_V3_P07_ACQUISITION_PLAN','schema_version':'1.0.0','phase':'AD-V3-P07','plan_id':stable_id('P07PLAN',seed),'subject':'XAUUSD','horizon':horizon,'p02_snapshot_horizon':kernel.get('p02_snapshot_horizon','ALL'),'mode':mode,'as_of_utc':as_of_utc or iso(),'fact_universe_count':len(facts),'facts':facts,'sources':source_rows,'counts':{'fact_tiers':dict(fc),'source_actions':dict(sc),'p02_planned_sources':len(planned)},'escalation':escalation,'hard_rules':{'knowledge_universe_not_live_kernel':True,'available_not_fresh':True,'fetch_time_not_economic_time':True,'p02_acquisition_authority':True,'direction_authority':False}}
