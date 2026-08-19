from __future__ import annotations
from .common import cfg

def _dom_root(p08):
    rid=p08.get('dominant_root');return next((r for r in p08.get('calibrated_roots') or [] if r.get('root_id')==rid),None)

def evaluate(p08,p03,event_context=None):
    dom=_dom_root(p08);direction=p08.get('causal_direction','UNKNOWN');health=(dom or {}).get('root_health') or {};opp=list(p08.get('opposing_roots') or []);breakers=[]
    for x in p08.get('invalidation_conditions') or []:breakers.append({'breaker_id':x,'source':'P08_INVALIDATION','state':'ARMED'})
    if opp:breakers.append({'breaker_id':'OPPOSING_PRIMARY_ROOT_ACTIVATES','source':'OPPOSING_ROOTS','roots':opp,'state':'WATCH'})
    if health.get('state') in ('DEGRADED','CRITICAL_GAP'):breakers.append({'breaker_id':'DOMINANT_ROOT_HEALTH_COLLAPSE','source':'ROOT_HEALTH','state':'FRAGILE' if health.get('state')=='DEGRADED' else 'BROKEN'})
    if p08.get('model_sensitivity')=='HIGH':breakers.append({'breaker_id':'MODEL_ASSUMPTION_INSTABILITY','source':'R02_MODEL_SENSITIVITY','state':'FRAGILE'})
    if p08.get('missing_driver_risk') in ('ELEVATED','HIGH'):breakers.append({'breaker_id':'OUTSIDE_MODEL_DRIVER','source':'MISSING_DRIVER_RISK','state':'WATCH'})
    events=((event_context or {}).get('events') or []);up=[]
    for e in events:
        st=str(e.get('status','UPCOMING')).upper()
        if st in ('UPCOMING','ARMED'):up.append({'event_id':e.get('event_id') or e.get('event') or 'EVENT','event_time':e.get('event_time'),'materiality':e.get('materiality'),'state':'ARMED'})
    assumptions=[]
    if dom:
        hs=health.get('state','UNKNOWN');as_state='STABLE' if hs=='HEALTHY' else 'WATCH' if hs=='PARTIAL' else 'FRAGILE' if hs=='DEGRADED' else 'BROKEN' if hs=='CRITICAL_GAP' else 'UNKNOWN'
        assumptions.append({'assumption':'DOMINANT_ROOT_REMAINS_HEALTHY','root_id':dom.get('root_id'),'state':as_state})
        direct=health.get('directness_state','UNKNOWN');assumptions.append({'assumption':'EVIDENCE_DIRECTNESS_REMAINS_ADEQUATE','root_id':dom.get('root_id'),'state':'FRAGILE' if direct in ('PROXY_ONLY','PROXY_HEAVY') else 'STABLE' if direct in ('DIRECT','MIXED') else 'UNKNOWN'})
    assumptions.append({'assumption':'CURRENT_REGIME_PERSISTS','state':'WATCH' if p08.get('regime_context') not in (None,'NORMAL') else 'STABLE'})
    trans=(p03.get('price_transmission') or {}).get('state','UNKNOWN');assumptions.append({'assumption':'PRICE_TRANSMISSION_CONFLICT_IS_TEMPORARY','state':'FRAGILE' if trans in ('NEGATIVE','CONFLICTED') else 'STABLE' if trans not in ('UNKNOWN','UNTESTED') else 'UNKNOWN'})
    missing=[];gaps=[]
    if dom:
        for g in health.get('critical_evidence_missing') or []:gaps.append({'root_id':dom.get('root_id'),'missing_group':g})
        if health.get('magnitude_coverage_share',1)<.5:missing.append('DOMINANT_ROOT_MAGNITUDE_COVERAGE_LOW')
        if health.get('directness_state') in ('PROXY_HEAVY','PROXY_ONLY'):missing.append('DIRECT_EVIDENCE_CONFIRMATION')
    contradictions=[]
    if p08.get('contradiction') not in (None,'NONE','MINOR_OFFSET'):contradictions.append(p08.get('contradiction'))
    return {'thesis_direction':direction,'thesis_breakers':breakers,'assumptions_at_risk':assumptions,'missing_confirmations':missing,'critical_gaps':gaps,'contradictory_evidence':contradictions,'upcoming_discontinuities':up,'price_move_alone_is_not_breaker':True}
