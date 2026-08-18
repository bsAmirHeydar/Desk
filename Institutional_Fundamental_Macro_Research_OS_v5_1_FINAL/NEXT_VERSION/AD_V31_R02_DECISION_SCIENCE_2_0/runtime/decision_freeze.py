from __future__ import annotations
from pathlib import Path
from .common import PH,NEXT,load,sha_file,sha_obj
SURFACES=[
'config/magnitude_method_registry.json','config/magnitude_threshold_policy.json','config/historical_normalization_policy.json','config/root_health_policy.json','config/root_critical_evidence_registry.json','config/causal_importance_matrix.json','config/regime_importance_policy.json','config/dominance_robustness_policy.json','config/decision_science_2_policy.json',
'runtime/historical_normalizer.py','runtime/magnitude_engine.py','runtime/root_health_engine.py','runtime/causal_importance_engine.py','runtime/robust_dominance_engine.py','runtime/sensitivity_engine.py','runtime/decision_science_runtime.py',
'../AD_V3_PHASE_08_DECISION_SCIENCE_CALIBRATION/config/decision_calibration_policy.json','../AD_V3_PHASE_08_DECISION_SCIENCE_CALIBRATION/config/causal_importance_policy.json','../AD_V3_PHASE_08_DECISION_SCIENCE_CALIBRATION/config/dominance_policy.json','../AD_V3_PHASE_08_DECISION_SCIENCE_CALIBRATION/config/magnitude_policy.json','../AD_V3_PHASE_08_DECISION_SCIENCE_CALIBRATION/runtime/decision_runtime.py','../AD_V3_PHASE_08_DECISION_SCIENCE_CALIBRATION/runtime/feature_builder.py','../AD_V3_PHASE_08_DECISION_SCIENCE_CALIBRATION/runtime/dominance_engine.py','../AD_V3_PHASE_08_DECISION_SCIENCE_CALIBRATION/runtime/magnitude_calibrator.py']
def _path(rel):return (PH/rel).resolve()
def make_manifest():
    rows=[{'path':rel,'sha256':sha_file(_path(rel))} for rel in SURFACES];fp='R02SCI_'+sha_obj(rows).upper();return {'record_type':'AD_V31_R02_DECISION_SCIENCE_FREEZE','schema_version':'1.0.0','version':'3.1.2-decision-science-2','surfaces':rows,'decision_science_fingerprint':fp,'random_optimization_forbidden':True,'production_qualification_requires_new_cohort':True}
def manifest_path():return PH/'calibration/R02_DECISION_SCIENCE_FREEZE_MANIFEST.json'
def verify_manifest():
    m=load(manifest_path(),{}) or {};bad=[]
    for r in m.get('surfaces') or []:
        p=_path(r['path']);got=sha_file(p) if p.exists() else None
        if got!=r.get('sha256'):bad.append({'path':r['path'],'expected':r.get('sha256'),'actual':got})
    return {'status':'PASS' if not bad else 'FAIL','drift':bad,'decision_science_fingerprint':m.get('decision_science_fingerprint')}
