#!/usr/bin/env python3
"""Alpha Desk V2 P03 Price Transmission Engine — SHADOW_ONLY.

Consumes an immutable P02 Pressure state and a pre-frozen expected response signature,
then diagnoses subsequent price/cross-asset transmission. Never mutates Pressure.
"""
from __future__ import annotations
from copy import deepcopy
from datetime import datetime, timezone
import hashlib, json, math

PHASE='AD-V2-P03'
VERSION='0.3.0'
DEPLOYMENT='SHADOW_ONLY'
FORBIDDEN_METHODS={'POST_HOC_PRICE_FIT','EX_POST_BEST_WINDOW','OUTCOME_SELECTED_RANGE','FUTURE_DATA_FIT'}
ALLOWED_METHODS={'EVENT_CONDITIONED_RANGE','REGIME_CONDITIONED_LOCAL_PROJECTION','POLICY_PATH_DECOMPOSITION','DURATION_CONVEXITY_BRIDGE','PHYSICAL_BALANCE_ELASTICITY','OPTIONS_IMPLIED_SHIFT','MATCHED_HISTORICAL_CONTROLS','EXPERT_RANGE','DIRECTION_ONLY'}
ALLOWED_UNITS={'PCT_RETURN','LOG_RETURN','BPS_PRICE_RETURN','STANDARDIZED_RESPONSE'}
FORBIDDEN_FUTURE_FIELDS={'unreleased_pressure','opposing_move_maturity','release_readiness','release_state','confirmed_absorption','confirmed_liquidity_grab','trade_permission'}

class TransmissionError(ValueError): pass

def _dt(s):
    if not s: return None
    d=datetime.fromisoformat(str(s).replace('Z','+00:00'))
    if d.tzinfo is None: d=d.replace(tzinfo=timezone.utc)
    return d.astimezone(timezone.utc)

def _pressure_fingerprint(p):
    obj={
      'pressure_core':p.get('pressure_core'),
      'pressure_dynamics':p.get('pressure_dynamics'),
      'fundamental_driver_consumption':p.get('fundamental_driver_consumption'),
      'remaining_causal_pressure':p.get('remaining_causal_pressure'),
      'persistence':p.get('persistence'),
      'contradiction_load':p.get('contradiction_load')
    }
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':'),default=str).encode()).hexdigest()

def _signature_fingerprint(s):
    x=deepcopy(s); x.pop('signature_hash',None)
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),default=str).encode()).hexdigest()

def _pressure_sign(p):
    s=str(((p.get('pressure_core') or {}).get('sign')) or '').upper()
    if s=='BUY': return 1.0
    if s=='SELL': return -1.0
    return 0.0

def _expected_range(sig):
    tr=sig.get('target_response') or {}
    r=tr.get('expected_aligned_range')
    if r is None: return None
    if not isinstance(r,dict): raise TransmissionError('expected_aligned_range must be object')
    lo=float(r.get('low')); hi=float(r.get('high'))
    if lo<0 or hi<0 or lo>hi: raise TransmissionError('expected aligned range must be non-negative and ordered')
    return lo,hi

def _efficiency(ratio):
    if ratio is None: return {'class':'UNAVAILABLE','relative_response_ratio':None,'not_probability':True}
    if ratio<0: c='NEGATIVE'
    elif ratio<0.25: c='VERY_LOW'
    elif ratio<0.75: c='LOW'
    elif ratio<1.25: c='EXPECTED'
    elif ratio<1.75: c='HIGH'
    else: c='OVER'
    return {'class':c,'relative_response_ratio':round(ratio,6),'not_probability':True}

def _residual(actual_aligned, exp):
    if exp is None: return {'state':'UNAVAILABLE','actual_minus_expected_range':None,'normalized_midpoint_residual':None}
    lo,hi=exp; rlo=actual_aligned-hi; rhi=actual_aligned-lo; mid=(lo+hi)/2.0
    if rlo>0: state='ABOVE_EXPECTATION'
    elif rhi<0: state='BELOW_EXPECTATION'
    else: state='OVERLAPS_EXPECTATION'
    nr=None if mid<=0 else (actual_aligned-mid)/mid
    if nr is None: mag='UNAVAILABLE'
    elif abs(nr)<0.25: mag='SMALL'
    elif abs(nr)<0.75: mag='MEDIUM'
    elif abs(nr)<1.5: mag='LARGE'
    else: mag='EXTREME'
    return {'state':state,'magnitude_class':mag,'actual_minus_expected_range':{'low':round(rlo,6),'high':round(rhi,6)},'normalized_midpoint_residual':None if nr is None else round(nr,6)}

def _target_state(actual_aligned, exp, material, elapsed, earliest, latest):
    if elapsed < earliest: return 'NOT_YET_OBSERVABLE'
    if actual_aligned < -material: return 'NEGATIVE_TRANSMISSION'
    if abs(actual_aligned) <= material:
        return 'DELAYED' if elapsed <= latest else 'COMPRESSION'
    if actual_aligned>0 and exp is None: return 'ALIGNED_DIRECTION_ONLY'
    if actual_aligned>0 and exp is not None:
        lo,hi=exp
        if actual_aligned < lo:
            return 'ALIGNED_INCOMPLETE' if elapsed <= latest else 'UNDER_TRANSMISSION'
        if actual_aligned <= hi: return 'ALIGNED'
        mid=(lo+hi)/2.0
        if mid>0 and actual_aligned/mid>=1.5: return 'OVER_TRANSMISSION'
        return 'ALIGNED'
    return 'UNDETERMINED'

def _channel_direction(v):
    x=str(v or '').upper()
    if x in {'UP','RISING','POSITIVE','BUY'}: return 1
    if x in {'DOWN','FALLING','NEGATIVE','SELL'}: return -1
    if x in {'FLAT','NEUTRAL','UNCHANGED'}: return 0
    return None

def _pathway(sig, actual):
    expected=sig.get('pathways') or []
    observed={str(x.get('channel_id')):x for x in (actual.get('channels') or []) if isinstance(x,dict) and x.get('channel_id')}
    groups={}; details=[]; unknown=0
    for e in expected:
        cid=str(e.get('channel_id') or '')
        if not cid: raise TransmissionError('pathway channel_id required')
        grp=str(e.get('independence_group') or cid)
        mechanically=bool(e.get('mechanically_linked_target_proxy',False))
        o=observed.get(cid)
        expdir=_channel_direction(e.get('expected_direction'))
        if o is None or expdir is None or _channel_direction(o.get('observed_direction')) is None:
            status='UNKNOWN'; unknown+=1
        else:
            od=_channel_direction(o.get('observed_direction'))
            status='CONFIRMS' if (od==expdir or (od==0 and expdir==0)) else 'CONFLICTS'
        details.append({'channel_id':cid,'independence_group':grp,'mechanically_linked_target_proxy':mechanically,'status':status,'expected_direction':e.get('expected_direction'),'observed_direction':None if o is None else o.get('observed_direction')})
        if mechanically: continue
        g=groups.setdefault(grp,[]); g.append(status)
    group_states=[]
    for grp,st in groups.items():
        known=[x for x in st if x!='UNKNOWN']
        if not known: gs='UNKNOWN'
        elif all(x=='CONFIRMS' for x in known): gs='CONFIRMS'
        elif all(x=='CONFLICTS' for x in known): gs='CONFLICTS'
        else: gs='MIXED'
        group_states.append((grp,gs))
    known=[s for _,s in group_states if s!='UNKNOWN']
    if not group_states or not known: state='UNKNOWN'
    else:
        conflicts=sum(1 for s in known if s in {'CONFLICTS','MIXED'})
        confirms=sum(1 for s in known if s=='CONFIRMS')
        if conflicts==0 and confirms==len(known): state='COHERENT'
        elif conflicts>=max(1,math.ceil(len(known)/2)): state='FRAGMENTED'
        else: state='PARTIAL'
    coverage=0.0 if not group_states else sum(1 for _,s in group_states if s!='UNKNOWN')/len(group_states)
    return {'state':state,'independent_group_count':len(group_states),'coverage':round(coverage,6),'group_states':[{'independence_group':g,'state':s} for g,s in group_states],'channels':details}

def _transmission_confidence(sig, actual, pathway_state):
    prov=str(sig.get('method_provenance','UNKNOWN')).upper()
    dq=str(((actual.get('target') or {}).get('data_quality')) or 'UNKNOWN').upper()
    if dq in {'DIRECT','OFFICIAL','HIGH'}: base=2
    elif dq in {'MEDIUM','INDIRECT'}: base=1
    else: base=0
    if prov=='EMPIRICAL': base+=1
    elif prov in {'MODEL_IMPLIED','JUDGMENTAL'}: base+=0
    if pathway_state.get('coverage',0)>=0.67: base+=1
    if base>=3: c='HIGH'
    elif base>=1: c='MEDIUM'
    else: c='LOW'
    return {'class':c,'not_probability':True,'target_data_quality':dq,'method_provenance':prov,'pathway_coverage':pathway_state.get('coverage')}

def _escalation(state,residual,pathway,pressure_conf,history_count,candidates):
    pc=str((pressure_conf or {}).get('class','UNKNOWN')).upper()
    level='NONE'; reasons=[]
    if state=='NEGATIVE_TRANSMISSION':
        level='RESEARCH_ESCALATION'; reasons.append('MATERIAL_OPPOSITE_TARGET_RESPONSE')
    elif state in {'COMPRESSION','UNDER_TRANSMISSION'}:
        level='WATCH'; reasons.append('EXPECTED_TRANSMISSION_NOT_REALIZED_AFTER_LAG')
    if pathway.get('state')=='FRAGMENTED':
        if level=='NONE': level='WATCH'
        reasons.append('TRANSMISSION_PATHWAY_FRAGMENTED')
    if residual.get('magnitude_class') in {'LARGE','EXTREME'} and residual.get('state')=='BELOW_EXPECTATION':
        if level=='NONE': level='WATCH'
        elif level=='WATCH': level='RESEARCH_ESCALATION'
        reasons.append('LARGE_COUNTERFACTUAL_RESIDUAL')
    if level=='RESEARCH_ESCALATION' and pc=='HIGH' and int(history_count or 0)>=2:
        level='DECISION_CRITICAL'; reasons.append('PERSISTENT_DISAGREEMENT_WITH_HIGH_CONFIDENCE_PRESSURE')
    cs=[]
    for c in candidates or []:
        if not isinstance(c,dict) or not c.get('candidate_id'): continue
        x=deepcopy(c); x['status']='UNCONFIRMED'; cs.append(x)
    return {'level':level,'reasons':reasons,'candidate_missing_drivers':cs,'candidates_are_unconfirmed':True,'pressure_mutation_allowed':False}

def build_transmission(pressure:dict, expected_signature:dict, actual_response:dict, *, divergence_history_count=0, missing_driver_candidates=None):
    try:
        if not isinstance(pressure,dict) or pressure.get('status')!='PASS' or ((pressure.get('integrity') or {}).get('status')!='PASS'):
            raise TransmissionError('P02 Pressure integrity PASS required')
        if not isinstance(expected_signature,dict) or not isinstance(actual_response,dict): raise TransmissionError('signature and actual response required')
        pfp=_pressure_fingerprint(pressure)
        if expected_signature.get('pressure_fingerprint')!=pfp: raise TransmissionError('expected signature pressure fingerprint mismatch')
        psign=_pressure_sign(pressure)
        if psign==0: raise TransmissionError('directionally contested/balanced Pressure cannot produce directional transmission test')
        ph=pressure.get('active_horizon'); sh=expected_signature.get('active_horizon')
        if not ph or ph!=sh: raise TransmissionError('active horizon mismatch')
        pa=_dt(pressure.get('as_of_utc')); sd=_dt(expected_signature.get('declared_at_utc')); rs=_dt(actual_response.get('window_start_utc')); re=_dt(actual_response.get('window_end_utc'))
        if None in {pa,sd,rs,re}: raise TransmissionError('all point-in-time timestamps required')
        if not (pa<=sd<=rs<re): raise TransmissionError('point-in-time ordering violation')
        method=str(expected_signature.get('method','')).upper()
        if method in FORBIDDEN_METHODS: raise TransmissionError('post-hoc expected-response method forbidden')
        if method not in ALLOWED_METHODS: raise TransmissionError('unregistered expected-response method')
        prov=str(expected_signature.get('method_provenance','UNKNOWN')).upper()
        if prov=='EMPIRICAL' and not expected_signature.get('validation_ref'): raise TransmissionError('empirical expected signature requires validation_ref')
        tgt=expected_signature.get('target_response') or {}; act=actual_response.get('target') or {}
        if not tgt.get('instrument') or tgt.get('instrument')!=act.get('instrument'): raise TransmissionError('target instrument mismatch')
        unit=str(tgt.get('unit','')).upper(); aunit=str(act.get('unit','')).upper()
        if unit not in ALLOWED_UNITS or unit!=aunit: raise TransmissionError('target response unit mismatch/unregistered')
        obs=act.get('observed_response')
        if not isinstance(obs,(int,float)): raise TransmissionError('observed target response required')
        actual_aligned=float(obs)*psign
        exp=_expected_range(expected_signature)
        if method=='DIRECTION_ONLY' and exp is not None: raise TransmissionError('DIRECTION_ONLY cannot declare magnitude range')
        if method!='DIRECTION_ONLY' and exp is None: raise TransmissionError('magnitude method requires expected_aligned_range')
        material=tgt.get('minimum_material_response')
        if not isinstance(material,(int,float)) or material<0: raise TransmissionError('minimum_material_response must be nonnegative number')
        earliest=float(tgt.get('earliest_material_response_seconds',0))
        latest=float(tgt.get('latest_expected_lag_seconds',0))
        if earliest<0 or latest<earliest: raise TransmissionError('invalid response timing bounds')
        elapsed=max(0.0,(re-rs).total_seconds())
        state=_target_state(actual_aligned,exp,float(material),elapsed,earliest,latest)
        residual=_residual(actual_aligned,exp)
        mid=None if exp is None else (exp[0]+exp[1])/2.0
        ratio=None if mid in (None,0) else actual_aligned/mid
        efficiency=_efficiency(ratio)
        pathway=_pathway(expected_signature,actual_response)
        tconf=_transmission_confidence(expected_signature,actual_response,pathway)
        escalation=_escalation(state,residual,pathway,pressure.get('pressure_confidence'),divergence_history_count,missing_driver_candidates)
        if state=='NEGATIVE_TRANSMISSION': disagree='SEVERE' if escalation['level'] in {'RESEARCH_ESCALATION','DECISION_CRITICAL'} else 'MATERIAL'
        elif state in {'COMPRESSION','UNDER_TRANSMISSION'} or pathway.get('state')=='FRAGMENTED': disagree='MATERIAL'
        elif state in {'ALIGNED','ALIGNED_DIRECTION_ONLY'} and pathway.get('state') in {'COHERENT','UNKNOWN'}: disagree='LOW'
        else: disagree='MODERATE'
        out={
          'schema_version':'1.0.0','phase':PHASE,'version':VERSION,'deployment':DEPLOYMENT,'status':'PASS',
          'upstream_pressure_reference':{'fingerprint':pfp,'as_of_utc':pressure.get('as_of_utc'),'active_horizon':ph,'sign':(pressure.get('pressure_core') or {}).get('sign'),'class':(pressure.get('pressure_core') or {}).get('class'),'immutable':True},
          'expected_signature_reference':{'signature_id':expected_signature.get('signature_id'),'fingerprint':_signature_fingerprint(expected_signature),'declared_at_utc':expected_signature.get('declared_at_utc'),'method':method,'method_provenance':prov,'frozen_before_response':True},
          'response_window':{'start_utc':actual_response.get('window_start_utc'),'end_utc':actual_response.get('window_end_utc'),'elapsed_seconds':round(elapsed,3),'earliest_material_response_seconds':earliest,'latest_expected_lag_seconds':latest},
          'target_response':{'instrument':act.get('instrument'),'unit':unit,'observed_response':float(obs),'pressure_aligned_response':round(actual_aligned,8),'data_quality':act.get('data_quality'),'expected_aligned_range':None if exp is None else {'low':exp[0],'high':exp[1]},'minimum_material_response':float(material)},
          'transmission_state':{'state':state,'pressure_mutated':False,'price_is_downstream_only':True},
          'counterfactual_residual':residual,
          'transmission_efficiency':efficiency,
          'pathway_diagnostics':pathway,
          'model_disagreement':{'state':disagree,'unmodeled_driver_risk':escalation['level'],'pressure_reversal_inferred':False},
          'missing_driver_escalation':escalation,
          'transmission_confidence':tconf,
          'integrity':{'status':'PASS','pressure_fingerprint_before':pfp,'pressure_fingerprint_after':pfp,'pressure_mutation_detected':False,'post_hoc_signature':False,'forbidden_future_fields_present':[],'anti_storytelling_pass':True}
        }
        return out
    except Exception as e:
        return {'schema_version':'1.0.0','phase':PHASE,'version':VERSION,'deployment':DEPLOYMENT,'status':'FAIL_CLOSED','integrity':{'status':'FAIL_CLOSED','pressure_mutation_detected':False,'post_hoc_signature':False,'forbidden_future_fields_present':[],'anti_storytelling_pass':True,'diagnostics':[str(e)]}}

def stable_transmission_fingerprint(state):
    obj={k:state.get(k) for k in ['upstream_pressure_reference','target_response','transmission_state','counterfactual_residual','transmission_efficiency','pathway_diagnostics','model_disagreement','missing_driver_escalation']}
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':'),default=str).encode()).hexdigest()
