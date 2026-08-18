from __future__ import annotations
from collections import defaultdict
from .common import P03,config,load,stable_id
from .empirical_calibration import authority_for
from AD_V31_R02_DECISION_SCIENCE_2_0.runtime.decision_science_runtime import enrich_roots

def _tier_map(horizon):
    from AD_V3_PHASE_07_LIVE_INTRADAY_GOLD_DATA_KERNEL.runtime.acquisition_planner import build_plan
    plan=build_plan(horizon=horizon,mode='FULL_REFRESH')
    return {x['fact_id']:x['operational_tier'] for x in plan['facts']}

def _freshness(fid,tier,kh,kernel):
    if fid in set((kernel or {}).get('known_provider_gap_facts') or []): return 'PROVIDER_GAP'
    if fid in set((kernel or {}).get('known_private_gap_facts') or []): return 'PRIVATE_GAP'
    if fid in set((kernel or {}).get('known_paid_gap_facts') or []): return 'PAID_GAP'
    if fid in set(kh.get('live_kernel_unfresh_fact_ids') or []): return 'CONTEXT_VALID' if tier=='LIVE_KERNEL' else 'STALE_FOR_HORIZON'
    if fid in set(kh.get('context_invalid_fact_ids') or []): return 'UNAVAILABLE'
    if tier=='LIVE_KERNEL': return 'FRESH_FOR_HORIZON'
    if tier=='CONTEXT_CACHE': return 'CONTEXT_VALID'
    return 'UNAVAILABLE'

def _persistence(root,fp,previous):
    if not previous:return 'NEW'
    old=next((x for x in previous.get('calibrated_roots') or [] if x.get('root_id')==root['root_id']),None)
    if not old:return 'NEW'
    if old.get('direction')!=root.get('direction') and root.get('direction') in ('BULLISH_GOLD','BEARISH_GOLD'): return 'REVERSING'
    if old.get('direction')==root.get('direction'):
        if old.get('economic_evidence_fingerprint')==fp:return 'PERSISTENT'
        rank={'UNKNOWN':0,'MINOR':1,'MATERIAL':2,'LARGE':3,'EXTREME':4};oldrank=rank.get(old.get('magnitude','UNKNOWN'),0);newrank=rank.get(root.get('magnitude','UNKNOWN'),0)
        return 'BUILDING' if newrank>=oldrank else 'FADING'
    return 'UNKNOWN'

def build_root_features(p03,kernel=None,previous=None,empirical_registry=None,magnitude_history=None,regime_context=None,return_timing=False):
    horizon=p03.get('horizon','SESSION_1_6H');tmap=_tier_map(horizon);kh=(kernel or {}).get('kernel_health') or {}
    reason=load(P03/'config/fact_reasoning_registry.json');cmap={x['fact_id']:x for x in reason['contracts']};rootreg=load(P03/'config/root_family_registry.json');expected={x['root_id']:list(x.get('facts') or []) for x in rootreg['roots']}
    rows=(p03.get('reasoning_ledger') or {}).get('rows') or [];byroot=defaultdict(list)
    for r in rows:
        if r.get('causal_root_family'):byroot[r['causal_root_family']].append(r)
    roots0=((p03.get('pressure_planes') or {}).get('causal_fundamental') or {}).get('root_states') or []
    roots=[]
    for root0 in roots0:
        root=dict(root0);rr=byroot.get(root['root_id'],[]);evidence=list(root.get('evidence_fact_ids') or []);erows=[r for r in rr if r.get('fact_id') in set(evidence)]
        fp=stable_id('P08EVID',[(r.get('fact_id'),r.get('observation_id'),r.get('effect_on_gold'),r.get('strength')) for r in erows]);sem_unknown=sum(1 for r in rr if r.get('reason_code')=='SEMANTIC_ADJUDICATION_REQUIRED' and r.get('effect_on_gold')=='UNKNOWN');emp=authority_for(empirical_registry or {'entries':[]},root['root_id'],horizon)
        root.update({'evidence_fact_ids':evidence,'fact_count_for_audit_only':len(evidence),'independence':'CANONICAL_ROOT_FAMILY_SINGLE_VOTE','semantic_unknown_count':sem_unknown,'empirical_information_state':emp['state'],'empirical_sample_state':emp['sample_state'],'empirical_sample_count':emp['sample_count'],'economic_evidence_fingerprint':fp,'current_direction_from_p03_only':True})
        roots.append(root)
    freshness_by_fact={fid:_freshness(fid,tmap.get(fid,'CONTEXT_CACHE'),kh,kernel) for fids in expected.values() for fid in fids}
    roots,timing=enrich_roots(p03,roots,byroot,expected,freshness_by_fact,cmap,history=magnitude_history,kernel=kernel,explicit_regime=regime_context)
    for root in roots:
        root['persistence']=_persistence(root,root['economic_evidence_fingerprint'],previous)
        root['independent_evidence_count']=(root.get('root_health') or {}).get('independent_evidence_count',0)
    return (roots,timing) if return_timing else roots
