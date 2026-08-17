from __future__ import annotations
from pathlib import Path
from .common import load_json,write_json,iso

def state_path(phase_root):return Path(phase_root)/'artifacts'/'state'/'promotion_state.json'
def default_state():return {'record_type':'AD_V3_P04_PROMOTION_STATE','state':'SHADOW_COMMISSIONING','updated_at_utc':iso(),'production_direction_authority':False,'production_trade_permission_authority':False,'trade_execution_authority':'NONE','v2_baseline_retained':True,'automatic_promotion_forbidden':True}
def load_state(phase_root):
 p=state_path(phase_root);return load_json(p,default_state()) if p.exists() else default_state()
def save_state(phase_root,s):write_json(state_path(phase_root),s);return s
def machine_enforced_gate_ids(phase_root):return tuple((load_json(Path(phase_root)/'config/promotion_policy.json',{}) or {}).get('promotion_requires') or ())
def enforce_declared_gates(policy,gate_results):
 if policy.get('automatic_promotion_forbidden') is not True:raise ValueError('AUTOMATIC_PROMOTION_POLICY_NOT_FAIL_CLOSED')
 declared=list(policy.get('promotion_requires') or []);machine=list(machine_enforced_gate_ids(Path(__file__).resolve().parents[1]))
 if declared!=machine:raise ValueError('PROMOTION_POLICY_IMPLEMENTATION_GATE_DRIFT')
 missing=[g for g in declared if g not in gate_results];failed=[g for g in declared if gate_results.get(g) is not True]
 if missing:raise ValueError('PROMOTION_GATES_UNAVAILABLE:'+','.join(missing))
 if failed:raise ValueError('PROMOTION_GATES_FAILED:'+','.join(failed))
 return True
def collect_machine_gate_results(phase_root,commissioning_state=None,approve=False):
 from AD_V3_PHASE_12_FINAL_CERTIFICATION_PRODUCTION_FREEZE.runtime.gates import collect
 return collect(approve=approve,deep=False)[0]
def promote(phase_root,commissioning_state=None,approve=False):
 from AD_V3_PHASE_12_FINAL_CERTIFICATION_PRODUCTION_FREEZE.runtime.promotion import perform_promotion
 return perform_promotion(approve)
def rollback(phase_root):
 from AD_V3_PHASE_12_FINAL_CERTIFICATION_PRODUCTION_FREEZE.runtime.promotion import perform_rollback
 return perform_rollback()
