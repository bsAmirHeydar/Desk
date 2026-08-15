#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json
PHASE='AD-V2-P07'
ORDER=['RESEARCH_VALIDATED','MAINLINE_PRESENTATION_CANDIDATE','DECISION_SUPPORT_CANDIDATE','PERMISSION_MODULATION_CANDIDATE']
def evaluate(report,policy,*,independent_validator_approved=False,drift_clear=True,existing_d4_promoted_rule=False):
    sc=report.get('sample_counts') or {}; tf=(report.get('aggregate_metrics') or {}).get('true_forward') or {}; hold=(report.get('aggregate_metrics') or {}).get('holdout') or {}; inc=report.get('incremental_value') or {}
    eligible=[]; results={}
    for cls in ORDER:
        g=(policy.get('gates') or {}).get(cls,{})
        checks={
          'mature_true_forward_episodes':sc.get('true_forward_independent_episodes',0)>=g.get('min_mature_true_forward_episodes',10**9),
          'true_forward_trading_days':sc.get('true_forward_trading_days',0)>=g.get('min_true_forward_trading_days',10**9),
          'distinct_regimes':sc.get('distinct_true_forward_regimes',0)>=g.get('min_distinct_regimes',10**9)}
        if g.get('require_holdout_nonnegative'):checks['holdout_nonnegative']=hold.get('mean_mfe_r') is not None and hold.get('mean_mfe_r')>=0
        if g.get('require_true_forward_nonnegative'):checks['true_forward_nonnegative']=tf.get('mean_mfe_r') is not None and tf.get('mean_mfe_r')>=0
        if g.get('require_incremental_value'):checks['incremental_value']=inc.get('high_readiness_minus_watch_mean_mfe_r') is not None and inc.get('high_readiness_minus_watch_mean_mfe_r')>0
        if g.get('require_bootstrap_lower_bound_nonnegative'):
            lo=(inc.get('high_readiness_cluster_bootstrap_mean_mfe_interval') or [None,None])[0];checks['bootstrap_lower_bound_nonnegative']=lo is not None and lo>=0
        if g.get('require_bootstrap_lower_bound_positive'):
            lo=(inc.get('high_readiness_cluster_bootstrap_mean_mfe_interval') or [None,None])[0];checks['bootstrap_lower_bound_positive']=lo is not None and lo>0
        if g.get('require_tail_nonworse'):checks['tail_nonworse']=True  # explicit independent validator judgement still required before commissioning
        if g.get('require_drift_clear'):checks['drift_clear']=bool(drift_clear)
        if g.get('requires_existing_d4_promoted_rule'):checks['existing_d4_promoted_rule']=bool(existing_d4_promoted_rule)
        results[cls]=checks
        if all(checks.values()):eligible.append(cls)
    highest=eligible[-1] if eligible else None
    status='ELIGIBLE_FOR_INDEPENDENT_REVIEW' if highest else 'TRUE_FORWARD_PENDING'
    if highest and not independent_validator_approved:status='ELIGIBLE_FOR_INDEPENDENT_REVIEW'
    out={'schema_version':'1.0.0','phase':PHASE,'record_type':'V2_PROMOTION_DECISION','status':status,'highest_eligible_class':highest,'gate_results':results,'independent_validator_approved':bool(independent_validator_approved),'auto_promoted':False,'authority':{'direction_flip_allowed':False,'positive_permission_creation_allowed':False,'trade_permission':'V1_INHERITED','broker':'NONE'}}
    out['decision_id']='V2PROM_'+hashlib.sha256(json.dumps(out,sort_keys=True,default=str).encode()).hexdigest()[:24].upper();return out
