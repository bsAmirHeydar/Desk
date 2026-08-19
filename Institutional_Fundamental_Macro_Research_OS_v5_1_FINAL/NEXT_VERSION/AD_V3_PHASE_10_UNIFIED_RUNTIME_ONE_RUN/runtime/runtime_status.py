from __future__ import annotations
from pathlib import Path
from .common import load
from .artifact_manager import ArtifactManager
from .runtime_router import resolve,promotion_state

def status(repo):
    repo=Path(repo);p=repo/'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL/NEXT_VERSION/AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN';am=ArtifactManager(p/'artifacts',create=False)
    try:r=resolve(repo,'Gold','PRODUCTION')
    except Exception as e:r={'error':str(e)}
    from AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0.runtime.forward_runtime import status as fs
    p09=p.parent/'AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0'
    return {'record_type':'AD_V3_P10_STATUS','phase':'AD-V3-P10','version':'3.10.3-r05-operations','acceptance_status':(load(p/'PHASE_10_HANDOFF.json',{}) or {}).get('p10_status','NOT_YET_ACCEPTED'),'active_subject':'Gold','default_horizon':'SESSION_1_6H','promotion_state':promotion_state(repo),'production_route':r.get('selected_runtime'),'shadow_route':'V3','last_attempt':am.read_pointer('last_attempt.json'),'last_success':am.read_pointer('last_success.json'),'p09_forward_state':(fs(p09).get('statistics') or {}).get('forward_evidence_state'),'runtime_lock':am.lock_state(),'trade_execution_authority':'NONE'}
