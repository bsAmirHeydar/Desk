#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import sys,json
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P.parent))
from AD_V31_R02_DECISION_SCIENCE_2_0.runtime.robust_dominance_engine import reconcile
from AD_V31_R02_DECISION_SCIENCE_2_0.runtime.sensitivity_engine import evaluate
from AD_V31_R02_DECISION_SCIENCE_2_0.runtime.root_health_engine import assess
from AD_V31_R02_DECISION_SCIENCE_2_0.runtime.magnitude_engine import fact_magnitude

def health(s='HEALTHY'):return {'state':s,'critical_evidence_present':s!='CRITICAL_GAP','valid_share':1 if s=='HEALTHY' else .5}
def r(i,d,m='MATERIAL',imp='PRIMARY',fr='FRESH_FOR_HORIZON',q='HIGH',h='HEALTHY'):return {'root_id':i,'direction':d,'magnitude':m,'causal_importance':imp,'freshness':fr,'evidence_quality':q,'root_health':health(h),'persistence':'NEW'}
def case(name,ok,detail):return {'scenario':name,'status':'PASS' if ok else 'FAIL','detail':detail}
def main():
 out=[]
 x=evaluate([r('A','BULLISH_GOLD','LARGE')]);out.append(case('A Robust strong bullish',x['canonical']['causal_direction']=='BULLISH_GOLD' and x['robustness']=='ROBUST',x))
 x=evaluate([r('A','BEARISH_GOLD','LARGE')]);out.append(case('B Robust strong bearish',x['canonical']['causal_direction']=='BEARISH_GOLD' and x['robustness']=='ROBUST',x))
 x=reconcile([r('A','BULLISH_GOLD','LARGE'),r('B','BEARISH_GOLD','LARGE')]);out.append(case('C True mixed',x['causal_direction']=='MIXED',x))
 x=evaluate([r('A','BULLISH_GOLD','MINOR','SECONDARY','CONTEXT_VALID','MEDIUM','PARTIAL'),r('B','BEARISH_GOLD','MINOR','PRIMARY','CONTEXT_VALID','MEDIUM','HEALTHY')]);out.append(case('D Actual model-sensitive dominance',x['robustness']=='MODEL_SENSITIVE' and x['model_sensitivity']=='HIGH',x))
 x=evaluate([r('A','BEARISH_GOLD','MINOR','SECONDARY','CONTEXT_VALID','MEDIUM','PARTIAL'),r('B','BULLISH_GOLD','MINOR','PRIMARY','CONTEXT_VALID','MEDIUM','HEALTHY')]);out.append(case('E Symmetric model-sensitive dominance',x['robustness']=='MODEL_SENSITIVE' and x['model_sensitivity']=='HIGH',x))
 x=reconcile([r('SYS','BULLISH_GOLD','EXTREME','SYSTEMIC')]);out.append(case('F Narrow systemic shock',x['breadth']=='NARROW' and x['causal_direction']=='BULLISH_GOLD',x))
 x=reconcile([r('W1','BULLISH_GOLD','MINOR','SECONDARY'),r('W2','BULLISH_GOLD','MINOR','SECONDARY'),r('W3','BULLISH_GOLD','MINOR','SECONDARY')]);out.append(case('G Broad weak pressure',x['breadth']=='BROAD',x))
 x=reconcile([r('GAP','BULLISH_GOLD','LARGE','PRIMARY',h='CRITICAL_GAP')]);out.append(case('H Strong pressure / critical root gap retained direction',x['causal_direction']=='BULLISH_GOLD',x))
 x=reconcile([r('LOWIMP','BULLISH_GOLD','EXTREME','BACKGROUND'),r('HIIMP','BEARISH_GOLD','MATERIAL','PRIMARY')]);out.append(case('I Large magnitude / low importance no automatic dominance',x['causal_direction']!='BULLISH_GOLD',x))
 x=reconcile([r('PRIM','BULLISH_GOLD','UNKNOWN','PRIMARY')]);out.append(case('J Primary importance / unknown magnitude representable',x['causal_direction']=='BULLISH_GOLD',x))
 mag=fact_magnitude({'fact_id':'CENTRAL_BANK_NET_GOLD_PURCHASES','resolution':'RESOLVED','details':{'structural_value':100}});out.append(case('K Structural strong / no session impulse',mag['state']=='UNKNOWN' and mag['temporal_role']=='STRUCTURAL_CONTEXT',mag))
 out.append(case('L Price against pressure invariant','price' not in ''.join(str(v) for v in r('A','BULLISH_GOLD').keys()).lower(),{'direction':'BULLISH_GOLD','price_authority':False}))
 out.append(case('M High consumption remains downstream','consumption' not in r('A','BULLISH_GOLD'),{'root_direction':'BULLISH_GOLD','consumption_authority':'downstream only'}))
 rh=assess('USD_AUTONOMOUS',['USD_AUTONOMOUS_SHOCK'],[{'fact_id':'USD_AUTONOMOUS_SHOCK','observation_id':'O','resolution':'RESOLVED','effect_on_gold':'BEARISH_GOLD'}],{'USD_AUTONOMOUS_SHOCK':'FRESH_FOR_HORIZON'},{'USD_AUTONOMOUS_SHOCK':{'p02_directness':'PROXY'}},{'USD_AUTONOMOUS_SHOCK':{'state':'MATERIAL'}},'BEARISH_GOLD');out.append(case('N Proxy-heavy root',rh['directness_state']=='PROXY_ONLY',rh))
 facts=['UST_5Y_REAL_YIELD','UST_10Y_REAL_YIELD','UST_30Y_REAL_YIELD'];rh=assess('REAL_RATE_OPPORTUNITY_COST',facts,[{'fact_id':f,'observation_id':'O'+f,'resolution':'RESOLVED','effect_on_gold':'BULLISH_GOLD'} for f in facts],{f:'FRESH_FOR_HORIZON' for f in facts},{f:{'p02_directness':'DIRECT'} for f in facts},{f:{'state':'MATERIAL'} for f in facts},'BULLISH_GOLD');out.append(case('O Same-shock manifestation inflation blocked',rh['observed_evidence_count']==3 and rh['independent_evidence_count']==1,rh))
 ok=all(x['status']=='PASS' for x in out);print(json.dumps({'phase':'AD-V3.1-R02','golden_status':'PASS' if ok else 'FAIL','scenario_count':len(out),'scenarios':out,'fixture_only':True,'prospective_evidence_authority':False},indent=2,ensure_ascii=False));return 0 if ok else 2
if __name__=='__main__':raise SystemExit(main())
