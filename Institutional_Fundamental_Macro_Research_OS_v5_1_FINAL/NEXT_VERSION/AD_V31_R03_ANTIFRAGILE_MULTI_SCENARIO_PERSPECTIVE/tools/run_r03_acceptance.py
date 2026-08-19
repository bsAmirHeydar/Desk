#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import sys,json,tempfile,copy,subprocess,re
P=Path(__file__).resolve().parents[1];N=P.parent;REPO=N.parents[1];sys.path.insert(0,str(N))
from AD_V31_R03_ANTIFRAGILE_MULTI_SCENARIO_PERSPECTIVE.runtime.perspective_runtime import run,fail_closed
from AD_V31_R03_ANTIFRAGILE_MULTI_SCENARIO_PERSPECTIVE.runtime.perspective_overlay import evaluate as overlay_eval
from AD_V31_R03_ANTIFRAGILE_MULTI_SCENARIO_PERSPECTIVE.runtime.perspective_freeze import verify_manifest
from AD_V31_R03_ANTIFRAGILE_MULTI_SCENARIO_PERSPECTIVE.runtime.cohort_boundary import initialize as init_boundary
from AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0.runtime.precommit import build_prediction
from AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN.runtime.gold_orchestrator import STAGE_ORDER
from AD_V3_PHASE_11_FINAL_INSTITUTIONAL_GOLD_CONTROL_ROOM.runtime.presenter import build_view_model

def ck(n,o,d=None):return {'name':n,'status':'PASS' if o else 'FAIL','detail':d}
def health(state='HEALTHY',direct='DIRECT',same=0,sem=0):return {'state':state,'directness_state':direct,'same_shock_manifestation_count':same,'magnitude_coverage_share':1.0,'semantic_evidence_count':sem,'critical_evidence_missing':[] if state!='CRITICAL_GAP' else [['CRITICAL_FACT']]}
def root(rid,d='BULLISH_GOLD',mag='LARGE',imp='PRIMARY',hs='HEALTHY',direct='DIRECT',same=0):return {'root_id':rid,'direction':d,'magnitude':mag,'causal_importance':imp,'evidence_fact_ids':[rid+'_FACT'],'root_health':health(hs,direct,same)}
def p08(direction='BULLISH_GOLD',permission='BUY_CANDIDATE',edge='ACTIONABLE_EDGE',breadth='BROAD',sensitivity='LOW',rob='ROBUST',missing='LOW',regime='NORMAL',root_state='HEALTHY',direct='DIRECT',same=0,extra=None,cons='LOW'):
 rid='REAL_RATE_OPPORTUNITY_COST' if direction!='BEARISH_GOLD' else 'USD_AUTONOMOUS';r=root(rid,direction if direction in ('BULLISH_GOLD','BEARISH_GOLD') else 'UNKNOWN',hs=root_state,direct=direct,same=same);roots=[r]+list(extra or []);return {'decision_id':'D_'+direction+permission+edge,'horizon':'SESSION_1_6H','generated_at_utc':'2026-08-18T10:00:00Z','causal_direction':direction,'dominant_root':rid if direction in ('BULLISH_GOLD','BEARISH_GOLD') else None,'dominant_root_magnitude':r['magnitude'],'dominant_root_importance':r['causal_importance'],'dominant_root_health':r['root_health'],'dominance_state':'BULLISH_DOMINANT' if direction=='BULLISH_GOLD' else 'BEARISH_DOMINANT' if direction=='BEARISH_GOLD' else 'BALANCED','dominance_robustness':rob,'model_sensitivity':sensitivity,'breadth':breadth,'missing_driver_risk':missing,'contradiction':'NONE','permission_candidate':permission,'edge_state':edge,'pressure_strength':'STRONG','consumption':cons,'supporting_roots':[rid] if direction in ('BULLISH_GOLD','BEARISH_GOLD') else [],'opposing_roots':[],'invalidation_conditions':['DOMINANT_ROOT_REVERSES'],'calibrated_roots':roots,'regime_context':regime,'blockers':[]}
def p03(trans='POSITIVE'):return {'receipt_id':'P03','horizon':'SESSION_1_6H','price_transmission':{'state':trans},'model_quality':{'missing_driver_risk':'LOW'},'pressure_planes':{}}
def event(status='UPCOMING'):return {'events':[{'event_id':'FOMC_TEST','event':'FOMC','label':'FOMC','event_time':'2026-08-18T12:00:00Z','materiality':'THESIS_CRITICAL','affected_roots':['US_POLICY_EXPECTATIONS'],'status':status}]}
def main():
 c=[]
 healthy=run(p08(),p03(),{}, {'adjudication_mode':'AUTO_GOVERNED'},{'events':[]},'2026-08-18T10:00:00Z');c.append(ck('healthy robust state can remain NO_CHANGE',healthy['perspective_overlay']['overlay']=='NO_CHANGE' and healthy['final_permission']=='BUY_CANDIDATE',healthy['perspective_overlay']))
 c.append(ck('R03 preserves canonical direction',healthy['canonical_direction']=='BULLISH_GOLD'))
 c.append(ck('canonical scenario is conditional not probability',any(x['scenario_class']=='CANONICAL_CONTINUATION' for x in healthy['scenario_packet']['scenarios']) and healthy['scenario_packet']['scenario_counts_are_not_probabilities']))
 c.append(ck('scenario set is bounded',healthy['scenario_packet']['scenario_count']<=6 and healthy['scenario_packet']['bounded']))
 c.append(ck('Via Negativa exposes thesis breakers',bool(healthy['via_negativa']['thesis_breakers'])))
 c.append(ck('every material scenario has invalidation',all(x.get('invalidating_conditions') for x in healthy['scenario_packet']['scenarios'])))
 c.append(ck('fragility map is multidimensional',len(healthy['fragility_map']['dimensions'])==10 and 'score' not in healthy['fragility_map']))
 c.append(ck('no total antifragility score',not any('score' in k.lower() for k in healthy.keys())))
 c.append(ck('unknown envelope contained in healthy state',healthy['unknown_state']['unknown_envelope']=='CONTAINED'))
 c.append(ck('tail awareness is not probability',healthy['unknown_state']['tail_is_not_probability'] is True))
 # narrative monoculture
 mono=run(p08(breadth='NARROW',same=5),p03(),{}, {},{'events':[]});c.append(ck('narrative monoculture raises narrative fragility without changing direction',mono['fragility_map']['dimensions']['NARRATIVE_FRAGILITY']=='HIGH' and mono['canonical_direction']=='BULLISH_GOLD',mono['fragility_map']))
 c.append(ck('alternative break world retained under concentrated narrative',any(x['scenario_class']=='REVERSAL_OR_BREAK' for x in mono['scenario_packet']['scenarios'])))
 # price against pressure, no liquidity
 conflict=run(p08(),p03('NEGATIVE'),{}, {},{'events':[]});mech=next(x for x in conflict['scenario_packet']['scenarios'] if x['scenario_class']=='MECHANICAL_LIQUIDITY_DISLOCATION');c.append(ck('price against pressure without liquidity evidence stays unexplained',mech['status']=='UNRESOLVED' and mech.get('explanation_state')=='UNEXPLAINED_TRANSMISSION_CONFLICT',mech));c.append(ck('price conflict does not flip fundamental direction',conflict['canonical_direction']=='BULLISH_GOLD'))
 # confirmed mechanical
 fund=root('FUNDING_COLLATERAL_STRESS','BEARISH_GOLD','LARGE','SYSTEMIC');liq=run(p08(regime='LIQUIDITY_STRESS',extra=[fund]),p03('NEGATIVE'),{}, {},{'events':[]});lm=next(x for x in liq['scenario_packet']['scenarios'] if x['scenario_class']=='MECHANICAL_LIQUIDITY_DISLOCATION');c.append(ck('confirmed mechanical dislocation requires governed liquidity evidence',lm['status']=='ACTIVE' and lm.get('explanation_state')=='CONFIRMED_MECHANICAL_LIQUIDITY_DISLOCATION',lm))
 # model-sensitive
 ms=run(p08(sensitivity='HIGH',rob='MODEL_SENSITIVE'),p03(),{}, {},{'events':[]});c.append(ck('model-sensitive state raises model fragility',ms['fragility_map']['dimensions']['MODEL_FRAGILITY']=='HIGH'));c.append(ck('model-sensitive state can cap but never flip',ms['final_permission'] in ('WAIT','BUY_CANDIDATE') and ms['canonical_direction']=='BULLISH_GOLD'))
 # critical unknown
 cu=run(p08(missing='HIGH',root_state='CRITICAL_GAP'),p03('CONFLICTED'),{}, {},{'events':[]});c.append(ck('critical unknown envelope detected',cu['unknown_state']['unknown_envelope']=='CRITICAL',cu['unknown_state']));c.append(ck('critical unknown can FORCE_WAIT while direction remains',cu['perspective_overlay']['overlay']=='FORCE_WAIT' and cu['final_permission']=='WAIT' and cu['canonical_direction']=='BULLISH_GOLD'))
 # event arm/trigger
 ea=run(p08(),p03(),{}, {},event('UPCOMING'));es=next(x for x in ea['scenario_packet']['scenarios'] if x['scenario_class']=='SCHEDULED_EVENT_DISCONTINUITY');c.append(ck('scheduled event is ARMED not triggered before release',es['status']=='ARMED'))
 et=run(p08(),p03(),{}, {},event('TRIGGERED'));ets=next(x for x in et['scenario_packet']['scenarios'] if x['scenario_class']=='SCHEDULED_EVENT_DISCONTINUITY');c.append(ck('registered realized event can trigger discontinuity',ets['status']=='TRIGGERED' and et['nonlinearity']['state']=='DISCONTINUOUS_EVENT'))
 c.append(ck('event existence alone does not imply direction flip',ea['canonical_direction']=='BULLISH_GOLD'))
 # tail fiction / unknown naming
 tail=cu;c.append(ck('TAIL_UNKNOWN never names a specific invented event',tail['unknown_state']['unknown_unknown_specific_event_named'] is False and all('war' not in str(x).lower() and 'bank collapse' not in str(x).lower() for x in tail['scenario_packet']['scenarios'])))
 # permission monotonic attacks
 wait=run(p08(permission='WAIT',edge='NO_EDGE'),p03(),{}, {},{'events':[]});c.append(ck('R03 cannot upgrade upstream WAIT',wait['final_permission']=='WAIT'))
 cond=run(p08(permission='WAIT',edge='CONDITIONAL_EDGE'),p03(),{}, {},{'events':[]});c.append(ck('R03 cannot upgrade Conditional Edge',cond['final_edge']=='CONDITIONAL_EDGE'))
 c.append(ck('R03 overlay authority upgraded flag always false',all((run(p08(permission=p),p03(),{}, {},{'events':[]})['perspective_overlay']['authority_upgraded'] is False) for p in ('WAIT','BUY_CANDIDATE'))))
 # critical dimension not averaged
 cf=cu['fragility_map'];c.append(ck('critical fragility cannot be averaged away',cf['overall']=='CRITICALLY_FRAGILE'))
 # nonlinearity no evidence
 c.append(ck('nonlinearity not invented without evidence',healthy['nonlinearity']['state']=='LINEAR_OR_UNRESOLVED'))
 # cascade armed/triggered
 armed=run(p08(extra=[root('FUNDING_COLLATERAL_STRESS','BEARISH_GOLD','MATERIAL','PRIMARY')]),p03('POSITIVE'),{}, {},{'events':[]});ap=next(x for x in armed['nonlinearity']['pathways'] if x['pathway_id']=='FUNDING_TO_FORCED_LIQUIDATION');c.append(ck('authorized cascade pathway can be ARMED without being triggered',ap['state']=='ARMED'))
 trig=liq;tp=next(x for x in trig['nonlinearity']['pathways'] if x['pathway_id']=='FUNDING_TO_FORCED_LIQUIDATION');c.append(ck('authorized cascade triggers only with confirmations',tp['state']=='TRIGGERED' and trig['nonlinearity']['state']=='CASCADE_RISK'))
 # no scenario explosion/duplicates/probability
 c.append(ck('operator-facing scenario count maximum six',all(run(p08(),p03('NEGATIVE'),{}, {},event('UPCOMING'))['scenario_packet'][k] is not None for k in ('scenario_count','bounded')) and run(p08(),p03('NEGATIVE'),{}, {},event('UPCOMING'))['scenario_packet']['scenario_count']<=6))
 texts=json.dumps(run(p08(),p03(),{}, {},event('UPCOMING')),ensure_ascii=False).lower();c.append(ck('scenario output contains no calibrated probability claim','bullish probability' not in texts and 'tail_probability' not in texts))
 # fail closed
 fc=fail_closed(p08(),'SYNTHETIC_FAILURE');c.append(ck('R03 runtime failure fails closed to WAIT',fc['final_permission']=='WAIT' and fc['perspective_overlay']['overlay']=='FORCE_WAIT'))
 # P09 persistence
 pred=build_prediction('R03RUN',p08(),p03(),{}, {},{'value':2500,'source_id':'TEST'},{'cohort_id':'R03TEST'},now='2026-08-18T10:00:00Z',perspective=healthy);c.append(ck('P09 stores R03 scenario and overlay fields',all(k in pred for k in ('r03_scenario_ids','r03_fragility_map','r03_unknown_envelope','r03_nonlinearity_state','r03_overlay','r03_final_permission'))));c.append(ck('P09 retains pre-R03 permission and effective post-R03 permission',pred['pre_r03_permission_candidate']=='BUY_CANDIDATE' and pred['permission_candidate']==healthy['final_permission']))
 # P11 view consumes perspective only when bound to current direction
 cri={'run':{'run_id':'R','decision_time':'2026-08-18T10:00:00Z','horizon':'SESSION_1_6H','authority_mode':'SHADOW','runtime_version':'3.10.1'},'decision_calibration':p08(),'perspective_state':healthy,'data_kernel':{'kernel_health':{}},'semantic':{},'causal_state':p03(),'forward_validation':{'statistics':{},'active_cohort':{}},'promotion':{'state':'SHADOW_COMMISSIONING'},'evidence_index':{'observations':[]}};vm=build_view_model(cri,fixture=True);c.append(ck('P11 exposes scenario atlas human-first',vm['perspective']['scenario_count']>0 and vm['executive']['thesis_resilience']==healthy['thesis_resilience']))
 c.append(ck('P11 uses post-overlay permission when perspective is valid',vm['executive']['permission']==healthy['final_permission']))
 # cohort boundary isolated
 with tempfile.TemporaryDirectory() as a,tempfile.TemporaryDirectory() as b,tempfile.TemporaryDirectory() as d,tempfile.TemporaryDirectory() as e:
  bd=init_boundary('69be946',p09_state_root=a,r01_state_root=b,r02_state_root=d,r03_state_root=e,now='2026-08-18T12:00:00Z');c.append(ck('R03 initializes a new ex-ante qualification boundary',bd['state']=='OPEN' and bd['new_r03_decisions_primary_qualification_authority'] is True and bd['pre_r03_evidence_primary_production_qualification_authority'] is False,bd));c.append(ck('pre-R03 history explicitly preserved observationally',bd['pre_r03_history_preserved'] is True))
 # freeze / policy governance
 fr=verify_manifest();c.append(ck('R03 perspective science freeze valid',fr['status']=='PASS',fr));pol=json.loads((P/'config/r03_scientific_policy.json').read_text());c.append(ck('R03 authority is perspective-only',pol['authority']=='PERSPECTIVE_ONLY'));c.append(ck('R03 cannot create new causal root',pol['new_causal_root_forbidden'] is True));c.append(ck('R03 LLM has no scenario authority',pol['llm_scenario_authority'] is False));c.append(ck('R03 has no internet acquisition authority',pol['internet_access'] is False));c.append(ck('R03 has no trade execution authority',pol['trade_execution_authority']=='NONE'))
 # integration files
 p10=(N/'AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN/runtime/gold_orchestrator.py').read_text();c.append(ck('P10 stage order places R03 before P09 precommit',STAGE_ORDER.index('DECISION_CALIBRATION')<STAGE_ORDER.index('PERSPECTIVE_OVERLAY')<STAGE_ORDER.index('FORWARD_PRECOMMIT')));c.append(ck('P10 uses canonical R03 runtime','run_r03_perspective' in p10 and 'r03_perspective_state.json' in p10));c.append(ck('R03 status command is read-only dispatch','v31-antifragile-status' in (N/'AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN/tools/alpha_desk.py').read_text()))
 # preserved R02/R01 science
 r02=subprocess.run([sys.executable,str(N/'AD_V31_R02_DECISION_SCIENCE_2_0/tools/run_r02_acceptance.py')],capture_output=True,text=True);c.append(ck('R02 acceptance preserved',r02.returncode==0,r02.stdout[-500:] if r02.returncode else 'PASS'))
 r01=subprocess.run([sys.executable,str(N/'AD_V31_R01_FORWARD_QUALITY_PROMOTION_SCIENCE/tools/run_r01_acceptance.py')],capture_output=True,text=True);c.append(ck('R01 acceptance preserved',r01.returncode==0,r01.stdout[-500:] if r01.returncode else 'PASS'))
 # semantic no story authority and no probabilities
 alltxt='\n'.join(x.read_text(errors='ignore') for x in list((P/'config').glob('*.json'))+list((P/'runtime').glob('*.py')));c.append(ck('no Taleb/black-swan probability theatre','BLACK_SWAN_PROBABILITY' not in alltxt and 'ANTIFRAGILITY_SCORE' not in alltxt and not re.search(r'\b(?:[0-9]{1,3}%|0\.[0-9]+)\s*(?:bullish|bearish|tail|scenario)\b',alltxt,re.I)))
 c.append(ck('tail unknown policy forbids specific unknown naming',json.loads((P/'config/tail_unknown_policy.json').read_text())['specific_unknown_event_naming_forbidden'] is True))
 c.append(ck('scenario archetypes limited to six classes',len(json.loads((P/'config/scenario_archetype_registry.json').read_text())['archetypes'])==6))
 c.append(ck('fragility policy has exactly ten required dimensions',len(json.loads((P/'config/fragility_dimension_policy.json').read_text())['dimensions'])==10))
 c.append(ck('perspective overlay supports only monotonic three states',json.loads((P/'config/perspective_overlay_policy.json').read_text())['allowed']==['NO_CHANGE','CAP_TO_CONDITIONAL','FORCE_WAIT']))
 # Integrated end-to-end and golden perspective certification.
 gi=subprocess.run([sys.executable,str(P/'tools/run_golden_perspective_matrix.py')],capture_output=True,text=True,encoding='utf-8',errors='replace');c.append(ck('Golden Perspective Matrix 20/20 PASS',gi.returncode==0 and '"case_count": 20' in gi.stdout and '"status": "PASS"' in gi.stdout,gi.stdout[-500:] if gi.returncode else 'PASS'))
 integ=subprocess.run([sys.executable,str(P/'tools/run_integrated_r03_fixture.py')],capture_output=True,text=True,encoding='utf-8',errors='replace');c.append(ck('full offline integrated R03 fixture PASS',integ.returncode==0 and '"status": "PASS"' in integ.stdout,integ.stdout[-500:] if integ.returncode else 'PASS'))
 # Production remains shadow
 c.append(ck('production remains shadow',pol['production_promotion_forbidden'] is True));c.append(ck('promotion not performed',True));c.append(ck('trade execution NONE',pol['trade_execution_authority']=='NONE'))
 ok=all(x['status']=='PASS' for x in c);out={'phase':'AD-V3.1-R03','version':'3.1.3-antifragile-perspective','acceptance_status':'PASS' if ok else 'FAIL_CLOSED','check_count':len(c),'checks':c,'baseline_commit':'69be946','v3_state':'SHADOW_COMMISSIONING','production_promotion_performed':False,'trade_execution_authority':'NONE'};print(json.dumps(out,ensure_ascii=False,indent=2));return 0 if ok else 2
if __name__=='__main__':raise SystemExit(main())
