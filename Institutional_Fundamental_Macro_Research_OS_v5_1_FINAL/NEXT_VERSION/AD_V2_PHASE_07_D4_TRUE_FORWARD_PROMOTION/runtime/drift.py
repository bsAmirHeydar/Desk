#!/usr/bin/env python3
from __future__ import annotations
PHASE='AD-V2-P07'
def evaluate(reference,current,policy):
    alerts=[]
    r=(reference or {}).get('aggregate_metrics',{}).get('true_forward',{});c=(current or {}).get('aggregate_metrics',{}).get('true_forward',{})
    if r.get('mean_mfe_r') is not None and c.get('mean_mfe_r') is not None and r['mean_mfe_r']-c['mean_mfe_r']>policy['alerts']['mean_mfe_deterioration_r']:alerts.append('MEAN_MFE_DETERIORATION')
    if r.get('mean_mae_r') is not None and c.get('mean_mae_r') is not None and c['mean_mae_r']-r['mean_mae_r']>policy['alerts']['mae_worsening_r']:alerts.append('MAE_WORSENING')
    return {'schema_version':'1.0.0','phase':PHASE,'record_type':'V2_DRIFT_ALERT','status':'ALERT' if alerts else 'CLEAR','alerts':alerts,'recommended_action':policy.get('demotion_target') if alerts else 'NONE','automatic_authority_change':False}
