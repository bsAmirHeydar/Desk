from __future__ import annotations

_HORIZON_ORDER=['MICRO_0_15M','SHORT_15_60M','SESSION_1_6H','DAILY_OPEN_TO_CLOSE','MULTI_DAY_2_10D','SWING_2_8W','CYCLICAL','STRUCTURAL']

def _current_label(horizon):
    if horizon in ('MICRO_0_15M','SHORT_15_60M'): return 'INTRADAY'
    if horizon in ('SESSION_1_6H','DAILY_OPEN_TO_CLOSE'): return 'SESSION'
    if horizon=='MULTI_DAY_2_10D': return 'MULTI_DAY'
    if horizon=='SWING_2_8W': return 'SWING'
    if horizon=='CYCLICAL': return 'CYCLICAL'
    if horizon=='STRUCTURAL': return 'STRUCTURAL'
    return 'UNKNOWN'

def _mode_persistence(mode,horizon):
    current=_current_label(horizon)
    if mode=='FED_POLICY_CURVE_IMPULSE':
        return 'MULTI_DAY' if current in ('INTRADAY','SESSION','MULTI_DAY') else current
    if mode=='REAL_YIELD_STOCK_AND_IMPULSE':
        return current
    if mode=='SUPPLY_CHANGE_INVERSE':
        return 'MULTI_DAY' if current in ('INTRADAY','SESSION','MULTI_DAY') else current
    return current

def persistence_stack(causal, contracts, horizon='SESSION_1_6H'):
    cmap={c['fact_id']:c for c in contracts}; rows=[]
    for root in causal.get('root_states',[]):
        if root.get('direction') not in ('BULLISH_GOLD','BEARISH_GOLD','MIXED'): continue
        modes=[cmap.get(fid,{}).get('reasoning_mode') for fid in root.get('evidence_fact_ids',[])]
        labels=[_mode_persistence(m,horizon) for m in modes if m]
        labels=[x for x in labels if x!='UNKNOWN']
        order=['INTRADAY','SESSION','MULTI_DAY','SWING','CYCLICAL','STRUCTURAL']
        persistence=max(labels,key=lambda x:order.index(x)) if labels else _current_label(horizon)
        rows.append({'root_id':root['root_id'],'direction':root['direction'],'persistence':persistence,'evidence_fact_ids':root.get('evidence_fact_ids',[]),'signal_horizon':horizon,'static_stock_does_not_extend_impulse_persistence':True})
    overall='UNKNOWN'
    if rows:
        order=['INTRADAY','SESSION','MULTI_DAY','SWING','CYCLICAL','STRUCTURAL']
        overall=max([x['persistence'] for x in rows],key=lambda x:order.index(x) if x in order else -1)
    return {'overall':overall,'by_root':rows,'freshness_is_not_persistence':True,'current_reasoning_horizon':horizon}

def consumption_vector(rows,causal,transaction,mechanical):
    resolved_roots=[x for x in causal.get('root_states',[]) if x.get('direction') in ('BULLISH_GOLD','BEARISH_GOLD','MIXED')]
    fed=next((r for r in rows if r['fact_id']=='FED_POLICY_PATH_PRICING'),None)
    real=[r for r in rows if r['fact_id'] in ('UST_5Y_REAL_YIELD','UST_10Y_REAL_YIELD','UST_30Y_REAL_YIELD')]
    cftc=[r for r in rows if r['fact_id'].startswith('CFTC_') and r.get('resolution')=='RESOLVED']
    narr=next((r for r in rows if r['fact_id']=='NARRATIVE_SATURATION'),None)
    causal_dir=causal.get('direction'); tx=transaction.get('direction'); mech=mechanical.get('direction')
    flow='UNKNOWN'
    if causal_dir in ('BULLISH_GOLD','BEARISH_GOLD') and tx in ('BULLISH_GOLD','BEARISH_GOLD'):
        flow='PRESENT' if causal_dir==tx else 'CONTRADICTED'
    pos='PRESENT' if any((r.get('details') or {}).get('net_change') not in (None,0) for r in cftc) else 'UNKNOWN'
    ns='UNKNOWN'
    if narr and narr.get('resolution')=='SEMANTICALLY_ADJUDICATED': ns='PRESENT' if narr.get('effect_on_gold') not in ('UNKNOWN','NO_DIRECTION') else 'PARTIAL'
    contradiction='PRESENT' if causal_dir=='MIXED' or (causal_dir in ('BULLISH_GOLD','BEARISH_GOLD') and ((tx in ('BULLISH_GOLD','BEARISH_GOLD') and tx!=causal_dir) or (mech in ('BULLISH_GOLD','BEARISH_GOLD') and mech!=causal_dir))) else ('ABSENT' if causal_dir in ('BULLISH_GOLD','BEARISH_GOLD') else 'UNKNOWN')
    reinforcement='PRESENT' if causal.get('strength') in ('MEDIUM','HIGH') and flow=='PRESENT' else 'PARTIAL' if len(resolved_roots)>=2 else 'UNKNOWN'
    fed_repricing=bool(fed and fed.get('resolution') in ('RESOLVED','SEMANTICALLY_ADJUDICATED') and fed.get('effect_on_gold') in ('BULLISH_GOLD','BEARISH_GOLD','MIXED'))
    real_repricing=any((r.get('details') or {}).get('fresh_impulse_present') for r in real)
    repricing='PRESENT' if fed_repricing else 'PARTIAL' if real_repricing else 'ABSENT' if any(r.get('resolution')=='RESOLVED' for r in real) else 'UNKNOWN'
    info='PRESENT' if len(resolved_roots)>=4 else 'PARTIAL' if resolved_roots else 'UNKNOWN'
    return {
      'information_absorption':info,
      'expectations_repricing':repricing,
      'flow_propagation':flow,'position_adjustment':pos,'narrative_saturation':ns,'time_decay':'UNKNOWN','reinforcement':reinforcement,'contradiction':contradiction,
      'scalar_percentage_forbidden':True,'price_distance_not_used':True
    }

def remaining_pressure(causal,consumption,persistence):
    d=causal.get('direction')
    if d not in ('BULLISH_GOLD','BEARISH_GOLD'): return {'state':'UNKNOWN','direction':d,'reason':'CAUSAL_DIRECTION_NOT_CLEAR'}
    if consumption.get('contradiction')=='PRESENT': return {'state':'CONTESTED','direction':d,'reason':'ACTIVE_CONTRADICTION'}
    if persistence.get('overall')=='UNKNOWN': return {'state':'PARTIAL','direction':d,'reason':'PERSISTENCE_NOT_RESOLVED'}
    return {'state':'PRESENT','direction':d,'persistence':persistence.get('overall'),'reason':'CLEAR_CAUSAL_DIRECTION_WITHOUT_ACTIVE_CONTRADICTION'}
