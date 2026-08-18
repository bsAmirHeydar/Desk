from __future__ import annotations
from pathlib import Path
from .common import PH,stable_id,iso,sha_obj,load
from .decision_freeze import verify_manifest

def _atomic(path,obj):
    from AD_V31_R01_FORWARD_QUALITY_PROMOTION_SCIENCE.runtime.common import atomic_json
    atomic_json(path,obj)
def state_dir(root=None):return Path(root) if root else PH/'artifacts/state'
def load_boundary(root=None):return load(state_dir(root)/'r02_qualification_boundary.json',None)
def initialize(baseline_commit=None,p09_state_root=None,r01_state_root=None,r02_state_root=None,now=None):
    from AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0.runtime.forward_ledger import load_state,save_state
    from AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0.runtime.cohort_manager import ensure_cohort,current_fingerprint
    from AD_V31_R01_FORWARD_QUALITY_PROMOTION_SCIENCE.runtime.cohort import load_cohort as load_r01,initialize as init_r01
    old_r01=load_r01(r01_state_root);state=load_state(p09_state_root);old_p09=next((x for x in reversed(state.get('cohorts',[])) if x.get('state')=='OPEN'),None);state,new_p09,created=ensure_cohort(state,now);save_state(state,p09_state_root)
    p09_status={'active_cohort':new_p09,'current_fingerprint':current_fingerprint()};new_r01=init_r01(p09_status,root=r01_state_root,now=now,baseline_commit=baseline_commit);fr=verify_manifest()
    obj={'record_type':'AD_V31_R02_QUALIFICATION_BOUNDARY','schema_version':'1.0.0','qualification_boundary_id':stable_id('R02Q',{'t':iso(now),'p09':new_p09.get('cohort_id'),'r01':new_r01.get('qualification_cohort_id'),'r02':fr.get('decision_science_fingerprint')}),'state':'OPEN','started_at_utc':iso(now),'baseline_commit':baseline_commit,'r02_decision_science_fingerprint':fr.get('decision_science_fingerprint'),'freeze_status':fr.get('status'),'old_p09_cohort_id':(old_p09 or {}).get('cohort_id'),'new_p09_cohort_id':new_p09.get('cohort_id'),'p09_cohort_created':created,'old_r01_qualification_cohort_id':(old_r01 or {}).get('qualification_cohort_id'),'old_r01_state':(old_r01 or {}).get('state'),'new_r01_qualification_cohort_id':new_r01.get('qualification_cohort_id'),'pre_r02_p09_history_preserved':True,'pre_r02_evidence_primary_production_qualification_authority':False,'new_r02_decisions_primary_qualification_authority':True}
    _atomic(state_dir(r02_state_root)/'r02_qualification_boundary.json',obj);return obj
