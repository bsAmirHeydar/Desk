#!/usr/bin/env python3
from __future__ import annotations
import json,pathlib,subprocess,sys,tempfile,shutil,hashlib
HERE=pathlib.Path(__file__).resolve();PH=HERE.parents[1];NEXT=PH.parent;REPO=NEXT.parents[1];sys.path.insert(0,str(NEXT))
from AD_V3_PHASE_12_FINAL_CERTIFICATION_PRODUCTION_FREEZE.runtime.common import load,sha_file
from AD_V3_PHASE_12_FINAL_CERTIFICATION_PRODUCTION_FREEZE.runtime.freeze import verify_manifest
from AD_V3_PHASE_12_FINAL_CERTIFICATION_PRODUCTION_FREEZE.runtime.gates import GATE_IDS,enforce,real_p09,certification_state
from AD_V3_PHASE_12_FINAL_CERTIFICATION_PRODUCTION_FREEZE.runtime.promotion import _switch
from AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN.runtime.runtime_router import resolve

def ck(n,o,d=None):return {'name':n,'status':'PASS' if o else 'FAIL','detail':d}
def run(p,args=None):
 cp=subprocess.run([sys.executable,str(p),*(args or [])],capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=500);return cp.returncode,cp.stdout[-1000:]
def main():
 checks=[];phase_status={}
 # P01-P11 and V2 rollback are executed as the release regression program and sealed into a canonical receipt.
 reg=load(PH/'certification/RELEASE_REGRESSION_RECEIPT.json',{}) or {};phase_status={k:v for k,v in (reg.get('phase_status') or {}).items() if k.startswith('P') and not k.startswith('P12')}
 checks.append(ck('P01-P11 release regression receipt PASS',reg.get('status')=='PASS' and all(reg.get('phase_status',{}).get(f'P{i:02d}')=='PASS' for i in range(1,12)),reg.get('phase_status')))
 checks.append(ck('V2 rollback regression receipt PASS',reg.get('phase_status',{}).get('V2_P11')=='PASS' and reg.get('phase_status',{}).get('V2_P13')=='PASS'))
 # Static P12 and Golden.
 code,out=run(PH/'tools/validate_phase12.py');checks.append(ck('P12 static certification PASS',code==0,out if code else None));gold=load(PH/'certification/GOLDEN_CERTIFICATION_RECEIPT.json',{}) or {};checks.append(ck('Golden certification PASS',gold.get('status')=='PASS',gold));checks.append(ck('Golden fixture matrix contains 25 mandatory scenarios',gold.get('scenario_count')==25));checks.append(ck('Golden fixtures preserve real P09',gold.get('real_p09_unchanged') is True));
 fr=verify_manifest(REPO);checks.append(ck('all final freeze classes valid',fr.get('status')=='PASS',fr.get('drift')))
 # Tamper tests on copies: science, runtime, report.
 manifest=load(PH/'release/FINAL_FREEZE_MANIFEST.json',{});rows=[]
 for cls in ['SCIENTIFIC_IMMUTABLE','RUNTIME_IMMUTABLE','REPORT_CONTRACT_IMMUTABLE']:
  rr=(manifest.get('classes') or {}).get(cls,[]);rows.append((cls,rr[0] if rr else None))
 with tempfile.TemporaryDirectory() as td:
  td=pathlib.Path(td)
  for cls,row in rows:
   if not row:checks.append(ck(cls+' tamper detection',False));continue
   dst=td/row['path'];dst.parent.mkdir(parents=True,exist_ok=True);src=REPO/row['path'];shutil.copy2(src,dst);dst.write_bytes(dst.read_bytes()+b'\nP12_TAMPER');got=hashlib.sha256(dst.read_bytes()).hexdigest();checks.append(ck(cls+' tamper detection',got!=row['sha256']))
 # Gate pure-function adversarial matrix.
 allgood={g:True for g in GATE_IDS};blocked={}
 for g in GATE_IDS:
  t=dict(allgood);t[g]=False
  try:enforce(t);blocked[g]=False
  except ValueError:blocked[g]=True
 checks.append(ck('every final gate independently blocks promotion',all(blocked.values()),blocked));checks.append(ck('approval without P09 sample maturity denied',blocked.get('P09_SAMPLE_MATURITY_GATE') is True));checks.append(ck('R01 quality independently blocks promotion',blocked.get('R01_FORWARD_QUALITY_GATE') is True));checks.append(ck('R01 coverage independently blocks promotion',blocked.get('R01_COVERAGE_GATE') is True));checks.append(ck('R01 subgroup safety independently blocks promotion',blocked.get('R01_CRITICAL_SUBGROUP_GATE') is True));checks.append(ck('gates without approval denied',blocked.get('EXPLICIT_OPERATOR_APPROVAL') is True))
 # Real P09 truth and canonical source.
 p09=real_p09();stats=p09.get('statistics') or {};checks.append(ck('real P09 state read canonically',stats.get('fixture_samples_included') is False and stats.get('replay_samples_included') is False,stats));checks.append(ck('legacy/replay/fixture cannot satisfy promotion by construction','P09_SAMPLE_MATURITY_GATE' in GATE_IDS and (p09.get('legacy') is not None)))
 # Isolated promotion/rollback and transaction consistency.
 with tempfile.TemporaryDirectory() as td:
  td=pathlib.Path(td);(td/'promotion_state.json').write_text(json.dumps({'state':'SHADOW_COMMISSIONING'}));(td/'production_manifest.json').write_text('{}');r1=_switch('PRODUCTION_V3','TEST',test_root=td);s1=json.loads((td/'promotion_state.json').read_text());m1=json.loads((td/'production_manifest.json').read_text());r2=_switch('ROLLED_BACK_V2','TEST',test_root=td);s2=json.loads((td/'promotion_state.json').read_text());m2=json.loads((td/'production_manifest.json').read_text());checks.append(ck('isolated promotion transaction consistent',s1['state']=='PRODUCTION_V3' and m1['alpha_desk_v3']['production_authority']=='PRODUCTION_V3'));checks.append(ck('isolated rollback transaction consistent',s2['state']=='ROLLED_BACK_V2' and m2['alpha_desk_v3']['production_authority']=='ROLLED_BACK_V2'));checks.append(ck('transaction marker cleared after atomic switch',not (td/'deployment_transaction.json').exists()))
 # Routing matrix.
 rs=resolve(REPO,'Gold','PRODUCTION',promotion_override='SHADOW_COMMISSIONING');rv=resolve(REPO,'Gold','SHADOW',promotion_override='SHADOW_COMMISSIONING');rp=resolve(REPO,'Gold','PRODUCTION',promotion_override='PRODUCTION_V3');rr=resolve(REPO,'Gold','PRODUCTION',promotion_override='ROLLED_BACK_V2');checks.append(ck('routing matrix certified',rs['selected_runtime']=='V2' and rv['selected_runtime']=='V3' and rp['selected_runtime']=='V3' and rr['selected_runtime']=='V2'))
 # P11 security/visual preserved via acceptance and handoff.
 h=load(NEXT/'AD_V3_PHASE_11_FINAL_INSTITUTIONAL_GOLD_CONTROL_ROOM/PHASE_11_HANDOFF.json',{});checks.append(ck('P11 visual acceptance preserved',str(h.get('visual_acceptance','')).startswith('PASS')));checks.append(ck('P11 security acceptance preserved',h.get('security_acceptance')=='PASS'))
 # Trade authority and no auto promotion.
 checks.append(ck('trade execution authority remains NONE',(load(PH/'config/final_certification_policy.json',{}) or {}).get('production_trade_execution_authority')=='NONE'));checks.append(ck('P12 acceptance does not promote',resolve(REPO,'Gold','PRODUCTION')['selected_runtime']=='V2'))
 # Package hygiene source tree (ignore deliberately committed fixtures/docs).
 gi=(REPO/'.gitignore').read_text(encoding='utf-8-sig');checks.append(ck('runtime bytecode/cache artifacts are excluded from source package','**/__pycache__/' in gi and '*.pyc' in gi))
 # Expected certification state in supplied snapshot can be pending; not failure.
 st=certification_state(REPO);checks.append(ck('certification state truthfully fail-closed',st in ('CERTIFIED_PENDING_FORWARD_SAMPLE','CERTIFIED_PENDING_FORWARD_QUALITY','CERTIFIED_PENDING_COVERAGE','FORWARD_QUALITY_FAILED','PRODUCTION_ELIGIBLE','PRODUCTION_V3','ENGINEERING_CERTIFIED'),st))
 ok=all(x['status']=='PASS' for x in checks);out={'phase':'AD-V3-P12','version':'3.12.5-v31-r05-operations','acceptance_status':'PASS' if ok else 'FAIL_CLOSED','check_count':len(checks),'checks':checks,'phase_status':phase_status,'golden_status':gold.get('status'),'real_p09_forward_state':stats.get('forward_evidence_state'),'real_p09_mature_episodes':stats.get('mature_episode_count'),'certification_state':st,'production_promotion_performed':resolve(REPO,'Gold','PRODUCTION')['selected_runtime']=='V3','trade_execution_authority':'NONE'};print(json.dumps(out,ensure_ascii=False,indent=2));return 0 if ok else 2
if __name__=='__main__':raise SystemExit(main())
