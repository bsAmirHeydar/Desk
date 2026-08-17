from __future__ import annotations

def shadow_decision(causal,transaction,mechanical,structural,transmission,quality):
    direction=causal.get('direction','UNKNOWN')
    action='WAIT'; blockers=[]
    if direction in ('MIXED','UNKNOWN'): blockers.append('CAUSAL_DIRECTION_NOT_CLEAR')
    if quality.get('model_completeness') in ('LOW','INVALID'): blockers.append('MODEL_COMPLETENESS_INSUFFICIENT')
    if quality.get('missing_driver_risk')=='HIGH': blockers.append('MISSING_DRIVER_RISK_HIGH')
    if transmission.get('state')=='NEGATIVE': blockers.append('NEGATIVE_PRICE_TRANSMISSION')
    opp='BEARISH_GOLD' if direction=='BULLISH_GOLD' else 'BULLISH_GOLD' if direction=='BEARISH_GOLD' else None
    if opp and transaction.get('direction')==opp: blockers.append('TRANSACTION_PRESSURE_OPPOSES')
    if opp and mechanical.get('direction')==opp and mechanical.get('strength') in ('MEDIUM','HIGH'): blockers.append('MECHANICAL_PRESSURE_OPPOSES')
    if not blockers and direction=='BULLISH_GOLD': action='BUY_CANDIDATE'
    elif not blockers and direction=='BEARISH_GOLD': action='SELL_CANDIDATE'
    return {'direction_candidate':direction,'action_candidate':action,'official_permission':'NO_AUTHORITY','production_authority':False,'blockers':blockers,'structural_bias':structural.get('direction','UNKNOWN'),'transaction_confirmation':transaction.get('direction','UNKNOWN'),'mechanical_path_pressure':mechanical.get('direction','UNKNOWN')}
