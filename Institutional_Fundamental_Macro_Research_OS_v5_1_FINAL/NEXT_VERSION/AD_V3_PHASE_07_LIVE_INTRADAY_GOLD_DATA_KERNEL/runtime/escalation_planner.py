from __future__ import annotations
from pathlib import Path
from .common import load

def evaluate(previous_control_room,policy):
    if not policy.get('enabled',True): return {'triggered':False,'reasons':['DISABLED'],'eligible_fact_ids':[],'direction_authority':False}
    if not previous_control_room: return {'triggered':False,'reasons':['NO_PREVIOUS_DIAGNOSTIC_STATE'],'eligible_fact_ids':[],'direction_authority':False}
    q=previous_control_room.get('model_quality') or {}; pt=previous_control_room.get('price_transmission') or {}; dc=previous_control_room.get('decision_calibration') or {}
    reasons=[]; tr=policy.get('triggers') or {}
    if q.get('missing_driver_risk') in (tr.get('missing_driver_risk') or []): reasons.append('MISSING_DRIVER_RISK:'+str(q.get('missing_driver_risk')))
    if dc.get('missing_driver_risk') in ('HIGH','ELEVATED'): reasons.append('P08_MISSING_DRIVER_RISK:'+str(dc.get('missing_driver_risk')))
    if dc.get('contradiction') in ('PRIMARY_ROOT_CONFLICT','BALANCED_CONFLICT'): reasons.append('P08_PRIMARY_CONTRADICTION:'+str(dc.get('contradiction')))
    if pt.get('state') in (tr.get('price_transmission') or []): reasons.append('PRICE_TRANSMISSION:'+str(pt.get('state')))
    if q.get('model_completeness') in (tr.get('model_completeness') or []): reasons.append('MODEL_COMPLETENESS:'+str(q.get('model_completeness')))
    return {'triggered':bool(reasons),'reasons':reasons or ['NO_TRIGGER'],'eligible_fact_ids':list(policy.get('eligible_fact_ids') or []) if reasons else [],'direction_authority':False,'trade_permission_authority':False}
