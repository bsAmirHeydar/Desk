from __future__ import annotations

def price_transmission(rows, causal_direction):
    prices=[r for r in rows if r.get('role')=='TARGET_PRICE_RESPONSE' and r.get('resolution')=='RESOLVED']
    if causal_direction not in ('BULLISH_GOLD','BEARISH_GOLD') or not prices:
        return {'state':'UNTESTED','price_effects':[{'fact_id':r['fact_id'],'effect':r.get('effect_on_gold')} for r in prices],'causal_pressure_changed':False}
    effects=[r.get('effect_on_gold') for r in prices if r.get('effect_on_gold') in ('BULLISH_GOLD','BEARISH_GOLD')]
    if not effects: return {'state':'UNTESTED','price_effects':[],'causal_pressure_changed':False}
    aligned=any(x==causal_direction for x in effects); opposite=any(x!=causal_direction for x in effects)
    state='CONFLICTED' if aligned and opposite else 'ALIGNED' if aligned else 'NEGATIVE'
    return {'state':state,'price_effects':[{'fact_id':r['fact_id'],'effect':r.get('effect_on_gold')} for r in prices],'causal_pressure_changed':False}

def model_quality(coverage,causal_plane,transmission):
    if not coverage.get('analysis_may_start'): return {'model_completeness':'INVALID','missing_driver_risk':'UNKNOWN','known_gap_cap':True,'resolved_root_families':0}
    roots=causal_plane.get('root_states',[]); resolved=sum(1 for r in roots if r.get('direction') in ('BULLISH_GOLD','BEARISH_GOLD','MIXED'))
    gaps=bool(coverage.get('observability_completeness_cap_applies'))
    comp='LOW' if resolved<4 else 'MEDIUM' if resolved<10 or gaps else 'HIGH'
    if gaps and comp=='HIGH': comp='MEDIUM'
    if transmission.get('state')=='NEGATIVE' and causal_plane.get('direction') in ('BULLISH_GOLD','BEARISH_GOLD'): miss='HIGH'; comp='LOW' if comp=='MEDIUM' else comp
    elif transmission.get('state') in ('CONFLICTED','UNTESTED'): miss='MEDIUM' if gaps else 'LOW'
    else: miss='LOW'
    return {'model_completeness':comp,'missing_driver_risk':miss,'known_gap_cap':gaps,'resolved_root_families':resolved,'unknown_not_renormalized':True}
