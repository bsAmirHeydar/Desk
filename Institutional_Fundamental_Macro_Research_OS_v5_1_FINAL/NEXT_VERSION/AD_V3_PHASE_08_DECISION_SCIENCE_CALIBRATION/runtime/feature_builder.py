from __future__ import annotations
from collections import defaultdict
from .common import P03,config,load,stable_id
from .magnitude_calibrator import magnitude_from_root
from .empirical_calibration import authority_for

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

def _root_freshness(evidence,tmap,kh,kernel):
    ranks=config('dominance_policy.json')['ordinal_ranks']['freshness']; vals=[_freshness(fid,tmap.get(fid,'CONTEXT_CACHE'),kh,kernel) for fid in evidence]
    return max(vals,key=lambda x:ranks.get(x,0)) if vals else 'UNKNOWN'

def _quality(rows,contract_map):
    if not rows:return 'UNKNOWN'
    rank={'UNKNOWN':0,'LOW':1,'MEDIUM':2,'HIGH':3}; vals=[]
    for r in rows:
        c=contract_map.get(r['fact_id'],{}); direct=c.get('p02_directness')
        q='HIGH' if direct=='DIRECT' else 'MEDIUM' if direct in ('PROXY','DERIVED') else 'LOW'
        if r.get('resolution') not in ('RESOLVED','SEMANTICALLY_ADJUDICATED'): q='LOW'
        vals.append(q)
    return max(vals,key=lambda x:rank[x])

def _importance(root,evidence,tmap,freshness):
    policy=config('causal_importance_policy.json'); allowed=set(policy.get('states') or [])
    if root.get('direction') not in ('BULLISH_GOLD','BEARISH_GOLD','MIXED'):
        state='BACKGROUND' if root.get('background_bias') in ('BULLISH_GOLD','BEARISH_GOLD') else 'UNKNOWN'; return state if state in allowed else 'UNKNOWN'
    tiers={tmap.get(x,'CONTEXT_CACHE') for x in evidence}
    state='PRIMARY' if 'LIVE_KERNEL' in tiers and freshness in ('FRESH_LIVE','FRESH_FOR_HORIZON','CONTEXT_VALID') else 'SECONDARY' if 'CONTEXT_CACHE' in tiers else 'CONDITIONAL' if 'ESCALATION' in tiers else 'UNKNOWN'
    return state if state in allowed else 'UNKNOWN'

def _persistence(root,fp,previous):
    if not previous:return 'NEW'
    old=next((x for x in previous.get('calibrated_roots') or [] if x.get('root_id')==root['root_id']),None)
    if not old:return 'NEW'
    if old.get('direction')!=root.get('direction') and root.get('direction') in ('BULLISH_GOLD','BEARISH_GOLD'): return 'REVERSING'
    if old.get('direction')==root.get('direction'):
        if old.get('economic_evidence_fingerprint')==fp:return 'PERSISTENT'
        oldrank=config('magnitude_policy.json')['rank'].get(old.get('magnitude','UNKNOWN'),0); newrank=config('magnitude_policy.json')['rank'].get(root.get('_magnitude','UNKNOWN'),0)
        return 'BUILDING' if newrank>=oldrank else 'FADING'
    return 'UNKNOWN'

def build_root_features(p03,kernel=None,previous=None,empirical_registry=None):
    horizon=p03.get('horizon','SESSION_1_6H'); tmap=_tier_map(horizon); kh=(kernel or {}).get('kernel_health') or {}
    reason=load(P03/'config/fact_reasoning_registry.json'); cmap={x['fact_id']:x for x in reason['contracts']}; rows=(p03.get('reasoning_ledger') or {}).get('rows') or []; byroot=defaultdict(list)
    for r in rows:
        if r.get('causal_root_family'): byroot[r['causal_root_family']].append(r)
    roots=((p03.get('pressure_planes') or {}).get('causal_fundamental') or {}).get('root_states') or []; out=[]
    for root0 in roots:
        root=dict(root0); rr=byroot.get(root['root_id'],[]); evidence=list(root.get('evidence_fact_ids') or []); erows=[r for r in rr if r.get('fact_id') in set(evidence)]
        mag=magnitude_from_root(root,erows); root['_magnitude']=mag['state']; fresh=_root_freshness(evidence,tmap,kh,kernel); imp=_importance(root,evidence,tmap,fresh); qual=_quality(erows,cmap)
        fp=stable_id('P08EVID',[(r.get('fact_id'),r.get('observation_id'),r.get('effect_on_gold'),r.get('strength')) for r in erows]); pers=_persistence(root,fp,previous)
        sem_unknown=sum(1 for r in rr if r.get('reason_code')=='SEMANTIC_ADJUDICATION_REQUIRED' and r.get('effect_on_gold')=='UNKNOWN')
        emp=authority_for(empirical_registry or {'entries':[]},root['root_id'],horizon)
        out.append({'root_id':root['root_id'],'direction':root.get('direction','UNKNOWN'),'background_bias':root.get('background_bias','UNKNOWN'),'evidence_fact_ids':evidence,'fact_count_for_audit_only':len(evidence),'causal_importance':imp,'magnitude':mag['state'],'magnitude_source':mag['source'],'freshness':fresh,'evidence_quality':qual,'independence':'CANONICAL_ROOT_FAMILY_SINGLE_VOTE','persistence':pers,'semantic_unknown_count':sem_unknown,'empirical_information_state':emp['state'],'empirical_sample_state':emp['sample_state'],'empirical_sample_count':emp['sample_count'],'economic_evidence_fingerprint':fp,'current_direction_from_p03_only':True})
    return out
