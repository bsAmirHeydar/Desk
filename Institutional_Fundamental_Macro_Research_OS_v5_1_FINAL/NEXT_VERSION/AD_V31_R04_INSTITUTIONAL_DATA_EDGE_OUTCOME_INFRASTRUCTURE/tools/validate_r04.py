from __future__ import annotations
import json,sys,hashlib,tempfile,subprocess,re
from pathlib import Path
HERE=Path(__file__).resolve();PH=HERE.parents[1];NEXT=PH.parent;REPO=NEXT.parents[2]
if str(NEXT) not in sys.path:sys.path.insert(0,str(NEXT))
from AD_V31_R04_INSTITUTIONAL_DATA_EDGE_OUTCOME_INFRASTRUCTURE.runtime.common import load_json
from AD_V31_R04_INSTITUTIONAL_DATA_EDGE_OUTCOME_INFRASTRUCTURE.runtime.data_edge_runtime import status
from AD_V31_R04_INSTITUTIONAL_DATA_EDGE_OUTCOME_INFRASTRUCTURE.runtime.provider_registry import capabilities
from AD_V31_R04_INSTITUTIONAL_DATA_EDGE_OUTCOME_INFRASTRUCTURE.runtime.data_freeze import verify_manifest

def ck(n,o,d=None):return {'name':n,'status':'PASS' if o else 'FAIL','detail':d}
def main():
 c=[];req=['config/provider_capability_registry.json','config/scientific_equivalence_groups.json','config/pit_store_policy.json','config/outcome_provider_policy.json','config/real_rate_proxy_policy.json','runtime/pit_store.py','runtime/outcome_recovery.py','runtime/provider_health.py','providers/ice_dxy_delayed.py','providers/ice_dxy_data_api.py','providers/goldprice_bars.py','providers/twelvedata_xau.py','tools/run_golden_data_matrix.py','tools/run_outcome_recovery_certification.py']
 c.append(ck('required R04 surfaces present',all((PH/x).exists() for x in req),[x for x in req if not (PH/x).exists()]))
 a=load_json(PH/'baseline/PRE_R04_DATA_EDGE_AUDIT.json',{}) or {};c.append(ck('full P02 data-edge audit covers 192 facts',a.get('fact_count')==192,a.get('fact_count')));c.append(ck('source audit covers canonical 96 source contracts',a.get('source_count')==96,a.get('source_count')));c.append(ck('generic HTML baseline quantified',a.get('generic_html_count')==55,a.get('generic_html_count')))
 caps=capabilities();by={x['provider_id']:x for x in caps};c.append(ck('provider implementation is distinct from configuration',by['ICE_DXY_DELAYED_PUBLIC']['configured'] is False and by['ICE_DXY_DELAYED_PUBLIC']['activation_state']=='IMPLEMENTED_NOT_LIVE_VERIFIED',by['ICE_DXY_DELAYED_PUBLIC']));c.append(ck('paid entitlement remains explicit',by['ICE_DXY_DATA_API']['entitlement_required'] is True));c.append(ck('private access class remains explicit',by['LONDON_OTC_PRIVATE_FLOW']['access_class']=='PRIVATE'))
 st=status();c.append(ck('direct DXY and USD proxy stay distinct',st['direct_dxy']['state']!='AVAILABLE_SEPARATE_IDENTITY' and st['usd_proxy']['state']=='AVAILABLE_SEPARATE_IDENTITY',{'direct':st['direct_dxy'],'proxy':st['usd_proxy']}));c.append(ck('intraday real-rate proxy never mislabeled official',st['intraday_real_rate_proxy']['identity']=='INTRADAY_REAL_RATE_PROXY' and st['intraday_real_rate_proxy']['official_real_yield'] is False));c.append(ck('official real yield remains daily context',st['official_real_yield']['state']=='OFFICIAL_DAILY_CONTEXT'))
 op=load_json(PH/'config/outcome_provider_policy.json',{});hp=load_json(NEXT/'AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0/config/horizon_evaluation_policy.json',{});c.append(ck('canonical P09 outcome instrument preserved',op.get('canonical_instrument')=='XAUUSD'));c.append(ck('SESSION_1_6H maturity remains 360m and 20m tolerance',hp['horizons']['SESSION_1_6H']['terminal_minutes']==360 and hp['horizons']['SESSION_1_6H']['terminal_tolerance_minutes']==20,hp['horizons']['SESSION_1_6H']))
 c.append(ck('current price substitution explicitly forbidden',load_json(PH/'config/historical_recovery_policy.json',{}).get('current_price_substitution_forbidden') is True));c.append(ck('backfill explicitly non-prospective',load_json(PH/'config/pit_store_policy.json',{}).get('backfill_is_prospective') is False));c.append(ck('provider redundancy not evidence independence',all(g.get('independence_units')==1 for g in load_json(PH/'config/scientific_equivalence_groups.json',{}).get('groups',[]))))
 gaps={x['gap_id']:x for x in load_json(PH/'config/data_gap_registry.json',{}).get('gaps',[])};c.append(ck('market depth remains paid gap',gaps['GC_MARKET_DEPTH']['gap_type']=='PAID_GAP'));c.append(ck('aggressor flow remains paid gap',gaps['GC_AGGRESSOR_FLOW']['gap_type']=='PAID_GAP'));c.append(ck('dealer gamma remains paid gap',gaps['DEALER_GAMMA']['gap_type']=='PAID_GAP'));c.append(ck('London OTC remains private gap',gaps['LONDON_OTC_PRIVATE_FLOW']['gap_type']=='PRIVATE_GAP'))
 # Science zero-drift baseline
 b=load_json(PH/'baseline/PRE_R04_SCIENCE_HASHES.json',{}) or {};drift=[]
 for rel,want in b.get('files',{}).items():
  p=NEXT/rel;got=hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
  if got!=want:drift.append(rel)
 c.append(ck('P01/P03/P06/R01/R02/R03/P09-classification science zero drift',not drift,drift))
 # Integration ownership
 orch=(NEXT/'AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN/runtime/gold_orchestrator.py').read_text();c.append(ck('P10 uses R04 historical recovery through P09 and PIT ingest','r04_state_root' in orch and 'r04_ingest_anchor' in orch));c.append(ck('P10 remains sole normal orchestrator','run-r04-gold' not in orch))
 p09=(NEXT/'AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0/runtime/forward_runtime.py').read_text();c.append(ck('P09 remains outcome classifier while R04 only supplies observations','evaluate_prediction' in p09 and 'recover_for_prediction' in p09))
 co=load_json(NEXT/'AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0/config/cohort_policy.json',{});c.append(ck('R04 data contract bound to prospective cohort',co.get('r04_data_contract_bound') is True and any('R04' in x for x in co.get('bound_surfaces',[]))))
 arch=load_json(NEXT/'AD_V3_PHASE_05_INTEGRITY_ARCHITECTURE_CONSOLIDATION/config/architecture_surface_registry.json',{});c.append(ck('P05 governance registers R04 authority',arch.get('r04_authority_registered') is True))
 # Secrets scan (simple, avoid flagging env variable names)
 bad=[]
 for p in list(PH.glob('config/*.json'))+list(PH.glob('providers/*.py')):
  t=p.read_text(errors='ignore')
  for pat in [r'(?i)api[_-]?key\s*[=:]\s*["\'][A-Za-z0-9_-]{20,}["\']',r'(?i)bearer\s+eyJ[A-Za-z0-9_-]+']:
   if re.search(pat,t):bad.append(p.name)
 c.append(ck('R04 source package contains no embedded credentials',not bad,bad))
 fr=verify_manifest();c.append(ck('R04 data-science freeze valid',fr.get('status')=='PASS',fr))
 ok=all(x['status']=='PASS' for x in c);out={'phase':'AD-V3.1-R04','validation_status':'PASS' if ok else 'FAIL_CLOSED','check_count':len(c),'checks':c,'data_edge_status':st};print(json.dumps(out,indent=2,ensure_ascii=False));return 0 if ok else 2
if __name__=='__main__':raise SystemExit(main())
