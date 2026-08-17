from __future__ import annotations

def evaluate(p03,promotion_state):
    dec=p03.get('shadow_decision') or {}; q=p03.get('model_quality') or {}; trans=p03.get('price_transmission') or {}; mech=(p03.get('pressure_planes') or {}).get('mechanical_forced') or {}
    direction=dec.get('direction_candidate','UNKNOWN'); blockers=list(dec.get('blockers') or [])
    edge='ABSENT' if direction in ('UNKNOWN','MIXED') else 'UNCERTAIN' if q.get('model_completeness') in ('LOW','INVALID') or q.get('missing_driver_risk') in ('HIGH','MEDIUM') else 'PRESENT'
    candidate=dec.get('action_candidate','WAIT')
    if direction in ('UNKNOWN','MIXED') or q.get('model_completeness') in ('LOW','INVALID') or q.get('missing_driver_risk')=='HIGH' or trans.get('state')=='NEGATIVE': candidate='WAIT'
    if mech.get('strength') in ('MEDIUM','HIGH') and mech.get('direction') in ('BULLISH_GOLD','BEARISH_GOLD') and direction in ('BULLISH_GOLD','BEARISH_GOLD') and mech.get('direction')!=direction: candidate='WAIT'; blockers.append('MECHANICAL_PRESSURE_OPPOSES')
    prod=promotion_state.get('state')=='PRODUCTION_V3'
    official=candidate if prod else 'NO_AUTHORITY'
    return {'direction':direction,'edge_state':edge,'research_action_candidate':candidate,'official_permission':official,'production_mode':prod,'blockers':sorted(set(blockers)),'direction_is_not_edge':True,'edge_is_not_permission':True,'trade_execution_authority':False}
