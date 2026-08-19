from __future__ import annotations
from pathlib import Path
from datetime import timedelta
from .common import PHASE,load_json,parse_dt,iso
from .pit_store import query,put
from .historical_market_recovery import normalize_row
from .provider_registry import get as provider_capability

def policy():return load_json(PHASE/'config/outcome_provider_policy.json',{}) or {}
def default_store(state_root=None):
    if state_root:return Path(state_root)/'r04_pit.sqlite3'
    return PHASE/'artifacts/state/r04_pit.sqlite3'

def _window(pred):
    mt=parse_dt(pred.get('maturity_time'));t0=parse_dt(pred.get('precommit_time'))
    hp=load_json(PHASE.parent/'AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0/config/horizon_evaluation_policy.json',{})['horizons'][pred['horizon']]
    tol=float(hp['terminal_tolerance_minutes'])
    return t0,mt,tol,mt+timedelta(minutes=tol) if mt else None

def _try_network(pred,state_root,series,t0,end):
    if series!='XAUUSD_SPOT_REFERENCE':return [],[]
    from AD_V31_R04_INSTITUTIONAL_DATA_EDGE_OUTCOME_INFRASTRUCTURE.providers.registry import instantiate
    attempts=[]
    for pid in policy().get('provider_selection_order',['GOLDPRICEDEV_XAU_BARS','TWELVEDATA_XAUUSD']):
        cap=provider_capability(pid) or {}
        if not cap.get('authorized_for_use'):
            attempts.append({'provider_id':pid,'state':'NOT_CONFIGURED_OR_ENTITLED'});continue
        try:
            adapter=instantiate(pid);bars=adapter.fetch_historical(t0,end,'1min')
            for b in bars:put(default_store(state_root),b)
            attempts.append({'provider_id':pid,'state':'PASS','records':len(bars)})
        except Exception as e:
            attempts.append({'provider_id':pid,'state':'FAIL','error':type(e).__name__+':'+str(e)[:160]})
    return [],attempts

def _nearest(rows,target,tol_minutes):
    t=parse_dt(target);valid=[r for r in rows if parse_dt(r.get('economic_time')) and abs((parse_dt(r['economic_time'])-t).total_seconds())<=tol_minutes*60]
    if not valid:return None
    return min(valid,key=lambda r:(abs((parse_dt(r['economic_time'])-t).total_seconds()),0 if parse_dt(r['economic_time'])<=t else 1,r['economic_time'],r['provider_id']))

def _select_provider_rows(rows,mt,tol):
    by={}
    for r in rows:by.setdefault(r['provider_id'],[]).append(r)
    terminals={pid:_nearest(rr,mt,tol) for pid,rr in by.items()};terminals={k:v for k,v in terminals.items() if v}
    if not terminals:return None,[],'NO_VALID_TERMINAL'
    vals=list(terminals.items());conf=float(policy().get('provider_conflict_relative_tolerance',0.0005))
    for i,(pa,a) in enumerate(vals):
        for pb,b in vals[i+1:]:
            denom=max(abs(float(a['value'])),abs(float(b['value'])),1e-9)
            if abs(float(a['value'])-float(b['value']))/denom>conf:
                return None,[],'OUTCOME_DATA_CONFLICT'
    order=policy().get('provider_selection_order',[])
    chosen=next((pid for pid in order if pid in terminals),None) or sorted(terminals)[0]
    return chosen,sorted(by[chosen],key=lambda r:r['economic_time']),'OK'

def recover_for_prediction(pred,state_root=None,allow_network=True):
    pa=pred.get('price_anchor') or {}; series=pa.get('scientific_series_id') or policy().get('canonical_series_id','XAUUSD_SPOT_REFERENCE')
    t0,mt,tol,end=_window(pred)
    if not mt or not t0:return {'state':'INVALID_PREDICTION','observations':[],'network_attempted':False}
    rows=query(default_store(state_root),series,iso(t0),iso(end));attempts=[]
    chosen,selected,state=_select_provider_rows(rows,mt,tol)
    if state=='NO_VALID_TERMINAL' and allow_network:
        _,attempts=_try_network(pred,state_root,series,t0,end);rows=query(default_store(state_root),series,iso(t0),iso(end));chosen,selected,state=_select_provider_rows(rows,mt,tol)
    if state=='OUTCOME_DATA_CONFLICT':
        return {'state':'OUTCOME_DATA_CONFLICT','series_id':series,'observations':[],'retrieval_time':iso(),'network_attempted':bool(attempts),'network_attempts':attempts,'outcome_science_authority':False,'current_price_substitution_used':False}
    obs=[normalize_row(r) for r in selected]
    return {'state':'RECOVERED_FROM_PIT' if obs else 'NO_VALID_HISTORY','series_id':series,'selected_provider':chosen,'observations':obs,'retrieval_time':iso(),'network_attempted':bool(attempts),'network_attempts':attempts,'outcome_science_authority':False,'current_price_substitution_used':False}
