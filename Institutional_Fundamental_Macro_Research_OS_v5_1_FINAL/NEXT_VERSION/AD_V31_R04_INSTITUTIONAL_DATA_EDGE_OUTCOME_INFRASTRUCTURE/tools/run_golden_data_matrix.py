from __future__ import annotations
import json,sys,tempfile,sqlite3,os
from pathlib import Path
from datetime import datetime,timezone,timedelta
HERE=Path(__file__).resolve();PH=HERE.parents[1];NEXT=PH.parent
if str(NEXT) not in sys.path:sys.path.insert(0,str(NEXT))
from AD_V31_R04_INSTITUTIONAL_DATA_EDGE_OUTCOME_INFRASTRUCTURE.providers.ice_dxy_delayed import ICEDXYDelayedPublic
from AD_V31_R04_INSTITUTIONAL_DATA_EDGE_OUTCOME_INFRASTRUCTURE.runtime.real_rate_proxy import build as real_rate
from AD_V31_R04_INSTITUTIONAL_DATA_EDGE_OUTCOME_INFRASTRUCTURE.runtime.provider_failover import choose,equivalent
from AD_V31_R04_INSTITUTIONAL_DATA_EDGE_OUTCOME_INFRASTRUCTURE.runtime.pit_store import put,query,verify
from AD_V31_R04_INSTITUTIONAL_DATA_EDGE_OUTCOME_INFRASTRUCTURE.runtime.outcome_recovery import recover_for_prediction,default_store
from AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0.runtime.outcome_evaluator import evaluate_prediction,select_window
from AD_V31_R02_DECISION_SCIENCE_2_0.runtime.historical_normalizer import normalize as r02_normalize

def ck(name,ok,detail=None):return {'name':name,'status':'PASS' if ok else 'FAIL','detail':detail}
def z(dt):return dt.astimezone(timezone.utc).isoformat().replace('+00:00','Z')
def pred(t0):
 return {'prediction_id':'PRED_R04','episode_id':'EP_R04','cohort_id':'COHORT_R04','horizon':'SESSION_1_6H','precommit_time':z(t0),'maturity_time':z(t0+timedelta(hours=6)),'price_anchor':{'value':2500.0,'scientific_series_id':'XAUUSD_SPOT_REFERENCE','instrument_key':'XAUUSD','source_fact_id':'XAUUSD_SPOT_PRICE','source_id':'T0_SOURCE'},'causal_direction':'BULLISH_GOLD','permission_candidate':'BUY_CANDIDATE','edge_state':'ACTIONABLE_EDGE','event_context':{'events':[]},'policy_versions':{}}
def addbars(root,pid='GOLDPRICEDEV_XAU_BARS',shift=0.0,partial=False):
 t0=datetime(2026,8,18,10,tzinfo=timezone.utc); idx=[0,60,120,180,240,300,350,360,370]
 if partial:idx=[0,180,360]
 for i,m in enumerate(idx):
  put(default_store(root),{'series_id':'XAUUSD_SPOT_REFERENCE','instrument':'XAUUSD','provider_id':pid,'economic_time':z(t0+timedelta(minutes=m)),'value':2500.0+shift+i*2,'unit':'USD_PER_OZ','quality':'TEST','directness':'DIRECT_MARKET_REFERENCE','record_class':'HISTORICAL_REFERENCE','metadata':{'resolution':'1m'}})
 return t0

def main():
 c=[]
 # A healthy direct DXY normalized fixture
 d=ICEDXYDelayedPublic.normalize_fixture({'value':102.5,'economic_time':'2026-08-18T12:00:00Z'});c.append(ck('A Healthy direct DXY typed identity',d['series_id']=='ICE_DXY_DIRECT' and d['directness']=='DIRECT' and d['value']==102.5,d))
 # B missing direct / proxy separate
 c.append(ck('B DXY missing never relabels USD proxy',not equivalent('ICE_DXY_DELAYED_PUBLIC','USD_PROXY_COMPLEX_PROVIDER')))
 # C conflict diagnostic semantic supported by separate identity
 c.append(ck('C DXY/proxy identities remain non-equivalent',not equivalent('ICE_DXY_DATA_API','USD_PROXY_COMPLEX_PROVIDER')))
 # D/E/F real rate
 n={'value':4.5,'economic_time':'2026-08-18T12:00:00Z','provider_id':'NOM'};i={'value':2.2,'economic_time':'2026-08-18T11:55:00Z','provider_id':'INF'};rr=real_rate(n,i);c.append(ck('D Intraday real-rate proxy healthy',rr['state']=='HEALTHY_PROXY' and rr['identity']=='INTRADAY_REAL_RATE_PROXY' and rr['official_real_yield'] is False,rr))
 bad=real_rate(n,{**i,'economic_time':'2026-08-18T10:00:00Z'});c.append(ck('E Stale proxy component degrades proxy',bad['state']=='STALE_COMPONENT_MISMATCH',bad))
 c.append(ck('F Official daily real yield distinct',rr['identity']!='OFFICIAL_REAL_YIELD_LIVE'))
 with tempfile.TemporaryDirectory() as td:
  root=Path(td);t0=addbars(root);p=pred(t0);rec=recover_for_prediction(p,root,allow_network=False);out=evaluate_prediction(p,[{'record_type':'AD_V3_P09_MARKET_OBSERVATION','observed_at_utc':o['observed_at_utc'],'value':o['value'],'provider_id':o['provider_id'],'source_id':o['provider_id'],'scientific_series_id':o['scientific_series_id'],'instrument_key':'XAUUSD','outcome_acquisition_mode':'HISTORICALLY_RECOVERED','metadata':o.get('metadata',{})} for o in rec['observations']],evaluation_time=z(t0+timedelta(hours=8)))
  c.append(ck('G Historical T+6H recovery',rec['state']=='RECOVERED_FROM_PIT' and out and out['outcome_acquisition_mode']=='HISTORICALLY_RECOVERED',{'recovery':rec['state'],'terminal':out and out['terminal_observation']}))
  # H no maturity observation in a clean store
  with tempfile.TemporaryDirectory() as t2:
   c.append(ck('H No valid maturity observation remains unevaluated',recover_for_prediction(p,Path(t2),allow_network=False)['state']=='NO_VALID_HISTORY'))
  c.append(ck('I Full path recovery',(out['path_coverage']['path_coverage_state']=='FULL'),out['path_coverage']))
  with tempfile.TemporaryDirectory() as t3:
   r3=Path(t3);addbars(r3,partial=True);rec3=recover_for_prediction(p,r3,allow_network=False);obs3=[{'observed_at_utc':o['observed_at_utc'],'value':o['value'],'source_id':o['provider_id'],'provider_id':o['provider_id'],'scientific_series_id':o['scientific_series_id'],'instrument_key':'XAUUSD','outcome_acquisition_mode':'HISTORICALLY_RECOVERED','metadata':o.get('metadata',{})} for o in rec3['observations']];o3=evaluate_prediction(p,obs3,evaluation_time=z(t0+timedelta(hours=8)));c.append(ck('J Partial path does not fabricate MFE/MAE',o3 is not None and o3['path_coverage']['path_coverage_state']=='PARTIAL' and o3['mfe_return'] is None and o3['mae_return'] is None,o3 and o3['path_coverage']))
  # idempotence/store integrity
  row={'series_id':'TEST','instrument':'X','provider_id':'P','economic_time':'2026-08-18T00:00:00Z','value':1.0,'unit':'x','quality':'TEST','directness':'DIRECT','record_class':'HISTORICAL_REFERENCE','metadata':{}}
  _,a=put(default_store(root),row);_,b=put(default_store(root),row);c.append(ck('K PIT duplicate write idempotent',a is True and b is False))
  # tamper
  db=default_store(root);con=sqlite3.connect(db);con.execute("UPDATE observations SET value=999 WHERE series_id='TEST'");con.commit();con.close();c.append(ck('T Store tamper detection',verify(db)['status']=='FAIL',verify(db)))
 # Failover
 h={'ICE_DXY_DELAYED_PUBLIC':{'state':'UNAVAILABLE'},'ICE_DXY_DATA_API':{'state':'HEALTHY'}};fo=choose('ICE_DXY_DELAYED_PUBLIC',['ICE_DXY_DATA_API'],h);c.append(ck('K2 Equivalent direct-provider failover',fo.get('fallback_used') is True and fo.get('provider_id')=='ICE_DXY_DATA_API',fo))
 inv=choose('ICE_DXY_DELAYED_PUBLIC',['USD_PROXY_COMPLEX_PROVIDER'],{'ICE_DXY_DELAYED_PUBLIC':{'state':'UNAVAILABLE'},'USD_PROXY_COMPLEX_PROVIDER':{'state':'HEALTHY'}});c.append(ck('L Invalid scientific failover rejected',inv.get('provider_id') is None,inv))
 # M/N schema drift semantics through strict fixture parser
 try:ICEDXYDelayedPublic.normalize_fixture({'x':1});m=False
 except Exception:m=True
 c.append(ck('M HTML/typed parser schema drift fails closed',m))
 try:ICEDXYDelayedPublic.normalize_fixture({'value':0,'economic_time':'2026-08-18T00:00:00Z'});n=False
 except Exception:n=True
 c.append(ck('N Value sanity rejects impossible DXY',n))
 # O/P/Q gap contracts
 reg=json.loads((PH/'config/provider_capability_registry.json').read_text());by={x['provider_id']:x for x in reg['providers']}
 c.append(ck('O Paid entitlement is explicit',by['ICE_DXY_DATA_API']['entitlement_required'] and by['ICE_DXY_DATA_API']['access_class']=='PAID'))
 c.append(ck('P Paid depth remains gap',by['CME_LICENSED_DEPTH']['activation_state']=='PAID_GAP'))
 c.append(ck('Q Private flow remains private gap',by['LONDON_OTC_PRIVATE_FLOW']['activation_state']=='PRIVATE_GAP'))
 # R backfill not prospective by policy
 pitpol=json.loads((PH/'config/pit_store_policy.json').read_text());c.append(ck('R Backfill never prospective',pitpol['backfill_is_prospective'] is False))
 # S revision preservation
 with tempfile.TemporaryDirectory() as td:
  db=Path(td)/'db.sqlite3';base={'series_id':'MACRO','provider_id':'OFFICIAL','economic_time':'2026-08-01T12:00:00Z','value':1.0,'record_class':'LIVE_CAPTURED','metadata':{},'revision':0};put(db,base);put(db,{**base,'value':1.1,'revision':1,'revision_time':'2026-08-02T12:00:00Z'});rows=query(db,'MACRO');c.append(ck('S Macro revision preserves first seen',len(rows)==2 and rows[0]['value']==1.0 and rows[1]['value']==1.1,[(x['revision'],x['value']) for x in rows]))
 # U/V scientific semantic config
 gap=json.loads((PH/'config/data_gap_registry.json').read_text());ids={x['gap_id'] for x in gap['gaps']};c.append(ck('U GC volume does not create signed aggressor flow','GC_AGGRESSOR_FLOW' in ids));c.append(ck('V Options activity does not create dealer gamma','DEALER_GAMMA' in ids))
 # W provider conflict
 with tempfile.TemporaryDirectory() as td:
  root=Path(td);t0=addbars(root,'GOLDPRICEDEV_XAU_BARS',0);addbars(root,'TWELVEDATA_XAUUSD',20);rc=recover_for_prediction(pred(t0),root,allow_network=False);c.append(ck('W Outcome provider conflict surfaced',rc['state']=='OUTCOME_DATA_CONFLICT',rc['state']))
 # X current price is never substituted
 with tempfile.TemporaryDirectory() as td:
  root=Path(td);p=pred(datetime(2026,8,18,10,tzinfo=timezone.utc));rc=recover_for_prediction(p,root,allow_network=False);c.append(ck('X Current-price-as-outcome rejected',rc['state']=='NO_VALID_HISTORY' and not rc['current_price_substitution_used'],rc))
 # R02 no lookahead: future is rejected
 hist=[{'value':x,'timestamp':f'2026-08-{d:02d}T00:00:00Z'} for d,x in zip(range(1,17),range(1,17))]
 try:r02_normalize(5,hist,as_of='2026-08-10T00:00:00Z');la=False
 except ValueError as e:la='LOOKAHEAD' in str(e)
 c.append(ck('R02 normalization rejects future history',la))
 # no secrets committed
 bad=[]
 for pth in list((PH/'config').glob('*'))+list((PH/'providers').glob('*.py')):
  txt=pth.read_text(encoding='utf-8',errors='ignore').lower()
  if any(x in txt for x in ['sk-'+'live','bearer eyj']):bad.append(pth.name)
 c.append(ck('Secret scan clean',not bad,bad))
 ok=all(x['status']=='PASS' for x in c);out={'phase':'AD-V3.1-R04','matrix':'GOLDEN_DATA_MATRIX','status':'PASS' if ok else 'FAIL','case_count':len(c),'cases':c};print(json.dumps(out,indent=2,ensure_ascii=False));return 0 if ok else 2
if __name__=='__main__':raise SystemExit(main())
