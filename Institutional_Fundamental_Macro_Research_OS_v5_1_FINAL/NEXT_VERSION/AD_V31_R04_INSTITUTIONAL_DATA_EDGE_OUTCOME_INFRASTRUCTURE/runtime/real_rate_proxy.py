from __future__ import annotations
from .common import PHASE,load_json,parse_dt,iso

def build(nominal,inflation,now=None):
    pol=load_json(PHASE/'config/real_rate_proxy_policy.json',{}) or {}
    if not nominal or not inflation:return {'state':'UNAVAILABLE_COMPONENT_GAP','identity':'INTRADAY_REAL_RATE_PROXY','causal_fact_authority':False}
    nt=parse_dt(nominal.get('economic_time'));it=parse_dt(inflation.get('economic_time'))
    if not nt or not it:return {'state':'UNAVAILABLE_TIMESTAMP','identity':'INTRADAY_REAL_RATE_PROXY','causal_fact_authority':False}
    mismatch=abs((nt-it).total_seconds())/60
    maxm=float(pol.get('max_component_timestamp_mismatch_minutes',15))
    if mismatch>maxm:return {'state':'STALE_COMPONENT_MISMATCH','identity':'INTRADAY_REAL_RATE_PROXY','component_mismatch_minutes':mismatch,'causal_fact_authority':False}
    if not isinstance(nominal.get('value'),(int,float)) or not isinstance(inflation.get('value'),(int,float)):
        return {'state':'UNAVAILABLE_COMPONENT_VALUE','identity':'INTRADAY_REAL_RATE_PROXY','causal_fact_authority':False}
    return {'state':'HEALTHY_PROXY','identity':'INTRADAY_REAL_RATE_PROXY','value':float(nominal['value'])-float(inflation['value']),'unit':'PERCENT','formula_version':pol.get('formula_version'),'component_mismatch_minutes':mismatch,'economic_time':iso(max(nt,it)),'components':[nominal.get('provider_id'),inflation.get('provider_id')],'directness':'DERIVED_PROXY','official_real_yield':False,'causal_fact_authority':False}
