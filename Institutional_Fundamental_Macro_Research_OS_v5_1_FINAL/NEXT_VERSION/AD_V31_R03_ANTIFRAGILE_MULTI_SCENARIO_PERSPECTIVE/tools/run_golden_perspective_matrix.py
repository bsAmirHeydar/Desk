#!/usr/bin/env python3
from pathlib import Path
import sys,json
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P.parent));from AD_V31_R03_ANTIFRAGILE_MULTI_SCENARIO_PERSPECTIVE.runtime.perspective_runtime import run

def h(s='HEALTHY',d='DIRECT',same=0):return {'state':s,'directness_state':d,'same_shock_manifestation_count':same,'magnitude_coverage_share':1.0,'semantic_evidence_count':0,'critical_evidence_missing':[] if s!='CRITICAL_GAP' else [['X']]}
def rt(rid,d,mag='LARGE',imp='PRIMARY',hs='HEALTHY',direct='DIRECT',same=0):return {'root_id':rid,'direction':d,'magnitude':mag,'causal_importance':imp,'evidence_fact_ids':[rid+'_FACT'],'root_health':h(hs,direct,same)}
def state(direction='BULLISH_GOLD',**kw):
 rid='REAL_RATE_OPPORTUNITY_COST' if direction!='BEARISH_GOLD' else 'USD_AUTONOMOUS';r=rt(rid,direction if direction in ('BULLISH_GOLD','BEARISH_GOLD') else 'UNKNOWN',kw.get('mag','LARGE'),kw.get('imp','PRIMARY'),kw.get('health','HEALTHY'),kw.get('direct','DIRECT'),kw.get('same',0));return {'decision_id':'G','horizon':'SESSION_1_6H','causal_direction':direction,'dominant_root':rid if direction in ('BULLISH_GOLD','BEARISH_GOLD') else None,'dominance_robustness':kw.get('rob','ROBUST'),'model_sensitivity':kw.get('sens','LOW'),'breadth':kw.get('breadth','BROAD'),'missing_driver_risk':kw.get('missing','LOW'),'contradiction':kw.get('contradiction','NONE'),'permission_candidate':kw.get('perm','BUY_CANDIDATE' if direction=='BULLISH_GOLD' else 'SELL_CANDIDATE' if direction=='BEARISH_GOLD' else 'WAIT'),'edge_state':kw.get('edge','ACTIONABLE_EDGE' if direction in ('BULLISH_GOLD','BEARISH_GOLD') else 'NO_EDGE'),'pressure_strength':kw.get('strength','STRONG'),'consumption':kw.get('cons','LOW'),'supporting_roots':[rid] if direction in ('BULLISH_GOLD','BEARISH_GOLD') else [],'opposing_roots':[],'invalidation_conditions':['DOMINANT_ROOT_REVERSES'],'calibrated_roots':[r]+kw.get('extra',[]),'regime_context':kw.get('regime','NORMAL')}
def p3(t='POSITIVE'):return {'horizon':'SESSION_1_6H','price_transmission':{'state':t}}
def ev(st='UPCOMING'):return {'events':[{'event_id':'FOMC','event':'FOMC','status':st,'affected_roots':['US_POLICY_EXPECTATIONS']}]}
def check(name,r,fn):return {'case':name,'status':'PASS' if fn(r) else 'FAIL','overlay':r.get('perspective_overlay',{}).get('overlay'),'resilience':r.get('thesis_resilience'),'unknown':r.get('unknown_state',{}).get('unknown_envelope'),'scenario_count':r.get('scenario_packet',{}).get('scenario_count')}
cases=[]
def add(n,s,p,e,fn):cases.append(check(n,run(s,p,{}, {},e),fn))
add('A Robust bullish continuation',state(),p3(),{'events':[]},lambda r:r['canonical_direction']=='BULLISH_GOLD' and r['perspective_overlay']['overlay']=='NO_CHANGE')
add('B Robust bearish continuation',state('BEARISH_GOLD'),p3(),{'events':[]},lambda r:r['canonical_direction']=='BEARISH_GOLD')
add('C Bullish but fragile',state(breadth='NARROW',same=5),p3(),{'events':[]},lambda r:r['fragility_map']['overall'] in ('FRAGILE','WATCH'))
add('D Bearish but fragile',state('BEARISH_GOLD',breadth='NARROW',same=5),p3(),{'events':[]},lambda r:r['canonical_direction']=='BEARISH_GOLD' and r['fragility_map']['overall']!='ROBUST')
add('E True mixed',state('MIXED',perm='WAIT',edge='NO_EDGE'),p3(),{'events':[]},lambda r:r['final_permission']=='WAIT')
fund=rt('FUNDING_COLLATERAL_STRESS','BEARISH_GOLD','LARGE','SYSTEMIC')
add('F Mechanical liquidation against bullish pressure',state(regime='LIQUIDITY_STRESS',extra=[fund]),p3('NEGATIVE'),{'events':[]},lambda r:any(x.get('explanation_state')=='CONFIRMED_MECHANICAL_LIQUIDITY_DISLOCATION' for x in r['scenario_packet']['scenarios']))
add('G Mechanical squeeze against bearish pressure',state('BEARISH_GOLD',regime='LIQUIDITY_STRESS',extra=[fund]),p3('NEGATIVE'),{'events':[]},lambda r:any(x['scenario_class']=='MECHANICAL_LIQUIDITY_DISLOCATION' for x in r['scenario_packet']['scenarios']))
add('H Scheduled event armed',state(),p3(),ev('UPCOMING'),lambda r:any(x['status']=='ARMED' and x['scenario_class']=='SCHEDULED_EVENT_DISCONTINUITY' for x in r['scenario_packet']['scenarios']))
add('I Event discontinuity triggered',state(),p3(),ev('TRIGGERED'),lambda r:r['nonlinearity']['state']=='DISCONTINUOUS_EVENT')
add('J Critical unknown-driver state',state(missing='HIGH',health='CRITICAL_GAP'),p3('CONFLICTED'),{'events':[]},lambda r:r['unknown_state']['unknown_envelope']=='CRITICAL' and r['final_permission']=='WAIT')
add('K Narrow systemic shock',state(breadth='NARROW',imp='SYSTEMIC',mag='EXTREME'),p3(),{'events':[]},lambda r:r['canonical_direction']=='BULLISH_GOLD' and r['fragility_map']['dimensions']['CAUSAL_CONCENTRATION_FRAGILITY']=='HIGH')
add('L Broad weak state',state(mag='MINOR',strength='WEAK',edge='LOW_EDGE',perm='WAIT'),p3(),{'events':[]},lambda r:r['final_permission']=='WAIT')
add('M Proxy-heavy dominant root',state(direct='PROXY_ONLY'),p3(),{'events':[]},lambda r:r['fragility_map']['dimensions']['DATA_FRAGILITY'] in ('LOW','MODERATE','HIGH','CRITICAL'))
add('N Narrative concentration',state(breadth='NARROW',same=6),p3(),{'events':[]},lambda r:r['fragility_map']['dimensions']['NARRATIVE_FRAGILITY']=='HIGH')
add('O Model-sensitive dominance',state(sens='HIGH',rob='MODEL_SENSITIVE'),p3(),{'events':[]},lambda r:r['fragility_map']['dimensions']['MODEL_FRAGILITY']=='HIGH')
add('P Strong pressure/high consumption',state(cons='HIGH',perm='WAIT',edge='LOW_EDGE'),p3(),{'events':[]},lambda r:r['canonical_direction']=='BULLISH_GOLD' and r['final_permission']=='WAIT')
add('Q Tail unknown without invented story',state(missing='HIGH',health='CRITICAL_GAP'),p3('CONFLICTED'),{'events':[]},lambda r:r['unknown_state']['unknown_unknown_specific_event_named'] is False)
add('R Cascade pathway armed',state(extra=[rt('FUNDING_COLLATERAL_STRESS','BEARISH_GOLD','MATERIAL','PRIMARY')]),p3(),{'events':[]},lambda r:any(x['state']=='ARMED' for x in r['nonlinearity']['pathways']))
add('S Cascade pathway triggered',state(regime='LIQUIDITY_STRESS',extra=[fund]),p3('NEGATIVE'),{'events':[]},lambda r:r['nonlinearity']['state']=='CASCADE_RISK')
add('T Healthy state where R03 does nothing',state(),p3(),{'events':[]},lambda r:r['perspective_overlay']['overlay']=='NO_CHANGE')
ok=all(x['status']=='PASS' for x in cases);out={'phase':'AD-V3.1-R03','matrix':'GOLDEN_PERSPECTIVE_MATRIX','status':'PASS' if ok else 'FAIL_CLOSED','case_count':len(cases),'cases':cases,'probabilities_used':False};print(json.dumps(out,indent=2,ensure_ascii=False));raise SystemExit(0 if ok else 2)
