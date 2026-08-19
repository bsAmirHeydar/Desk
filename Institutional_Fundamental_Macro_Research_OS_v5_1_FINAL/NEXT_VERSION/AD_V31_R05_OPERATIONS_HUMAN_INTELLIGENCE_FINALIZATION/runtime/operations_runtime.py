from __future__ import annotations
from pathlib import Path
import os,tempfile,time,json
from .common import PHASE,NEXT,REPO,load_json,atomic_json,iso
from .health_aggregator import aggregate

def _paths(repo):
    repo=Path(repo);n=repo/'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL'/'NEXT_VERSION'
    return {'next':n,'p09':n/'AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0','p10':n/'AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN','p12':n/'AD_V3_PHASE_12_FINAL_CERTIFICATION_PRODUCTION_FREEZE','r01':n/'AD_V31_R01_FORWARD_QUALITY_PROMOTION_SCIENCE','r04':n/'AD_V31_R04_INSTITUTIONAL_DATA_EDGE_OUTCOME_INFRASTRUCTURE','r05':n/'AD_V31_R05_OPERATIONS_HUMAN_INTELLIGENCE_FINALIZATION'}

def semantic_host_state():
    if os.environ.get('ALPHALAB_HOST_COMMAND') or os.environ.get('OPENAI_API_KEY'):return 'CONFIGURED'
    return 'CONSERVATIVE_FALLBACK'

def preflight(repo,artifact_root=None,p09_state_root=None,r04_state_root=None,fixture_mode=False,strict_freeze=True):
    from AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0.runtime.forward_runtime import status as p09_status
    from AD_V31_R04_INSTITUTIONAL_DATA_EDGE_OUTCOME_INFRASTRUCTURE.runtime.data_edge_runtime import status as r04_status
    from AD_V3_PHASE_12_FINAL_CERTIFICATION_PRODUCTION_FREEZE.runtime.freeze import verify_manifest
    repo=Path(repo);p=_paths(repo); blockers=[];warnings=[];subs={}
    freeze={'status':'SKIPPED_FIXTURE'} if not strict_freeze else verify_manifest(repo)
    if freeze.get('status')!='PASS' and freeze.get('status')!='SKIPPED_FIXTURE':blockers.append('FINAL_FREEZE_INVALID')
    subs['FREEZE']={'state':'HEALTHY' if freeze.get('status') in {'PASS','SKIPPED_FIXTURE'} else 'BLOCKED','detail':freeze.get('status')}
    try:
        fw=p09_status(p['p09'],state_root=p09_state_root)
        bad=int(fw.get('integrity_failures',0))>0
    except Exception as e:
        fw={'error':type(e).__name__};bad=True
    if bad:blockers.append('P09_INTEGRITY_FAILURE')
    subs['FORWARD_LEDGER']={'state':'BLOCKED' if bad else 'HEALTHY','detail':(fw.get('statistics') or {}).get('forward_evidence_state')}
    try:r04=r04_status(r04_state_root);pit=(r04.get('pit_store') or {});pit_bad=pit.get('status')=='FAIL'
    except Exception as e:r04={'error':type(e).__name__};pit={'status':'UNKNOWN'};pit_bad=False;warnings.append('R04_STATUS_UNAVAILABLE')
    if pit_bad:blockers.append('PIT_INTEGRITY_FAILURE')
    subs['PIT_STORE']={'state':'BLOCKED' if pit_bad else ('HEALTHY' if pit.get('status')=='PASS' else 'DEGRADED'),'detail':pit}
    direct=((r04.get('direct_dxy') or {}).get('state') or 'UNKNOWN');rr=((r04.get('intraday_real_rate_proxy') or {}).get('state') or 'UNKNOWN')
    if 'LIVE' not in direct and 'CONFIGURED' not in direct:warnings.append('DIRECT_DXY_UNAVAILABLE')
    if rr.startswith('UNAVAILABLE'):warnings.append('INTRADAY_REAL_RATE_PROXY_UNAVAILABLE')
    subs['DATA']={'state':'DEGRADED' if warnings else 'HEALTHY','detail':{'direct_dxy':direct,'intraday_real_rate_proxy':rr}}
    sem=semantic_host_state();
    if sem!='CONFIGURED':warnings.append('SEMANTIC_CONSERVATIVE_FALLBACK')
    subs['SEMANTIC']={'state':'DEGRADED' if sem!='CONFIGURED' else 'HEALTHY','detail':sem}
    tx=p['p12']/'release/deployment_transaction.json'
    if tx.exists():blockers.append('DEPLOYMENT_TRANSACTION_IN_PROGRESS')
    target=Path(artifact_root) if artifact_root else p['p10']/'artifacts'
    try:
        target.mkdir(parents=True,exist_ok=True);fd,tmp=tempfile.mkstemp(prefix='.r05_write_test_',dir=str(target));os.close(fd);os.unlink(tmp);writable=True
    except Exception:writable=False
    if not writable:blockers.append('ARTIFACT_ROOT_NOT_WRITABLE')
    subs['RUNTIME']={'state':'BLOCKED' if not writable or tx.exists() else 'HEALTHY','detail':{'artifact_root':str(target),'writable':writable,'deployment_transaction':tx.exists()}}
    overall='BLOCKED' if blockers else ('DEGRADED_NONBLOCKING' if warnings else 'READY')
    health=aggregate(subs)
    return {'record_type':'AD_V31_R05_PREFLIGHT','version':'3.1.5-operations-human-intelligence','state':overall,'blockers':blockers,'warnings':warnings,'subsystems':subs,'health':health,'semantic_host_state':sem,'r04_status':r04,'p09_status':fw,'operator_action_required':bool(blockers),'scientific_authority':False,'checked_at_utc':iso()}

def build_operations_receipt(run_id,decision_time,mode,runtime_state,stage_receipts,preflight,run_dir=None,report_state=None,outcome_recovery_state=None,forward_precommit_state=None,seal_state='PENDING',last_success_pointer_state=None,error=None):
    return {'record_type':'AD_V31_R05_OPERATIONS_RECEIPT','schema_version':'1.0.0','version':'3.1.5-operations-human-intelligence','run_id':run_id,'decision_time':decision_time,'mode':mode,'runtime_state':runtime_state,'stage_states':[{'stage_id':x.get('stage_id'),'status':x.get('status'),'duration_ms':x.get('duration_ms')} for x in (stage_receipts or [])],'provider_health_summary':((preflight or {}).get('r04_status') or {}).get('outcome_providers'),'data_health_summary':((preflight or {}).get('subsystems') or {}).get('DATA'),'semantic_mode':(preflight or {}).get('semantic_host_state'),'outcome_recovery_state':outcome_recovery_state,'forward_precommit_state':forward_precommit_state,'report_state':report_state,'seal_state':seal_state,'last_success_pointer_state':last_success_pointer_state,'operator_action_required':(preflight or {}).get('operator_action_required',False),'preflight_state':(preflight or {}).get('state'),'run_dir':str(run_dir) if run_dir else None,'error':error,'scientific_authority':False,'trade_execution_authority':'NONE','created_at_utc':iso()}

def write_operations_receipt(path,**kwargs):
    obj=build_operations_receipt(**kwargs);atomic_json(path,obj);return obj
