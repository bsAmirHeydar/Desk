from __future__ import annotations
from .common import effect_sign, rank_strength
SUCCESS={'OBSERVED_CURRENT','OBSERVED_DELAYED','LATEST_VALID','RELEASE_NOT_DUE','PUBLIC_PROXY','MODEL_DERIVED'}
_SESSION_LIKE={'MICRO_0_15M','SHORT_15_60M','SESSION_1_6H','DAILY_OPEN_TO_CLOSE'}

def quality(o):
    if not o: return 'UNKNOWN'
    st=o.get('epistemic_state'); direct=o.get('directness')
    if st in ('PRIVATE_UNOBSERVABLE','PAID_ONLY','UNKNOWN_TRUE','FETCH_FAILED','PARSE_FAILED','STALE'): return 'UNKNOWN'
    if st=='PUBLIC_PROXY' or direct=='PROXY': return 'LOW'
    if st in ('OBSERVED_DELAYED','LATEST_VALID','MODEL_DERIVED'): return 'MEDIUM'
    if st=='OBSERVED_CURRENT' and direct=='DIRECT': return 'HIGH'
    return 'MEDIUM'

def _num(o):
    v=(o or {}).get('value'); return float(v) if isinstance(v,(int,float)) else None

def _delta(cur,prev):
    a=_num(cur); b=_num(prev)
    if a is None or b is None: return None
    d=a-b
    return 0.0 if abs(d) < 1e-12 else d

def _flow_number(v):
    """Return an explicitly signed flow, never an unsigned gross level.

    Scalar positive values are ambiguous by default: holdings, withdrawals,
    imports, deliveries and activity levels are usually non-negative levels.
    They must not be treated as bullish merely because the number is > 0.
    """
    if isinstance(v,dict):
        for k in ('net','net_flow','flow_change','change','tonnes_change','holdings_change','net_purchases','net_imports','net_redemptions'):
            if isinstance(v.get(k),(int,float)): return float(v[k])
    return None

def _level_number(v):
    if isinstance(v,(int,float)): return float(v)
    if isinstance(v,dict):
        for k in ('level','holdings','shares','tonnes','imports','withdrawals','value'):
            if isinstance(v.get(k),(int,float)): return float(v[k])
    return None

def _flow_effect(contract,cur,prev):
    """Resolve flow direction only from declared semantics.

    - EXPLICIT_SIGNED_ONLY: requires a signed net/change field in the current value.
    - LEVEL_DELTA: uses change in a non-negative level versus the previous observation.
    - EXPLICIT_SIGNED_OR_LEVEL_DELTA: prefers signed field, otherwise level delta.
    - GROSS_ACTIVITY_CONTEXT: never assigns direction automatically.
    """
    sem=contract.get('flow_semantics','EXPLICIT_SIGNED_ONLY')
    if sem=='GROSS_ACTIVITY_CONTEXT':
        return None,None,'GROSS_ACTIVITY_NOT_DIRECTIONAL'
    signed=_flow_number((cur or {}).get('value'))
    if signed is not None and sem in ('EXPLICIT_SIGNED_ONLY','EXPLICIT_SIGNED_OR_LEVEL_DELTA'):
        return signed,'SIGNED_FLOW','EXPLICIT_SIGNED_FLOW'
    if sem in ('LEVEL_DELTA','EXPLICIT_SIGNED_OR_LEVEL_DELTA'):
        a=_level_number((cur or {}).get('value')); b=_level_number((prev or {}).get('value'))
        if a is None or b is None: return None,None,'FLOW_LEVEL_DELTA_UNAVAILABLE'
        d=a-b
        if abs(d)<1e-12: d=0.0
        return d,'LEVEL_DELTA','FLOW_LEVEL_DELTA'
    return None,None,'SIGNED_FLOW_UNAVAILABLE'

def auto_interpret(contract,cur,prev,horizon='SESSION_1_6H'):
    rule=contract['reasoning_mode']; fid=contract['fact_id']; q=quality(cur)
    active_horizons=contract.get('active_horizons') or []
    horizon_active=(not active_horizons) or (horizon in active_horizons)
    base={'fact_id':fid,'observation_id':(cur or {}).get('observation_id'),'role':contract['role'],'pressure_plane':contract['pressure_plane'],'causal_root_family':contract.get('causal_root_family'),'effect_on_gold':'UNKNOWN','effect_kind':'CONTEXT','strength':q,'is_additive':False,'causal_owner_id':None,'resolution':'UNRESOLVED','reason_code':rule,'details':{},'horizon_active':horizon_active,'active_horizons':active_horizons}
    if not cur: return base
    st=cur.get('epistemic_state')
    if st not in SUCCESS: base['reason_code']='EPISTEMIC_STATE_'+str(st); return base
    # Slow causal/transaction/mechanical facts may remain visible in the ledger,
    # but they cannot create current-horizon pressure when their own contract
    # says the horizon is inactive. Structural carry is intentionally separate
    # and remains available as a slow background plane.
    if (not horizon_active) and contract.get('pressure_plane') in ('CAUSAL_FUNDAMENTAL','REALIZED_TRANSACTION','MECHANICAL_FORCED'):
        base.update(effect_on_gold='NO_DIRECTION',effect_kind='HORIZON_CONTEXT',is_additive=False,resolution='ACCOUNTED_HORIZON_INACTIVE',reason_code='HORIZON_INACTIVE_FOR_CURRENT_REASONING')
        base['details']={'current_horizon':horizon,'active_horizons':active_horizons,'cannot_contribute_current_horizon_pressure':True}
        return base
    if rule=='REAL_YIELD_STOCK_AND_IMPULSE':
        v=_num(cur); d=_delta(cur,prev)
        if v is None: return base
        stock='BEARISH_GOLD' if v>0 else 'BULLISH_GOLD' if v<0 else 'NEUTRAL'
        impulse='BULLISH_GOLD' if d is not None and d<0 else 'BEARISH_GOLD' if d is not None and d>0 else 'NEUTRAL' if d==0 else 'UNKNOWN'
        combined=stock if impulse in ('UNKNOWN','NEUTRAL') else impulse if stock=='NEUTRAL' else stock if stock==impulse else 'MIXED'
        session_like=horizon in _SESSION_LIKE
        # Directional pressure is marginal. A static positive/negative real-yield
        # level is a background carry/headwind state and must not re-fire a
        # fresh session Direction every run.
        if session_like:
            if impulse=='UNKNOWN':
                eff='UNKNOWN'; add=False; resolution='UNRESOLVED'; kind='IMPULSE'
            elif impulse=='NEUTRAL':
                eff='NEUTRAL'; add=False; resolution='RESOLVED'; kind='IMPULSE'
            else:
                eff=combined; add=True; resolution='RESOLVED'; kind='IMPULSE' if combined==impulse else 'STOCK_IMPULSE_CONFLICT'
        elif horizon in ('MULTI_DAY_2_10D','SWING_2_8W'):
            eff=combined; add=eff in ('BULLISH_GOLD','BEARISH_GOLD','MIXED'); resolution='RESOLVED'; kind='STOCK_AND_IMPULSE'
        else:
            eff=stock; add=eff in ('BULLISH_GOLD','BEARISH_GOLD'); resolution='RESOLVED'; kind='STOCK'
        base.update(effect_on_gold=eff,effect_kind=kind,is_additive=add,causal_owner_id=contract.get('causal_root_family') if add else None,resolution=resolution)
        base['details']={'level':v,'delta':d,'background_bias':stock,'stock_effect':stock,'impulse_effect':impulse,'combined_state':combined,'directional_pressure_effect':eff,'fresh_impulse_present':impulse in ('BULLISH_GOLD','BEARISH_GOLD'),'horizon_semantics':horizon,'static_stock_cannot_refire_session_direction':session_like}
        return base
    if rule=='FED_POLICY_CURVE_IMPULSE':
        def rates(o):
            v=(o or {}).get('value'); rows=v.get('fed_funds_futures_curve') if isinstance(v,dict) else None
            if not isinstance(rows,list): return []
            return [float(x['implied_average_rate']) for x in rows[:3] if isinstance(x.get('implied_average_rate'),(int,float))]
        a=rates(cur); b=rates(prev)
        if not a or not b: return base
        da=sum(a)/len(a)-sum(b)/len(b)
        if abs(da) < 1e-12: da=0.0
        eff='BULLISH_GOLD' if da<0 else 'BEARISH_GOLD' if da>0 else 'NEUTRAL'
        add=eff in ('BULLISH_GOLD','BEARISH_GOLD')
        base.update(effect_on_gold=eff,effect_kind='IMPULSE',is_additive=add,causal_owner_id=contract.get('causal_root_family') if add else None,resolution='RESOLVED')
        base['details']={'near_curve_change':da,'meeting_probabilities_inferred':False,'fresh_impulse_present':add,'horizon_semantics':horizon}
        return base
    if rule=='USD_INDEX_IMPULSE_NONADDITIVE':
        d=_delta(cur,prev)
        if d is None: return base
        eff='BULLISH_GOLD' if d<0 else 'BEARISH_GOLD' if d>0 else 'NEUTRAL'
        base.update(effect_on_gold=eff,effect_kind='CONFIRMATION',is_additive=False,resolution='RESOLVED'); base['details']={'delta':d}; return base
    if rule=='PRICE_RESPONSE_DELTA_ONLY':
        d=_delta(cur,prev)
        if d is None: return base
        eff='BULLISH_GOLD' if d>0 else 'BEARISH_GOLD' if d<0 else 'NEUTRAL'
        base.update(effect_on_gold=eff,effect_kind='CONFIRMATION',is_additive=False,resolution='RESOLVED'); base['details']={'delta':d,'cannot_modify_causal_pressure':True}; return base
    if rule=='POSITIVE_FLOW_DIRECTION':
        x,sem,why=_flow_effect(contract,cur,prev)
        if x is None:
            if why=='GROSS_ACTIVITY_NOT_DIRECTIONAL':
                base.update(effect_on_gold='NO_DIRECTION',effect_kind='ACTIVITY_LEVEL',is_additive=False,resolution='ACCOUNTED_NON_DIRECTIONAL',reason_code=why)
                base['details']={'flow_semantics':contract.get('flow_semantics','EXPLICIT_SIGNED_ONLY'),'gross_positive_level_not_direction':True}
            else:
                base['reason_code']=why; base['details']={'flow_semantics':contract.get('flow_semantics','EXPLICIT_SIGNED_ONLY')}
            return base
        eff='BULLISH_GOLD' if x>0 else 'BEARISH_GOLD' if x<0 else 'NEUTRAL'
        base.update(effect_on_gold=eff,effect_kind='CONFIRMATION',is_additive=False,resolution='RESOLVED',reason_code=why)
        base['details']={'flow_value':x,'flow_semantics':sem,'absolute_positive_level_not_used_as_direction':True}
        return base
    if rule=='POSITIVE_OFFICIAL_DEMAND':
        x=_flow_number(cur.get('value'))
        if x is None: return base
        eff='BULLISH_GOLD' if x>0 else 'BEARISH_GOLD' if x<0 else 'NEUTRAL'
        base.update(effect_on_gold=eff,effect_kind='STOCK',is_additive=False,causal_owner_id=contract.get('causal_root_family'),resolution='RESOLVED'); base['details']={'structural_value':x,'session_direction_authority':False}; return base
    if rule=='SUPPLY_CHANGE_INVERSE':
        d=_delta(cur,prev)
        if d is None: return base
        eff='BEARISH_GOLD' if d>0 else 'BULLISH_GOLD' if d<0 else 'NEUTRAL'
        add=contract['pressure_plane']=='CAUSAL_FUNDAMENTAL' and contract['can_add_to_session_causal_direction'] and eff in ('BULLISH_GOLD','BEARISH_GOLD')
        base.update(effect_on_gold=eff,effect_kind='IMPULSE',is_additive=add,causal_owner_id=contract.get('causal_root_family') if add else None,resolution='RESOLVED'); base['details']={'delta':d,'fresh_impulse_present':add,'horizon_semantics':horizon}; return base
    if rule=='CFTC_POSITIONING_CONTEXT':
        v=cur.get('value')
        if not isinstance(v,dict): return base
        net=v.get('net')
        pnet=((prev or {}).get('value') or {}).get('net') if isinstance((prev or {}).get('value'),dict) else None
        state='LONG' if isinstance(net,(int,float)) and net>0 else 'SHORT' if isinstance(net,(int,float)) and net<0 else 'FLAT' if net==0 else 'UNKNOWN'
        change=(net-pnet) if isinstance(net,(int,float)) and isinstance(pnet,(int,float)) else None
        base.update(effect_on_gold='NO_DIRECTION',effect_kind='VULNERABILITY',is_additive=False,resolution='RESOLVED'); base['details']={'position_state':state,'net':net,'net_change':change,'not_live_flow':True}; return base
    if rule=='EVENT_SHOCK_NONADDITIVE':
        base.update(effect_on_gold='NO_DIRECTION',effect_kind='SHOCK',is_additive=False,resolution='ACCOUNTED_NON_DIRECTIONAL'); return base
    if rule in ('NO_AUTOMATIC_DIRECTION','STRUCTURAL_PRIOR_ONLY','MECHANICAL_SEMANTIC','SEMANTIC_ADJUDICATION_REQUIRED'):
        base['resolution']='ACCOUNTED_REQUIRES_SEMANTIC' if rule!='NO_AUTOMATIC_DIRECTION' else 'ACCOUNTED_NON_DIRECTIONAL'
        base['effect_on_gold']='NO_DIRECTION' if rule=='NO_AUTOMATIC_DIRECTION' else 'UNKNOWN'
        return base
    return base

def apply_bundle(row,bundle_item,contract,cur):
    if not bundle_item: return row
    if bundle_item.get('observation_id')!=(cur or {}).get('observation_id') or bundle_item.get('fact_id')!=contract['fact_id']:
        row=dict(row); row['adjudication_error']='OBSERVATION_REFERENCE_MISMATCH'; return row
    if (not row.get('horizon_active',True)) and contract.get('pressure_plane') in ('CAUSAL_FUNDAMENTAL','REALIZED_TRANSACTION','MECHANICAL_FORCED'):
        row=dict(row); row['adjudication_error']='HORIZON_AUTHORITY_VIOLATION'; return row
    add=bool(bundle_item.get('is_additive'))
    if add and not contract.get('can_add_to_session_causal_direction'):
        row=dict(row); row['adjudication_error']='ADDITIVE_AUTHORITY_VIOLATION'; return row
    owner=bundle_item.get('causal_owner_id')
    if add and owner!=contract.get('causal_root_family'):
        row=dict(row); row['adjudication_error']='CAUSAL_OWNER_MISMATCH'; return row
    requested=bundle_item.get('strength','UNKNOWN'); evidence_cap=quality(cur)
    strength=requested if rank_strength(requested)<=rank_strength(evidence_cap) else evidence_cap
    row=dict(row); row.update(effect_on_gold=bundle_item.get('effect_on_gold','UNKNOWN'),effect_kind=bundle_item.get('effect_kind','CONTEXT'),strength=strength,is_additive=add,causal_owner_id=owner if add else None,resolution='SEMANTICALLY_ADJUDICATED',rationale_summary=bundle_item.get('rationale_summary',''))
    if strength!=requested: row['strength_capped_by_evidence']=evidence_cap
    return row
