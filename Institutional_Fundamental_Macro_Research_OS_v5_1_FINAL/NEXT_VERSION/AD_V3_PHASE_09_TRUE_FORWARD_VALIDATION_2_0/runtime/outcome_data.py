from __future__ import annotations
from .common import stable_id,parse_dt,iso,canonical_hash

def observation_from_anchor(anchor):
    if not anchor or not isinstance(anchor.get('value'),(int,float)):return None
    t=anchor.get('economic_marker') or anchor.get('event_time') or anchor.get('published_at') or anchor.get('retrieved_at')
    if not parse_dt(t):return None
    obj={'record_type':'AD_V3_P09_MARKET_OBSERVATION','observed_at_utc':iso(parse_dt(t)),'value':float(anchor['value']),'source_fact_id':anchor.get('source_fact_id'),'source_id':anchor.get('source_id'),'instrument_key':anchor.get('instrument_key'),'anchor_kind':anchor.get('anchor_kind'),'proxy_for_xauusd':bool(anchor.get('proxy_for_xauusd')),'outcome_evaluation_only':True,'causal_direction_authority':False}
    obj['observation_id']=anchor.get('observation_id') or stable_id('P09PX',obj);return obj

def add_observation(state,obs):
    if not obs:return False
    old=next((x for x in state['market_observations'] if x.get('observation_id')==obs['observation_id']),None)
    if old:
        if canonical_hash(old)!=canonical_hash(obs):raise RuntimeError('P09_MARKET_OBSERVATION_MUTATION')
        return False
    state['market_observations'].append(obs);state['market_observations'].sort(key=lambda x:x.get('observed_at_utc',''));return True

def compatible(pred,o):
    pa=pred.get('price_anchor') or {}
    if not o:return False
    if pa.get('source_fact_id') and o.get('source_fact_id')!=pa.get('source_fact_id'):return False
    if pa.get('source_id') and o.get('source_id')!=pa.get('source_id'):return False
    if pa.get('instrument_key') and o.get('instrument_key') and o.get('instrument_key')!=pa.get('instrument_key'):return False
    return True
