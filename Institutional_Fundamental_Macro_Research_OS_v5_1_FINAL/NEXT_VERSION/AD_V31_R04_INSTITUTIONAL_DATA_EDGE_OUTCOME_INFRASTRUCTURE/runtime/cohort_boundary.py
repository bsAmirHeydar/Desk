from __future__ import annotations
from pathlib import Path
from .common import PHASE,canonical_hash,iso,load_json,save_json

def state_dir(root=None):return Path(root) if root else PHASE/'artifacts/state'
def load_boundary(root=None):return load_json(state_dir(root)/'r04_qualification_boundary.json',None)
def initialize(baseline_commit=None,p09_state_root=None,r01_state_root=None,r03_state_root=None,r04_state_root=None,now=None):
    from AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0.runtime.forward_ledger import load_state,save_state
    from AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0.runtime.cohort_manager import ensure_cohort,current_fingerprint
    from AD_V31_R01_FORWARD_QUALITY_PROMOTION_SCIENCE.runtime.cohort import load_cohort as load_r01,initialize as init_r01
    from AD_V31_R03_ANTIFRAGILE_MULTI_SCENARIO_PERSPECTIVE.runtime.cohort_boundary import load_boundary as load_r03
    state=load_state(p09_state_root);old_p09=next((x for x in reversed(state.get('cohorts',[])) if x.get('state')=='OPEN'),None);old_r01=load_r01(r01_state_root);old_r03=load_r03(r03_state_root)
    state,new_p09,created=ensure_cohort(state,now);save_state(state,p09_state_root)
    p09_status={'active_cohort':new_p09,'current_fingerprint':current_fingerprint()};new_r01=init_r01(p09_status,root=r01_state_root,now=now,baseline_commit=baseline_commit)
    obj={'record_type':'AD_V31_R04_QUALIFICATION_BOUNDARY','schema_version':'1.0.0','state':'OPEN','started_at_utc':iso(),'baseline_commit':baseline_commit,'r04_data_contract_fingerprint':current_fingerprint(),'old_p09_cohort_id':(old_p09 or {}).get('cohort_id'),'new_p09_cohort_id':new_p09.get('cohort_id'),'p09_cohort_created':created,'old_r01_qualification_cohort_id':(old_r01 or {}).get('qualification_cohort_id'),'new_r01_qualification_cohort_id':new_r01.get('qualification_cohort_id'),'old_r03_boundary_id':(old_r03 or {}).get('qualification_boundary_id'),'old_r03_state':'SUPERSEDED_FOR_PRIMARY_PRODUCTION_QUALIFICATION' if old_r03 else None,'pre_r04_history_preserved':True,'pre_r04_evidence_primary_production_qualification_authority':False,'new_r04_decisions_primary_qualification_authority':True,'last_planned_major_input_science_reset':True}
    obj['qualification_boundary_id']='R04Q_'+canonical_hash(obj)[:20].upper();save_json(state_dir(r04_state_root)/'r04_qualification_boundary.json',obj);return obj
