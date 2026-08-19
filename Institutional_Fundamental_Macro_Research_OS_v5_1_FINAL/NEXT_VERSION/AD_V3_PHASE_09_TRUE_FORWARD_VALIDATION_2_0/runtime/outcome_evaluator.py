from __future__ import annotations
from .common import cfg,parse_dt,iso,canonical_hash,stable_id
from .outcome_data import compatible
from .permission_evaluator import evaluate as eval_permission

def neutral_band(pred):
    h=cfg('horizon_evaluation_policy.json')['horizons'][pred['horizon']]; floor=float(h['neutral_band_min_return']); vr=pred.get('volatility_reference')
    if isinstance(vr,(int,float)) and vr>0:return max(floor,float(vr)*0.15)
    return floor

def select_window(pred,observations):
    t0=parse_dt(pred['precommit_time']); mt=parse_dt(pred['maturity_time']); hp=cfg('horizon_evaluation_policy.json')['horizons'][pred['horizon']]; tol=float(hp['terminal_tolerance_minutes'])*60
    same=[o for o in observations if compatible(pred,o) and parse_dt(o.get('observed_at_utc'))]
    path=[o for o in same if t0<=parse_dt(o['observed_at_utc'])<=mt]
    terminal_candidates=[o for o in same if abs((parse_dt(o['observed_at_utc'])-mt).total_seconds())<=tol]
    terminal=min(terminal_candidates,key=lambda o:(abs((parse_dt(o['observed_at_utc'])-mt).total_seconds()), 0 if parse_dt(o['observed_at_utc'])<=mt else 1, o.get('observed_at_utc',''), o.get('provider_id') or o.get('source_id') or '')) if terminal_candidates else None
    return path,terminal


def _event_exposure(pred):
    t0=parse_dt(pred.get('precommit_time')); mt=parse_dt(pred.get('maturity_time')); events=((pred.get('event_context') or {}).get('events') or [])
    exposed=[]
    for e in events:
        et=parse_dt(e.get('event_time') or e.get('timestamp') or e.get('scheduled_at')) if isinstance(e,dict) else None
        if et and t0 and mt and t0 < et <= mt: exposed.append(e)
    return ('EVENT_EXPOSED' if exposed else 'EVENT_FREE'),exposed

def evaluate_prediction(pred,observations,evaluation_time=None,event_exposure=None):
    path,terminal=select_window(pred,observations); t0v=float((pred.get('price_anchor') or {}).get('value')) if pred.get('price_anchor') else None
    if terminal is None or t0v in (None,0):return None
    tv=float(terminal['value']); ret=(tv-t0v)/t0v; band=neutral_band(pred); direction=pred.get('causal_direction')
    if direction not in ('BULLISH_GOLD','BEARISH_GOLD'):dout='UNRESOLVED'
    elif abs(ret)<=band:dout='NEUTRAL_BAND'
    elif (direction=='BULLISH_GOLD' and ret>0) or (direction=='BEARISH_GOLD' and ret<0):dout='ALIGNED'
    else:dout='OPPOSED'
    h=cfg('horizon_evaluation_policy.json')['horizons'][pred['horizon']]; path_ok=len(path)>=int(h['path_min_points']); mfe=mae=None;ttmfe=ttmae=None;quality='UNAVAILABLE'; coverage={'expected_min_points':int(h['path_min_points']),'actual_points':len(path),'path_metric_authority':'AVAILABLE' if path_ok else 'UNAVAILABLE','path_coverage_state':'FULL' if path_ok else ('PARTIAL' if len(path)>1 else 'UNAVAILABLE'),'granularity':next((o.get('metadata',{}).get('resolution') for o in path if isinstance(o.get('metadata'),dict) and o.get('metadata',{}).get('resolution')),None)}
    if path_ok and direction in ('BULLISH_GOLD','BEARISH_GOLD'):
        vals=[(parse_dt(o['observed_at_utc']),float(o['value'])) for o in path]
        directed=[((v-t0v)/t0v if direction=='BULLISH_GOLD' else (t0v-v)/t0v,t) for t,v in vals]
        fav=max(directed,key=lambda x:x[0]); adv=min(directed,key=lambda x:x[0]); mfe=max(0.0,fav[0]);mae=max(0.0,-adv[0]);ttmfe=(fav[1]-parse_dt(pred['precommit_time'])).total_seconds()/60;ttmae=(adv[1]-parse_dt(pred['precommit_time'])).total_seconds()/60
        pp=cfg('permission_evaluation_policy.json'); mf=pp['meaningful_favorable_band_multiple']*band;cf=pp['clean_favorable_band_multiple']*band;aa=pp['acceptable_adverse_band_multiple']*band;sa=pp['severe_adverse_band_multiple']*band
        if mfe>=cf and mae<=band:quality='CLEAN'
        elif mfe>=mf and mae<=aa:quality='ACCEPTABLE'
        elif mfe>=mf and mae>aa:quality='CHOPPY'
        elif mae>=sa and mfe<mf:quality='ADVERSE'
        else:quality='NO_MEANINGFUL_EDGE'
    exposure,exposed_events=_event_exposure(pred) if event_exposure is None else (event_exposure,[])
    metrics={'terminal_return':ret,'neutral_band_return':band,'direction_outcome':dout,'mfe_return':mfe,'mae_return':mae,'time_to_mfe_minutes':ttmfe,'time_to_mae_minutes':ttmae,'path_quality':quality,'path_coverage':coverage}
    pe=eval_permission(pred,metrics); out={'record_type':'AD_V3_P09_FORWARD_OUTCOME','schema_version':'1.0.0','prediction_id':pred['prediction_id'],'episode_id':pred['episode_id'],'cohort_id':pred['cohort_id'],'evaluation_time':iso(parse_dt(evaluation_time)) if evaluation_time else iso(),'maturity_time':pred['maturity_time'],'terminal_observation':terminal,'terminal_return':ret,'neutral_band_return':band,'direction_outcome':dout,'mfe_return':mfe,'mae_return':mae,'time_to_mfe_minutes':ttmfe,'time_to_mae_minutes':ttmae,'path_quality':quality,'path_coverage':coverage,'permission_outcome':pe['permission_outcome'],'wait_outcome':pe['wait_outcome'],'event_exposure':exposure,'exposed_events':exposed_events,'policy_versions':pred.get('policy_versions'),'outcome_source_predetermined':True,'prediction_rewritten':False,'outcome_acquisition_mode':terminal.get('outcome_acquisition_mode') or 'LIVE_CAPTURED','outcome_provider_id':terminal.get('provider_id') or terminal.get('source_id'),'terminal_distance_seconds':abs((parse_dt(terminal['observed_at_utc'])-parse_dt(pred['maturity_time'])).total_seconds())}
    out['evaluation_hash']=canonical_hash(out);out['outcome_id']=stable_id('P09OUT',out);return out
