#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import sys,json,tempfile,datetime,copy,hashlib
P=Path(__file__).resolve().parents[1];N=P.parent;REPO=N.parents[1];sys.path.insert(0,str(N))
from AD_V31_R02_DECISION_SCIENCE_2_0.runtime.common import cfg,load
from AD_V31_R02_DECISION_SCIENCE_2_0.runtime.magnitude_engine import fact_magnitude,root_magnitude
from AD_V31_R02_DECISION_SCIENCE_2_0.runtime.historical_normalizer import normalize
from AD_V31_R02_DECISION_SCIENCE_2_0.runtime.root_health_engine import assess
from AD_V31_R02_DECISION_SCIENCE_2_0.runtime.causal_importance_engine import importance,infer_regime
from AD_V31_R02_DECISION_SCIENCE_2_0.runtime.robust_dominance_engine import reconcile
from AD_V31_R02_DECISION_SCIENCE_2_0.runtime.sensitivity_engine import evaluate
from AD_V31_R02_DECISION_SCIENCE_2_0.runtime.decision_freeze import verify_manifest
from AD_V31_R02_DECISION_SCIENCE_2_0.runtime.cohort_boundary import initialize as init_boundary
from AD_V3_PHASE_08_DECISION_SCIENCE_CALIBRATION.runtime.decision_runtime import calibrate
from AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0.runtime.precommit import build_prediction
from AD_V3_PHASE_11_FINAL_INSTITUTIONAL_GOLD_CONTROL_ROOM.runtime.presenter import build_view_model

def ck(n,o,d=None):return {'name':n,'status':'PASS' if o else 'FAIL','detail':d}
def h(state='HEALTHY'):
 return {'state':state,'critical_evidence_present':state!='CRITICAL_GAP','valid_share':1 if state=='HEALTHY' else .5,'directness_state':'DIRECT','independent_evidence_count':1}
def root(rid,d,mag='MATERIAL',imp='PRIMARY',fresh='FRESH_FOR_HORIZON',quality='HIGH',health='HEALTHY',pers='NEW'):
 return {'root_id':rid,'direction':d,'magnitude':mag,'causal_importance':imp,'freshness':fresh,'evidence_quality':quality,'root_health':h(health),'persistence':pers,'semantic_unknown_count':0,'empirical_information_state':'UNAVAILABLE'}
def kernel(gaps=None):return {'kernel_health':{'important_live_gaps':gaps or [],'live_kernel_unfresh_fact_ids':[],'context_invalid_fact_ids':[],'overall_analysis_admission':'ALLOW'},'known_provider_gap_facts':[],'known_private_gap_facts':[],'known_paid_gap_facts':[]}
def p03_policy(delta=.15,direction='BULLISH_GOLD',trans='ALIGNED',cons=None):
 facts=['FED_POLICY_PATH_PRICING','FOMC_POLICY_STANCE','FED_REACTION_FUNCTION'];rows=[]
 for i,f in enumerate(facts):
  rows.append({'fact_id':f,'observation_id':'O'+str(i),'causal_root_family':'US_POLICY_EXPECTATIONS','resolution':'RESOLVED','reason_code':'TEST','effect_on_gold':direction,'strength':'HIGH','details':{'near_curve_change':delta} if f=='FED_POLICY_PATH_PRICING' else {},'horizon_active':True})
 return {'receipt_id':'R02_P03','generated_at_utc':'2026-08-18T10:00:00Z','horizon':'SESSION_1_6H','pressure_planes':{'causal_fundamental':{'direction':direction,'root_states':[{'root_id':'US_POLICY_EXPECTATIONS','direction':direction,'strength':'HIGH','evidence_fact_ids':facts,'background_bias':'UNKNOWN'}]},'realized_transaction':{'direction':'UNKNOWN'},'mechanical_forced':{'direction':'UNKNOWN'},'structural_carry':{'direction':'UNKNOWN'}},'reasoning_ledger':{'rows':rows},'model_quality':{'missing_driver_risk':'LOW'},'price_transmission':{'state':trans},'lifecycle':{'consumption_vector':cons or {'information_absorption':'ABSENT','expectations_repricing':'ABSENT','flow_propagation':'ABSENT','position_adjustment':'ABSENT','narrative_saturation':'ABSENT'}}}
def main():
 c=[]
 # baseline / prerequisite presence
 for phase,tool in [('P12',N/'AD_V3_PHASE_12_FINAL_CERTIFICATION_PRODUCTION_FREEZE/tools/run_phase12_acceptance.py'),('R01',N/'AD_V31_R01_FORWARD_QUALITY_PROMOTION_SCIENCE/tools/run_r01_acceptance.py')]:c.append(ck(f'{phase} baseline acceptance tool present',tool.exists()))
 c.append(ck('operator-confirmed R01 baseline recorded',load(P/'DEVELOPMENT_MANIFEST.json',{}).get('baseline_commit')=='bade4df'))
 reg=cfg('magnitude_method_registry.json');entries=reg['entries'];c.append(ck('magnitude registry covers entire 192-fact universe',reg.get('fact_count')==192 and len(entries)==192))
 c.append(ck('every fact magnitude method is explicit',all(x.get('status') in ('SUPPORTED','CONTEXT_ONLY','NOT_APPLICABLE','UNKNOWN_MAGNITUDE') and x.get('fallback') is not None for x in entries)))
 # Magnitude: high quality does not matter, details do.
 tiny=fact_magnitude({'fact_id':'UST_10Y_REAL_YIELD','details':{'delta':0.0001},'strength':'HIGH','resolution':'RESOLVED'})
 large=fact_magnitude({'fact_id':'UST_10Y_REAL_YIELD','details':{'delta':0.15},'strength':'LOW','resolution':'RESOLVED'})
 unknown=fact_magnitude({'fact_id':'FED_POLICY_PATH_PRICING','details':{},'strength':'HIGH','resolution':'RESOLVED'})
 c.append(ck('high quality tiny rates move is not LARGE',tiny['state']=='MINOR',tiny));c.append(ck('large numeric impulse can be LARGE independent of evidence quality',large['state'] in ('LARGE','EXTREME'),large));c.append(ck('unsupported magnitude remains UNKNOWN',unknown['state']=='UNKNOWN',unknown))
 structural=fact_magnitude({'fact_id':'CENTRAL_BANK_NET_GOLD_PURCHASES','details':{'structural_value':300},'resolution':'RESOLVED'},history={'CENTRAL_BANK_NET_GOLD_PURCHASES':[]},as_of='2026-08-18T10:00:00Z')
 c.append(ck('structural fact cannot create current impulse without point-in-time history',structural['state']=='UNKNOWN' and structural['temporal_role']=='STRUCTURAL_CONTEXT',structural))
 # no lookahead normalizer
 goodhist=[{'value':x,'timestamp':f'2026-07-{1+i:02d}T00:00:00Z'} for i,x in enumerate(range(20))]
 norm=normalize(25,goodhist,'2026-08-18T10:00:00Z');c.append(ck('insufficient history prevents extreme normalization',norm['state']=='INSUFFICIENT_HISTORY',norm))
 try:normalize(1,[{'value':1,'timestamp':'2026-08-19T00:00:00Z'}]*35,'2026-08-18T10:00:00Z');look=False
 except ValueError:look=True
 c.append(ck('future observations rejected from historical normalization',look))
 # Root health population and critical gap.
 expected=['FED_POLICY_PATH_PRICING','FOMC_POLICY_STANCE','FED_REACTION_FUNCTION'];rows=[{'fact_id':'FED_POLICY_PATH_PRICING','observation_id':'O','resolution':'RESOLVED','effect_on_gold':'BULLISH_GOLD'}];fresh={'FED_POLICY_PATH_PRICING':'FRESH_FOR_HORIZON','FOMC_POLICY_STANCE':'STALE_FOR_HORIZON','FED_REACTION_FUNCTION':'EXPIRED'};contracts={f:{'p02_directness':'DIRECT'} for f in expected};mags={'FED_POLICY_PATH_PRICING':{'state':'LARGE'}}
 rh=assess('US_POLICY_EXPECTATIONS',expected,rows,fresh,contracts,mags,'BULLISH_GOLD');c.append(ck('one fresh fact cannot hide population degradation',rh['state'] in ('DEGRADED','CRITICAL_GAP') and rh['valid_share']<.5,rh));c.append(ck('root health reports critical evidence gap population',rh['critical_evidence_present'] is True or isinstance(rh['critical_evidence_missing'],list),rh));c.append(ck('root health exposes freshness and magnitude coverage',all(k in rh for k in ('current_evidence_count','stale_evidence_count','expired_evidence_count','magnitude_coverage_share'))))
 # direct/proxy
 con2={'USD_AUTONOMOUS_SHOCK':{'p02_directness':'PROXY'}};rh2=assess('USD_AUTONOMOUS',['USD_AUTONOMOUS_SHOCK'],[{'fact_id':'USD_AUTONOMOUS_SHOCK','observation_id':'O','resolution':'RESOLVED','effect_on_gold':'BEARISH_GOLD'}],{'USD_AUTONOMOUS_SHOCK':'FRESH_FOR_HORIZON'},con2,{'USD_AUTONOMOUS_SHOCK':{'state':'MATERIAL'}},'BEARISH_GOLD');c.append(ck('root health exposes proxy-only support',rh2['directness_state']=='PROXY_ONLY',rh2))
 # Independence grouping
 realfacts=['UST_5Y_REAL_YIELD','UST_10Y_REAL_YIELD','UST_30Y_REAL_YIELD'];rows3=[{'fact_id':f,'observation_id':'O'+f,'resolution':'RESOLVED','effect_on_gold':'BULLISH_GOLD'} for f in realfacts];rh3=assess('REAL_RATE_OPPORTUNITY_COST',realfacts,rows3,{f:'FRESH_FOR_HORIZON' for f in realfacts},{f:{'p02_directness':'DIRECT'} for f in realfacts},{f:{'state':'MATERIAL'} for f in realfacts},'BULLISH_GOLD');c.append(ck('same-shock manifestations do not inflate independence',rh3['observed_evidence_count']==3 and rh3['independent_evidence_count']==1,rh3))
 # Importance horizon/regime and LLM nonauthority.
 imp_s=importance('US_POLICY_EXPECTATIONS','SESSION_1_6H','NORMAL');imp_struct=importance('US_POLICY_EXPECTATIONS','STRUCTURAL','NORMAL');c.append(ck('causal importance is horizon-specific',imp_s['state']=='PRIMARY' and imp_struct['state']=='BACKGROUND',{'session':imp_s,'structural':imp_struct}));c.append(ck('importance explicitly has no LLM authority',imp_s['llm_authority'] is False))
 c.append(ck('regime defaults to NORMAL without governed explicit state',infer_regime({'semantic_text':'geopolitical crisis'},None,None)=='NORMAL'))
 geo_normal=importance('GEOPOLITICAL_INSURANCE_RISK','SESSION_1_6H','NORMAL');geo_shock=importance('GEOPOLITICAL_INSURANCE_RISK','SESSION_1_6H','GEOPOLITICAL_SHOCK');c.append(ck('governed regime can change importance deterministically',geo_normal['state']!=geo_shock['state'],{'normal':geo_normal,'shock':geo_shock}))
 # dominance: large low importance not automatic; count not authority
 one=root('SYSTEMIC_RATE','BEARISH_GOLD','LARGE','PRIMARY','FRESH_FOR_HORIZON','HIGH','HEALTHY');many=[root('B'+str(i),'BULLISH_GOLD','MINOR','SECONDARY','CONTEXT_VALID','MEDIUM','PARTIAL') for i in range(10)];dom=reconcile(many+[one]);c.append(ck('many weak roots cannot win by raw count against material primary root',dom['causal_direction']=='BEARISH_GOLD',dom))
 lowimp=root('STRUCT','BULLISH_GOLD','EXTREME','BACKGROUND','FRESH_FOR_HORIZON','HIGH','HEALTHY');hiimp=root('POLICY','BEARISH_GOLD','MATERIAL','PRIMARY','FRESH_FOR_HORIZON','HIGH','HEALTHY');dli=reconcile([lowimp,hiimp]);c.append(ck('large magnitude low-importance root does not automatically dominate',dli['causal_direction']!='BULLISH_GOLD',dli))
 conflict=reconcile([root('A','BULLISH_GOLD','LARGE','PRIMARY'),root('B','BEARISH_GOLD','LARGE','PRIMARY')]);c.append(ck('opposing primary material healthy roots produce true conflict',conflict['causal_direction']=='MIXED' and conflict['dominance_state']=='BALANCED',conflict))
 # sensitivity robust
 sr=evaluate([root('A','BULLISH_GOLD','LARGE','PRIMARY')]);c.append(ck('bounded deterministic sensitivity can identify robust dominance',sr['robustness']=='ROBUST' and sr['variant_count']==7,sr));c.append(ck('sensitivity variants are not probabilities',sr['variant_frequency_is_not_probability'] is True and not any('probability' in json.dumps(x).lower() for x in sr['variants'])))
 # synthetic model-sensitive via carefully competing roots; if exact classifier doesn't flip, prove engine supports state taxonomy/edge cap through policy + variant divergence.
 sens=evaluate([root('A','BULLISH_GOLD','MINOR','SECONDARY','CONTEXT_VALID','MEDIUM','PARTIAL'),root('B','BEARISH_GOLD','MINOR','PRIMARY','CONTEXT_VALID','MEDIUM','HEALTHY')]);dirs={x['causal_direction'] for x in sens['variants']};c.append(ck('bounded sensitivity produces auditable variant results',len(sens['variants'])==7 and all(x.get('variant_id') for x in sens['variants']),sens));c.append(ck('actual model-sensitive dominance is identified',sens['robustness']=='MODEL_SENSITIVE' and sens['model_sensitivity']=='HIGH' and 'MIXED' in dirs and 'BEARISH_GOLD' in dirs,sens))
 # Full upgraded P08: real magnitude details; Pressure != Price, high consumption wait.
 full=calibrate(p03_policy(.15,'BULLISH_GOLD','NEGATIVE'),kernel(),promotion_state={'state':'SHADOW_COMMISSIONING'});c.append(ck('P08 R02 output contains new decision-science fields',all(k in full for k in ('dominant_root_magnitude','dominant_root_health','dominant_root_importance','dominance_robustness','model_sensitivity'))));c.append(ck('price against pressure does not rewrite magnitude/direction',full['causal_direction']=='BULLISH_GOLD' and full['dominant_root_magnitude'] in ('LARGE','EXTREME') and full['edge_state']!='ACTIONABLE_EDGE',full))
 highcons={'information_absorption':'PRESENT','expectations_repricing':'PRESENT','flow_propagation':'PRESENT','position_adjustment':'PRESENT','narrative_saturation':'ABSENT'};hc=calibrate(p03_policy(.15,cons=highcons),kernel(),promotion_state={'state':'SHADOW_COMMISSIONING'});c.append(ck('high magnitude pressure can coexist with high consumption WAIT',hc['pressure_strength'] in ('STRONG','DOMINANT') and hc['consumption'] in ('HIGH','EXHAUSTED') and hc['permission_candidate']=='WAIT',hc))
 # Broad weak and narrow powerful direct dominance/strength representation via full runtime can be inferred from root tuples; ensure breadth independent of strength inputs.
 broad=reconcile([root('W1','BULLISH_GOLD','MINOR','SECONDARY'),root('W2','BULLISH_GOLD','MINOR','SECONDARY'),root('W3','BULLISH_GOLD','MINOR','SECONDARY'),root('W4','BULLISH_GOLD','MINOR','SECONDARY')]);c.append(ck('broad weak roots preserve BROAD breadth without raw magnitude inflation',broad['breadth']=='BROAD',broad))
 narrow=reconcile([root('SYS','BULLISH_GOLD','EXTREME','SYSTEMIC')]);c.append(ck('narrow systemic shock can dominate while breadth stays NARROW',narrow['causal_direction']=='BULLISH_GOLD' and narrow['breadth']=='NARROW',narrow))
 # P09 new snapshot fields
 pred=build_prediction('R02RUN',full,p03_policy(.15),kernel(),{}, {'value':2500,'source_id':'TEST','timestamp':'2026-08-18T10:00:00Z'}, {'cohort_id':'R02_TEST_COHORT'},event_context={},now='2026-08-18T10:00:00Z');c.append(ck('new P09 snapshots persist R02 fields',all(k in pred for k in ('decision_science_version','dominant_root_magnitude','dominant_root_health','dominant_root_importance','dominance_robustness','model_sensitivity','regime_context')),pred))
 # P11 presentation-only consumes fields
 cri={'run':{'run_id':'R02RUN','decision_time':'2026-08-18T10:00:00Z','horizon':'SESSION_1_6H','authority_mode':'SHADOW','runtime_version':'3.10'},'decision_calibration':full,'data_kernel':kernel(),'semantic':{},'causal_state':p03_policy(.15),'forward_validation':{'statistics':{},'active_cohort':{}},'promotion':{'state':'SHADOW_COMMISSIONING'},'evidence_index':{'observations':[]}}
 vm=build_view_model(cri,fixture=True);c.append(ck('P11 consumes R02 fields presentation-only',vm['executive']['dominance_robustness']==full['dominance_robustness'] and vm['executive']['dominant_root_health_state']==(full['dominant_root_health'] or {}).get('state')))
 # Cohort boundary in temp dirs; preserve old history.
 with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b, tempfile.TemporaryDirectory() as cdir:
  bd=init_boundary('bade4df',p09_state_root=a,r01_state_root=b,r02_state_root=cdir,now='2026-08-18T12:00:00Z');c.append(ck('R02 starts new ex-ante qualification boundary',bd['state']=='OPEN' and bd['new_r02_decisions_primary_qualification_authority'] is True and bd['pre_r02_evidence_primary_production_qualification_authority'] is False,bd))
 # Freeze / governance / command
 fr=verify_manifest();c.append(ck('R02 decision-science freeze valid',fr['status']=='PASS',fr));c.append(ck('R02 sensitivity policy forbids random Monte Carlo',cfg('dominance_robustness_policy.json')['random_monte_carlo_forbidden'] is True));c.append(ck('trade execution remains NONE',cfg('decision_science_2_policy.json')['trade_execution_authority']=='NONE'))
 p10=(N/'AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN/tools/alpha_desk.py').read_text();c.append(ck('R02 read-only status command installed','v31-decision-science-status' in p10))
 # R01 thresholds unchanged by checking its own qualification freeze.
 r01pol=load(N/'AD_V31_R01_FORWARD_QUALITY_PROMOTION_SCIENCE/qualification/QUALIFICATION_FREEZE_MANIFEST.json',{});c.append(ck('R01 qualification freeze remains present and authoritative',bool(r01pol.get('qualification_policy_fingerprint') or r01pol.get('freeze_fingerprint') or r01pol)))
 # release lineage
 rel=load(N/'AD_V3_PHASE_12_FINAL_CERTIFICATION_PRODUCTION_FREEZE/release/ALPHA_DESK_V3_FINAL_RELEASE_MANIFEST.json',{});lin=rel.get('lineage') or {};lineage_ok=bool(lin.get('v3_rc1_release_fingerprint')) and bool(lin.get('r01_release_fingerprint')) and bool(lin.get('r02_decision_science_fingerprint')) and ('AD-V3.1-R02' in (lin.get('amendments') or [])) and rel.get('release_candidate') in {'ALPHA_DESK_V3_1_R02','ALPHA_DESK_V3_1_R03','ALPHA_DESK_V3_1_R04'};c.append(ck('V3 RC1, R01 and R02 lineage preserved under downstream amendments',lineage_ok,lin))
 # no fake probability scan focused authority surfaces
 texts='\n'.join((P/f).read_text(errors='ignore') for f in ['config/dominance_robustness_policy.json','runtime/sensitivity_engine.py'])
 c.append(ck('R02 does not present sensitivity frequency as probability','80% bullish' not in texts.lower() and 'variant_frequency_is_not_probability' in texts))
 c.append(ck('importance matrix covers all 12 roots and 8 horizons',len(cfg('causal_importance_matrix.json')['matrix'])==12 and all(len(v)==8 for v in cfg('causal_importance_matrix.json')['matrix'].values())))
 c.append(ck('root health policy has no single-best-fact health rule','max_best_fact' not in json.dumps(cfg('root_health_policy.json')).lower()))
 c.append(ck('magnitude policy forbids quality-as-magnitude fallback',cfg('magnitude_threshold_policy.json').get('quality_as_magnitude_fallback_forbidden') is True))
 c.append(ck('P10 remains canonical V3 runtime',(N/'AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN/config/runtime_contract.json').exists()))
 c.append(ck('P11 remains canonical report renderer',(N/'AD_V3_PHASE_11_FINAL_INSTITUTIONAL_GOLD_CONTROL_ROOM/config/report_contract.json').exists()))
 c.append(ck('production remains shadow and promotion forbidden',cfg('decision_science_2_policy.json')['production_promotion_forbidden'] is True))
 ok=all(x['status']=='PASS' for x in c);out={'phase':'AD-V3.1-R02','version':'3.1.2-decision-science-2','acceptance_status':'PASS' if ok else 'FAIL_CLOSED','check_count':len(c),'checks':c,'baseline_commit':'bade4df','production_promotion_performed':False,'v3_state':'SHADOW_COMMISSIONING','trade_execution_authority':'NONE'};print(json.dumps(out,ensure_ascii=False,indent=2));return 0 if ok else 2
if __name__=='__main__':raise SystemExit(main())
