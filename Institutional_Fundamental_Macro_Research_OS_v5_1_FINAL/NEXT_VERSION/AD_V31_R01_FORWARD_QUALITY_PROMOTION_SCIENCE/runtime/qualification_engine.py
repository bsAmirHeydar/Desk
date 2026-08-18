from __future__ import annotations
from .common import P09,cfg,load,sha_obj,state_dir
from .cohort import load_cohort
from .qualification_freeze import verify_manifest
from .quality_metrics import primary_records,all_metrics
from .coverage_engine import compute as coverage_compute
from .subgroup_safety import evaluate as subgroup_evaluate

def _p09_state(root=None):
    from AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0.runtime.forward_ledger import load_state
    return load_state(root)
def _p09_status(root=None):
    from AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0.runtime.forward_runtime import status
    return status(P09,state_root=root)
def qualify(p09_state_root=None,qualification_root=None):
    p09s=_p09_status(p09_state_root);state=_p09_state(p09_state_root);qc=load_cohort(qualification_root);fr=verify_manifest();sample=(p09s.get('statistics') or {}).get('forward_evidence_state','NO_SAMPLES')
    if not qc:return {'record_type':'AD_V31_R01_PRODUCTION_QUALIFICATION','version':'3.1.1-forward-quality','qualification_cohort':None,'sample_maturity':sample,'sample_gate':False,'forward_quality_state':'UNAVAILABLE','quality_gate':False,'coverage_state':'UNAVAILABLE','coverage_gate':False,'critical_subgroup_state':'UNAVAILABLE','critical_subgroup_gate':False,'production_qualification_state':'INSUFFICIENT_EVIDENCE','production_eligible':False,'reason':'R01_QUALIFICATION_COHORT_NOT_INITIALIZED','policy_freeze':fr}
    if fr.get('status')!='PASS' or qc.get('policy_fingerprint')!=fr.get('policy_fingerprint'):
        return {'record_type':'AD_V31_R01_PRODUCTION_QUALIFICATION','version':'3.1.1-forward-quality','qualification_cohort':qc,'sample_maturity':sample,'sample_gate':False,'forward_quality_state':'FAIL','quality_gate':False,'coverage_state':'FAIL','coverage_gate':False,'critical_subgroup_state':'FAIL','critical_subgroup_gate':False,'production_qualification_state':'QUALITY_FAILED','production_eligible':False,'reason':'R01_POLICY_FREEZE_DRIFT','policy_freeze':fr}
    active=(p09s.get('active_cohort') or {});bound=qc.get('p09_cohort_id')
    if bound and active.get('cohort_id') and active.get('cohort_id')!=bound:
        return {'record_type':'AD_V31_R01_PRODUCTION_QUALIFICATION','version':'3.1.1-forward-quality','qualification_cohort':qc,'sample_maturity':sample,'sample_gate':False,'forward_quality_state':'FAIL','quality_gate':False,'coverage_state':'FAIL','coverage_gate':False,'critical_subgroup_state':'FAIL','critical_subgroup_gate':False,'production_qualification_state':'QUALITY_FAILED','production_eligible':False,'reason':'P09_COHORT_CHANGED_NEW_R01_QUALIFICATION_COHORT_REQUIRED','policy_freeze':fr}
    rows=primary_records(state,qc);metrics=all_metrics(rows);coverage=coverage_compute(rows);sub=subgroup_evaluate(rows);hard=cfg('forward_quality_policy.json')['core_hard_gates'];mapn={'DIRECTION_QUALITY':'direction','EDGE_SEPARATION':'edge','PERMISSION_QUALITY':'permission','WAIT_QUALITY':'wait','PATH_COMPLETENESS':'path_completeness'};hard_states={g:metrics[mapn[g]]['state'] for g in hard};quality_pass=all(v=='PASS' for v in hard_states.values());quality_fail=any(v=='FAIL' for v in hard_states.values());quality_state='PASS' if quality_pass else ('FAIL' if quality_fail else 'INSUFFICIENT');sample_gate=sample in ('PROVISIONAL','MATURE');coverage_gate=coverage['state']=='PASS';subgroup_gate=sub['state']=='PASS';eligible=sample_gate and quality_pass and coverage_gate and subgroup_gate
    if eligible:prod='QUALIFIED'
    elif not sample_gate:prod='INSUFFICIENT_EVIDENCE'
    elif quality_fail:prod='QUALITY_FAILED'
    elif not coverage_gate:prod='COVERAGE_INSUFFICIENT'
    elif not subgroup_gate:prod='CRITICAL_SUBGROUP_FAILED'
    else:prod='INSUFFICIENT_EVIDENCE'
    receipt={'record_type':'AD_V31_R01_PRODUCTION_QUALIFICATION','schema_version':'1.0.0','version':'3.1.1-forward-quality','qualification_cohort':qc,'p09_active_cohort':active,'sample_maturity':sample,'sample_gate':sample_gate,'qualifying_evaluated_episodes':len(rows),'forward_quality_state':quality_state,'quality_gate':quality_pass,'hard_quality_states':hard_states,'dimensions':metrics,'coverage':coverage,'coverage_state':coverage['state'],'coverage_gate':coverage_gate,'critical_subgroups':sub,'critical_subgroup_state':sub['state'],'critical_subgroup_gate':subgroup_gate,'production_qualification_state':prod,'production_eligible':eligible,'policy_freeze':fr,'fixture_samples_included':False,'replay_samples_included':False,'existing_p09_history_rewritten':False}
    receipt['qualification_hash']=sha_obj(receipt);return receipt
