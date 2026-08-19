from __future__ import annotations
from pathlib import Path
from .common import iso

def recovery_status(repo):
    from AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN.runtime.artifact_manager import ArtifactManager
    repo=Path(repo);p=repo/'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL/NEXT_VERSION/AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN/artifacts';am=ArtifactManager(p,create=False);ls=am.lock_state();tmps=[]
    latest=p/'latest'
    if latest.exists():tmps=[str(x) for x in latest.glob('*.tmp')]
    need=ls.get('state') in ('STALE_RECOVERABLE','CORRUPT') or bool(tmps)
    return {'record_type':'AD_V31_R05_RECOVERY_STATUS','state':'RECOVERY_REQUIRED' if need else 'READY','lock':ls,'abandoned_temp_files':tmps,'scientific_state_mutation_allowed':False,'checked_at_utc':iso()}

def recover(repo):
    from AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN.runtime.artifact_manager import ArtifactManager
    repo=Path(repo);p=repo/'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL/NEXT_VERSION/AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN/artifacts';am=ArtifactManager(p);actions=[]
    ls=am.lock_state()
    if ls.get('state')=='STALE_RECOVERABLE' and am.recover_stale_lock():actions.append('STALE_LOCK_REMOVED')
    latest=p/'latest'
    if latest.exists():
        for x in latest.glob('*.tmp'):
            try:x.unlink();actions.append('ABANDONED_TEMP_REMOVED:'+x.name)
            except Exception:pass
    return {'record_type':'AD_V31_R05_RECOVERY_RESULT','status':'RECOVERED' if actions else 'NO_ACTION','actions':actions,'forbidden_scientific_mutation':True,'completed_at_utc':iso()}
