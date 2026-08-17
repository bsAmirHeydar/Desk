from __future__ import annotations
from pathlib import Path
from .common import load_json, write_json, iso

def state_path(phase_root): return Path(phase_root)/'artifacts'/'state'/'promotion_state.json'
def default_state(): return {'record_type':'AD_V3_P04_PROMOTION_STATE','state':'SHADOW_COMMISSIONING','updated_at_utc':iso(),'production_direction_authority':False,'production_trade_permission_authority':False,'v2_baseline_retained':True,'automatic_promotion_forbidden':True}
def load_state(phase_root):
    p=state_path(phase_root); return load_json(p,default_state()) if p.exists() else default_state()
def save_state(phase_root,s): write_json(state_path(phase_root),s); return s
def promote(phase_root,commissioning_state,approve=False):
    if not approve: raise ValueError('EXPLICIT_OPERATOR_APPROVAL_REQUIRED')
    if commissioning_state.get('sample_state')!='PROVISIONAL': raise ValueError('TRUE_FORWARD_SAMPLE_NOT_PROVISIONAL')
    if commissioning_state.get('integrity_failures',0)!=0: raise ValueError('INTEGRITY_FAILURES_PRESENT')
    s=default_state(); s.update(state='PRODUCTION_V3',updated_at_utc=iso(),promoted_at_utc=iso(),production_direction_authority=True,production_trade_permission_authority=True,manual_operator_approval=True)
    return save_state(phase_root,s)
def rollback(phase_root):
    s=default_state(); s.update(updated_at_utc=iso(),rollback_reason='OPERATOR_ROLLBACK_TO_SHADOW')
    return save_state(phase_root,s)
