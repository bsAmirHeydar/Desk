from __future__ import annotations
import time
from .common import cfg,iso,stable_id
from .via_negativa_engine import evaluate as via_eval
from .tail_unknown_engine import evaluate as unknown_eval
from .nonlinearity_engine import evaluate as nonlin_eval
from .scenario_engine import build as scenario_build
from .fragility_engine import evaluate as frag_eval
from .perspective_overlay import evaluate as overlay_eval

def _resilience(p08,frag,unknown,scenarios,via):
    if p08.get('causal_direction') not in ('BULLISH_GOLD','BEARISH_GOLD'):return 'UNKNOWN'
    if any(a.get('state')=='BROKEN' for a in via.get('assumptions_at_risk') or []):return 'BROKEN'
    if unknown.get('unknown_envelope')=='CRITICAL' or frag.get('overall')=='CRITICALLY_FRAGILE':return 'FRAGILE'
    if frag.get('overall') in ('FRAGILE','WATCH') or p08.get('dominance_robustness') not in ('ROBUST','MOSTLY_ROBUST'):return 'CONDITIONALLY_RESILIENT'
    return 'RESILIENT'
def _adaptability(scenarios,via,unknown):
    s=scenarios.get('scenarios') or []
    all_inv=all(bool(x.get('invalidating_conditions')) for x in s) if s else False
    alt=any(x.get('scenario_class') in ('REVERSAL_OR_BREAK','TAIL_UNKNOWN','MECHANICAL_LIQUIDITY_DISLOCATION') for x in s)
    if all_inv and alt:return 'ADAPTIVE'
    if s:return 'CONSTRAINED'
    return 'UNKNOWN'
def run(p08,p03,kernel=None,semantic_bundle=None,event_context=None,now=None):
    t0=time.perf_counter();tn=time.perf_counter();nonlin=nonlin_eval(p08,p03,event_context);nonlin_ms=(time.perf_counter()-tn)*1000;tu=time.perf_counter();unknown=unknown_eval(p08,p03,event_context);tail_ms=(time.perf_counter()-tu)*1000;ts=time.perf_counter();scenarios=scenario_build(p08,p03,event_context,unknown,nonlin);scenario_ms=(time.perf_counter()-ts)*1000;tf=time.perf_counter();frag=frag_eval(p08,p03,kernel,semantic_bundle,event_context,unknown,scenarios);frag_ms=(time.perf_counter()-tf)*1000;tv=time.perf_counter();via=via_eval(p08,p03,event_context);via_ms=(time.perf_counter()-tv)*1000;to=time.perf_counter();overlay=overlay_eval(p08,frag,unknown,scenarios,nonlin);overlay_ms=(time.perf_counter()-to)*1000;res=_resilience(p08,frag,unknown,scenarios,via);adapt=_adaptability(scenarios,via,unknown)
    return {'record_type':'AD_V31_R03_PERSPECTIVE_STATE','schema_version':'1.0.0','phase':'AD-V3.1-R03','version':'3.1.3-antifragile-perspective','perspective_id':stable_id('R03PER',{'p08':p08.get('decision_id'),'scenarios':[x['scenario_id'] for x in scenarios['scenarios']],'overlay':overlay['overlay'],'t':p08.get('generated_at_utc')}),'generated_at_utc':iso(now),'horizon':p08.get('horizon') or p03.get('horizon'),'canonical_direction':p08.get('causal_direction'),'scenario_packet':scenarios,'via_negativa':via,'fragility_map':frag,'nonlinearity':nonlin,'unknown_state':unknown,'thesis_resilience':res,'research_adaptability':adapt,'narrative_lock_risk':adapt!='ADAPTIVE','perspective_overlay':overlay,'final_permission':overlay['post_overlay_permission'],'final_edge':overlay['post_overlay_edge'],'audit':{'perspective_only':True,'direction_unchanged':True,'no_new_causal_root':True,'no_probability':True,'tail_is_not_prediction':True,'stress_is_not_forecast':True,'monotonic_permission_defense':True,'internet_access':False,'llm_scenario_authority':False},'timing_ms':{'scenario_engine_ms':round(scenario_ms,3),'fragility_engine_ms':round(frag_ms,3),'via_negativa_ms':round(via_ms,3),'nonlinearity_ms':round(nonlin_ms,3),'tail_engine_ms':round(tail_ms,3),'overlay_ms':round(overlay_ms,3),'total_r03_ms':round((time.perf_counter()-t0)*1000,3)}}

def fail_closed(p08,error='R03_RUNTIME_FAILURE'):
    pre=p08.get('permission_candidate') or 'WAIT';edge=p08.get('edge_state','NO_EDGE')
    return {'record_type':'AD_V31_R03_PERSPECTIVE_STATE','schema_version':'1.0.0','phase':'AD-V3.1-R03','version':'3.1.3-antifragile-perspective','canonical_direction':p08.get('causal_direction'),'scenario_packet':{'scenarios':[],'scenario_count':0,'bounded':True},'via_negativa':{},'fragility_map':{'dimensions':{},'overall':'UNKNOWN','largest_dimensions':[]},'nonlinearity':{'state':'UNKNOWN_NONLINEARITY','pathways':[]},'unknown_state':{'unknown_envelope':'CRITICAL','primary_reasons':[error],'epistemic_shock':True,'tail_exposure':{},'tail_is_not_probability':True},'thesis_resilience':'UNKNOWN','research_adaptability':'UNKNOWN','narrative_lock_risk':True,'perspective_overlay':{'overlay':'FORCE_WAIT','pre_overlay_permission':pre,'post_overlay_permission':'WAIT','pre_overlay_edge':edge,'post_overlay_edge':'LOW_EDGE' if edge=='ACTIONABLE_EDGE' else edge,'reasons':[error],'authority_upgraded':False},'final_permission':'WAIT','final_edge':'LOW_EDGE' if edge=='ACTIONABLE_EDGE' else edge,'audit':{'perspective_only':True,'direction_unchanged':True,'fail_closed':True,'no_probability':True}}
