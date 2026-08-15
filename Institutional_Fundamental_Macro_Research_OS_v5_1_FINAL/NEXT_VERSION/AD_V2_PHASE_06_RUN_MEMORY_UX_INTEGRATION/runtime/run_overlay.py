#!/usr/bin/env python3
from __future__ import annotations
from copy import deepcopy
import hashlib,json
from .change_detector import detect

PHASE='AD-V2-P06'; VERSION='0.6.0'; DEPLOYMENT='SHADOW_ONLY'

class IntegrationError(ValueError): pass

def _canon(x): return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,default=str)
def _hash(x): return hashlib.sha256(_canon(x).encode('utf-8')).hexdigest()

def _p02_fp(p):
    obj={k:p.get(k) for k in ['pressure_core','pressure_dynamics','fundamental_driver_consumption','remaining_causal_pressure','persistence','contradiction_load']}
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':'),default=str).encode()).hexdigest()

def _p03_fp(t):
    obj={k:t.get(k) for k in ['upstream_pressure_reference','target_response','transmission_state','counterfactual_residual','transmission_efficiency','pathway_diagnostics','model_disagreement','missing_driver_escalation']}
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':'),default=str).encode()).hexdigest()

def _subject_ok(s): return str(s or '').upper().replace('/','').replace('_','') in {'XAUUSD','GOLD'}

def _require_pass(name,x):
    if not isinstance(x,dict) or x.get('status')!='PASS' or ((x.get('integrity') or {}).get('status') not in (None,'PASS')):
        raise IntegrationError(name+' PASS integrity required')

def compose(base_capsule:dict,pressure:dict,transmission:dict,latent:dict,gold:dict,*,previous=None):
    _require_pass('P02 Pressure',pressure); _require_pass('P03 Transmission',transmission); _require_pass('P04 Latent/Release',latent); _require_pass('P05 Gold Intelligence',gold)
    if not isinstance(base_capsule,dict): raise IntegrationError('base capsule required')
    subject=base_capsule.get('subject') or base_capsule.get('canonical_subject')
    if not _subject_ok(subject): raise IntegrationError('P06 currently certifies Gold/XAUUSD only')
    horizon=base_capsule.get('horizon')
    if not horizon: raise IntegrationError('base capsule horizon required')
    for name,x in [('P02',pressure),('P04',latent),('P05',gold)]:
        if x.get('active_horizon')!=horizon: raise IntegrationError(name+' horizon mismatch')
    if ((transmission.get('upstream_pressure_reference') or {}).get('active_horizon'))!=horizon: raise IntegrationError('P03 horizon mismatch')
    pfp=_p02_fp(pressure); tfp=_p03_fp(transmission)
    if ((transmission.get('upstream_pressure_reference') or {}).get('fingerprint'))!=pfp: raise IntegrationError('P03->P02 fingerprint mismatch')
    if ((latent.get('upstream_pressure_reference') or {}).get('fingerprint'))!=pfp: raise IntegrationError('P04->P02 fingerprint mismatch')
    if ((latent.get('upstream_transmission_reference') or {}).get('fingerprint'))!=tfp: raise IntegrationError('P04->P03 fingerprint mismatch')
    refs=gold.get('upstream_references') or {}
    if refs.get('pressure_fingerprint')!=_hash(pressure): raise IntegrationError('P05->P02 whole-state fingerprint mismatch')
    if refs.get('transmission_fingerprint')!=_hash(transmission): raise IntegrationError('P05->P03 whole-state fingerprint mismatch')
    if refs.get('latent_fingerprint')!=_hash(latent): raise IntegrationError('P05->P04 whole-state fingerprint mismatch')
    base_permission=base_capsule.get('permission')
    if bool(((latent.get('release_readiness') or {}).get('trade_permission_granted'))): raise IntegrationError('P04 illegally grants trade permission')
    if bool(((gold.get('integrity') or {}).get('trade_permission_granted'))): raise IntegrationError('P05 illegally grants trade permission')
    out={
      'schema_version':'1.0.0','phase':PHASE,'version':VERSION,'deployment':DEPLOYMENT,'status':'PASS',
      'run_id':base_capsule.get('run_id'),'request_id':base_capsule.get('request_id'),'subject':'XAUUSD','mode':base_capsule.get('mode'),'as_of':base_capsule.get('as_of'),'horizon':horizon,
      'base_run':{'run_id':base_capsule.get('run_id'),'capsule_hash':base_capsule.get('capsule_hash'),'canonical_result_hash':base_capsule.get('canonical_result_hash'),'quality_status':base_capsule.get('quality_status'),'v1_capsule_immutable':True},
      'science_v2':{'pressure':deepcopy(pressure),'transmission':deepcopy(transmission),'latent_release':deepcopy(latent),'gold_intelligence':deepcopy(gold)},
      'execution':{'permission':base_permission,'permission_source':'V1_BASE_CAPSULE','v2_override_allowed':False,'release_readiness_is_permission':False,'broker_authority':'NONE'},
      'authority':{'pressure':'AD-V2-P02','transmission':'AD-V2-P03','latent_release':'AD-V2-P04','gold_specialization':'AD-V2-P05','composition_memory_ux':'AD-V2-P06','trade_permission':'V1_INHERITED','broker':'NONE'},
      'integrity':{'status':'PASS','upstream_mutated':False,'v1_capsule_mutated':False,'trade_permission_overridden':False,'decision_world_write':False,'pressure_price_separation_preserved':True}
    }
    out['change_set']=detect(previous,out)
    out['portable_memory']=portable_memory(out)
    out['canonical_v2_state_hash']='sha256:'+_hash({k:v for k,v in out.items() if k not in {'canonical_v2_state_hash'}})
    return out

def portable_memory(state):
    p=((state.get('science_v2') or {}).get('pressure') or {}); t=((state.get('science_v2') or {}).get('transmission') or {}); l=((state.get('science_v2') or {}).get('latent_release') or {}); g=((state.get('science_v2') or {}).get('gold_intelligence') or {})
    return {'schema_version':'1.0.0','subject':state.get('subject'),'run_id':state.get('run_id'),'as_of':state.get('as_of'),'horizon':state.get('horizon'),
      'pressure':{'class':(p.get('pressure_core') or {}).get('class'),'sign':(p.get('pressure_core') or {}).get('sign'),'trend':(p.get('pressure_dynamics') or {}).get('trend'),'acceleration':(p.get('pressure_dynamics') or {}).get('acceleration')},
      'transmission':{'state':(t.get('transmission_state') or {}).get('state'),'efficiency':(t.get('transmission_efficiency') or {}).get('class'),'residual':(t.get('counterfactual_residual') or {}).get('magnitude_class'),'missing_driver':(t.get('missing_driver_escalation') or {}).get('level')},
      'latent':{'unreleased':(l.get('unreleased_pressure') or {}).get('class'),'maturity':(l.get('opposing_move_maturity') or {}).get('state'),'reserve':(l.get('latent_causal_reserve') or {}).get('class'),'readiness':(l.get('release_readiness') or {}).get('state'),'lifecycle':(l.get('release_lifecycle') or {}).get('state')},
      'gold':{'event_cap':(g.get('event_reset') or {}).get('release_readiness_cap_recommended'),'missing_search_required':(g.get('missing_driver_search') or {}).get('required')},
      'permission':((state.get('execution') or {}).get('permission')),'change_count':len(((state.get('change_set') or {}).get('items')) or []),'authoritative':False}
