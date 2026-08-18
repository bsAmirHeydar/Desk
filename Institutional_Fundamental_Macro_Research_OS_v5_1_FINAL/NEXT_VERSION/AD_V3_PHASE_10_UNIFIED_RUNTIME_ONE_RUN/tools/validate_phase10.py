from __future__ import annotations
import json,pathlib,sys,hashlib
HERE=pathlib.Path(__file__).resolve();PH=HERE.parents[1];NEXT=PH.parent;REPO=NEXT.parents[1];sys.path.insert(0,str(NEXT))
from AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN.runtime.common import load

def ck(n,o,d=None):return {'name':n,'status':'PASS' if o else 'FAIL','detail':d}
def main():
 c=[]
 req=['config/runtime_contract.json','config/route_policy.json','config/stage_dag.json','runtime/gold_orchestrator.py','runtime/runtime_router.py','runtime/artifact_manager.py','tools/alpha_desk.py','schemas/run_result.schema.json','schemas/stage_receipt.schema.json','schemas/control_room_input.schema.json','schemas/routing_receipt.schema.json']
 c.append(ck('required P10 surfaces present',all((PH/x).exists() for x in req),[x for x in req if not (PH/x).exists()]))
 dag=load(PH/'config/stage_dag.json');ids={x['stage_id'] for x in dag['stages']};deps={x['stage_id']:x['depends_on'] for x in dag['stages']}
 c.append(ck('mandatory stage DAG contains canonical stages',{'PRECHECK','FORWARD_EVALUATION','ACQUISITION_PLAN','ACQUISITION','PRE_SEMANTIC','SEMANTIC','FINAL_CAUSAL','DECISION_CALIBRATION','FORWARD_PRECOMMIT','CONTROL_MODEL','REPORT','SEAL'}<=ids,sorted(ids)))
 # cycle check
 visiting=set();done=set();cyc=False
 def walk(n):
  nonlocal cyc
  if n in visiting:cyc=True;return
  if n in done:return
  visiting.add(n)
  for d in deps.get(n,[]):
   if d not in ids:cyc=True
   else:walk(d)
  visiting.remove(n);done.add(n)
 for n in ids:walk(n)
 c.append(ck('V3 stage DAG acyclic and dependencies reachable',not cyc and done==ids,{'visited':len(done),'stages':len(ids)}))
 rt=load(PH/'config/runtime_contract.json');c.append(ck('P10 has no scientific authority',rt['semantic_authority']=='AD-V3-P06' and rt['causal_authority']=='AD-V3-P03' and rt['decision_authority']=='AD-V3-P08' and rt['forward_authority']=='AD-V3-P09' and rt['trade_execution_authority']=='NONE',rt))
 legacy=load(PH/'config/legacy_authority_policy.json');c.append(ck('V2 P11 prompt authority retired from V3',legacy['v2_p11_prompt_cluster']['v3_decision_authority'] is False and legacy['canonical_v3_orchestrator']=='AD-V3-P10',legacy))
 src=(PH/'runtime/gold_orchestrator.py').read_text(encoding='utf-8-sig');c.append(ck('V3 orchestrator has no V2 P11 prompt dependency','AD_V2_PHASE_11' not in src and 'prompt_cluster' not in src))
 launch=(REPO/'AlphaDesk.ps1').read_text(encoding='utf-8-sig');c.append(ck('PowerShell is thin P10 wrapper','AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN' in launch and 'alpha_desk.py' in launch and 'Get-V3RouteMode' not in launch and 'Invoke-V2' not in launch))
 gi=(REPO/'.gitignore').read_text(encoding='utf-8-sig');c.append(ck('P10 runtime artifacts gitignored','/Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL/NEXT_VERSION/AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN/artifacts/' in gi))
 baseline=load(PH/'baseline/PRE_P10_AUTHORITY_HASHES.json',{}) or {};drift=[]
 allowed_r01={
 'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL/NEXT_VERSION/AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0/runtime/forward_statistics.py',
 'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL/NEXT_VERSION/AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0/runtime/forward_runtime.py'}
 for rel,want in (baseline.get('files') or {}).items():
  fp=REPO/rel
  got=hashlib.sha256(fp.read_bytes()).hexdigest() if fp.exists() else None
  if got!=want and rel not in allowed_r01: drift.append({'file':rel,'expected':want,'actual':got})
 c.append(ck('P03/P06/P07/P08 unchanged and P09 drift bounded to R01 instrumentation',not drift,drift))
 ok=all(x['status']=='PASS' for x in c);out={'phase':'AD-V3-P10','validation_status':'PASS' if ok else 'FAIL','check_count':len(c),'checks':c};print(json.dumps(out,indent=2,ensure_ascii=False));return 0 if ok else 2
if __name__=='__main__':raise SystemExit(main())
