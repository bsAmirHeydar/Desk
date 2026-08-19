from __future__ import annotations
import json,sys,subprocess,tempfile,hashlib
from pathlib import Path
HERE=Path(__file__).resolve();PH=HERE.parents[1];NEXT=PH.parent;REPO=NEXT.parents[1]
if str(NEXT) not in sys.path:sys.path.insert(0,str(NEXT))
from AD_V31_R04_INSTITUTIONAL_DATA_EDGE_OUTCOME_INFRASTRUCTURE.runtime.common import load_json
from AD_V31_R04_INSTITUTIONAL_DATA_EDGE_OUTCOME_INFRASTRUCTURE.runtime.data_freeze import verify_manifest
from AD_V31_R04_INSTITUTIONAL_DATA_EDGE_OUTCOME_INFRASTRUCTURE.runtime.data_edge_runtime import status

def ck(n,o,d=None):return {'name':n,'status':'PASS' if o else 'FAIL','detail':d}
def run(path):
 cp=subprocess.run([sys.executable,str(path)],capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=300)
 try:o=json.loads(cp.stdout)
 except Exception:o={'raw':cp.stdout[-1000:],'stderr':cp.stderr[-1000:]}
 return cp.returncode,o

def main():
 checks=[]
 # R04 static validation
 rc,v=run(PH/'tools/validate_r04.py');checks.append(ck('R04 static validation PASS',rc==0 and v.get('validation_status')=='PASS',v if rc else None));checks.extend(v.get('checks',[]) if isinstance(v,dict) else [])
 # Golden Data Matrix every case is an acceptance check.
 rc,g=run(PH/'tools/run_golden_data_matrix.py');checks.append(ck('Golden Data Matrix PASS',rc==0 and g.get('status')=='PASS',g if rc else None));checks.extend(g.get('cases',[]) if isinstance(g,dict) else [])
 # Outcome certification dimensions.
 rc,o=run(PH/'tools/run_outcome_recovery_certification.py');checks.append(ck('Outcome recovery certification PASS',rc==0 and o.get('status')=='PASS',o if rc else None))
 for k,val in (o.get('checks') or {}).items():checks.append(ck('Outcome recovery: '+k,val))
 # Previous science/regression compatibility.
 prev=[('P05',NEXT/'AD_V3_PHASE_05_INTEGRITY_ARCHITECTURE_CONSOLIDATION/tools/run_phase05_acceptance.py','acceptance_status'),('P09',NEXT/'AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0/tools/run_phase09_acceptance.py','acceptance_status'),('P10',NEXT/'AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN/tools/run_phase10_acceptance.py','acceptance_status'),('P11',NEXT/'AD_V3_PHASE_11_FINAL_INSTITUTIONAL_GOLD_CONTROL_ROOM/tools/run_phase11_acceptance.py','acceptance_status'),('R01',NEXT/'AD_V31_R01_FORWARD_QUALITY_PROMOTION_SCIENCE/tools/run_r01_acceptance.py','acceptance_status'),('R02',NEXT/'AD_V31_R02_DECISION_SCIENCE_2_0/tools/run_r02_acceptance.py','acceptance_status'),('R03',NEXT/'AD_V31_R03_ANTIFRAGILE_MULTI_SCENARIO_PERSPECTIVE/tools/run_r03_acceptance.py','acceptance_status')]
 for name,path,key in prev:
  rc,x=run(path);checks.append(ck(name+' downstream compatibility PASS',rc==0 and x.get(key)=='PASS',x.get(key) if isinstance(x,dict) else None))
 # Governance and operator contract.
 fr=verify_manifest();checks.append(ck('R04 data freeze PASS',fr.get('status')=='PASS',fr))
 st=status();checks.append(ck('V3 remains SHADOW_COMMISSIONING',st.get('V3_state')=='SHADOW_COMMISSIONING'));checks.append(ck('R04 cannot promote',st.get('promotion_performed') is False));checks.append(ck('trade execution authority NONE',st.get('trade_execution_authority')=='NONE'))
 alpha=(NEXT/'AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN/tools/alpha_desk.py').read_text();checks.append(ck('commission Gold remains canonical front door','run-r04-gold' not in alpha and "cmd=='commission'" in alpha));checks.append(ck('R04 status commands are read-only dispatches','v31-data-edge-status' in alpha and 'v31-outcome-infrastructure-status' in alpha))
 gates=load_json(NEXT/'AD_V3_PHASE_12_FINAL_CERTIFICATION_PRODUCTION_FREEZE/config/final_promotion_gate_registry.json',{}) or {};gids=[x['gate_id'] for x in gates.get('gates',[])];checks.append(ck('P12 declares R04 implementation gate','R04_IMPLEMENTATION_PASS' in gids));checks.append(ck('automatic promotion remains forbidden',gates.get('automatic_promotion_forbidden') is True))
 # Live smoke honesty.
 ls=load_json(PH/'qualification/R04_LIVE_SMOKE.json',{}) or {};checks.append(ck('live smoke is truthfully not fabricated',str(ls.get('status','')).startswith('NOT_RUN') or ls.get('status')=='PASS',ls))
 # PIT runtime artifacts ignored.
 gi=(REPO/'.gitignore').read_text(encoding='utf-8-sig');checks.append(ck('R04 runtime artifacts gitignored','AD_V31_R04_INSTITUTIONAL_DATA_EDGE_OUTCOME_INFRASTRUCTURE/artifacts/' in gi))
 # Count goal informational but not magic.
 ok=all(x['status']=='PASS' for x in checks);out={'phase':'AD-V3.1-R04','version':'3.1.4-institutional-data-edge','acceptance_status':'PASS' if ok else 'FAIL_CLOSED','check_count':len(checks),'checks':checks,'golden_data_status':g.get('status'),'golden_case_count':g.get('case_count'),'outcome_recovery_status':o.get('status'),'live_smoke_status':ls.get('status'),'data_edge_status':st,'baseline_commit':'f0bba8e','V3_state':'SHADOW_COMMISSIONING','production_promotion_performed':False,'trade_execution_authority':'NONE'};print(json.dumps(out,indent=2,ensure_ascii=False));return 0 if ok else 2
if __name__=='__main__':raise SystemExit(main())
