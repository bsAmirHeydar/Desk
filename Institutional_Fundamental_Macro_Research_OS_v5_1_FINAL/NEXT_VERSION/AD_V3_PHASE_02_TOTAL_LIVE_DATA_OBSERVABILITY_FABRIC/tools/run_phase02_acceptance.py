from __future__ import annotations
import json, pathlib, shutil, subprocess, sys, tempfile
HERE=pathlib.Path(__file__).resolve(); PHASE=HERE.parents[1]; sys.path.insert(0,str(PHASE))
from runtime.executor import execute, _attempt_source
import runtime.executor as executor_runtime
from runtime.http_client import FetchResult
from runtime.common import sha256_bytes
from runtime.planner import build_plan
from runtime.common import load_json

def C(name,ok,detail=None): return {'name':name,'status':'PASS' if ok else 'FAIL','detail':detail}
def main():
 checks=[]
 v=subprocess.run([sys.executable,str(PHASE/'tools/validate_phase02.py'),'--json'],capture_output=True,text=True)
 try: vd=json.loads(v.stdout)
 except: vd={'status':'FAIL','raw':v.stdout,'stderr':v.stderr}
 checks.append(C('phase02 static validation',v.returncode==0,vd))
 # Deterministic live-adapter contract smoke. This exercises the same _attempt_source
 # branch used by real network mode without depending on external Internet uptime.
 sr0=load_json(PHASE/'config/source_contract_registry.json'); pol0=load_json(PHASE/'config/acquisition_policy.json')
 src0=next(x for x in sr0['sources'] if x.get('collector_type') not in ('STATIC','GAP_ONLY','DERIVED_SOURCE'))
 class ContractClient:
  def __init__(self): self.calls=[]
  def fetch(self,source_id,url,method='GET',data=None,headers=None):
   self.calls.append((source_id,url)); body=b'AD_V3_P02_NETWORK_ADAPTER_SMOKE'
   return FetchResult(source_id,url,'SUCCESS',200,'text/plain',body,None,'2026-08-16T18:00:00Z',sha256_bytes(body),1)
 cc=ContractClient(); ca=_attempt_source(src0,pol0,'2026-08-16T18:00:00Z',None,False,cc)
 checks.append(C('live network adapter contract smoke',ca.get('ok') is True and ca.get('status_code')==200 and ca.get('source_id')==src0['source_id'] and len(cc.calls)==1,{'attempt':{k:v for k,v in ca.items() if k!='body'},'calls':cc.calls}))
 # A worker exception must be represented by the coverage system rather than crash execute().
 original_client=executor_runtime.PublicHttpClient
 class ExplodingClient:
  def __init__(self,policy): pass
  def fetch(self,source_id,url,method='GET',data=None,headers=None): raise RuntimeError('intentional_acceptance_worker_fault')
 executor_runtime.PublicHttpClient=ExplodingClient
 try:
  contained=executor_runtime.execute(PHASE,'ALL','2026-08-16T18:00:00Z',None,None,False)['coverage_receipt']
  worker_ok=(contained['analysis_admission']=='BLOCKED' and any((a.get('error') or '').startswith('NETWORK_WORKER_EXCEPTION:RuntimeError:') for a in contained.get('source_attempts',[])))
  checks.append(C('network worker exception contained by coverage gate',worker_ok,{'state':contained['analysis_admission'],'failed_blocking':contained['fact_counts']['failed_blocking'],'sample_errors':[a.get('error') for a in contained.get('source_attempts',[]) if a.get('error')][:3]}))
 finally:
  executor_runtime.PublicHttpClient=original_client
 with tempfile.TemporaryDirectory(prefix='ad_v3_p02_accept_') as td:
  result=execute(PHASE,'ALL','2026-08-16T17:00:00Z',pathlib.Path(td)/'store',PHASE/'tests/fixtures/generated',False)
  rec=result['coverage_receipt']; obs=result['observations']
  checks.append(C('fixture acquisition not blocked',rec['analysis_admission']!='BLOCKED',rec['analysis_admission']))
  checks.append(C('all 192 facts accounted',rec['fact_counts']['observations']==192,rec['fact_counts']))
  checks.append(C('zero mandatory source omission',rec['fact_counts']['unattempted_blocking']==0,rec['unattempted_blocking_facts']))
  checks.append(C('zero blocking parser failure in certified fixtures',rec['fact_counts']['failed_blocking']==0,rec['failed_blocking_facts']))
  checks.append(C('source fetch deduplicated',rec['source_counts']['deduplicated'] and rec['source_counts']['planned_unique']==rec['source_counts']['attempted_unique'],rec['source_counts']))
  checks.append(C('private gaps explicit',rec['fact_counts']['private_gaps']>0,rec['private_unobservable_facts']))
  checks.append(C('paid gaps explicit',rec['fact_counts']['paid_gaps']>0,rec['paid_only_facts']))
  checks.append(C('provider gaps explicit',rec['fact_counts']['provider_gaps']>0,rec['provider_gap_facts']))
  checks.append(C('known gaps cap completeness',rec['observability_completeness_cap_applies'] is True))
  checks.append(C('p02 grants no direction authority',rec['direction_authority_granted'] is False))
  checks.append(C('p02 grants no permission authority',rec['trade_permission_authority_granted'] is False))
  checks.append(C('zero silent omission',rec['zero_silent_omission'] is True))
  run_id=rec.get('acquisition_run_id')
  checks.append(C('every observation bound to exact acquisition run',bool(run_id) and all(o.get('acquisition_run_id')==run_id for o in obs),{'run_id':run_id,'bound':sum(1 for o in obs if o.get('acquisition_run_id')==run_id),'total':len(obs)}))
  checks.append(C('receipt completion covers observation cutoff',bool(rec.get('acquisition_completed_at_utc')) and rec.get('generated_at_utc')==rec.get('acquisition_completed_at_utc') and rec.get('acquisition_completed_at_utc')>=rec.get('observation_cutoff_utc',''),{'started':rec.get('acquisition_started_at_utc'),'cutoff':rec.get('observation_cutoff_utc'),'completed':rec.get('acquisition_completed_at_utc'),'generated':rec.get('generated_at_utc')}))
  logp=pathlib.Path(td)/'store'/'observations'/'gold_fact_observations.jsonl'
  logged=[json.loads(x) for x in logp.read_text(encoding='utf-8').splitlines() if x.strip()]
  current_logged=[o for o in logged if o.get('acquisition_run_id')==run_id]
  checks.append(C('published receipt has complete current-run observation set',len(current_logged)==192,{'run_id':run_id,'current_run_observations':len(current_logged)}))
  # raw provenance
  raw=list((pathlib.Path(td)/'store'/'raw').rglob('*'))
  rawfiles=[p for p in raw if p.is_file()]
  checks.append(C('raw snapshots persisted',len(rawfiles)>20,len(rawfiles)))
  checks.append(C('observations carry provenance hashes',sum(1 for o in obs if o.get('raw_sha256'))>20,sum(1 for o in obs if o.get('raw_sha256'))))
  ob={o['fact_id']:o for o in obs}
  checks.append(C('treasury 10y real parser exact',ob.get('UST_10Y_REAL_YIELD',{}).get('value')==2.41,ob.get('UST_10Y_REAL_YIELD')))
  checks.append(C('treasury 10y nominal parser exact',ob.get('UST_10Y_NOMINAL_YIELD',{}).get('value')==4.68,ob.get('UST_10Y_NOMINAL_YIELD')))
  checks.append(C('sofr parser exact',ob.get('SOFR_RATE',{}).get('value')==3.65,ob.get('SOFR_RATE')))
  mm=ob.get('CFTC_MANAGED_MONEY',{}).get('value') or {}
  checks.append(C('cftc managed money parser exact',mm.get('long')==148000 and mm.get('short')==11000 and mm.get('net')==137000,mm))
  be=ob.get('US_10Y_BREAKEVEN',{})
  checks.append(C('breakeven dependency derivation exact',abs((be.get('value') or 0)-2.27)<1e-9,be))
  # REV 3.2.3 official API/free-fallback parsers.
  checks.append(C('bls cpi api parser exact',ob.get('US_CPI',{}).get('value')==326.821,ob.get('US_CPI')))
  checks.append(C('bls payroll api parser exact',ob.get('US_PAYROLLS',{}).get('value')==160500.0,ob.get('US_PAYROLLS')))
  checks.append(C('bls unemployment api parser exact',ob.get('US_UNEMPLOYMENT',{}).get('value')==4.2,ob.get('US_UNEMPLOYMENT')))
  checks.append(C('bls jolts api parser exact',ob.get('US_JOLTS',{}).get('value')==7437.0,ob.get('US_JOLTS')))
  checks.append(C('fed h10 afe daily parser exact',abs((ob.get('FED_AFE_DOLLAR',{}).get('value') or 0)-108.2345)<1e-9,ob.get('FED_AFE_DOLLAR')))
  checks.append(C('fed h10 eme daily parser exact',abs((ob.get('FED_EME_DOLLAR',{}).get('value') or 0)-127.3456)<1e-9,ob.get('FED_EME_DOLLAR')))
  rs=ob.get('US_RETAIL_SALES',{})
  checks.append(C('census retail direct parser exact',rs.get('value')=={'level_billion_usd':763.6,'mom_percent':-0.6,'yoy_percent':5.0} and rs.get('epistemic_state')=='OBSERVED_DELAYED' and rs.get('source_id')=='CENSUS_RETAIL',rs))
  f55=ob.get('US_5Y5Y_FORWARD_INFLATION',{})
  checks.append(C('5y5y is derived not fetched',f55.get('epistemic_state')=='MODEL_DERIVED' and isinstance(f55.get('value'),(int,float)),f55))
  xau=ob.get('XAUUSD_SPOT_PRICE',{})
  checks.append(C('xauusd numeric price anchor fallback available',xau.get('value')==4402.10 and xau.get('source_id')=='GOLDPRICEDEV_XAU_SPOT_PROXY' and xau.get('epistemic_state')=='PUBLIC_PROXY',xau))
  checks.append(C('xauusd proxy is transmission only with zero causal authority',(xau.get('metadata') or {}).get('transmission_only') is True and (xau.get('metadata') or {}).get('causal_direction_authority') is False and xau.get('directness')=='PROXY',xau))
  checks.append(C('cme gold price json exact',ob.get('GC_FUTURES_PRICE',{}).get('value')==4437.3,ob.get('GC_FUTURES_PRICE')))
  goi=ob.get('GC_OPEN_INTEREST',{})
  checks.append(C('cme gold open interest json exact',goi.get('value')==388924.0,goi))
  checks.append(C('gld observation bound only to SPDR sponsor',ob.get('GLD_HOLDINGS_SHARES',{}).get('source_id')=='ETF_SPONSOR',ob.get('GLD_HOLDINGS_SHARES')))
  checks.append(C('iau observation bound only to iShares sponsor',ob.get('IAU_HOLDINGS_SHARES',{}).get('source_id')=='ETF_SPONSOR_IAU',ob.get('IAU_HOLDINGS_SHARES')))
  gvol=ob.get('GC_VOLUME',{})
  checks.append(C('gc volume cannot fall back to cftc positioning text',gvol.get('source_id')!='CFTC_COT' and 'WHEAT-SRW' not in json.dumps(gvol.get('value')),gvol))
  gcurve=(ob.get('GC_CURVE_TERM_STRUCTURE',{}).get('value') or {}).get('contracts') or []
  checks.append(C('cme gold curve structured',len(gcurve)>=3,gcurve[:3]))
  fp=(ob.get('FED_POLICY_PATH_PRICING',{}).get('value') or {}).get('fed_funds_futures_curve') or []
  checks.append(C('fed funds futures curve structured',len(fp)>=4 and abs(fp[1].get('implied_average_rate',0)-3.77)<1e-9,fp[:4]))
  sgew=ob.get('SGE_WITHDRAWALS',{})
  checks.append(C('sge primary-or-wgc fallback admissible',sgew.get('epistemic_state') in ('OBSERVED_CURRENT','OBSERVED_DELAYED','LATEST_VALID','PUBLIC_PROXY'),sgew))
  inr=ob.get('INR_GOLD_AFFORDABILITY',{})
  checks.append(C('fed h10 inr affordability remains proxy',inr.get('epistemic_state')=='PUBLIC_PROXY' and inr.get('source_id')=='FED_H10_INR_HISTORY' and (inr.get('value') or {}).get('usd_inr')==95.21,inr))
  duty=ob.get('INDIA_IMPORT_DUTY_TAX',{})
  checks.append(C('india gold duty current policy proxy parsed',duty.get('epistemic_state')=='PUBLIC_PROXY' and duty.get('source_id')=='PIB_GOLD_DUTY_POLICY' and (duty.get('value') or {}).get('concessional_regime_extended') is True and (duty.get('value') or {}).get('exact_current_legal_rate_confirmed') is False,duty))
  # Contract must carry POST JSON request metadata without secrets.
  sr_now=load_json(PHASE/'config/source_contract_registry.json')
  bls_src=next(x for x in sr_now['sources'] if x['source_id']=='BLS_PUBLIC_API_BATCH')
  checks.append(C('bls batch request contract is post json',bls_src.get('request_method')=='POST' and len((bls_src.get('request_json') or {}).get('seriesid',[]))==7,{'method':bls_src.get('request_method'),'series_count':len((bls_src.get('request_json') or {}).get('seriesid',[]))}))
  # lineage: identical raw snapshot preserves first_seen; changed raw increments revision and supersedes.
  second=execute(PHASE,'ALL','2026-08-16T18:00:00Z',pathlib.Path(td)/'store',PHASE/'tests/fixtures/generated',False)['observations']
  s2={o['fact_id']:o for o in second}
  checks.append(C('identical snapshot preserves first seen',s2['UST_10Y_REAL_YIELD']['first_seen_at']==ob['UST_10Y_REAL_YIELD']['first_seen_at'],{'first':ob['UST_10Y_REAL_YIELD']['first_seen_at'],'second':s2['UST_10Y_REAL_YIELD']['first_seen_at']}))
  checks.append(C('identical snapshot does not invent revision',s2['UST_10Y_REAL_YIELD']['revision_number']==ob['UST_10Y_REAL_YIELD']['revision_number'],s2['UST_10Y_REAL_YIELD']['revision_number']))
  # attack: no network and no fixture MUST block public world.
  attack=execute(PHASE,'ALL','2026-08-16T17:00:00Z',None,None,True)['coverage_receipt']
  checks.append(C('unattempted public acquisition fails closed',attack['analysis_admission']=='BLOCKED',{'state':attack['analysis_admission'],'unattempted':attack['fact_counts']['unattempted_blocking']}))
  # attack: delete Treasury nominal fixture, must block at least material rate facts.
  fx=pathlib.Path(td)/'fixtures'; shutil.copytree(PHASE/'tests/fixtures/generated',fx)
  for x in fx.glob('UST_YIELD_CURVE.*'): x.unlink()
  atk2=execute(PHASE,'ALL','2026-08-16T17:00:00Z',None,fx,True)['coverage_receipt']
  checks.append(C('missing critical fixture produces blocked coverage',atk2['analysis_admission']=='BLOCKED',{'state':atk2['analysis_admission'],'failed':atk2['failed_blocking_facts'][:8],'unattempted':atk2['unattempted_blocking_facts'][:8]}))
 # source registry/fact mapping invariants
 fr=load_json(PHASE/'config/fact_acquisition_registry.json'); sr=load_json(PHASE/'config/source_contract_registry.json')
 last3={c['fact_id']:c for c in fr['contracts'] if c['fact_id'] in ('US_RETAIL_SALES','INDIA_IMPORT_DUTY_TAX','INR_GOLD_AFFORDABILITY')}
 checks.append(C('last three live blockers have preferred official paths',last3['US_RETAIL_SALES']['source_ids'][0]=='CENSUS_RETAIL' and last3['INDIA_IMPORT_DUTY_TAX']['source_ids'][0]=='PIB_GOLD_DUTY_POLICY' and last3['INR_GOLD_AFFORDABILITY']['source_ids'][0]=='FED_H10_INR_HISTORY',last3))
 fmap={c['fact_id']:c for c in fr['contracts']}
 checks.append(C('gld and iau sponsor bindings isolated',fmap['GLD_HOLDINGS_SHARES']['source_ids']==['ETF_SPONSOR'] and fmap['IAU_HOLDINGS_SHARES']['source_ids']==['ETF_SPONSOR_IAU'],{'gld':fmap['GLD_HOLDINGS_SHARES']['source_ids'],'iau':fmap['IAU_HOLDINGS_SHARES']['source_ids']}))
 checks.append(C('gc volume cftc fallback forbidden','CFTC_COT' not in fmap['GC_VOLUME']['source_ids'],fmap['GC_VOLUME']['source_ids']))
 checks.append(C('xauusd price source chain prefers WGC then explicit transmission proxy',fmap['XAUUSD_SPOT_PRICE']['source_ids'][:2]==['WGC_GOLD_PRICE','GOLDPRICEDEV_XAU_SPOT_PROXY'],fmap['XAUUSD_SPOT_PRICE']['source_ids']))
 plan=build_plan(fr,sr,'ALL','2026-08-16T17:00:00Z')
 checks.append(C('plan includes mandatory acquisition source set',len(plan['source_ids_to_attempt'])>=60,len(plan['source_ids_to_attempt'])))
 # P01 remains shadow boundary by sibling presence/config.
 p01=PHASE.parent/'AD_V3_PHASE_01_TOTAL_GOLD_KNOWLEDGE_SCIENCE_FOUNDATION'
 checks.append(C('p01 dependency present',p01.exists()))
 # immutable file hashes if present
 manifest=PHASE/'baseline/P02_IMMUTABLE_HASHES.json'
 if manifest.exists():
  import hashlib
  m=load_json(manifest); drift=[]
  for rel,want in m.get('files',{}).items():
   p=PHASE/rel
   got=hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
   if got!=want: drift.append({'file':rel,'expected':want,'actual':got})
  checks.append(C('p02 immutable payload hashes',not drift,drift[:10]))
 status='PASS' if all(c['status']=='PASS' for c in checks) else 'FAIL'
 out={'phase':'AD-V3-P02','acceptance_status':status,'checks':checks,'fact_count':fr['contract_count'],'source_count':sr['source_count'],'mandatory_attempt_contracts':sum(c['must_attempt_when_applicable'] for c in fr['contracts']),'fixture_coverage_state':rec['analysis_admission'],'p03_handoff':{'ready':status=='PASS','requires_nonblocked_live_coverage_receipt':True,'direction_authority_still_false':True,'trade_permission_authority_still_false':True}}
 print(json.dumps(out,indent=2,ensure_ascii=False)); return 0 if status=='PASS' else 1
if __name__=='__main__': raise SystemExit(main())
