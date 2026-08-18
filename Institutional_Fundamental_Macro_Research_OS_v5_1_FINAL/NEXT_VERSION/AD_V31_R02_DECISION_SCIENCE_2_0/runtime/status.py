from __future__ import annotations
from .common import PH,cfg,load
from .decision_freeze import verify_manifest
from .cohort_boundary import load_boundary

def status():
    reg=cfg('magnitude_method_registry.json');cnt={}
    for x in reg.get('entries',[]):cnt[x['status']]=cnt.get(x['status'],0)+1
    imp=cfg('causal_importance_matrix.json');rob=cfg('dominance_robustness_policy.json');boundary=load_boundary();latest=None
    p10=PH.parent/'AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN/artifacts/latest/last_success.json'
    ptr=load(p10,None)
    if ptr and ptr.get('run_dir'):
        d=load(__import__('pathlib').Path(ptr['run_dir'])/'p08_decision_calibration.json',None);latest=d
    return {'record_type':'AD_V31_R02_STATUS','status':'PASS','version':'3.1.2-decision-science-2','primary_horizon':'SESSION_1_6H','magnitude_method_coverage':cnt,'fact_universe_count':reg.get('fact_count'),'importance_matrix_version':imp.get('schema_version'),'sensitivity_model_count':len(rob.get('variants') or []),'decision_science_freeze':verify_manifest(),'qualification_boundary':boundary,'current_decision_robustness':(latest or {}).get('dominance_robustness'),'current_model_sensitivity':(latest or {}).get('model_sensitivity'),'V3_state':'SHADOW_COMMISSIONING','promotion_performed':False,'trade_execution_authority':'NONE'}
