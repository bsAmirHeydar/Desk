from __future__ import annotations
from pathlib import Path
from .common import PH,stable_id,iso,sha_obj,load,atomic_json

def state_dir(root=None):return Path(root) if root else PH/'artifacts/state'
def load_boundary(root=None):return load(state_dir(root)/'r03_qualification_boundary.json',None)
def initialize(baseline_commit=None,p09_state_root=None,r01_state_root=None,r02_state_root=None,r03_state_root=None,now=None):
    from AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0.runtime.forward_ledger import load_state,save_state
    from AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0.runtime.cohort_manager import ensure_cohort,current_fingerprint
    from AD_V31_R01_FORWARD_QUALITY_PROMOTION_SCIENCE.runtime.cohort import load_cohort as load_r01,initialize as init_r01
    from AD_V31_R02_DECISION_SCIENCE_2_0.runtime.cohort_boundary import load_boundary as load_r02
    from .perspective_freeze import verify_manifest
    state=load_state(p09_state_root);old_p09=next((x for x in reversed(state.get('cohorts',[])) if x.get('state')=='OPEN'),None);old_r01=load_r01(r01_state_root);old_r02=load_r02(r02_state_root);state,new_p09,created=ensure_cohort(state,now);save_state(state,p09_state_root);p09_status={'active_cohort':new_p09,'current_fingerprint':current_fingerprint()};new_r01=init_r01(p09_status,root=r01_state_root,now=now,baseline_commit=baseline_commit);fr=verify_manifest()
    obj={'record_type':'AD_V31_R03_QUALIFICATION_BOUNDARY','schema_version':'1.0.0','qualification_boundary_id':stable_id('R03Q',{'t':iso(now),'p09':new_p09.get('cohort_id'),'r01':new_r01.get('qualification_cohort_id'),'r03':fr.get('perspective_science_fingerprint')}),'state':'OPEN','started_at_utc':iso(now),'baseline_commit':baseline_commit,'r03_perspective_fingerprint':fr.get('perspective_science_fingerprint'),'freeze_status':fr.get('status'),'old_p09_cohort_id':(old_p09 or {}).get('cohort_id'),'new_p09_cohort_id':new_p09.get('cohort_id'),'p09_cohort_created':created,'old_r01_qualification_cohort_id':(old_r01 or {}).get('qualification_cohort_id'),'new_r01_qualification_cohort_id':new_r01.get('qualification_cohort_id'),'old_r02_boundary_id':(old_r02 or {}).get('qualification_boundary_id'),'old_r02_state':'SUPERSEDED_FOR_PRIMARY_PRODUCTION_QUALIFICATION' if old_r02 else None,'pre_r03_evidence_primary_production_qualification_authority':False,'pre_r03_history_preserved':True,'new_r03_decisions_primary_qualification_authority':True}
    atomic_json(state_dir(r03_state_root)/'r03_qualification_boundary.json',obj);return obj
