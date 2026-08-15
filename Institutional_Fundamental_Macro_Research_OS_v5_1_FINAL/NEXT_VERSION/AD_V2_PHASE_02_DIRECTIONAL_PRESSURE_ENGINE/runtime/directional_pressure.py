#!/usr/bin/env python3
"""Alpha Desk V2 P02 Directional Pressure Engine — SHADOW_ONLY.

Pressure is causal and horizon-specific. Target price is never a pressure input.
"""
from __future__ import annotations
from copy import deepcopy
from datetime import datetime, timezone
import math

PHASE="AD-V2-P02"
VERSION="0.2.0"
DEPLOYMENT="SHADOW_ONLY"

BANDS=[("VERY_LOW",0,20),("LOW",20,40),("MEDIUM",40,60),("HIGH",60,75),("VERY_HIGH",75,90),("EXTREME",90,101)]
FORBIDDEN_SOURCE_KINDS={"TARGET_PRICE","TARGET_PRICE_RETURN","TARGET_TECHNICAL_MOMENTUM","TARGET_BREAKOUT","TARGET_SUPPORT_RESISTANCE","TARGET_CANDLE_PATTERN","TRADE_OUTCOME"}
ALLOWED_SOURCE_KINDS={"OFFICIAL_MACRO_FACT","EXPECTATIONS_STATE","POLICY_REACTION_STATE","CROSS_ASSET_CAUSAL_STATE","PHYSICAL_BALANCE","VERIFIED_FLOW","POSITIONING_STATE","FUNDING_LIQUIDITY_STATE","STRUCTURAL_DEMAND_SUPPLY","GEOPOLITICAL_POLICY_STATE","CORPORATE_CASH_FLOW","MODEL_DERIVED_CAUSAL_STATE"}
FUTURE_FIELDS={"price_transmission","unreleased_pressure","opposing_move_maturity","release_readiness"}

class PressureError(ValueError):
    pass

def _dt(s):
    if not s: return None
    s=str(s).replace('Z','+00:00')
    d=datetime.fromisoformat(s)
    if d.tzinfo is None: d=d.replace(tzinfo=timezone.utc)
    return d.astimezone(timezone.utc)

def _band(v):
    if v is None: return "UNDETERMINED"
    v=max(0.0,min(100.0,float(v)))
    for name,lo,hi in BANDS:
        if lo <= v < hi: return name
    return "EXTREME"

def _signed_interval(direction, r):
    if not isinstance(r,dict): raise PressureError('magnitude range missing')
    lo=float(r.get('low')); hi=float(r.get('high'))
    if lo<0 or hi>100 or lo>hi: raise PressureError('invalid magnitude range')
    if direction=='BUY': return lo,hi
    if direction=='SELL': return -hi,-lo
    if direction=='BALANCED': return 0.0,0.0
    raise PressureError('unknown pressure direction')

def _direction_from_v1(v):
    x=str(v or '').upper()
    if x in {'BULLISH','BUY','LONG'}: return 'BUY'
    if x in {'BEARISH','SELL','SHORT'}: return 'SELL'
    if x in {'NEUTRAL','BALANCED','MIXED'}: return 'BALANCED'
    return 'UNKNOWN'

def _headline(lo,hi):
    if lo <= 0 <= hi and not (lo==0 and hi==0):
        return {'sign':'CONTESTED_OR_UNDETERMINED','class':'CONTESTED_OR_UNDETERMINED','magnitude_class':'UNDETERMINED'}
    mid=(lo+hi)/2.0
    if mid>0: sign='BUY'
    elif mid<0: sign='SELL'
    else: sign='BALANCED'
    mag=_band(abs(mid))
    cls='BALANCED' if sign=='BALANCED' else f'{sign}_{mag}'
    return {'sign':sign,'class':cls,'magnitude_class':mag}

def _precision(lo,hi):
    width=abs(float(hi)-float(lo))
    if width<=15: return 'NARROW'
    if width<=30: return 'MEDIUM'
    return 'BROAD'

def _trend(current_mid, history):
    hist=[x for x in (history or []) if isinstance(x,dict) and isinstance(x.get('signed_midpoint'),(int,float))]
    if not hist:
        return {'trend':'UNKNOWN','snapshot_delta':None,'acceleration':'UNKNOWN','second_difference':None}
    prev=float(hist[-1]['signed_midpoint']); delta=float(current_mid)-prev
    if delta>=12: tr='RISING_FAST'
    elif delta>=4: tr='RISING'
    elif delta<=-12: tr='FALLING_FAST'
    elif delta<=-4: tr='FALLING'
    else: tr='STABLE'
    if len(hist)<2:
        acc='UNKNOWN'; second=None
    else:
        prevprev=float(hist[-2]['signed_midpoint']); prev_delta=prev-prevprev; second=delta-prev_delta
        if second>=4: acc='BUYWARD_ACCELERATION'
        elif second<=-4: acc='SELLWARD_ACCELERATION'
        else: acc='STEADY'
    return {'trend':tr,'snapshot_delta':round(delta,6),'acceleration':acc,'second_difference':None if second is None else round(second,6)}

def _freshness(root, as_of):
    observed=_dt(root.get('observed_at_utc')); ttl=root.get('freshness_ttl_seconds')
    if observed is None or ttl in (None,''):
        return {'state':'UNKNOWN','age_seconds':None if observed is None else max(0,(as_of-observed).total_seconds()),'ttl_seconds':ttl}
    ttl=float(ttl)
    if ttl<=0: raise PressureError('freshness_ttl_seconds must be positive')
    age=max(0.0,(as_of-observed).total_seconds()); f=age/ttl
    if f<=0.50: state='FRESH'
    elif f<=0.75: state='AGING'
    elif f<=1.0: state='STALE'
    else: state='EXPIRED'
    return {'state':state,'age_seconds':round(age,3),'ttl_seconds':ttl,'age_fraction_of_ttl':round(f,6)}

def _half_life_valid(root):
    h=root.get('half_life')
    if not h: return True,None
    prov=str(h.get('provenance','UNKNOWN')).upper()
    if prov not in {'EMPIRICAL','MODEL_IMPLIED','JUDGMENTAL','UNKNOWN'}: return False,'invalid half-life provenance'
    if prov=='EMPIRICAL' and not h.get('validation_ref'): return False,'empirical half-life requires validation_ref'
    return True,None

def _confidence(roots, norm_weights, effective_states):
    coverage=0.0; weighted_conf=0.0; conf_weight=0.0
    for r,w,state in zip(roots,norm_weights,effective_states):
        if state=='PRESENT':
            coverage+=w
            c=r.get('confidence')
            if isinstance(c,(int,float)):
                weighted_conf+=w*float(c); conf_weight+=w
    avg=None if conf_weight<=0 else weighted_conf/conf_weight
    if coverage>=0.90 and (avg is None or avg>=70): cls='HIGH'
    elif coverage>=0.70 and (avg is None or avg>=50): cls='MEDIUM'
    else: cls='LOW'
    return {'class':cls,'root_coverage_weight':round(coverage,6),'unknown_weight':round(1-coverage,6),'weighted_evidence_confidence':None if avg is None else round(avg,3),'not_probability':True}

def _contradiction(roots,norm_weights,effective_states,sign):
    if sign not in {'BUY','SELL'}: return {'class':'UNDETERMINED','opposing_weight':None}
    opp='SELL' if sign=='BUY' else 'BUY'; weight=0.0
    for r,w,state in zip(roots,norm_weights,effective_states):
        if state=='PRESENT' and str(r.get('polarity')).upper()==opp: weight+=w
    if weight<=0.15: cls='LOW'
    elif weight<=0.35: cls='MEDIUM'
    else: cls='HIGH'
    return {'class':cls,'opposing_weight':round(weight,6)}

def build_from_p01(p01:dict, *, as_of_utc:str, history=None, target_price_context=None):
    """Backward-compatible P02 wrap of P01/Module89 semantic lifecycle.

    target_price_context is accepted only so adversarial tests can prove it has no effect; it is never read.
    """
    if not isinstance(p01,dict) or ((p01.get('semantic_integrity') or {}).get('status')!='PASS'):
        return _failed('P01_SEMANTIC_INTEGRITY_REQUIRED')
    direction=_direction_from_v1((p01.get('fundamental_direction') or {}).get('value'))
    fr=(p01.get('fundamental_force') or {}).get('active_horizon_range')
    try: lo,hi=_signed_interval(direction,fr)
    except Exception as e: return _failed('LEGACY_FORCE_RANGE_INVALID',str(e))
    head=_headline(lo,hi); mid=(lo+hi)/2.0; dynamics=_trend(mid,history)
    rem=deepcopy(p01.get('remaining_fundamental_pressure'))
    cons=deepcopy(p01.get('fundamental_consumption'))
    pers=deepcopy(p01.get('persistence'))
    out={
      'schema_version':'1.0.0','phase':PHASE,'version':VERSION,'deployment':DEPLOYMENT,'status':'PASS','aggregation_mode':'LEGACY_MODULE89_WRAP',
      'active_horizon':p01.get('active_horizon'),'as_of_utc':as_of_utc,
      'pressure_core':{**head,'signed_range':{'low':round(lo,6),'high':round(hi,6),'unit':'ordinal_pressure'},'signed_midpoint':round(mid,6),'magnitude_interval_classes':{'low':_band(min(abs(lo),abs(hi))),'high':_band(max(abs(lo),abs(hi)) )},'precision':_precision(lo,hi),'scale':'ANALYTICAL_ORDINAL_NOT_PROBABILITY'},
      'pressure_dynamics':dynamics,
      'causal_root_ledger':[],
      'freshness_and_coverage':{'class':'LEGACY_MODULE89_PROVENANCE','root_coverage_weight':None,'unknown_weight':None},
      'fundamental_driver_consumption':cons,
      'remaining_causal_pressure':rem,
      'persistence':pers,
      'contradiction_load':{'class':'LEGACY_MODULE89_NOT_REAGGREGATED','opposing_weight':None},
      'pressure_confidence':{'class':'LEGACY_MODULE89_PROVENANCE','not_probability':True},
      'provenance':{'direction_source':deepcopy(p01.get('fundamental_direction')),'force_source':deepcopy(p01.get('fundamental_force')),'target_price_used':False},
      'integrity':{'status':'PASS','target_price_contamination':False,'future_fields_present':[],'diagnostics':[]}
    }
    return out

def build_from_roots(inp:dict, *, history=None, target_price_context=None):
    """V2 explicit independent-root shadow aggregation.

    Target price context is intentionally ignored and never enters the result.
    """
    try:
        if not isinstance(inp,dict): raise PressureError('pressure input must be object')
        horizon=inp.get('active_horizon'); as_of_s=inp.get('as_of_utc'); as_of=_dt(as_of_s)
        if not horizon or as_of is None: raise PressureError('active_horizon and as_of_utc required')
        roots=inp.get('roots')
        if not isinstance(roots,list) or not roots: raise PressureError('roots required')
        ids=[]; kept=[]
        for r0 in roots:
            if not isinstance(r0,dict): raise PressureError('root must be object')
            r=deepcopy(r0); rid=r.get('root_id')
            if not rid or rid in ids: raise PressureError('duplicate/missing root_id')
            ids.append(rid)
            if r.get('active_horizon')!=horizon: raise PressureError('root horizon mismatch: '+str(rid))
            if r.get('depends_on_root_ids'): raise PressureError('top-level dependent root forbidden: '+str(rid))
            sk=str(r.get('source_kind','')).upper()
            if sk in FORBIDDEN_SOURCE_KINDS: raise PressureError('target/technical price source forbidden: '+str(rid))
            if sk not in ALLOWED_SOURCE_KINDS: raise PressureError('unregistered source_kind: '+str(rid))
            if not str(r.get('mechanism','')).strip(): raise PressureError('causal mechanism required: '+str(rid))
            app=str(r.get('applicability','')).upper()
            if app not in {'APPLICABLE','UNAVAILABLE','NOT_APPLICABLE'}: raise PressureError('invalid applicability: '+str(rid))
            wt=r.get('weight')
            if not isinstance(wt,(int,float)) or wt<0: raise PressureError('invalid weight: '+str(rid))
            ok,err=_half_life_valid(r)
            if not ok: raise PressureError(f'{rid}: {err}')
            if app!='NOT_APPLICABLE': kept.append(r)
        if not kept: raise PressureError('no applicable economic roots')
        total=sum(float(r['weight']) for r in kept)
        if total<=0: raise PressureError('applicable root weights sum to zero')
        norm=[float(r['weight'])/total for r in kept]
        ledger=[]; lows=[]; highs=[]; states=[]
        for r,wgt in zip(kept,norm):
            fres=_freshness(r,as_of); app=str(r['applicability']).upper(); pol=str(r.get('polarity','UNKNOWN')).upper()
            state='PRESENT'
            if app=='UNAVAILABLE' or fres['state']=='EXPIRED': state='UNAVAILABLE'
            if state=='UNAVAILABLE' or pol=='UNKNOWN':
                clo,chi=-100*wgt,100*wgt
            elif pol=='NEUTRAL': clo,chi=0.0,0.0
            elif pol in {'BUY','SELL'}:
                rr=r.get('magnitude_range')
                if not isinstance(rr,dict): raise PressureError('magnitude_range required: '+str(r['root_id']))
                lo=float(rr.get('low')); hi=float(rr.get('high'))
                if lo<0 or hi>100 or lo>hi: raise PressureError('invalid magnitude_range: '+str(r['root_id']))
                if pol=='BUY': clo,chi=lo*wgt,hi*wgt
                else: clo,chi=-hi*wgt,-lo*wgt
            else: raise PressureError('invalid polarity: '+str(r['root_id']))
            lows.append(clo); highs.append(chi); states.append('PRESENT' if state=='PRESENT' and pol!='UNKNOWN' else 'UNAVAILABLE')
            ledger.append({**r,'normalized_weight':round(wgt,8),'freshness':fres,'effective_state':states[-1],'signed_contribution_interval':{'low':round(clo,6),'high':round(chi,6)}})
        lo=sum(lows); hi=sum(highs); head=_headline(lo,hi); mid=(lo+hi)/2.0
        conf=_confidence(kept,norm,states); contra=_contradiction(kept,norm,states,head['sign']); dyn=_trend(mid,history)
        rem=deepcopy(inp.get('remaining_causal_pressure'))
        cons=deepcopy(inp.get('fundamental_driver_consumption'))
        pers=deepcopy(inp.get('persistence'))
        diagnostics=[]
        if conf['unknown_weight']>0: diagnostics.append('APPLICABLE_ROOT_UNAVAILABLE_OR_EXPIRED')
        out={
          'schema_version':'1.0.0','phase':PHASE,'version':VERSION,'deployment':DEPLOYMENT,'status':'PASS','aggregation_mode':'EXPLICIT_ROOT_LEDGER',
          'active_horizon':horizon,'as_of_utc':as_of_s,
          'pressure_core':{**head,'signed_range':{'low':round(lo,6),'high':round(hi,6),'unit':'ordinal_pressure'},'signed_midpoint':round(mid,6),'magnitude_interval_classes':{'low':_band(min(abs(lo),abs(hi))),'high':_band(max(abs(lo),abs(hi)))},'precision':_precision(lo,hi),'scale':'ANALYTICAL_ORDINAL_NOT_PROBABILITY'},
          'pressure_dynamics':dyn,
          'causal_root_ledger':ledger,
          'freshness_and_coverage':conf,
          'fundamental_driver_consumption':cons,
          'remaining_causal_pressure':rem,
          'persistence':pers,
          'contradiction_load':contra,
          'pressure_confidence':conf,
          'provenance':{'root_count':len(ledger),'aggregation':'DISCLOSED_WEIGHTED_ORDINAL_INTERVAL','target_price_used':False},
          'integrity':{'status':'PASS','target_price_contamination':False,'future_fields_present':[],'diagnostics':diagnostics}
        }
        return out
    except Exception as e:
        return _failed('EXPLICIT_ROOT_LEDGER_INVALID',str(e))

def _failed(code,detail=None):
    return {'schema_version':'1.0.0','phase':PHASE,'version':VERSION,'deployment':DEPLOYMENT,'status':'FAIL_CLOSED','integrity':{'status':'FAIL_CLOSED','target_price_contamination':False,'future_fields_present':[],'diagnostics':[x for x in [code,detail] if x]}}

def pressure_core_fingerprint(state):
    """Stable equality object for contamination attacks; excludes no causal field and contains no price input."""
    import json, hashlib
    obj={'pressure_core':state.get('pressure_core'),'pressure_dynamics':state.get('pressure_dynamics'),'fundamental_driver_consumption':state.get('fundamental_driver_consumption'),'remaining_causal_pressure':state.get('remaining_causal_pressure'),'persistence':state.get('persistence'),'contradiction_load':state.get('contradiction_load')}
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':'),default=str).encode()).hexdigest()
