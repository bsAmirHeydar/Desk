from __future__ import annotations
import json,sys,tempfile,hashlib
from pathlib import Path
HERE=Path(__file__).resolve();PH=HERE.parents[1];NEXT=PH.parent;REPO=NEXT.parents[1]
if str(NEXT) not in sys.path:sys.path.insert(0,str(NEXT))
from AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN.runtime.gold_orchestrator import run_gold,STAGE_ORDER
from AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN.runtime.common import load

def sig(p):
 p=Path(p)
 if not p.exists():return None
 if p.is_file():return hashlib.sha256(p.read_bytes()).hexdigest()
 rows=[]
 for f in sorted(x for x in p.rglob('*') if x.is_file()):rows.append((f.relative_to(p).as_posix(),hashlib.sha256(f.read_bytes()).hexdigest()))
 return hashlib.sha256(json.dumps(rows,sort_keys=True).encode()).hexdigest()
def main():
 real=[NEXT/'AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0/artifacts/state',NEXT/'AD_V31_R01_FORWARD_QUALITY_PROMOTION_SCIENCE/artifacts/state',NEXT/'AD_V31_R04_INSTITUTIONAL_DATA_EDGE_OUTCOME_INFRASTRUCTURE/artifacts/state']
 before={str(x):sig(x) for x in real}
 p02=NEXT/'AD_V3_PHASE_02_TOTAL_LIVE_DATA_OBSERVABILITY_FABRIC';fix=p02/'tests/fixtures/generated'
 with tempfile.TemporaryDirectory() as td:
  t=Path(td);out=run_gold(REPO,'SESSION_1_6H','FIXTURE','NORMAL',p02_data_root_override=t/'data',artifact_root_override=t/'art',kernel_fixture_dir=fix,kernel_output_root_override=t/'kernel',p09_state_root_override=t/'p09',as_of_utc='2026-08-19T10:00:00Z',fixture_mode=True,update_latest=False,quiet=True)
  rd=next((t/'art/runs').iterdir()); ops=load(rd/'r05_operations_receipt.json');cri=load(rd/'control_room_input.json');vm=load(rd/'control_room_view_model.json');pred=load(rd/'p09_forward_precommit.json')
  checks={
   'full_stage_order':[x['stage_id'] for x in out['stage_receipts']]==STAGE_ORDER,
   'r05_operations_receipt':ops.get('record_type')=='AD_V31_R05_OPERATIONS_RECEIPT',
   'one_run_id':all(x['run_id']==out['run_id'] for x in out['stage_receipts']) and ops.get('run_id')==out['run_id'],
   'one_decision_time':all(x['decision_time']==out['decision_time'] for x in out['stage_receipts']) and ops.get('decision_time')==out['decision_time'],
   'r03_before_p09':STAGE_ORDER.index('PERSPECTIVE_OVERLAY')<STAGE_ORDER.index('FORWARD_PRECOMMIT'),
   'p09_has_r03_state':pred.get('r03_perspective_version') is not None,
   'p11_human_profile':(vm.get('human_intelligence') or {}).get('presentation_profile')=='HUMAN_INSTITUTIONAL_FA',
   'report_exists':(rd/'control_room.html').exists(),
   'seal_exists':(rd/'run_seal.json').exists(),
   'fixture_latest_not_mutated':not (t/'art/latest/last_success.json').exists(),
  }
 after={str(x):sig(x) for x in real};checks['real_forward_state_unchanged']=before==after
 ok=all(checks.values());res={'record_type':'AD_V31_R05_INTEGRATED_OFFLINE_FIXTURE','status':'PASS' if ok else 'FAIL','run_id':out.get('run_id'),'overall_status':out.get('overall_status'),'checks':checks,'real_state_before':before,'real_state_after':after,'fixture_only':True};print(json.dumps(res,ensure_ascii=False,indent=2));return 0 if ok else 2
if __name__=='__main__':raise SystemExit(main())
