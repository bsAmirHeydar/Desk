#!/usr/bin/env python3
from __future__ import annotations
import json,pathlib,sys,re
HERE=pathlib.Path(__file__).resolve();PH=HERE.parents[1];NEXT=PH.parent;REPO=NEXT.parents[1];sys.path.insert(0,str(NEXT))
from AD_V3_PHASE_12_FINAL_CERTIFICATION_PRODUCTION_FREEZE.runtime.common import load
from AD_V3_PHASE_12_FINAL_CERTIFICATION_PRODUCTION_FREEZE.runtime.freeze import verify_manifest
from AD_V3_PHASE_12_FINAL_CERTIFICATION_PRODUCTION_FREEZE.runtime.gates import GATE_IDS

def ck(n,o,d=None):return {'name':n,'status':'PASS' if o else 'FAIL','detail':d}
def main():
 c=[];auth=load(PH/'config/final_authority_map.json',{});c.append(ck('one canonical owner per major authority',all(x.get('canonical_count')==1 for x in auth.get('authorities',[])) and len({x['domain'] for x in auth.get('authorities',[])})==15));const=load(PH/'config/final_scientific_constitution.json',{});c.append(ck('scientific constitution consolidated',len(const.get('invariants',[]))>=24));fr=verify_manifest(REPO);c.append(ck('science freeze valid',fr.get('classes',{}).get('SCIENTIFIC_IMMUTABLE',{}).get('status')=='PASS'));c.append(ck('runtime freeze valid',fr.get('classes',{}).get('RUNTIME_IMMUTABLE',{}).get('status')=='PASS'));c.append(ck('report freeze valid',fr.get('classes',{}).get('REPORT_CONTRACT_IMMUTABLE',{}).get('status')=='PASS'));c.append(ck('certification governance freeze valid',fr.get('classes',{}).get('CERTIFICATION_IMMUTABLE',{}).get('status')=='PASS'));pol=load(PH/'config/final_promotion_gate_registry.json',{});decl=tuple(x['gate_id'] for x in pol.get('gates',[]));c.append(ck('declared gates equal machine gates',decl==GATE_IDS));c.append(ck('automatic promotion forbidden',pol.get('automatic_promotion_forbidden') is True));c.append(ck('P09 sample maturity gate is mandatory','P09_SAMPLE_MATURITY_GATE' in decl));c.append(ck('R01 forward quality gates are mandatory',all(x in decl for x in ['R01_FORWARD_QUALITY_GATE','R01_COVERAGE_GATE','R01_CRITICAL_SUBGROUP_GATE'])));c.append(ck('R01-R05 implementation gates are mandatory',all(x in decl for x in ['R01_IMPLEMENTATION_PASS','R02_IMPLEMENTATION_PASS','R03_IMPLEMENTATION_PASS','R04_IMPLEMENTATION_PASS','R05_IMPLEMENTATION_PASS'])));c.append(ck('explicit approval is mandatory','EXPLICIT_OPERATOR_APPROVAL' in decl));rp=load(NEXT/'AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN/config/route_policy.json',{});c.append(ck('production routing source remains P10',rp.get('routing_authority')=='AD-V3-P10'));rc=load(NEXT/'AD_V3_PHASE_11_FINAL_INSTITUTIONAL_GOLD_CONTROL_ROOM/config/report_contract.json',{});c.append(ck('canonical V3 HTML remains P11',rc.get('canonical_v3_html_authority')=='AD-V3-P11'));c.append(ck('trade execution authority NONE',auth.get('trade_execution_authority')=='NONE'))
 # Obvious secret and absolute-path scan in canonical V3 source/config surfaces.
 files=[]
 for d in [NEXT/'AD_V3_PHASE_03_CAUSAL_GOLD_BRAIN_DECISION_ENGINE',NEXT/'AD_V3_PHASE_06_GOVERNED_SEMANTIC_INTELLIGENCE',NEXT/'AD_V3_PHASE_07_LIVE_INTRADAY_GOLD_DATA_KERNEL',NEXT/'AD_V3_PHASE_08_DECISION_SCIENCE_CALIBRATION',NEXT/'AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0',NEXT/'AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN',NEXT/'AD_V3_PHASE_11_FINAL_INSTITUTIONAL_GOLD_CONTROL_ROOM',NEXT/'AD_V31_R01_FORWARD_QUALITY_PROMOTION_SCIENCE',NEXT/'AD_V31_R02_DECISION_SCIENCE_2_0',NEXT/'AD_V31_R03_ANTIFRAGILE_MULTI_SCENARIO_PERSPECTIVE',NEXT/'AD_V31_R04_INSTITUTIONAL_DATA_EDGE_OUTCOME_INFRASTRUCTURE',NEXT/'AD_V31_R05_OPERATIONS_HUMAN_INTELLIGENCE_FINALIZATION',PH]:
  files += [p for p in d.rglob('*') if p.is_file() and p.suffix.lower() in {'.py','.json','.md','.ps1'} and 'artifacts' not in p.parts and '__pycache__' not in p.parts]
 secret=[];absu=[]
 for p in files:
  t=p.read_text(encoding='utf-8',errors='ignore')
  if re.search(r'(?i)(sk-[A-Za-z0-9]{24,}|AKIA[0-9A-Z]{16}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)',t):secret.append(p.relative_to(REPO).as_posix())
  if re.search(r'(?i)C:\\\\Users\\\\SARMAYEHM-PC',t):absu.append(p.relative_to(REPO).as_posix())
 c.append(ck('obvious secret scan clean',not secret,secret));c.append(ck('user-specific absolute source paths absent',not absu,absu))
 ok=all(x['status']=='PASS' for x in c);out={'phase':'AD-V3-P12','version':'3.12.5-v31-r05-operations','status':'PASS' if ok else 'FAIL_CLOSED','check_count':len(c),'checks':c};print(json.dumps(out,ensure_ascii=False,indent=2));return 0 if ok else 2
if __name__=='__main__':raise SystemExit(main())
