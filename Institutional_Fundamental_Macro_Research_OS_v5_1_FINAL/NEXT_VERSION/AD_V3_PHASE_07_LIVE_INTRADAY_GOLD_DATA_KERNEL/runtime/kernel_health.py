from __future__ import annotations
from collections import Counter
from .common import config

def evaluate(plan,observations,p02_receipt,freshness_rows):
    policy=config('gold_kernel_policy.json'); fmap={x['fact_id']:x for x in plan['facts']}; fr={x['fact_id']:x for x in freshness_rows}; obs={x['fact_id']:x for x in observations}
    live=[x for x in plan['facts'] if x['operational_tier']=='LIVE_KERNEL']; context=[x for x in plan['facts'] if x['operational_tier']=='CONTEXT_CACHE']; esc=[x for x in plan['facts'] if x['operational_tier']=='ESCALATION']
    live_ok=set(policy.get('fresh_live_states') or []); ctx_ok=set(policy.get('valid_context_states') or [])
    live_fresh=[x for x in live if (fr.get(x['fact_id']) or {}).get('freshness_state') in live_ok]
    context_valid=[x for x in context if (fr.get(x['fact_id']) or {}).get('freshness_state') in ctx_ok]
    live_bad=[x['fact_id'] for x in live if x not in live_fresh]
    context_bad=[x['fact_id'] for x in context if x not in context_valid]
    cluster=list(policy.get('market_anchor_blocking_cluster') or [])
    anchor_ok=any((fr.get(fid) or {}).get('freshness_state') in live_ok for fid in cluster)
    ratio=(len(live_fresh)/len(live)) if live else 0.0
    important=[fid for fid in policy.get('important_nonblocking_live_facts') or [] if (fmap.get(fid) or {}).get('operational_tier')=='LIVE_KERNEL' and (fr.get(fid) or {}).get('freshness_state') not in live_ok]
    live_health='HEALTHY' if anchor_ok and ratio>=float(policy.get('minimum_live_fresh_ratio_for_pass',0.7)) and not important else ('DEGRADED' if anchor_ok else 'BLOCKED')
    context_health='HEALTHY' if not context_bad else 'DEGRADED'
    escalation_health='TRIGGERED' if (plan.get('escalation') or {}).get('triggered') else 'IDLE'
    if live_health=='BLOCKED': admission='BLOCK'; may=False
    elif live_health=='HEALTHY' and context_health=='HEALTHY' and p02_receipt.get('analysis_admission')!='BLOCKED': admission='ALLOW'; may=True
    else: admission='DEGRADED_ALLOW'; may=True
    states=Counter((x.get('freshness_state') or 'UNKNOWN') for x in freshness_rows)
    return {'record_type':'AD_V3_P07_KERNEL_HEALTH','live_kernel_health':live_health,'context_health':context_health,'escalation_health':escalation_health,'overall_analysis_admission':admission,'analysis_may_start':may,'market_anchor_cluster_healthy':anchor_ok,'live_kernel_total':len(live),'live_kernel_fresh':len(live_fresh),'live_kernel_fresh_ratio':ratio,'live_kernel_unfresh_fact_ids':live_bad,'important_live_gaps':important,'context_total':len(context),'context_valid':len(context_valid),'context_invalid_fact_ids':context_bad,'escalation_total':len(esc),'freshness_state_counts':dict(states),'p02_original_admission':p02_receipt.get('analysis_admission'),'p02_original_may_start':p02_receipt.get('analysis_may_start')}
