from __future__ import annotations
from collections import Counter,defaultdict
from .common import cfg

def sample_state(n):
    for r in cfg('sample_maturity_policy.json')['overall_episode_thresholds']:
        if n>=r['min'] and (r['max'] is None or n<=r['max']):return r['state']
    return 'NO_SAMPLES'
def _dim_state(n,name):
    need=int(cfg('sample_maturity_policy.json')['dimension_min_episode_counts'][name]);return 'PROVISIONAL' if n>=need else ('EARLY' if n>=max(10,need//2) else 'INSUFFICIENT')
def compute(state,cohort_id=None):
    cohort=cohort_id or next((x.get('cohort_id') for x in reversed(state['cohorts']) if x.get('state')=='OPEN'),None)
    preds=[p for p in state['predictions'] if not cohort or p.get('cohort_id')==cohort]; outs={o['prediction_id']:o for o in state['outcomes'] if not cohort or o.get('cohort_id')==cohort}; eps=[e for e in state['episodes'] if not cohort or e.get('cohort_id')==cohort]
    prim=[e for e in eps if e.get('primary_prediction_id') in outs and next((p for p in preds if p['prediction_id']==e.get('primary_prediction_id')),{}).get('eligibility')=='VALIDATION_ELIGIBLE']
    mature=len(prim); ss=sample_state(mature); raw=len(preds); pending=sum(1 for p in preds if p['prediction_id'] not in outs); mature_uneval=0
    primary_preds=[next(p for p in preds if p['prediction_id']==e['primary_prediction_id']) for e in prim]
    primary_outs=[outs[p['prediction_id']] for p in primary_preds]
    dir_counts=Counter(o.get('direction_outcome') for o in primary_outs); perm_counts=Counter(o.get('permission_outcome') for o in primary_outs); wait_counts=Counter(o.get('wait_outcome') for o in primary_outs if o.get('wait_outcome'))
    def grouping(field):
        z=defaultdict(lambda:Counter())
        for p,o in zip(primary_preds,primary_outs):z[str(p.get(field))][o.get('direction_outcome')]+=1
        return {k:dict(v) for k,v in z.items()}
    return {'record_type':'AD_V3_P09_FORWARD_STATISTICS','active_cohort':cohort,'raw_prediction_count':raw,'episode_count':len(eps),'mature_episode_count':mature,'pending_prediction_count':pending,'mature_unevaluated_count':mature_uneval,'forward_evidence_state':ss,'direction_calibration_state':_dim_state(mature,'direction'),'strength_calibration_state':_dim_state(mature,'strength'),'dominance_calibration_state':_dim_state(mature,'dominance'),'edge_calibration_state':_dim_state(mature,'edge'),'permission_calibration_state':_dim_state(mature,'permission'),'wait_calibration_state':_dim_state(sum(wait_counts.values()),'wait'),'consumption_calibration_state':_dim_state(mature,'consumption'),'fragility_calibration_state':_dim_state(mature,'fragility'),'missing_driver_calibration_state':_dim_state(mature,'missing_driver'),'direction_counts':dict(dir_counts),'permission_counts':dict(perm_counts),'wait_counts':dict(wait_counts),'by_strength':grouping('pressure_strength'),'by_dominance':grouping('dominance_state'),'by_edge':grouping('edge_state'),'by_consumption':grouping('consumption'),'by_fragility':grouping('fragility'),'class_balance':dict(Counter(p.get('causal_direction') for p in primary_preds)),'actionable_frequency':(sum(1 for p in primary_preds if p.get('permission_candidate') in ('BUY_CANDIDATE','SELL_CANDIDATE'))/mature if mature else None),'primary_maturity_unit':'MATURE_VALIDATION_ELIGIBLE_EPISODE','fixture_samples_included':False,'replay_samples_included':False}
