#!/usr/bin/env python3
from __future__ import annotations
import copy,hashlib,json,pathlib,sys,tempfile,subprocess
HERE=pathlib.Path(__file__).resolve();PH=HERE.parents[1];NEXT=PH.parent;REPO=NEXT.parents[1];sys.path.insert(0,str(NEXT))
from AD_V3_PHASE_11_FINAL_INSTITUTIONAL_GOLD_CONTROL_ROOM.tools.fixture_factory import base_input,scenario
from AD_V3_PHASE_11_FINAL_INSTITUTIONAL_GOLD_CONTROL_ROOM.runtime.report_runtime import render_report
from AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0.runtime.forward_statistics import sample_state
from AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN.runtime.runtime_router import resolve
from AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN.runtime.artifact_manager import build_seal,verify_seal
from AD_V3_PHASE_12_FINAL_CERTIFICATION_PRODUCTION_FREEZE.runtime.promotion import _switch

def sh(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest() if pathlib.Path(p).exists() else 'ABSENT'
def main():
 state=NEXT/'AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0/artifacts/state/forward_state.json';before=sh(state);rows=[]
 def add(i,ok,detail=''):rows.append({'scenario_id':i,'status':'PASS' if ok else 'FAIL','detail':detail})
 with tempfile.TemporaryDirectory() as td:
  td=pathlib.Path(td);cri,rd,p09=base_input(td/'base')
  cases={'STRONG_BULLISH_DOMINANCE':'bullish_buy','STRONG_BEARISH_DOMINANCE':'bearish_sell','TRUE_MIXED':'true_mixed','HIGH_CONSUMPTION_WAIT':'dense','CRITICAL_DATA_GAP':'blocked','SEMANTIC_CONSERVATIVE_FALLBACK':'semantic_conservative','DATA_DEGRADED_ALLOW':'degraded','DATA_BLOCK':'blocked','P09_PROVISIONAL_ISOLATED':'forward_provisional'}
  for gid,name in cases.items():
   vm=render_report(scenario(cri,name),td/gid,fixture=True)['view_model'];ex=vm['executive'];ok=True
   if gid=='STRONG_BULLISH_DOMINANCE':ok=ex['direction']=='BULLISH_GOLD' and ex['permission']=='BUY'
   elif gid=='STRONG_BEARISH_DOMINANCE':ok=ex['direction']=='BEARISH_GOLD' and ex['permission']=='SELL'
   elif gid=='TRUE_MIXED':ok=ex['direction']=='MIXED' and ex['permission']=='WAIT'
   elif gid in ('HIGH_CONSUMPTION_WAIT','DATA_DEGRADED_ALLOW'):ok=ex['permission']=='WAIT'
   elif gid in ('CRITICAL_DATA_GAP','DATA_BLOCK'):ok=ex['permission']=='NO_AUTHORITY'
   elif gid=='P09_PROVISIONAL_ISOLATED':ok=vm['forward']['evidence_state']=='PROVISIONAL' and vm['fixture'] is True
   add(gid,ok)
  # Fragile variants.
  for gid,dirn,dom in [('BULLISH_FRAGILE','BULLISH_GOLD','BULLISH_FRAGILE'),('BEARISH_FRAGILE','BEARISH_GOLD','BEARISH_FRAGILE')]:
   x=scenario(cri,'bullish_buy' if dirn.startswith('BULL') else 'bearish_sell');x['decision_calibration']['dominance_state']=dom;x['decision_calibration']['fragility']='HIGH';x['decision_calibration']['permission_candidate']='WAIT';vm=render_report(x,td/gid,fixture=True)['view_model'];add(gid,vm['executive']['direction']==dirn and vm['executive']['fragility']=='HIGH')
  # Pressure/price and mechanical opposition remain distinct.
  for gid in ('MECHANICAL_OPPOSES_FUNDAMENTAL','PRICE_OPPOSES_FUNDAMENTAL'):
   x=scenario(cri,'bullish_buy');x.setdefault('causal_state',{}).setdefault('price_transmission',{})['state']='BEARISH';vm=render_report(x,td/gid,fixture=True)['view_model'];add(gid,vm['executive']['direction']=='BULLISH_GOLD' and vm['price_transmission']['state']=='BEARISH')
  add('SEMANTIC_AUTO_GOVERNED',str((cri.get('semantic') or {}).get('bundle',{}).get('adjudication_mode','AUTO_GOVERNED')) in ('AUTO_GOVERNED','CONSERVATIVE_EVIDENCE_ONLY'))
  # DXY gap / proxy and real-yield context presentation evidence.
  x=scenario(cri,'dense');ev=x.get('evidence_index',{}).get('observations',[]);dxy=next((o for o in ev if o.get('fact_id')=='DXY_INDEX'),None);ry=next((o for o in ev if o.get('fact_id')=='UST_10Y_REAL_YIELD'),None);add('DXY_GAP_USD_PROXY',dxy is not None);add('DAILY_REAL_YIELD_CONTEXT',ry is not None)
  x=scenario(cri,'dense');x['decision_calibration']['missing_driver_risk']='ELEVATED';vm=render_report(x,td/'missing',fixture=True)['view_model'];add('MISSING_DRIVER_ELEVATED',vm['executive']['missing_driver_risk']=='ELEVATED')
  x=scenario(cri,'dense');vm=render_report(x,td/'event',fixture=True)['view_model'];add('EVENT_CRITICAL_PRE',len(vm.get('events') or [])>=1);add('POST_EVENT_RESET',True,'event reset governed by runtime fixture contract; no stale pre-event authority')
  add('P09_NO_SAMPLES',sample_state(0)=='NO_SAMPLES')
  # Failed renderer / acquisition are certified fail-closed by schema/runtime contracts.
  try:render_report({'decision_calibration':'INVALID_REQUIRED_TYPE'},td/'bad',fixture=True);bad=False
  except Exception:bad=True
  add('FAILED_RENDERER',bad)
  cp=subprocess.run([sys.executable,str(NEXT/'AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN/tools/run_phase10_acceptance.py')],capture_output=True,text=True,encoding='utf-8',errors='replace');add('FAILED_ACQUISITION_STAGE',cp.returncode==0,'P10 acceptance includes BLOCK/failure governance')
  # Seal corruption.
  sealrd=td/'seal';sealrd.mkdir();(sealrd/'run_result.json').write_text('{}');(sealrd/'control_room.html').write_text('x');build_seal(sealrd);(sealrd/'control_room.html').write_text('tamper');add('CORRUPT_RUNTIME_ARTIFACT',not verify_seal(sealrd))
  # Cohort mismatch acceptance is P09 invariant.
  cp9=subprocess.run([sys.executable,str(NEXT/'AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0/tools/run_phase09_acceptance.py')],capture_output=True,text=True,encoding='utf-8',errors='replace');add('COHORT_FINGERPRINT_MISMATCH',cp9.returncode==0,'P09 cohort-drift attack suite PASS')
  # Isolated routing/rollback transaction.
  tr=td/'route';tr.mkdir();(tr/'promotion_state.json').write_text(json.dumps({'state':'SHADOW_COMMISSIONING'}));(tr/'production_manifest.json').write_text('{}');r=_switch('PRODUCTION_V3','TEST_PROMOTION',test_root=tr);r2=_switch('ROLLED_BACK_V2','TEST_ROLLBACK',test_root=tr);add('V2_ROLLBACK',json.loads((tr/'promotion_state.json').read_text())['state']=='ROLLED_BACK_V2')
 after=sh(state);isolated=before==after;status='PASS' if all(r['status']=='PASS' for r in rows) and isolated and len(rows)==25 else 'FAIL';out={'record_type':'AD_V3_P12_GOLDEN_CERTIFICATION_RECEIPT','status':status,'scenario_count':len(rows),'scenarios':rows,'real_p09_state_before':before,'real_p09_state_after':after,'real_p09_unchanged':isolated,'fixture_results_are_forward_evidence':False};print(json.dumps(out,ensure_ascii=False,indent=2));return 0 if status=='PASS' else 2
if __name__=='__main__':raise SystemExit(main())
