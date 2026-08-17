from __future__ import annotations
import json
from .common import stable_id, iso


def authority_scope(row, contract):
    plane=row.get('pressure_plane')
    active=bool(row.get('horizon_active', True))
    role=row.get('role')
    if plane=='CAUSAL_FUNDAMENTAL':
        return 'CAUSAL_CURRENT_HORIZON' if active else 'CAUSAL_HORIZON_INACTIVE'
    if plane=='STRUCTURAL_CARRY':
        return 'STRUCTURAL_BACKGROUND_ONLY'
    if plane=='MECHANICAL_FORCED':
        return 'MECHANICAL_CURRENT_HORIZON' if active else 'MECHANICAL_HORIZON_INACTIVE'
    if role=='VULNERABILITY_STATE':
        return 'VULNERABILITY_CONTEXT_ONLY'
    if role in ('MECHANICAL_STATE','EVENT_STATE'):
        return 'CONTEXT_ONLY'
    return 'NON_DIRECTIONAL_CONTEXT'


def _same_value(a,b):
    if a is None or b is None:
        return None
    try:
        return json.dumps(a.get('value'),sort_keys=True,separators=(',',':'),ensure_ascii=False)==json.dumps(b.get('value'),sort_keys=True,separators=(',',':'),ensure_ascii=False)
    except Exception:
        return a.get('value')==b.get('value')


def _dependency_ids(cur):
    v=(cur or {}).get('value')
    if not isinstance(v,dict):
        return []
    deps=v.get('dependencies')
    if not isinstance(deps,list):
        return []
    out=[]
    for x in deps:
        if isinstance(x,str) and x and x not in out:
            out.append(x)
    return out


def _marker(obs):
    if not obs:
        return None
    for key in ('reference_period','event_time','published_at'):
        val=obs.get(key)
        if val not in (None,''):
            return {'kind':key,'value':str(val)}
    return None

def _comparison_diagnostics(pair):
    cur=pair.get('current')
    prev_fetch=pair.get('previous_fetch',pair.get('previous'))
    prev_econ=pair.get('previous_economic')
    status=pair.get('economic_anchor_status') or ('DISTINCT_ECONOMIC_ANCHOR_AVAILABLE' if prev_econ else 'UNKNOWN')
    return {
        'previous_fetch_value_equal':_same_value(cur,prev_fetch),
        'economic_anchor_status':status,
        'economic_comparison_available':prev_econ is not None,
        'current_economic_marker':_marker(cur),
        'previous_economic_marker':_marker(prev_econ),
        'current_previous_economic_value_equal':_same_value(cur,prev_econ) if prev_econ is not None else None,
        'fetch_equality_is_not_economic_delta':True
    }

def _dependency_evidence(fid, history_pairs, contract_map, horizon):
    pair=history_pairs.get(fid,{})
    cur=pair.get('current'); prev=pair.get('previous_fetch',pair.get('previous')); prev_econ=pair.get('previous_economic')
    c=contract_map.get(fid,{})
    active_horizons=c.get('active_horizons') or []
    active=(not active_horizons) or (horizon in active_horizons)
    return {
        'fact_id':fid,
        'role':c.get('role'),
        'pressure_plane':c.get('pressure_plane'),
        'causal_root_family':c.get('causal_root_family'),
        'horizon_active':active,
        'active_horizons':active_horizons,
        'current_observation':cur,
        'previous_observation':prev,
        'previous_fetch_observation':prev,
        'previous_economic_observation':prev_econ,
        'current_previous_value_equal':_same_value(cur,prev),
        'comparison_diagnostics':_comparison_diagnostics(pair)
    }


def build_semantic_evidence_packet(receipt, history_pairs, contract_map, coverage):
    items=[]
    row_map={r['fact_id']:r for r in receipt.get('reasoning_ledger',{}).get('rows',[])}
    horizon=receipt.get('horizon')
    acquisition_run_id=receipt.get('handoff_integrity',{}).get('acquisition_run_id')
    for req in receipt.get('semantic_adjudication_request',[]):
        fid=req['fact_id']; row=row_map.get(fid,{})
        pair=history_pairs.get(fid,{})
        cur=pair.get('current'); prev=pair.get('previous_fetch',pair.get('previous')); prev_econ=pair.get('previous_economic')
        contract=contract_map.get(fid,{})
        scope=authority_scope(row,contract)
        dep_ids=_dependency_ids(cur)
        deps=[_dependency_evidence(x,history_pairs,contract_map,horizon) for x in dep_ids]
        dep_missing=[x['fact_id'] for x in deps if x.get('current_observation') is None]
        dep_wrong_run=[x['fact_id'] for x in deps if x.get('current_observation') is not None and x['current_observation'].get('acquisition_run_id')!=acquisition_run_id]
        warnings=(cur or {}).get('warnings') or []
        items.append({
            'fact_id':fid,
            'requested_observation_id':req.get('observation_id'),
            'role':row.get('role'),
            'pressure_plane':row.get('pressure_plane'),
            'causal_root_family':row.get('causal_root_family'),
            'current_reasoning_horizon':horizon,
            'horizon_active':row.get('horizon_active',True),
            'active_horizons':row.get('active_horizons') or contract.get('active_horizons') or [],
            'authority_scope':scope,
            'may_add_to_current_causal_direction': bool(scope=='CAUSAL_CURRENT_HORIZON' and contract.get('can_add_to_session_causal_direction')),
            'current_observation':cur,
            'previous_observation':prev,
            'previous_fetch_observation':prev,
            'previous_economic_observation':prev_econ,
            'dependency_evidence':deps,
            'evidence_diagnostics':{
                'current_previous_value_equal':_same_value(cur,prev),
                'current_raw_sha_equal_previous': None if not cur or not prev else cur.get('raw_sha256')==prev.get('raw_sha256'),
                'current_warning_count':len(warnings),
                'declared_dependency_count':len(dep_ids),
                'attached_dependency_count':len(deps),
                'dependency_current_observations_complete':not dep_missing,
                'dependency_exact_acquisition_run_complete':not dep_wrong_run,
                'missing_dependency_current_fact_ids':dep_missing,
                'wrong_run_dependency_fact_ids':dep_wrong_run,
                'derived_dependency_closure_attached':bool(dep_ids),
                **_comparison_diagnostics(pair)
            },
            'required_semantic_output':req.get('required_semantic_output',[]),
            'hard_guards':{
                'exact_observation_reference_required':True,
                'proxy_strength_capped':True,
                'positioning_is_not_direction': role_is_positioning(row),
                'price_is_not_causal_pressure': role_is_price(row),
                'inactive_causal_or_mechanical_fact_cannot_affect_current_horizon': not row.get('horizon_active',True) and row.get('pressure_plane') in ('CAUSAL_FUNDAMENTAL','MECHANICAL_FORCED','REALIZED_TRANSACTION'),
                'structural_carry_has_no_session_direction_authority': row.get('pressure_plane')=='STRUCTURAL_CARRY',
                'derived_fact_requires_dependency_evidence_review': bool(dep_ids),
                'previous_fetch_is_not_previous_economic_state': True,
                'neutral_or_impulse_claim_requires_economic_or_explicit_event_evidence': True
            }
        })
    seed={'receipt_id':receipt.get('receipt_id'),'coverage':coverage.get('receipt_id'),'horizon':horizon,'items':[(x['fact_id'],x['requested_observation_id']) for x in items]}
    return {
        'record_type':'AD_V3_P03_SEMANTIC_EVIDENCE_PACKET',
        'packet_id':stable_id('P03SEMPKT',seed),
        'phase':'AD-V3-P03',
        'subject':'XAUUSD',
        'generated_at_utc':iso(),
        'causal_brain_receipt_id':receipt.get('receipt_id'),
        'p02_coverage_receipt_id':coverage.get('receipt_id'),
        'acquisition_run_id':acquisition_run_id,
        'horizon':horizon,
        'item_count':len(items),
        'items':items,
        'hard_note':'Evidence packet only. It grants no Direction or trade permission. Derived facts require attached dependency observations. Previous fetch/run is NOT previous economic state; neutral/impulse claims require a distinct economic anchor or explicit event evidence.'
    }

def role_is_positioning(row):
    return row.get('role')=='POSITIONING_STATE'

def role_is_price(row):
    return row.get('role')=='TARGET_PRICE_RESPONSE'
