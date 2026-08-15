#!/usr/bin/env python3
from pathlib import Path
import argparse, json, sys, importlib.util, copy, hashlib
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('g',ROOT/'runtime/gold_intelligence.py'); g=importlib.util.module_from_spec(spec); spec.loader.exec_module(g)

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--json',action='store_true'); a=ap.parse_args(); checks=[]
 def ck(name,ok,detail=None): checks.append({'name':name,'status':'PASS' if ok else 'FAIL','detail':detail})
 fixture=json.loads((ROOT/'tests/fixtures/gold_valid_observations.json').read_text())
 out=g.build_gold_intelligence(copy.deepcopy(fixture),as_of_utc='2026-08-15T10:01:00Z',active_horizon='SESSION_1_6H')
 ck('valid fixture pass',out.get('status')=='PASS',out.get('integrity'))
 ck('subject xau',out.get('subject')=='XAUUSD')
 ck('shadow deployment',out.get('deployment')=='SHADOW_ONLY')
 ck('p02 not mutated',out.get('integrity',{}).get('p02_mutated') is False)
 ck('p03 not mutated',out.get('integrity',{}).get('p03_mutated') is False)
 ck('p04 not mutated',out.get('integrity',{}).get('p04_mutated') is False)
 ck('no trade permission',out.get('integrity',{}).get('trade_permission_granted') is False)
 ck('broker none',out.get('integrity',{}).get('broker_authority')=='NONE')
 ck('target price not pressure root',out.get('integrity',{}).get('target_price_used_as_pressure_root') is False)
 ck('target price not p04 evidence',out.get('integrity',{}).get('target_price_used_as_independent_release_evidence') is False)
 roots={x['root_id'] for x in out.get('p02_adapter',{}).get('root_candidate_bundles',[])}
 ck('policy root candidate','POLICY_EXPECTATIONS' in roots)
 ck('real yield root candidate','REAL_RATE_DISCOUNT' in roots)
 ck('dxy not default root','USD_AUTONOMOUS' not in roots)
 p03=out.get('p03_adapter',{}); ck('xau target candidate',any(x['metric_id']=='XAUUSD_RETURN' for x in p03.get('target_response_candidates',[])))
 ck('dxy pathway candidate',any(x['metric_id']=='DXY_STATE' for x in p03.get('pathway_channel_candidates',[])))
 p04=out.get('p04_adapter',{}).get('evidence_packet',{}).get('observations',[])
 ck('signed flow p04 mapped',any(x['role']=='OPPOSING_FLOW_DECAYING' for x in p04))
 ck('depth release support mapped',any(x['role']=='RELEASE_SUPPORT' for x in p04))
 ck('unique flow/depth independence',len({x['independence_group'] for x in p04})==2)
 ck('deterministic fingerprint',g.stable_gold_intelligence_fingerprint(out)==g.stable_gold_intelligence_fingerprint(copy.deepcopy(out)))
 # target price cannot be re-roled
 bad=copy.deepcopy(fixture); bad[0]['roles']=['P02_ROOT_ELIGIBLE']; ck('role override blocked',g.build_gold_intelligence(bad,as_of_utc='2026-08-15T10:01:00Z',active_horizon='SESSION_1_6H').get('status')=='FAIL_CLOSED')
 # provider required
 bad=copy.deepcopy(fixture); bad[0].pop('provider_id',None); ck('runtime provider required',g.build_gold_intelligence(bad,as_of_utc='2026-08-15T10:01:00Z',active_horizon='SESSION_1_6H').get('status')=='FAIL_CLOSED')
 # future obs
 bad=copy.deepcopy(fixture); bad[1]['observed_at_utc']='2026-08-16T10:00:00Z'; ck('future observation blocked',g.build_gold_intelligence(bad,as_of_utc='2026-08-15T10:01:00Z',active_horizon='SESSION_1_6H').get('status')=='FAIL_CLOSED')
 # horizon mismatch slow WGC on session
 slow=[{'observation_id':'gdt','metric_id':'GOLD_DEMAND_TRENDS','source_id':'WGC_GDT','observed_at_utc':'2026-08-15T00:00:00Z','status':'AVAILABLE'}]
 ck('slow source horizon bleed blocked',g.build_gold_intelligence(slow,as_of_utc='2026-08-15T10:01:00Z',active_horizon='SESSION_1_6H').get('status')=='FAIL_CLOSED')
 # volume excluded from p04 release evidence
 vol=[{'observation_id':'v','metric_id':'GC_VOLUME','source_id':'CME_VOLUME_OI','observed_at_utc':'2026-08-15T10:00:00Z','status':'AVAILABLE','state_code':'RELEASE_FLOW_SUPPORT'}]
 ov=g.build_gold_intelligence(vol,as_of_utc='2026-08-15T10:01:00Z',active_horizon='SESSION_1_6H'); ck('volume not release evidence',not ov.get('p04_adapter',{}).get('evidence_packet',{}).get('observations'))
 ck('volume integrity non-directional',ov.get('integrity',{}).get('volume_treated_as_directional_flow') is False)
 # oi excluded
 oi=[{'observation_id':'oi','metric_id':'GC_OPEN_INTEREST','source_id':'CME_VOLUME_OI','observed_at_utc':'2026-08-15T10:00:00Z','status':'AVAILABLE','state_code':'OPPOSING_FLOW_ACTIVE'}]
 oo=g.build_gold_intelligence(oi,as_of_utc='2026-08-15T10:01:00Z',active_horizon='SESSION_1_6H'); ck('oi not directional evidence',not oo.get('p04_adapter',{}).get('evidence_packet',{}).get('observations'))
 ck('oi integrity non-directional',oo.get('integrity',{}).get('oi_treated_as_directional_flow') is False)
 # options model lineage
 opt=[{'observation_id':'op','metric_id':'GC_DEALER_CONVEXITY_MODEL','source_id':'CME_MARKET_DEPTH','observed_at_utc':'2026-08-15T10:00:00Z','status':'AVAILABLE','state_code':'RELEASE_OPTIONS_SUPPORT'}]
 ck('dealer model requires model_ref',g.build_gold_intelligence(opt,as_of_utc='2026-08-15T10:01:00Z',active_horizon='SESSION_1_6H').get('status')=='FAIL_CLOSED')
 opt[0]['model_ref']='MODEL:TEST'; opt[0]['strength']='HIGH'; opt[0]['confidence']='MEDIUM'; op=g.build_gold_intelligence(opt,as_of_utc='2026-08-15T10:01:00Z',active_horizon='SESSION_1_6H'); ck('dealer model accepted with lineage',op.get('status')=='PASS' and len(op.get('p04_adapter',{}).get('evidence_packet',{}).get('observations',[]))==1)
 # CFTC cannot be session due horizon registry; multi-day allowed and only positioning role.
 cot=[{'observation_id':'cot','metric_id':'CFTC_GOLD_POSITIONING','source_id':'CFTC_COT','observed_at_utc':'2026-08-15T09:00:00Z','status':'AVAILABLE','state_code':'OPPOSING_UNWIND_ACTIVE','strength':'MEDIUM','confidence':'MEDIUM'}]
 ck('cftc session horizon blocked',g.build_gold_intelligence(cot,as_of_utc='2026-08-15T10:01:00Z',active_horizon='SESSION_1_6H').get('status')=='FAIL_CLOSED')
 co=g.build_gold_intelligence(cot,as_of_utc='2026-08-15T10:01:00Z',active_horizon='MULTI_DAY_2_10D'); ck('cftc multi-day accepted',co.get('status')=='PASS')
 ck('cftc not live flow',all(x.get('domain')=='POSITIONING' for x in co.get('p04_adapter',{}).get('evidence_packet',{}).get('observations',[])))
 # LBMA clearing / vault cannot directionally map.
 lb=[{'observation_id':'lb','metric_id':'LBMA_CLEARING_ACTIVITY','source_id':'LBMA_CLEARING','observed_at_utc':'2026-08-15T09:00:00Z','status':'AVAILABLE','state_code':'RELEASE_FLOW_SUPPORT'}]
 lo=g.build_gold_intelligence(lb,as_of_utc='2026-08-15T10:01:00Z',active_horizon='STRUCTURAL'); ck('lbma clearing not p04 directional',not lo.get('p04_adapter',{}).get('evidence_packet',{}).get('observations'))
 lv=[{'observation_id':'lv','metric_id':'LBMA_VAULT_STOCK','source_id':'LBMA_VAULT','observed_at_utc':'2026-08-15T09:00:00Z','status':'AVAILABLE','state_code':'RELEASE_FLOW_SUPPORT'}]
 lvo=g.build_gold_intelligence(lv,as_of_utc='2026-08-15T10:01:00Z',active_horizon='STRUCTURAL'); ck('vault stock not daily flow',not lvo.get('p04_adapter',{}).get('evidence_packet',{}).get('observations'))
 # ETF requires state mapping and retains one independence group with sponsor.
 et=[{'observation_id':'e1','metric_id':'ETF_HOLDINGS_FLOW','source_id':'WGC_ETF','observed_at_utc':'2026-08-15T09:00:00Z','status':'AVAILABLE','state_code':'RELEASE_FLOW_SUPPORT','strength':'HIGH','confidence':'HIGH'}, {'observation_id':'e2','metric_id':'ETF_SPONSOR_SHARES_HOLDINGS','source_id':'ETF_SPONSOR','observed_at_utc':'2026-08-15T09:00:00Z','status':'AVAILABLE','state_code':'CREATION_SUPPORT','strength':'HIGH','confidence':'HIGH'}]
 eo=g.build_gold_intelligence(et,as_of_utc='2026-08-15T10:01:00Z',active_horizon='MULTI_DAY_2_10D'); ep=eo.get('p04_adapter',{}).get('evidence_packet',{}).get('observations',[]); ck('etf duplicate independence retained same group',len({x['independence_group'] for x in ep})==1)
 # Event reset
 ev=[{'observation_id':'evt','metric_id':'US_MACRO_EVENT','source_id':'BLS_MACRO','observed_at_utc':'2026-08-15T10:00:00Z','status':'AVAILABLE','event':{'state':'UPCOMING','event_time_utc':'2026-08-15T12:30:00Z','materiality':'HIGH','requires_post_event_recompute':True},'state_code':'EVENT_RESET_RISK','strength':'HIGH','confidence':'HIGH'}]
 evout=g.build_gold_intelligence(ev,as_of_utc='2026-08-15T10:01:00Z',active_horizon='SESSION_1_6H'); ck('event cap watch recommended',evout.get('event_reset',{}).get('release_readiness_cap_recommended')=='WATCH')
 ck('event calendar not p02 root',not evout.get('p02_adapter',{}).get('root_candidate_bundles'))
 # unavailable OTC gap remains gap not neutral
 un=[{'observation_id':'otc','metric_id':'GOLD_FINANCING_STATE','source_id':'GOLD_FINANCING_EVIDENCE','observed_at_utc':'2026-08-15T10:00:00Z','status':'LICENSED_REQUIRED'}]
 uo=g.build_gold_intelligence(un,as_of_utc='2026-08-15T10:01:00Z',active_horizon='SESSION_1_6H'); ck('licensed required admitted as unavailable state',uo.get('status')=='PASS' and uo.get('admitted_observations',[{}])[0].get('status')=='LICENSED_REQUIRED')
 ck('otc coverage gap disclosed',uo.get('coverage_gaps',{}).get('otc_client_dealer_flow')=='LICENSED_REQUIRED_OR_UNAVAILABLE')
 # source mismatch, unknown metric, duplicate id
 bad=copy.deepcopy(fixture); bad[1]['source_id']='CME_VOLUME_OI'; ck('source metric mismatch blocked',g.build_gold_intelligence(bad,as_of_utc='2026-08-15T10:01:00Z',active_horizon='SESSION_1_6H').get('status')=='FAIL_CLOSED')
 bad=copy.deepcopy(fixture); bad[1]['metric_id']='UNKNOWN'; ck('unknown metric blocked',g.build_gold_intelligence(bad,as_of_utc='2026-08-15T10:01:00Z',active_horizon='SESSION_1_6H').get('status')=='FAIL_CLOSED')
 bad=copy.deepcopy(fixture); bad[1]['observation_id']='xau'; ck('duplicate observation id blocked',g.build_gold_intelligence(bad,as_of_utc='2026-08-15T10:01:00Z',active_horizon='SESSION_1_6H').get('status')=='FAIL_CLOSED')
 # Target and GC price same independence group.
 gc=copy.deepcopy(fixture)+[{'observation_id':'gc','metric_id':'GC_PRICE_RETURN','source_id':'GC_RUNTIME_FEED','observed_at_utc':'2026-08-15T10:00:00Z','status':'AVAILABLE'}]
 go=g.build_gold_intelligence(gc,as_of_utc='2026-08-15T10:01:00Z',active_horizon='SESSION_1_6H'); groups=[x['independence_group'] for x in go.get('p03_adapter',{}).get('target_response_candidates',[])+go.get('p03_adapter',{}).get('diagnostic_proxy_candidates',[]) if x['metric_id'] in {'XAUUSD_RETURN','GC_PRICE_RETURN'}]; ck('xau and gc same target complex',len(set(groups))==1)
 # Silver never P02 root.
 si=copy.deepcopy(fixture)+[{'observation_id':'si','metric_id':'SILVER_PRICE_RESPONSE','source_id':'SILVER_RUNTIME_FEED','observed_at_utc':'2026-08-15T10:00:00Z','status':'AVAILABLE'}]
 so=g.build_gold_intelligence(si,as_of_utc='2026-08-15T10:01:00Z',active_horizon='SESSION_1_6H'); ck('silver not p02 root',all(x['root_id']!='SILVER' for x in so.get('p02_adapter',{}).get('root_candidate_bundles',[])))
 # Missing-driver search from synthetic P03 escalation.
 tr={'missing_driver_escalation':{'level':'RESEARCH_ESCALATION'}}; mo=g.build_gold_intelligence([],as_of_utc='2026-08-15T10:01:00Z',active_horizon='SESSION_1_6H',upstream_transmission=tr); ck('missing driver search activated',mo.get('missing_driver_search',{}).get('required') is True)
 ck('missing search starts data integrity',mo.get('missing_driver_search',{}).get('priorities',[{}])[0].get('family')=='DATA_INTEGRITY')
 # Upstream fingerprints immutable / target price variant doesn't modify provided upstream refs.
 up={'status':'PASS','pressure_core':{'sign':'BUY','class':'HIGH'}}; a1=g.build_gold_intelligence(copy.deepcopy(fixture),as_of_utc='2026-08-15T10:01:00Z',active_horizon='SESSION_1_6H',upstream_pressure=up); f2=copy.deepcopy(fixture); f2[0]['value']=99; a2=g.build_gold_intelligence(f2,as_of_utc='2026-08-15T10:01:00Z',active_horizon='SESSION_1_6H',upstream_pressure=up); ck('target price change upstream pressure ref invariant',a1.get('upstream_references',{}).get('pressure_fingerprint')==a2.get('upstream_references',{}).get('pressure_fingerprint'))
 # Config/governance checks.
 reg=g.load_registries(); ck('single venue equivalence false',reg['gold_instrument_ontology'].get('global_gold_single_venue_equivalence') is False)
 pol=reg['gold_release_evidence_policy']['gold_rules']; ck('volume cannot release',pol.get('volume_alone_can_support_release') is False); ck('oi cannot release',pol.get('oi_alone_can_support_release') is False); ck('cftc not live trigger',pol.get('cftc_can_be_live_release_trigger') is False); ck('gdt not live trigger',pol.get('wgc_gdt_can_be_live_release_trigger') is False); ck('options oi not gamma',pol.get('options_oi_can_define_dealer_gamma_without_model') is False); ck('price reversal not absorption proof',pol.get('target_price_reversal_can_confirm_absorption') is False)
 sr=reg['gold_source_registry']; ck('registered source not assumed available',sr.get('registered_source_is_not_assumed_available') is True)
 om=reg['gold_observability_matrix']; ck('missing not neutral',om.get('missing_is_not_neutral') is True)
 er=reg['gold_event_window_registry']; ck('event registry not current calendar',er.get('registry_is_not_current_calendar') is True)
 mr=reg['gold_missing_driver_search_registry']; ck('new causal driver recompute',mr.get('new_causal_driver_requires_p02_recompute') is True)
 # Registry integrity: unique ids, all metric sources exist, all groups exist, roots valid.
 srcids=[x['source_id'] for x in sr['sources']]; mids=[x['metric_id'] for x in reg['gold_evidence_role_registry']['metrics']]; ck('source ids unique',len(srcids)==len(set(srcids))); ck('metric ids unique',len(mids)==len(set(mids)))
 srcset=set(srcids); groups=set(reg['gold_independence_registry']['groups']); rootset={x['root_id'] for x in reg['gold_pressure_root_registry']['root_families']}
 ck('all metric sources registered',all(x['source_id'] in srcset for x in reg['gold_evidence_role_registry']['metrics']))
 ck('all metric independence groups registered',all(x['independence_group'] in groups for x in reg['gold_evidence_role_registry']['metrics']))
 ck('all explicit roots registered',all((x.get('root_id') in rootset) for x in reg['gold_evidence_role_registry']['metrics'] if x.get('p02_policy')=='EXPLICIT_ROOT_ONLY'))
 # Files exist / schema strict / attack count.
 for rel in ['config/gold_source_registry.json','config/gold_instrument_ontology.json','config/gold_pressure_root_registry.json','config/gold_evidence_role_registry.json','config/gold_transmission_pathway_registry.json','config/gold_independence_registry.json','config/gold_event_window_registry.json','config/gold_observability_matrix.json','config/gold_release_evidence_policy.json','config/gold_missing_driver_search_registry.json','DEVELOPMENT_MANIFEST.json','PHASE_05_ROADMAP_HANDOFF.json']:
  ck('file exists:'+rel,(ROOT/rel).is_file())
 sch=json.loads((ROOT/'schemas/AlphaDesk_V2_GoldIntelligenceState.schema.json').read_text()); ck('schema strict',sch.get('additionalProperties') is False)
 ac=json.loads((ROOT/'tests/gold_specialization_attack_cases.json').read_text()); ck('attack case count >=25',len(ac.get('cases',[]))>=25)
 # No forbidden output keys.
 def has(obj,key):
  if isinstance(obj,dict): return key in obj or any(has(v,key) for v in obj.values())
  if isinstance(obj,list): return any(has(v,key) for v in obj)
  return False
 ck('no probability output',not has(out,'probability')); ck('no expected return',not has(out,'expected_return')); ck('no technical trigger',not has(out,'technical_trigger'))
 failed=[x for x in checks if x['status']!='PASS']; report={'schema_version':'1.0.0','phase':'AD-V2-P05','status':'PASS' if not failed else 'FAIL','passed':len(checks)-len(failed),'failed':len(failed),'checks':checks}
 print(json.dumps(report,ensure_ascii=False,indent=2) if a.json else f"P05 VALIDATION: {report['status']} ({report['passed']}/{len(checks)} PASS)")
 return 0 if not failed else 2
if __name__=='__main__': raise SystemExit(main())
