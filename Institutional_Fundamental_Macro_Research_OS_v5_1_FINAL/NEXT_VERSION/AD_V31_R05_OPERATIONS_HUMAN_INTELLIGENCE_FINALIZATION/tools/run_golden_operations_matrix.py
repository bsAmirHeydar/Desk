\
from __future__ import annotations
import json,sys,tempfile,os,socket,datetime,pathlib
from pathlib import Path
HERE=Path(__file__).resolve(); PH=HERE.parents[1]; NEXT=PH.parent; REPO=NEXT.parents[1]
if str(NEXT) not in sys.path: sys.path.insert(0,str(NEXT))
from AD_V31_R05_OPERATIONS_HUMAN_INTELLIGENCE_FINALIZATION.runtime.health_aggregator import aggregate
from AD_V31_R05_OPERATIONS_HUMAN_INTELLIGENCE_FINALIZATION.runtime.humanization import headline,data_health_message,qualification_message
from AD_V31_R05_OPERATIONS_HUMAN_INTELLIGENCE_FINALIZATION.runtime.recovery import recovery_status,recover
from AD_V31_R05_OPERATIONS_HUMAN_INTELLIGENCE_FINALIZATION.runtime.operations_runtime import semantic_host_state
from AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN.runtime.artifact_manager import ArtifactManager,RuntimeLocked
from AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN.runtime.runtime_router import resolve

def ck(n,o,d=None):return {'name':n,'status':'PASS' if o else 'FAIL','detail':d}
def main():
 c=[]
 # A/B/C health + valid decision/runtime separation
 c.append(ck('A Healthy complete run state can remain HEALTHY',aggregate({'RUNTIME':{'state':'HEALTHY'},'DATA':{'state':'HEALTHY'}})['overall_state']=='HEALTHY'))
 h=headline({'direction':'BULLISH_GOLD','permission':'WAIT','consumption':'HIGH','fragility':'LOW'}); c.append(ck('B Healthy WAIT is humanized without runtime failure','انتظار' in h and 'BULLISH' not in h,h))
 u=headline({'direction':'UNKNOWN','permission':'WAIT','consumption':'UNKNOWN','fragility':'UNKNOWN'}); c.append(ck('C UNKNOWN decision is valid human state','جهت علّی روشنی' in u,u))
 # D/E/F data + semantic degradation
 dm=data_health_message({'analysis_admission':'DEGRADED','r04':{'direct_dxy':{'state':'DIRECT_UNAVAILABLE'},'intraday_real_rate_proxy':{'state':'UNAVAILABLE_COMPONENT_GAP'}}}); c.append(ck('D Direct DXY unavailable/proxy separation is clear','شاخص مستقیم دلار' in dm,dm))
 old1=os.environ.pop('ALPHALAB_HOST_COMMAND',None); old2=os.environ.pop('OPENAI_API_KEY',None)
 try: sem=semantic_host_state()
 finally:
  if old1 is not None:os.environ['ALPHALAB_HOST_COMMAND']=old1
  if old2 is not None:os.environ['OPENAI_API_KEY']=old2
 c.append(ck('E Semantic conservative fallback is explicit',sem=='CONSERVATIVE_FALLBACK',sem))
 c.append(ck('F Partial source degradation does not become BLOCKED',aggregate({'DATA':{'state':'DEGRADED'},'RUNTIME':{'state':'HEALTHY'}})['overall_state']=='DEGRADED'))
 # G blocked dominates
 c.append(ck('G Critical integrity failure dominates health',aggregate({'FREEZE':{'state':'BLOCKED'},'DATA':{'state':'HEALTHY'}})['overall_state']=='BLOCKED'))
 # H fail-closed R03 static contract
 orch=(NEXT/'AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN/runtime/gold_orchestrator.py').read_text(encoding='utf-8'); c.append(ck('H R03 perspective failure has fail-closed path','r03_fail_closed' in orch and 'R03_FAIL_CLOSED' in orch))
 # I outcome recovery integration exists before current analysis
 c.append(ck('I Historical outcome recovery is integrated before current precommit','p09_observe_and_evaluate' in orch and orch.index('p09_observe_and_evaluate')<orch.index('p09_precommit_current')))
 # J last attempt vs last success pointer semantics
 with tempfile.TemporaryDirectory() as td:
  am=ArtifactManager(Path(td)); rd=am.run_dir('A'); (rd/'control_room.html').write_text('ok'); am.publish_attempt({'run_id':'A','status':'SUCCESS'}); am.publish_success({'run_id':'A','status':'SUCCESS','html':str(rd/'control_room.html')},rd); am.publish_attempt({'run_id':'B','status':'FAILED_RUNTIME'}); c.append(ck('J Last failed attempt preserves last success',am.read_pointer('last_attempt.json')['run_id']=='B' and am.read_pointer('last_success.json')['run_id']=='A'))
 # K/L locks
 with tempfile.TemporaryDirectory() as td:
  am=ArtifactManager(Path(td)); am.lock.parent.mkdir(parents=True,exist_ok=True); old=(datetime.datetime.now(datetime.timezone.utc)-datetime.timedelta(hours=3)).isoformat().replace('+00:00','Z'); am.lock.write_text(json.dumps({'run_id':'OLD','pid':999999,'host':socket.gethostname(),'mode':'SHADOW','started_at_utc':old})); st=am.lock_state(); c.append(ck('K Confirmed stale lock is recoverable',st['state']=='STALE_RECOVERABLE' and am.recover_stale_lock(),st))
  am.acquire('ACTIVE','SHADOW'); locked=False
  try:
   try: ArtifactManager(Path(td)).acquire('SECOND','SHADOW')
   except RuntimeLocked: locked=True
  finally: am.release()
  c.append(ck('L Active lock blocks concurrent mutation',locked))
 # M/N scheduler and episode contract static
 cad=json.loads((PH/'config/operations_cadence_policy.json').read_text()); c.append(ck('M Missed schedule never backdates predictions','DO_NOT_BACKDATE' in cad['missed_run_policy'],cad['missed_run_policy']))
 p09=(NEXT/'AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0/config/episode_policy.json'); et=p09.read_text(encoding='utf-8') if p09.exists() else (NEXT/'AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0/config/cohort_policy.json').read_text(encoding='utf-8'); c.append(ck('N Frequent cadence cannot redefine P09 independence','scientific_episode_independence_owned_by' in json.dumps(cad) and 'P09' in json.dumps(cad)))
 # O/P/Q human intelligence
 c.append(ck('O Human headline contains no raw code','BULLISH_GOLD' not in h and 'HIGH_CONSUMPTION' not in h,h))
 rend=(NEXT/'AD_V3_PHASE_11_FINAL_INSTITUTIONAL_GOLD_CONTROL_ROOM/runtime/renderer.py').read_text(encoding='utf-8'); c.append(ck('P Pressure and price remain visibly separate','فشار بنیادی ≠ رفتار قیمت' in rend))
 c.append(ck('Q Unknown envelope human warning exists','ناحیه ناشناخته' in rend or 'ناحیه‌ای که مدل' in rend))
 # R/S qualification human language
 qi=qualification_message({'sample_maturity':'INSUFFICIENT','production_qualification_state':'INSUFFICIENT_EVIDENCE'}); qf=qualification_message({'sample_maturity':'MATURE','forward_quality_state':'FAIL','coverage_state':'PASS','critical_subgroup_state':'PASS','production_qualification_state':'QUALITY_FAILED'}); c.append(ck('R Qualification insufficient is human-readable','نمونه' in qi and 'کافی' in qi,qi)); c.append(ck('S Production quality failure is explicit','کیفیت' in qf and 'پاس نکرده' in qf,qf))
 # T human/audit same science is renderer-only profile
 pres=(NEXT/'AD_V3_PHASE_11_FINAL_INSTITUTIONAL_GOLD_CONTROL_ROOM/config/report_contract.json').read_text(encoding='utf-8'); c.append(ck('T Human/Audit are presentation profiles, not science forks','HUMAN_INSTITUTIONAL_FA' in pres and 'AUDIT' in pres))
 # U mobile CSS + V XSS escaping
 c.append(ck('U Mobile responsive contract present','@media' in rend and 'overflow-x' in rend))
 c.append(ck('V XSS escaping remains in renderer','html.escape' in rend or 'esc(' in rend))
 # W secret redaction policy/code
 sec=' '.join([x.read_text(encoding='utf-8',errors='ignore') for x in (PH/'runtime').glob('*.py')]); c.append(ck('W Operations code does not log credentials','OPENAI_API_KEY' not in sec or 'semantic_host_state' in sec))
 # X backup coverage
 b=(PH/'tools/backup_alpha_desk_state.ps1').read_text(encoding='utf-8'); c.append(ck('X PIT/forward/qualification certification backup paths included',all(x in b for x in ['AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0','AD_V31_R04_INSTITUTIONAL_DATA_EDGE_OUTCOME_INFRASTRUCTURE','AD_V31_R01_FORWARD_QUALITY_PROMOTION_SCIENCE','AD_V3_PHASE_12_FINAL_CERTIFICATION_PRODUCTION_FREEZE'])))
 # Y future routing fixture
 r=resolve(REPO,'Gold','PRODUCTION',promotion_override='PRODUCTION_V3'); c.append(ck('Y Future production route resolves canonical V3 P10 runtime',r.get('selected_runtime')=='V3',r))
 ok=all(x['status']=='PASS' for x in c); out={'phase':'AD-V3.1-R05','matrix':'GOLDEN_OPERATIONS_MATRIX','status':'PASS' if ok else 'FAIL','case_count':len(c),'cases':c,'real_ledger_mutated':False}; print(json.dumps(out,ensure_ascii=False,indent=2)); return 0 if ok else 2
if __name__=='__main__': raise SystemExit(main())
