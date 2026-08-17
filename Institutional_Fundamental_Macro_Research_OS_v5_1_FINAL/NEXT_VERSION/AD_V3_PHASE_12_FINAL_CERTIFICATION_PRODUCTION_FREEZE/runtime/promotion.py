from __future__ import annotations
from pathlib import Path
import shutil,uuid
from .common import PHASE,NEXT,VAULT,REPO,load,atomic_json,iso,git_commit
from .gates import collect,enforce

def _p04():return NEXT/'AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING'
def _state_path():return _p04()/'artifacts/state/promotion_state.json'
def _manifest_path():return VAULT/'CURRENT_PRODUCTION_MANIFEST.json'
def _tx_path():return PHASE/'artifacts/state/deployment_transaction.json'
def transaction_in_progress():return _tx_path().exists()
def _release():return load(PHASE/'release/ALPHA_DESK_V3_FINAL_RELEASE_MANIFEST.json',{}) or {}
def _current_state():
 from AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING.runtime.promotion import load_state
 return load_state(_p04())
def _switch(target,receipt_kind,reason=None,test_root=None):
 # test_root only supports isolated temp fixtures and is never used by the production CLI.
 if test_root:
  root=Path(test_root);sp=root/'promotion_state.json';mp=root/'production_manifest.json';tx=root/'deployment_transaction.json';old_s=load(sp,{'state':'SHADOW_COMMISSIONING'});old_m=load(mp,{})
 else:
  sp=_state_path();mp=_manifest_path();tx=_tx_path();old_s=_current_state();old_m=load(mp,{}) or {}
 rel=_release();finger=rel.get('release_fingerprint');tid='P12TX_'+uuid.uuid4().hex[:20].upper();atomic_json(tx,{'transaction_id':tid,'target':target,'started_at_utc':iso()})
 try:
  newm=dict(old_m);newm['alpha_desk_v3']={'release':'ALPHA_DESK_V3_GOLD_RC1','release_fingerprint':finger,'production_authority':target,'canonical_runtime':'AD-V3-P10','canonical_html':'AD-V3-P11','rollback_target':'V2','trade_execution_authority':'NONE','updated_at_utc':iso()};atomic_json(mp,newm)
  ns=dict(old_s);ns.update({'state':target,'updated_at_utc':iso(),'release_fingerprint':finger,'trade_execution_authority':'NONE','v2_baseline_retained':True,'automatic_promotion_forbidden':True})
  if target=='PRODUCTION_V3':ns.update({'promoted_at_utc':iso(),'production_direction_authority':True,'production_trade_permission_authority':True,'manual_operator_approval':True})
  else:ns.update({'production_direction_authority':False,'production_trade_permission_authority':False,'rollback_reason':reason or 'OPERATOR_ROLLBACK_TO_V2'})
  atomic_json(sp,ns)
 except Exception:
  atomic_json(mp,old_m);atomic_json(sp,old_s);raise
 finally:
  try:tx.unlink()
  except FileNotFoundError:pass
 rec={'record_type':receipt_kind,'timestamp_utc':iso(),'transaction_id':tid,'previous_production_authority':old_s.get('state','SHADOW_COMMISSIONING'),'new_production_authority':target,'release_fingerprint':finger,'git_commit':git_commit() if not test_root else None,'trade_execution_authority':'NONE'}
 return rec

def perform_promotion(approve=False):
 # Fast fail-closed preview first: do not run deep regression if approval/P09 is already closed.
 pre,_=collect(approve=approve,deep=False);enforce(pre)
 # Only an actually eligible release receives the deep pre-switch revalidation.
 gates,evidence=collect(approve=approve,deep=True);enforce(gates)
 rec=_switch('PRODUCTION_V3','AD_V3_P12_PRODUCTION_PROMOTION_RECEIPT');rec['gate_results']=gates;rec['operator_approval']=True;atomic_json(PHASE/'artifacts/state/production_promotion_receipt.json',rec);return rec

def perform_rollback(reason='OPERATOR_ROLLBACK_TO_V2'):
 # certify rollback target before switching real authority.
 import subprocess,sys
 for phase,tool in [('P11',NEXT/'AD_V2_PHASE_11_UNIFIED_COMMAND_RESEARCH_ORCHESTRATION/tools/run_phase11_acceptance.py'),('P13',NEXT/'AD_V2_PHASE_13_CANONICAL_GOLD_CONTROL_ROOM_OUTPUT/tools/run_phase13_acceptance.py')]:
  cp=subprocess.run([sys.executable,str(tool),'--repo-root',str(REPO)],capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=300)
  if cp.returncode!=0:raise RuntimeError('ROLLBACK_TARGET_FAILED:'+phase)
 rec=_switch('ROLLED_BACK_V2','AD_V3_P12_ROLLBACK_RECEIPT',reason);atomic_json(PHASE/'artifacts/state/rollback_receipt.json',rec);return rec
