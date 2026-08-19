from __future__ import annotations
import sys,json,tempfile
from pathlib import Path
from datetime import datetime,timezone,timedelta
HERE=Path(__file__).resolve();PH=HERE.parents[1];NEXT=PH.parent
if str(NEXT) not in sys.path:sys.path.insert(0,str(NEXT))
from AD_V31_R04_INSTITUTIONAL_DATA_EDGE_OUTCOME_INFRASTRUCTURE.runtime.pit_store import put
from AD_V31_R04_INSTITUTIONAL_DATA_EDGE_OUTCOME_INFRASTRUCTURE.runtime.outcome_recovery import default_store,recover_for_prediction
from AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0.runtime.outcome_evaluator import evaluate_prediction

def z(x):return x.isoformat().replace('+00:00','Z')
def main():
 t0=datetime(2026,8,18,10,tzinfo=timezone.utc);p={'prediction_id':'CERT_PRED','episode_id':'CERT_EP','cohort_id':'CERT_COHORT','horizon':'SESSION_1_6H','precommit_time':z(t0),'maturity_time':z(t0+timedelta(hours=6)),'price_anchor':{'value':2500.0,'scientific_series_id':'XAUUSD_SPOT_REFERENCE','instrument_key':'XAUUSD'},'causal_direction':'BULLISH_GOLD','permission_candidate':'BUY_CANDIDATE','edge_state':'ACTIONABLE_EDGE','event_context':{'events':[]},'policy_versions':{}}
 with tempfile.TemporaryDirectory() as td:
  root=Path(td)
  for m,v in [(0,2500),(60,2504),(120,2502),(180,2510),(240,2512),(300,2514),(350,2515),(360,2518),(370,2517)]:
   put(default_store(root),{'series_id':'XAUUSD_SPOT_REFERENCE','instrument':'XAUUSD','provider_id':'GOLDPRICEDEV_XAU_BARS','economic_time':z(t0+timedelta(minutes=m)),'value':float(v),'record_class':'HISTORICAL_REFERENCE','metadata':{'resolution':'1m'}})
  r1=recover_for_prediction(p,root,False);r2=recover_for_prediction(p,root,False)
  def p09obs(r):return [{'observed_at_utc':o['observed_at_utc'],'value':o['value'],'provider_id':o['provider_id'],'source_id':o['provider_id'],'scientific_series_id':o['scientific_series_id'],'instrument_key':'XAUUSD','outcome_acquisition_mode':'HISTORICALLY_RECOVERED','metadata':o.get('metadata',{})} for o in r['observations']]
  out=evaluate_prediction(p,p09obs(r1),evaluation_time=z(t0+timedelta(hours=12)))
  checks={'late_fixed_horizon_recovery':r1['state']=='RECOVERED_FROM_PIT','idempotent_recovery':[o['record_checksum'] for o in r1['observations']]==[o['record_checksum'] for o in r2['observations']],'terminal_not_retrieval_time':out and out['terminal_observation']['observed_at_utc']==z(t0+timedelta(hours=6)),'acquisition_mode':out and out['outcome_acquisition_mode']=='HISTORICALLY_RECOVERED','path_full':out and out['path_coverage']['path_coverage_state']=='FULL','current_price_substitution':r1['current_price_substitution_used'] is False}
  ok=all(checks.values());res={'record_type':'AD_V31_R04_OUTCOME_RECOVERY_CERTIFICATION','status':'PASS' if ok else 'FAIL','prediction_created_prospectively_fixture':True,'backfill_created_prediction':False,'checks':checks,'outcome':out,'real_forward_ledger_mutated':False};print(json.dumps(res,indent=2));return 0 if ok else 2
if __name__=='__main__':raise SystemExit(main())
