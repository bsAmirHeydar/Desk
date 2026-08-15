#!/usr/bin/env python3
from __future__ import annotations
from datetime import datetime,timezone
import hashlib,json
PHASE='AD-V2-P07'; VERSION='0.7.0'
FORBIDDEN=('mfe','mae','realized_r','future_price','exit_reason','matured_at','outcome','profit','loss')
class FreezeError(ValueError): pass
def _canon(x): return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,default=str)
def _hash(x): return 'sha256:'+hashlib.sha256(_canon(x).encode()).hexdigest()
def _dt(s):
    d=datetime.fromisoformat(str(s).replace('Z','+00:00')); return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
def _get(o,p):
    c=o
    for x in p.split('.'):
        if not isinstance(c,dict): return None
        c=c.get(x)
    return c
def _scan_forbidden(o,path=''):
    bad=[]
    if isinstance(o,dict):
        for k,v in o.items():
            kp=(path+'.'+str(k)).strip('.')
            if any(t in str(k).lower() for t in FORBIDDEN): bad.append(kp)
            bad.extend(_scan_forbidden(v,kp))
    elif isinstance(o,list):
        for i,v in enumerate(o): bad.extend(_scan_forbidden(v,f'{path}[{i}]'))
    return bad
def _rootset(state):
    rows=_get(state,'science_v2.pressure.causal_root_ledger') or []
    return sorted(str(r.get('root_id')) for r in rows if isinstance(r,dict) and r.get('root_id'))
def extract_features(state):
    paths={
      'pressure_class':'science_v2.pressure.pressure_core.class','pressure_sign':'science_v2.pressure.pressure_core.sign','pressure_trend':'science_v2.pressure.pressure_dynamics.trend','pressure_acceleration':'science_v2.pressure.pressure_dynamics.acceleration','remaining_causal_pressure':'science_v2.pressure.remaining_causal_pressure.value',
      'transmission_state':'science_v2.transmission.transmission_state.state','transmission_efficiency':'science_v2.transmission.transmission_efficiency.class','residual_state':'science_v2.transmission.counterfactual_residual.state','residual_magnitude':'science_v2.transmission.counterfactual_residual.magnitude_class','missing_driver_escalation':'science_v2.transmission.missing_driver_escalation.level',
      'unreleased_pressure':'science_v2.latent_release.unreleased_pressure.class','opposing_move_maturity':'science_v2.latent_release.opposing_move_maturity.state','latent_reserve':'science_v2.latent_release.latent_causal_reserve.class','transmission_inflection':'science_v2.latent_release.transmission_inflection.state','release_readiness':'science_v2.latent_release.release_readiness.state','release_lifecycle':'science_v2.latent_release.release_lifecycle.state',
      'event_readiness_cap':'science_v2.gold_intelligence.event_reset.release_readiness_cap_recommended','gold_missing_driver_search':'science_v2.gold_intelligence.missing_driver_search.required','v1_permission':'execution.permission'}
    return {k:_get(state,p) for k,p in paths.items()}
def freeze(state:dict,*,sample_provenance='TRUE_FORWARD',sealed_at_utc=None,episode_key=None,regime='UNKNOWN',hypothesis_family_id='AD_V2_LATENT_RELEASE_V1'):
    if not isinstance(state,dict) or state.get('phase')!='AD-V2-P06' or state.get('status')!='PASS': raise FreezeError('valid P06 state required')
    if state.get('subject')!='XAUUSD': raise FreezeError('P07 currently certifies XAUUSD only')
    if ((state.get('integrity') or {}).get('status'))!='PASS': raise FreezeError('P06 integrity PASS required')
    if sample_provenance not in {'TRUE_FORWARD','DEVELOPMENT_CASE','HISTORICAL_RECONSTRUCTION','HOLDOUT'}: raise FreezeError('invalid sample provenance')
    if sample_provenance=='TRUE_FORWARD' and state.get('deployment') not in {'SHADOW_ONLY','TRUE_FORWARD_SHADOW'}: raise FreezeError('unexpected upstream deployment')
    analysis=state.get('as_of'); seal=sealed_at_utc or datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
    if not analysis: raise FreezeError('analysis cutoff required')
    if _dt(seal)<_dt(analysis): raise FreezeError('commitment seal before analysis cutoff')
    features=extract_features(state); bad=_scan_forbidden(features)
    if bad: raise FreezeError('future/outcome fields forbidden in commitment: '+','.join(bad))
    roots=_rootset(state); day=_dt(analysis).date().isoformat()
    ep=episode_key or ('|'.join(['XAUUSD',str(state.get('horizon')),day,','.join(roots) or 'NO_ROOTSET']))
    seed={'run_id':state.get('run_id'),'p06_hash':state.get('canonical_v2_state_hash'),'sealed_at_utc':seal,'sample_provenance':sample_provenance}
    cid='V2FC_'+hashlib.sha256(_canon(seed).encode()).hexdigest()[:24].upper()
    out={'schema_version':'1.0.0','phase':PHASE,'version':VERSION,'record_type':'V2_FORWARD_COMMITMENT','commitment_id':cid,'run_id':state.get('run_id'),'subject':'XAUUSD','horizon':state.get('horizon'),'mode':state.get('mode'),'analysis_cutoff_utc':analysis,'sealed_at_utc':seal,'trading_day':day,'sample_provenance':sample_provenance,'true_forward_eligible':sample_provenance=='TRUE_FORWARD','independent_episode_key':ep,'dominant_root_ids':roots,'regime':regime,'hypothesis_family_id':hypothesis_family_id,'features':features,'p06_state_hash':state.get('canonical_v2_state_hash'),'base_run':state.get('base_run'),'authority':{'trade_permission':'V1_INHERITED','broker':'NONE','promotion':'NONE_FROM_COMMITMENT'},'integrity':{'status':'PASS','frozen_before_outcome':True,'outcome_fields_present':False,'upstream_mutated':False,'historical_relabel_forbidden':True}}
    out['commitment_hash']=_hash(out)
    return out
