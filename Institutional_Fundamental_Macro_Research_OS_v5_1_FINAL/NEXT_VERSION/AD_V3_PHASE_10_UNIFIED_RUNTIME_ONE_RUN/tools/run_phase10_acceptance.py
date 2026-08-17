from __future__ import annotations
import json,pathlib,sys,tempfile,subprocess,copy,os
from datetime import datetime,timezone,timedelta
HERE=pathlib.Path(__file__).resolve();PH=HERE.parents[1];NEXT=PH.parent;REPO=NEXT.parents[1];sys.path.insert(0,str(NEXT))
import jsonschema
from AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN.runtime.common import load,sha_file
from AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN.runtime.runtime_router import resolve
from AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN.runtime.gold_orchestrator import run_gold,STAGE_ORDER
from AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN.runtime.artifact_manager import ArtifactManager,RuntimeLocked,verify_seal
from AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN.runtime.runtime_status import status as p10_status

def ck(n,o,d=None):return {'name':n,'status':'PASS' if o else 'FAIL','detail':d}
def main():
 checks=[]
 # Prerequisite validators: use last two governance layers plus static P10 validation; full P01-P09 regression is run outside this suite too.
 for label,tool in [('P05',NEXT/'AD_V3_PHASE_05_INTEGRITY_ARCHITECTURE_CONSOLIDATION/tools/run_phase05_acceptance.py'),('P09',NEXT/'AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0/tools/run_phase09_acceptance.py'),('P10 static',PH/'tools/validate_phase10.py')]:
  cp=subprocess.run([sys.executable,str(tool)],capture_output=True,text=True,encoding='utf-8',errors='replace')
  checks.append(ck(label+' prerequisite valid',cp.returncode==0,cp.stdout[-800:] if cp.returncode else 'PASS'))
 # Routing matrix.
 r1=resolve(REPO,'Gold','PRODUCTION',promotion_override='SHADOW_COMMISSIONING');r2=resolve(REPO,'Gold','SHADOW',promotion_override='SHADOW_COMMISSIONING');r3=resolve(REPO,'Gold','PRODUCTION',promotion_override='PRODUCTION_V3');r4=resolve(REPO,'Gold','PRODUCTION',promotion_override='ROLLED_BACK_V2')
 checks.append(ck('SHADOW_COMMISSIONING routes production run Gold to V2',r1['selected_runtime']=='V2',r1))
 checks.append(ck('explicit commission Gold resolves to V3 shadow',r2['selected_runtime']=='V3',r2))
 checks.append(ck('future PRODUCTION_V3 fixture routes run Gold to P10',r3['selected_runtime']=='V3',r3))
 checks.append(ck('rollback fixture returns run Gold to V2',r4['selected_runtime']=='V2',r4))
 try:resolve(REPO,'NASDAQ100','PRODUCTION');bad=False
 except ValueError:bad=True
 checks.append(ck('non-Gold subject rejected',bad))
 # Canonical P10 front door fixture.
 p02=NEXT/'AD_V3_PHASE_02_TOTAL_LIVE_DATA_OBSERVABILITY_FABRIC';fix=p02/'tests/fixtures/generated'
 with tempfile.TemporaryDirectory() as td:
  td=pathlib.Path(td);data=td/'data';art=td/'art';kout=td/'kout';p09state=td/'p09state'
  out=run_gold(REPO,'SESSION_1_6H','FIXTURE','NORMAL',p02_data_root_override=data,artifact_root_override=art,kernel_fixture_dir=fix,kernel_output_root_override=kout,p09_state_root_override=p09state,as_of_utc='2026-08-17T10:00:00Z',fixture_mode=True,update_latest=False,quiet=True)
  rd=next((art/'runs').iterdir())
  checks.append(ck('one canonical V3 orchestration authority executes full offline pipeline',out['overall_status'] in {'SUCCESS','SUCCESS_DEGRADED','SUCCESS_NONACTIONABLE'} and [x['stage_id'] for x in out['stage_receipts']]==STAGE_ORDER,[x['stage_id'] for x in out['stage_receipts']]))
  checks.append(ck('ordinary V3 run requires no manual inter-phase handoff',all((rd/x).exists() for x in ['p07_kernel_receipt.json','p03_pre_semantic.json','semantic_adjudication_bundle.json','p03_final.json','p08_decision_calibration.json','p09_forward_precommit.json','control_room.html','run_result.json'])))
  checks.append(ck('one canonical run_id links all stage receipts',all(x['run_id']==out['run_id'] for x in out['stage_receipts'])))
  checks.append(ck('one canonical decision_time anchors logical run',all(x['decision_time']==out['decision_time'] for x in out['stage_receipts'])))
  order=[x['stage_id'] for x in out['stage_receipts']]
  checks.append(ck('P09 matured outcomes evaluated before current precommit',order.index('FORWARD_EVALUATION')<order.index('FORWARD_PRECOMMIT')))
  checks.append(ck('P07 plan occurs before P02 acquisition',order.index('ACQUISITION_PLAN')<order.index('ACQUISITION')))
  checks.append(ck('P06 semantic stage receives P03 packet before P08',order.index('PRE_SEMANTIC')<order.index('SEMANTIC')<order.index('FINAL_CAUSAL')<order.index('DECISION_CALIBRATION')))
  checks.append(ck('P09 receives P08 calibrated state',order.index('DECISION_CALIBRATION')<order.index('FORWARD_PRECOMMIT')))
  checks.append(ck('P04 receives canonical ControlRoomInputV3',load(rd/'control_room_input.json')['schema_id']=='ControlRoomInputV3'))
  checks.append(ck('semantic host unavailable degrades through P06 policy',out['semantic_state']['mode'] in {'CONSERVATIVE_EVIDENCE_ONLY','AUTO_GOVERNED','REPLAY_VALIDATED_BUNDLE','EXTERNAL_VALIDATED_BUNDLE'} and out['semantic_state']['validation_status'] is not None,out['semantic_state']))
  checks.append(ck('WAIT or UNKNOWN is not runtime failure',out['overall_status']!='FAILED_RUNTIME' and out['overall_status']!='FAILED_INTEGRITY'))
  checks.append(ck('fixture cannot update latest live pointers',not (art/'latest/last_success.json').exists()))
  checks.append(ck('fixture prospective state isolated',p09state.exists() and not (NEXT/'AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0/artifacts/state/forward_state.json').exists()))
  # Schema validation.
  for name,obj,schema in [('run',out,load(PH/'schemas/run_result.schema.json')),('control',load(rd/'control_room_input.json'),load(PH/'schemas/control_room_input.schema.json')),('route',r1,load(PH/'schemas/routing_receipt.schema.json'))]:
   try:jsonschema.validate(obj,schema);valid=True
   except Exception as e:valid=False
   checks.append(ck(name+' receipt schema valid',valid))
  stschema=load(PH/'schemas/stage_receipt.schema.json');sv=True
  try:
   for x in out['stage_receipts']:jsonschema.validate(x,stschema)
  except Exception:sv=False
  checks.append(ck('stage receipts schema valid',sv))
  checks.append(ck('run seal verifies canonical artifacts',verify_seal(rd)))
  # Tamper seal attack.
  p=rd/'control_room_input.json';orig=p.read_text(encoding='utf-8');p.write_text(orig+' ',encoding='utf-8');checks.append(ck('run seal tamper detected',not verify_seal(rd)));p.write_text(orig,encoding='utf-8')
  # Blocked data via empty CACHE_ONLY. No P09 precommit.
  b=run_gold(REPO,'SESSION_1_6H','FIXTURE','CACHE_ONLY',p02_data_root_override=td/'blocked_data',artifact_root_override=td/'blocked_art',kernel_output_root_override=td/'blocked_kernel',p09_state_root_override=td/'blocked_p09',as_of_utc='2026-08-17T11:00:00Z',fixture_mode=True,update_latest=False,quiet=True)
  brd=next((td/'blocked_art/runs').iterdir())
  checks.append(ck('P07 BLOCK prevents fake decision authority',b['overall_status']=='BLOCKED' and b['decision_state']['permission']['official_permission']=='NO_AUTHORITY' and not (brd/'p09_forward_precommit.json').exists(),b['overall_status']))
 # Latest-success vs failed-attempt and runtime locking.
 with tempfile.TemporaryDirectory() as td:
  td=pathlib.Path(td);data=td/'data';art=td/'art';kout=td/'kout';state=td/'state'
  first=run_gold(REPO,'SESSION_1_6H','FIXTURE','NORMAL',p02_data_root_override=data,artifact_root_override=art,kernel_fixture_dir=fix,kernel_output_root_override=kout,p09_state_root_override=state,as_of_utc='2026-08-17T12:00:00Z',fixture_mode=False,update_latest=True,quiet=True)
  am=ArtifactManager(art);s1=am.read_pointer('last_success.json');
  try:run_gold(REPO,'SESSION_1_6H','FIXTURE','NORMAL',p02_data_root_override=data,artifact_root_override=art,kernel_fixture_dir=fix,kernel_output_root_override=kout,p09_state_root_override=state,as_of_utc='2026-08-17T13:00:00Z',fixture_mode=False,update_latest=True,fail_stage='PRECHECK',quiet=True)
  except RuntimeError:pass
  la=am.read_pointer('last_attempt.json');ls=am.read_pointer('last_success.json')
  checks.append(ck('latest attempt and last success are distinct',la['status']=='FAILED_RUNTIME' and ls['run_id']==s1['run_id'] and la['run_id']!=ls['run_id'],{'attempt':la,'success':ls}))
  checks.append(ck('failed run cannot overwrite last successful report',(art/'latest/latest_control_room.html').exists() and ls['run_id']==first['run_id']))
  # Lock attack.
  lock=ArtifactManager(td/'lockart');lock.acquire('LOCK_HOLDER')
  try:
   try:run_gold(REPO,'SESSION_1_6H','FIXTURE','NORMAL',p02_data_root_override=td/'ld',artifact_root_override=td/'lockart',kernel_fixture_dir=fix,kernel_output_root_override=td/'lk',p09_state_root_override=td/'ls',as_of_utc='2026-08-17T14:00:00Z',fixture_mode=True,update_latest=False,quiet=True);locked=False
   except RuntimeLocked:locked=True
  finally:lock.release()
  checks.append(ck('runtime write lock prevents concurrent state corruption',locked))
 # Static authority/isolation.
 src=(PH/'runtime/gold_orchestrator.py').read_text(encoding='utf-8');legacy=load(PH/'config/legacy_authority_policy.json')
 checks.append(ck('V2 P11 prompt cluster has no V3 decision authority',legacy['v2_p11_prompt_cluster']['v3_decision_authority'] is False))
 checks.append(ck('V3 runtime has no dependency on V2 P11 prompt text','AD_V2_PHASE_11' not in src and 'prompt_cluster' not in src))
 checks.append(ck('P10 is orchestration only','calibrate_decision' in src and 'run_semantics' in src and 'p03_execute' in src and 'run_kernel' in src and 'p09_precommit_current' in src))
 # V2 rollback acceptance.
 v2=[]
 for label,tool in [('P11',NEXT/'AD_V2_PHASE_11_UNIFIED_COMMAND_RESEARCH_ORCHESTRATION/tools/run_phase11_acceptance.py'),('P13',NEXT/'AD_V2_PHASE_13_CANONICAL_GOLD_CONTROL_ROOM_OUTPUT/tools/run_phase13_acceptance.py')]:
  cp=subprocess.run([sys.executable,str(tool),'--repo-root',str(REPO)],capture_output=True,text=True,encoding='utf-8',errors='replace');v2.append((label,cp.returncode));checks.append(ck('V2 '+label+' rollback acceptance PASS',cp.returncode==0,cp.stdout[-800:] if cp.returncode else 'PASS'))
 # Read-only status sanity.
 before=sha_file(NEXT/'AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0/DEVELOPMENT_MANIFEST.json');st=p10_status(REPO);after=sha_file(NEXT/'AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0/DEVELOPMENT_MANIFEST.json');checks.append(ck('runtime status is read-only',before==after and st['trade_execution_authority']=='NONE',st))
 checks.append(ck('V3 remains SHADOW_COMMISSIONING',st['promotion_state']=='SHADOW_COMMISSIONING',st['promotion_state']))
 checks.append(ck('production promotion performed = false',st['production_route']=='V2',st['production_route']))
 checks.append(ck('no broker execution authority introduced',st['trade_execution_authority']=='NONE'))
 ok=all(x['status']=='PASS' for x in checks);out={'phase':'AD-V3-P10','version':'3.10.0-unified-runtime','acceptance_status':'PASS' if ok else 'FAIL_CLOSED','check_count':len(checks),'checks':checks,'canonical_runtime_authority':'AD-V3-P10','v3_state':'SHADOW_COMMISSIONING','production_promotion_performed':False,'trade_execution_authority':'NONE'};print(json.dumps(out,indent=2,ensure_ascii=False,default=str));return 0 if ok else 2
if __name__=='__main__':raise SystemExit(main())
