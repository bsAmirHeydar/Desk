from __future__ import annotations
import time
from pathlib import Path
from .common import config,iso,stable_id,clamp_edge
from .feature_builder import build_root_features
from .dominance_engine import reconcile
from .empirical_calibration import load_registry

def _consumption(p03):
    c=((p03.get('lifecycle') or {}).get('consumption_vector') or {}); core=[c.get('information_absorption'),c.get('expectations_repricing'),c.get('flow_propagation'),c.get('position_adjustment'),c.get('narrative_saturation')]
    present=sum(x=='PRESENT' for x in core); partial=sum(x=='PARTIAL' for x in core)
    if present>=4:return 'EXHAUSTED'
    if present>=3:return 'HIGH'
    if present>=1 and present+partial>=2:return 'MODERATE'
    if any(x=='ABSENT' for x in core):return 'LOW'
    return 'UNKNOWN'

def _strength(dom,roots):
    if dom['causal_direction'] not in ('BULLISH_GOLD','BEARISH_GOLD'):return 'UNKNOWN'
    d=next((x for x in roots if x['root_id']==dom['dominant_root']),None)
    if not d:return 'UNKNOWN'
    if d['causal_importance']=='PRIMARY' and d['freshness'] in ('FRESH_LIVE','FRESH_FOR_HORIZON') and d['magnitude']=='EXTREME':return 'DOMINANT'
    if d['causal_importance']=='PRIMARY' and d['freshness'] in ('FRESH_LIVE','FRESH_FOR_HORIZON','CONTEXT_VALID') and d['magnitude'] in ('LARGE','MATERIAL'):return 'STRONG'
    if d['magnitude'] in ('LARGE','MATERIAL') or dom['breadth'] in ('MODERATE','BROAD'):return 'MODERATE'
    return 'WEAK'

def _fragility(dom,roots,p03,kernel):
    if dom['causal_direction'] not in ('BULLISH_GOLD','BEARISH_GOLD'):return ('HIGH',['NO_CLEAR_DIRECTION'])
    factors=[]; d=next((x for x in roots if x['root_id']==dom['dominant_root']),None)
    if dom['breadth']=='NARROW':factors.append('NARROW_BREADTH')
    if dom['contradiction'] not in ('NONE','MINOR_OFFSET'):factors.append('ACTIVE_CONTRADICTION')
    if d and d.get('freshness') not in ('FRESH_LIVE','FRESH_FOR_HORIZON'):factors.append('FRESHNESS_CAP')
    if d and d.get('semantic_unknown_count',0)>0:factors.append('SEMANTIC_UNCERTAINTY')
    if d and d.get('persistence') in ('FADING','REVERSING'):factors.append('PERSISTENCE_DECAY')
    if ((p03.get('model_quality') or {}).get('missing_driver_risk'))=='HIGH':factors.append('MISSING_DRIVER_RISK')
    if ((kernel or {}).get('kernel_health') or {}).get('important_live_gaps'):factors.append('CRITICAL_LIVE_GAP')
    return ('HIGH' if len(factors)>=3 else 'ELEVATED' if factors else 'LOW',factors)

def _edge(direction,strength,dom,fragility,consumption,p03,kernel,roots):
    if direction not in ('BULLISH_GOLD','BEARISH_GOLD') or dom['dominance_state']=='BALANCED':return 'NO_EDGE',['NO_CLEAR_DOMINANCE']
    if dom['contradiction'] in ('PRIMARY_ROOT_CONFLICT','BALANCED_CONFLICT'):return 'NO_EDGE',['PRIMARY_CONFLICT']
    edge='LOW_EDGE' if strength in ('WEAK','UNKNOWN') else 'CONDITIONAL_EDGE'
    if strength in ('STRONG','DOMINANT') and fragility in ('LOW','ELEVATED') and dom['contradiction'] in ('NONE','MINOR_OFFSET'): edge='ACTIONABLE_EDGE'
    blockers=[]
    kh=(kernel or {}).get('kernel_health') or {}
    if kh.get('important_live_gaps'): edge=clamp_edge(edge,'CONDITIONAL_EDGE');blockers.append('CRITICAL_LIVE_GAPS')
    if fragility=='HIGH': edge=clamp_edge(edge,'CONDITIONAL_EDGE');blockers.append('HIGH_FRAGILITY')
    miss=(p03.get('model_quality') or {}).get('missing_driver_risk')
    if miss=='HIGH': edge=clamp_edge(edge,'CONDITIONAL_EDGE');blockers.append('MISSING_DRIVER_RISK_HIGH')
    trans=(p03.get('price_transmission') or {}).get('state')
    if trans=='NEGATIVE': edge=clamp_edge(edge,'CONDITIONAL_EDGE');blockers.append('NEGATIVE_PRICE_TRANSMISSION')
    if consumption in ('HIGH','EXHAUSTED'): edge=clamp_edge(edge,'LOW_EDGE');blockers.append('HIGH_CONSUMPTION')
    d=next((x for x in roots if x['root_id']==dom['dominant_root']),None)
    if d and d.get('freshness') not in ('FRESH_LIVE','FRESH_FOR_HORIZON'): edge=clamp_edge(edge,'CONDITIONAL_EDGE');blockers.append('DOMINANT_ROOT_NOT_LIVE_FRESH')
    if d and d.get('semantic_unknown_count',0)>0: edge=clamp_edge(edge,'CONDITIONAL_EDGE');blockers.append('DOMINANT_ROOT_SEMANTIC_UNCERTAINTY')
    if d and d.get('empirical_information_state')=='CAUTION': edge=clamp_edge(edge,'CONDITIONAL_EDGE');blockers.append('HISTORICAL_INFORMATION_CAUTION')
    return edge,blockers

def calibrate(p03,kernel=None,previous=None,promotion_state=None,empirical_registry_path=None):
    policy=config('decision_calibration_policy.json'); t0=time.perf_counter(); registry=load_registry(empirical_registry_path); roots=build_root_features(p03,kernel,previous,registry); t1=time.perf_counter(); dom=reconcile(roots); t2=time.perf_counter(); strength=_strength(dom,roots); frag,frag_reasons=_fragility(dom,roots,p03,kernel); cons=_consumption(p03); edge,blockers=_edge(dom['causal_direction'],strength,dom,frag,cons,p03,kernel,roots)
    action='WAIT'
    if edge=='ACTIONABLE_EDGE' and dom['causal_direction']=='BULLISH_GOLD':action='BUY_CANDIDATE'
    elif edge=='ACTIONABLE_EDGE' and dom['causal_direction']=='BEARISH_GOLD':action='SELL_CANDIDATE'
    prod=(promotion_state or {}).get('state')=='PRODUCTION_V3'; official=action if prod else 'NO_AUTHORITY'
    raw=((p03.get('pressure_planes') or {}).get('causal_fundamental') or {}).get('direction','UNKNOWN')
    missing=(p03.get('model_quality') or {}).get('missing_driver_risk','UNKNOWN')
    if strength in ('STRONG','DOMINANT') and (p03.get('price_transmission') or {}).get('state') in ('NEGATIVE','CONFLICTED') and missing!='HIGH': missing='ELEVATED'
    invalid=[]
    if dom['dominant_root']:
        invalid=['DOMINANT_ROOT_REVERSES','PRIMARY_EVIDENCE_EXPIRES','OPPOSING_PRIMARY_ROOT_BECOMES_DOMINANT','CRITICAL_LIVE_DATA_DISAPPEARS']
    out={'record_type':'AD_V3_P08_DECISION_CALIBRATION_STATE','schema_version':'1.0.0','phase':'AD-V3-P08','version':'3.8.0-decision-science-calibration','decision_id':stable_id('P08DEC',{'p03':p03.get('receipt_id'),'roots':[(r['root_id'],r['direction'],r['economic_evidence_fingerprint']) for r in roots]}),'run_id':p03.get('receipt_id'),'generated_at_utc':iso(),'horizon':p03.get('horizon','SESSION_1_6H'),'raw_p03_causal_direction':raw,'causal_direction':dom['causal_direction'],'pressure_strength':strength,'dominance_state':dom['dominance_state'],'dominant_root':dom['dominant_root'],'supporting_roots':dom['supporting_roots'],'opposing_roots':dom['opposing_roots'],'breadth':dom['breadth'],'fragility':frag,'fragility_reasons':frag_reasons,'contradiction':dom['contradiction'],'consumption':cons,'missing_driver_risk':missing,'edge_state':edge,'permission_candidate':action,'blockers':sorted(set(blockers+frag_reasons if action=='WAIT' else blockers)),'calibrated_roots':roots,'empirical_calibration':{'overall_sample_state':registry.get('overall_sample_state','UNAVAILABLE'),'episode_count':registry.get('episode_count',0),'historical_calibration_is_not_forward_validation':True},'invalidation_conditions':invalid,'escalation_feedback':{'missing_driver_risk':missing,'contradiction':dom['contradiction'],'unresolved_primary_root':dom['dominant_root'] if frag=='HIGH' else None,'direction_authority':False},'permission':{'direction':dom['causal_direction'],'edge_state':edge,'research_action_candidate':action,'official_permission':official,'production_mode':prod,'blockers':sorted(set(blockers+frag_reasons if action=='WAIT' else blockers)),'direction_is_not_edge':True,'edge_is_not_permission':True,'trade_execution_authority':False},'audit':{'p03_raw_direction_retained':True,'causal_direction_invented':False,'raw_fact_count_not_in_authority_vector':True,'pressure_separate_from_price':True,'historical_calibration_not_forward_validation':True,'no_user_facing_probability':True},'timing_ms':{'feature_build_ms':round((t1-t0)*1000,3),'dominance_ms':round((t2-t1)*1000,3),'total_p08_ms':round((time.perf_counter()-t0)*1000,3)}}
    if out['pressure_strength'] not in policy['pressure_strength_states'] or out['dominance_state'] not in policy['dominance_states'] or out['edge_state'] not in policy['edge_states'] or out['permission_candidate'] not in policy['permission_candidates']:
        raise RuntimeError('P08_POLICY_ENUM_VIOLATION')
    if policy.get('trade_execution_authority')!='NONE' or not policy.get('production_promotion_forbidden',False): raise RuntimeError('P08_AUTHORITY_POLICY_VIOLATION')
    return out
