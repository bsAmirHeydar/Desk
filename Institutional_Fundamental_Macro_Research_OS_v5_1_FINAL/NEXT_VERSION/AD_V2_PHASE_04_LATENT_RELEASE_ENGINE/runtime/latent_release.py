#!/usr/bin/env python3
"""Alpha Desk V2 P04 Latent Pressure / Maturity / Release Engine — SHADOW_ONLY.

Consumes immutable P02 Pressure + P03 Transmission and independent non-price evidence.
Never mutates upstream science and never grants trade permission.
"""
from __future__ import annotations
from copy import deepcopy
from datetime import datetime, timezone
import hashlib, json

PHASE='AD-V2-P04'
VERSION='0.4.0'
DEPLOYMENT='SHADOW_ONLY'

ALLOWED_DOMAINS={'FLOW','POSITIONING','FUNDING_LIQUIDITY','MECHANICS','OPTIONS_DEALER','PHYSICAL_BALANCE','EVENT_STATE','CROSS_ASSET_CAUSAL','STRUCTURAL','MARKET_LIQUIDITY'}
ALLOWED_SOURCE_KINDS={'VERIFIED_FLOW','POSITIONING_STATE','FUNDING_LIQUIDITY_STATE','MECHANICS_STATE','OPTIONS_DEALER_STATE','PHYSICAL_BALANCE','EVENT_STATE','CROSS_ASSET_CAUSAL_STATE','STRUCTURAL_STATE','MARKET_LIQUIDITY_STATE'}
FORBIDDEN_SOURCE_KINDS={'TARGET_PRICE','TARGET_PRICE_RETURN','TARGET_CANDLE_PATTERN','TARGET_TECHNICAL_MOMENTUM','TARGET_SUPPORT_RESISTANCE','TARGET_BREAKOUT','TRADE_OUTCOME'}
ROLES={
 'PRESSURE_SUPPORT_PERSISTENT','OPPOSING_DRIVER_ACTIVE','NEW_CAUSAL_DRIVER_AGAINST_PRESSURE','REPLACEMENT_OPPOSING_DRIVER',
 'OPPOSING_FLOW_ACTIVE','OPPOSING_FLOW_DECAYING','POSITIONING_UNWIND_ACTIVE','POSITIONING_UNWIND_EXHAUSTING',
 'FUNDING_HEADWIND_ACTIVE','FUNDING_HEADWIND_EASING','MECHANICAL_HEADWIND_ACTIVE','MECHANICAL_HEADWIND_EASING',
 'RELEASE_SUPPORT','RELEASE_OPPOSITION','EVENT_RESET_RISK','ABSORPTION_EVIDENCE','LIQUIDITY_SWEEP_EVIDENCE'
}
ACTIVE_ROLES={'OPPOSING_DRIVER_ACTIVE','OPPOSING_FLOW_ACTIVE','POSITIONING_UNWIND_ACTIVE','FUNDING_HEADWIND_ACTIVE','MECHANICAL_HEADWIND_ACTIVE'}
EXHAUSTION_ROLES={'OPPOSING_FLOW_DECAYING','POSITIONING_UNWIND_EXHAUSTING','FUNDING_HEADWIND_EASING','MECHANICAL_HEADWIND_EASING'}
HARD_VETO_ROLES={'NEW_CAUSAL_DRIVER_AGAINST_PRESSURE','REPLACEMENT_OPPOSING_DRIVER'}
TRANSMISSION_RANK={
 'NEGATIVE_TRANSMISSION':-2.0,'COMPRESSION':-1.0,'DELAYED':-1.0,'UNDER_TRANSMISSION':-0.5,
 'ALIGNED_INCOMPLETE':0.5,'ALIGNED_DIRECTION_ONLY':1.0,'ALIGNED':1.5,'OVER_TRANSMISSION':2.0,
 'NOT_YET_OBSERVABLE':-1.0,'UNDETERMINED':0.0
}
MAG_RANK={'VERY_LOW':0,'LOW':1,'MEDIUM':2,'HIGH':3,'VERY_HIGH':4,'EXTREME':5}

class LatentReleaseError(ValueError): pass

def _dt(s):
    if not s: return None
    d=datetime.fromisoformat(str(s).replace('Z','+00:00'))
    if d.tzinfo is None: d=d.replace(tzinfo=timezone.utc)
    return d.astimezone(timezone.utc)

def _stable_hash(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':'),default=str).encode()).hexdigest()

def _pressure_fingerprint(p):
    obj={
      'pressure_core':p.get('pressure_core'),'pressure_dynamics':p.get('pressure_dynamics'),
      'fundamental_driver_consumption':p.get('fundamental_driver_consumption'),'remaining_causal_pressure':p.get('remaining_causal_pressure'),
      'persistence':p.get('persistence'),'contradiction_load':p.get('contradiction_load')
    }
    return _stable_hash(obj)

def _transmission_fingerprint(t):
    obj={k:t.get(k) for k in ['upstream_pressure_reference','target_response','transmission_state','counterfactual_residual','transmission_efficiency','pathway_diagnostics','model_disagreement','missing_driver_escalation']}
    return _stable_hash(obj)

def _consumption_level(p):
    x=str(((p.get('fundamental_driver_consumption') or {}).get('state')) or '').upper()
    if any(k in x for k in ['EXHAUST','FULLY_CONSUMED','HIGH_CONSUM']): return 'HIGH'
    if any(k in x for k in ['PARTIAL','MEDIUM','ABSORB']): return 'MEDIUM'
    if any(k in x for k in ['FRESH','UNCONSUM','LOW','EARLY']): return 'LOW'
    return 'UNKNOWN'

def _remaining_rank(p):
    r=p.get('remaining_causal_pressure') or {}
    x=str(r.get('class') or r.get('state') or '').upper()
    if x in MAG_RANK: return MAG_RANK[x]
    if 'VERY_HIGH' in x: return 4
    if 'HIGH' in x: return 3
    if 'MEDIUM' in x or 'MODERATE' in x: return 2
    if 'LOW' in x: return 1
    return None

def _persistence_material(p):
    x=str(((p.get('persistence') or {}).get('class')) or ((p.get('persistence') or {}).get('state')) or '').upper()
    if not x or x=='UNKNOWN': return False
    return any(k in x for k in ['MULTI_DAY','STRUCTURAL','SESSION','HIGH','PERSIST','1_6H','2_10D'])

def _pressure_mag_rank(p):
    x=str(((p.get('pressure_core') or {}).get('magnitude_class')) or '').upper()
    return MAG_RANK.get(x)

def _confidence_class(p):
    return str(((p.get('pressure_confidence') or {}).get('class')) or 'UNKNOWN').upper()

def _fresh_obs(obs,as_of):
    st=str(obs.get('status','PRESENT')).upper()
    if st=='NOT_APPLICABLE': return 'NOT_APPLICABLE'
    if st!='PRESENT': return 'UNAVAILABLE'
    od=_dt(obs.get('observed_at_utc'))
    if od is None: return 'UNAVAILABLE'
    if od>as_of: raise LatentReleaseError('future-dated independent evidence: '+str(obs.get('evidence_id')))
    ttl=obs.get('freshness_ttl_seconds')
    if ttl in (None,''): return 'PRESENT'
    ttl=float(ttl)
    if ttl<=0: raise LatentReleaseError('freshness_ttl_seconds must be positive')
    return 'PRESENT' if (as_of-od).total_seconds()<=ttl else 'EXPIRED'

def _normalize_evidence(packet,as_of,horizon):
    if not isinstance(packet,dict): raise LatentReleaseError('evidence_packet required')
    if packet.get('active_horizon')!=horizon: raise LatentReleaseError('evidence horizon mismatch')
    pa=_dt(packet.get('as_of_utc'))
    if pa is None or pa>as_of: raise LatentReleaseError('invalid evidence packet as_of')
    out=[]; ids=set()
    for raw in packet.get('observations') or []:
        if not isinstance(raw,dict): raise LatentReleaseError('evidence observation must be object')
        o=deepcopy(raw); eid=str(o.get('evidence_id') or '')
        if not eid or eid in ids: raise LatentReleaseError('duplicate/missing evidence_id')
        ids.add(eid)
        dom=str(o.get('domain') or '').upper(); role=str(o.get('role') or '').upper(); sk=str(o.get('source_kind') or '').upper()
        if dom not in ALLOWED_DOMAINS: raise LatentReleaseError('unregistered evidence domain: '+eid)
        if role not in ROLES: raise LatentReleaseError('unregistered evidence role: '+eid)
        if sk in FORBIDDEN_SOURCE_KINDS or sk not in ALLOWED_SOURCE_KINDS: raise LatentReleaseError('forbidden/unregistered source_kind: '+eid)
        if bool(o.get('target_price_derived',False)): raise LatentReleaseError('target-price-derived independent evidence forbidden: '+eid)
        if not str(o.get('independence_group') or '').strip(): raise LatentReleaseError('independence_group required: '+eid)
        if str(o.get('strength','')).upper() not in {'LOW','MEDIUM','HIGH'}: raise LatentReleaseError('invalid strength: '+eid)
        c=o.get('confidence')
        if not isinstance(c,(int,float)) or c<0 or c>100: raise LatentReleaseError('confidence 0..100 required: '+eid)
        if not str(o.get('provenance_ref') or '').strip(): raise LatentReleaseError('provenance_ref required: '+eid)
        fs=_fresh_obs(o,as_of); o['freshness_state']=fs; o['role']=role; o['domain']=dom; o['source_kind']=sk
        out.append(o)
    return out

def _groups(obs,roles,*,min_strength='LOW'):
    rank={'LOW':1,'MEDIUM':2,'HIGH':3}; need=rank[min_strength]; g=set()
    for o in obs:
        if o.get('freshness_state')!='PRESENT' or o.get('role') not in roles: continue
        if rank.get(str(o.get('strength')).upper(),0)<need: continue
        if float(o.get('confidence',0))<40: continue
        g.add(str(o.get('independence_group')))
    return g

def _summary(obs):
    present=[o for o in obs if o.get('freshness_state')=='PRESENT']
    unavailable=[o for o in obs if o.get('freshness_state') in {'UNAVAILABLE','EXPIRED'}]
    groups=set(str(o.get('independence_group')) for o in present)
    return {'present_observations':len(present),'unavailable_or_expired':len(unavailable),'independent_group_count':len(groups),'domains':sorted(set(o.get('domain') for o in present))}

def _maturity(obs,current_tstate):
    veto=_groups(obs,HARD_VETO_ROLES,min_strength='MEDIUM')
    active=_groups(obs,ACTIVE_ROLES,min_strength='MEDIUM')
    exhaust=_groups(obs,EXHAUSTION_ROLES,min_strength='MEDIUM')
    release=_groups(obs,{'RELEASE_SUPPORT'},min_strength='MEDIUM')
    if veto:
        state='ACTIVE'
    elif not active and not exhaust:
        state='UNRESOLVED'
    elif len(exhaust)>=3 and len(active)==0 and len(release)>=1:
        state='EXHAUSTED'
    elif len(exhaust)>=2 and len(active)<=1:
        state='EXHAUSTING'
    elif len(exhaust)>=1 and len(exhaust)>=len(active):
        state='MATURE'
    elif len(active)>=1:
        state='ACTIVE' if current_tstate=='NEGATIVE_TRANSMISSION' or len(active)>=2 else 'FORMING'
    else:
        state='UNRESOLVED'
    total=len(active|exhaust|veto)
    conf='HIGH' if total>=4 else ('MEDIUM' if total>=2 else 'LOW')
    return {'state':state,'confidence':conf,'active_opposition_groups':sorted(active),'exhaustion_groups':sorted(exhaust),'hard_veto_groups':sorted(veto),'release_support_groups':sorted(release),'price_distance_used':False,'elapsed_time_used_as_maturity_evidence':False}

def _inflection(current,history):
    cur=str(((current.get('transmission_state') or {}).get('state')) or 'UNDETERMINED')
    valid=[]
    for h in history or []:
        if isinstance(h,dict):
            st=str(((h.get('transmission_state') or {}).get('state')) or '')
            if st in TRANSMISSION_RANK: valid.append(st)
    if not valid or cur not in TRANSMISSION_RANK:
        return {'state':'UNKNOWN','prior_state':None,'current_state':cur,'rank_delta':None}
    prev=valid[-1]; d=TRANSMISSION_RANK[cur]-TRANSMISSION_RANK[prev]
    if d>=1.5: s='IMPROVING_FAST'
    elif d>0: s='IMPROVING'
    elif d<0: s='DETERIORATING'
    else: s='STABLE'
    return {'state':s,'prior_state':prev,'current_state':cur,'rank_delta':round(d,3)}

def _unreleased(p,t,obs,research_blocked):
    pm=_pressure_mag_rank(p); rr=_remaining_rank(p); pc=_confidence_class(p); cons=_consumption_level(p); pers=_persistence_material(p)
    ts=str(((t.get('transmission_state') or {}).get('state')) or 'UNDETERMINED')
    residual=t.get('counterfactual_residual') or {}; eff=t.get('transmission_efficiency') or {}
    support=_groups(obs,{'PRESSURE_SUPPORT_PERSISTENT'},min_strength='MEDIUM')
    reasons=[]; caps=[]
    if research_blocked:
        return {'class':'UNDETERMINED','confidence':'LOW','ordinal_score':None,'reasons':['P02_RECOMPUTE_OR_MISSING_DRIVER_RESOLUTION_REQUIRED'],'caps':['RESEARCH_BLOCKED'],'not_probability':True}
    if pm is None or rr is None or pc=='LOW':
        return {'class':'UNDETERMINED','confidence':'LOW','ordinal_score':None,'reasons':['INSUFFICIENT_UPSTREAM_CONFIDENCE_OR_REMAINING_PRESSURE'],'caps':['UPSTREAM_UNCERTAINTY'],'not_probability':True}
    score=0
    if pm>=4: score+=3; reasons.append('PRESSURE_VERY_HIGH_OR_MORE')
    elif pm>=3: score+=2; reasons.append('PRESSURE_HIGH')
    elif pm>=2: score+=1; reasons.append('PRESSURE_MEDIUM')
    if rr>=3: score+=2; reasons.append('REMAINING_CAUSAL_PRESSURE_HIGH')
    elif rr>=2: score+=1; reasons.append('REMAINING_CAUSAL_PRESSURE_MEDIUM')
    if pers: score+=1; reasons.append('PERSISTENCE_MATERIAL')
    if cons=='LOW': score+=1; reasons.append('DRIVER_CONSUMPTION_LOW')
    elif cons=='HIGH': score-=1; reasons.append('DRIVER_CONSUMPTION_HIGH')
    if ts in {'NEGATIVE_TRANSMISSION','COMPRESSION'}: score+=2; reasons.append('TRANSMISSION_NOT_EXPRESSED')
    elif ts in {'DELAYED','UNDER_TRANSMISSION','ALIGNED_INCOMPLETE'}: score+=1; reasons.append('TRANSMISSION_PARTIAL_OR_DELAYED')
    elif ts=='OVER_TRANSMISSION': score-=2; reasons.append('PRICE_OVER_TRANSMITTED')
    if residual.get('state')=='BELOW_EXPECTATION' and residual.get('magnitude_class') in {'LARGE','EXTREME'}:
        score+=1; reasons.append('LARGE_NEGATIVE_COUNTERFACTUAL_RESIDUAL')
    if str(eff.get('class')).upper() in {'NEGATIVE','VERY_LOW'}:
        score+=1; reasons.append('LOW_OR_NEGATIVE_TRANSMISSION_EFFICIENCY')
    if support: score+=1; reasons.append('INDEPENDENT_PRESSURE_CONTINUITY_SUPPORT')
    if score<=2: cls='LOW'
    elif score<=4: cls='MEDIUM'
    elif score<=6: cls='HIGH'
    else: cls='VERY_HIGH'
    # Remaining causal capacity and causal consumption are hard semantic caps.
    if rr<=1 and cls in {'HIGH','VERY_HIGH'}:
        cls='MEDIUM'; caps.append('LOW_REMAINING_CAUSAL_PRESSURE_CAP')
    if cons=='HIGH' and cls=='VERY_HIGH':
        cls='HIGH'; caps.append('HIGH_DRIVER_CONSUMPTION_CAP')
    # P03 research escalation caps pre-calibration confidence/class.
    mel=str(((t.get('missing_driver_escalation') or {}).get('level')) or 'NONE').upper()
    if mel=='RESEARCH_ESCALATION' and cls=='VERY_HIGH':
        cls='HIGH'; caps.append('P03_RESEARCH_ESCALATION_CAP')
    conf='HIGH' if pc=='HIGH' and len(support)>=1 else ('MEDIUM' if pc in {'HIGH','MEDIUM'} else 'LOW')
    if mel=='RESEARCH_ESCALATION': conf='LOW'
    return {'class':cls,'confidence':conf,'ordinal_score':score,'reasons':reasons,'caps':caps,'not_probability':True,'price_distance_used':False}

def _reserve(unreleased,maturity):
    u=str(unreleased.get('class')); m=str(maturity.get('state'))
    if u=='UNDETERMINED': return {'class':'UNDETERMINED','not_expected_return':True}
    if u=='LOW': c='LOW'
    elif u=='MEDIUM': c='BUILDING'
    elif u=='HIGH' and m in {'MATURE','EXHAUSTING','EXHAUSTED'}: c='HIGH'
    elif u=='VERY_HIGH' and m in {'EXHAUSTING','EXHAUSTED'}: c='VERY_HIGH'
    elif u in {'HIGH','VERY_HIGH'}: c='ELEVATED'
    else: c='BUILDING'
    return {'class':c,'not_expected_return':True,'not_probability':True}

def _hypothesis(obs,role):
    g=_groups(obs,{role},min_strength='MEDIUM')
    if len(g)>=3: s='STRONGLY_SUPPORTED'
    elif len(g)>=2: s='SUPPORTED'
    elif len(g)==1: s='UNCONFIRMED'
    else: s='UNSUPPORTED'
    return {'status':s,'independent_support_groups':sorted(g),'confirmation_claim_allowed':False}

def _readiness(unreleased,maturity,inflection,obs,research_blocked):
    if research_blocked: return {'state':'BLOCKED_UNRESOLVED','reasons':['RESEARCH_BLOCKER_ACTIVE'],'event_cap_applied':False}
    u=unreleased.get('class'); m=maturity.get('state'); inf=inflection.get('state')
    rel=_groups(obs,{'RELEASE_SUPPORT'},min_strength='MEDIUM')
    opp=_groups(obs,{'RELEASE_OPPOSITION'},min_strength='MEDIUM')
    evt=_groups(obs,{'EVENT_RESET_RISK'},min_strength='HIGH')
    reasons=[]
    if u not in {'HIGH','VERY_HIGH'}:
        state='NOT_READY'; reasons.append('UNRELEASED_PRESSURE_NOT_HIGH')
    elif m in {'UNRESOLVED','FORMING','ACTIVE'}:
        state='WATCH'; reasons.append('OPPOSING_MOVE_NOT_MATURE')
    elif m in {'MATURE','EXHAUSTING','EXHAUSTED'} and inf in {'UNKNOWN','STABLE','DETERIORATING'}:
        state='PRE_RELEASE'; reasons.append('MATURITY_PRESENT_BUT_TRANSMISSION_NOT_IMPROVING')
    elif m in {'MATURE','EXHAUSTING','EXHAUSTED'} and inf in {'IMPROVING','IMPROVING_FAST'} and len(rel)>=1 and len(opp)==0:
        state='HIGH_READINESS'; reasons.append('MATURE_OPPOSITION_PLUS_IMPROVING_TRANSMISSION_PLUS_INDEPENDENT_RELEASE_SUPPORT')
    else:
        state='PRE_RELEASE'; reasons.append('PARTIAL_RELEASE_EVIDENCE')
    cap=False
    if evt and state in {'PRE_RELEASE','HIGH_READINESS'}:
        state='WATCH'; cap=True; reasons.append('HIGH_EVENT_RESET_RISK_CAP')
    if opp and state=='HIGH_READINESS':
        state='PRE_RELEASE'; reasons.append('INDEPENDENT_RELEASE_OPPOSITION')
    return {'state':state,'reasons':reasons,'independent_release_support_groups':sorted(rel),'release_opposition_groups':sorted(opp),'event_reset_groups':sorted(evt),'event_cap_applied':cap,'not_probability':True,'trade_permission_granted':False}

def _lifecycle(p,t,maturity,unreleased,readiness,inflection,obs,history):
    ts=str(((t.get('transmission_state') or {}).get('state')) or 'UNDETERMINED')
    prior_t=inflection.get('prior_state'); m=maturity.get('state'); u=unreleased.get('class'); r=readiness.get('state')
    rel=_groups(obs,{'RELEASE_SUPPORT'},min_strength='MEDIUM')
    veto=_groups(obs,HARD_VETO_ROLES,min_strength='MEDIUM')
    cons=_consumption_level(p); rr=_remaining_rank(p); ptr=str(((p.get('pressure_dynamics') or {}).get('trend')) or 'UNKNOWN').upper()
    prior_lifecycle=None
    for h in history or []:
        if isinstance(h,dict) and (h.get('release_lifecycle') or {}).get('state'):
            prior_lifecycle=(h.get('release_lifecycle') or {}).get('state')
    evidence=[]
    if veto: return {'state':'UNDETERMINED','evidence':['FRESH_OR_REPLACEMENT_OPPOSING_DRIVER_PRESENT'],'independent_release_groups':sorted(rel),'price_flip_alone_sufficient':False}
    if prior_lifecycle in {'RELEASE','EXPANSION'} and ts in {'ALIGNED','OVER_TRANSMISSION'}:
        if cons=='HIGH' or (rr is not None and rr<=1) or ptr in {'FALLING','FALLING_FAST'}:
            state='CONSUMPTION'; evidence.append('UPSTREAM_CAUSAL_CAPACITY_CONSUMING')
        else:
            state='EXPANSION'; evidence.append('POST_RELEASE_ALIGNED_TRANSMISSION_CONTINUES')
    elif prior_lifecycle=='CONSUMPTION' and cons=='HIGH' and (rr is not None and rr<=1):
        state='EXHAUSTION'; evidence.append('HIGH_DRIVER_CONSUMPTION_AND_LOW_REMAINING_PRESSURE')
    elif ts in {'ALIGNED','OVER_TRANSMISSION'} and prior_t in {'NEGATIVE_TRANSMISSION','COMPRESSION','UNDER_TRANSMISSION','DELAYED'} and m in {'EXHAUSTING','EXHAUSTED'} and u in {'HIGH','VERY_HIGH'} and len(rel)>=2 and r=='HIGH_READINESS':
        state='RELEASE'; evidence.extend(['TRANSMISSION_FLIPPED_ALIGNED','OPPOSING_MOVE_EXHAUSTING','UNRELEASED_PRESSURE_HIGH','TWO_INDEPENDENT_RELEASE_GROUPS'])
    elif ts in {'ALIGNED_INCOMPLETE','ALIGNED_DIRECTION_ONLY','ALIGNED'} and prior_t in {'NEGATIVE_TRANSMISSION','COMPRESSION','UNDER_TRANSMISSION','DELAYED'} and m in {'MATURE','EXHAUSTING','EXHAUSTED'} and u in {'HIGH','VERY_HIGH'} and len(rel)>=1:
        state='RELEASE_CANDIDATE'; evidence.extend(['TRANSMISSION_INFLECTION','MATURE_OPPOSING_MOVE','INDEPENDENT_RELEASE_SUPPORT'])
    elif r=='HIGH_READINESS':
        state='PRE_RELEASE'; evidence.append('HIGH_READINESS_BEFORE_RELEASE_CONFIRMATION')
    elif ts=='NEGATIVE_TRANSMISSION' and m in {'FORMING','ACTIVE'}:
        state='OPPOSING_MOVE_ACTIVE'; evidence.append('NEGATIVE_TRANSMISSION_WITH_ACTIVE_OPPOSITION')
    elif ts in {'NEGATIVE_TRANSMISSION','COMPRESSION','UNDER_TRANSMISSION'}:
        state='DIVERGENCE'; evidence.append('PRESSURE_PRICE_DIVERGENCE')
    elif ptr in {'RISING','RISING_FAST'} and ts in {'DELAYED','COMPRESSION','NOT_YET_OBSERVABLE'}:
        state='PRESSURE_BUILDING'; evidence.append('PRESSURE_BUILDING_WITHOUT_FULL_TRANSMISSION')
    else:
        state='UNDETERMINED'
    return {'state':state,'evidence':evidence,'independent_release_groups':sorted(rel),'price_flip_alone_sufficient':False,'trade_permission_granted':False}

def build_latent_release(pressure:dict, transmission:dict, evidence_packet:dict, *, transmission_history=None, lifecycle_history=None):
    try:
        if not isinstance(pressure,dict) or pressure.get('status')!='PASS' or ((pressure.get('integrity') or {}).get('status')!='PASS'):
            raise LatentReleaseError('P02 Pressure integrity PASS required')
        if not isinstance(transmission,dict) or transmission.get('status')!='PASS' or ((transmission.get('integrity') or {}).get('status')!='PASS'):
            raise LatentReleaseError('P03 Transmission integrity PASS required')
        pfp=_pressure_fingerprint(pressure)
        if str(((transmission.get('upstream_pressure_reference') or {}).get('fingerprint')) or '')!=pfp:
            raise LatentReleaseError('P03 does not reference exact supplied P02 Pressure fingerprint')
        h=pressure.get('active_horizon')
        if not h or h!=(transmission.get('upstream_pressure_reference') or {}).get('active_horizon'):
            raise LatentReleaseError('P02/P03 active horizon mismatch')
        as_of=_dt(((transmission.get('response_window') or {}).get('end_utc')) or pressure.get('as_of_utc'))
        if as_of is None: raise LatentReleaseError('P04 as_of unavailable')
        obs=_normalize_evidence(evidence_packet,as_of,h)
        veto=_groups(obs,HARD_VETO_ROLES,min_strength='MEDIUM')
        missing=str(((transmission.get('missing_driver_escalation') or {}).get('level')) or 'NONE').upper()
        research_blocked=bool(veto) or missing=='DECISION_CRITICAL'
        maturity=_maturity(obs,str(((transmission.get('transmission_state') or {}).get('state')) or 'UNDETERMINED'))
        inflection=_inflection(transmission,transmission_history)
        unreleased=_unreleased(pressure,transmission,obs,research_blocked)
        reserve=_reserve(unreleased,maturity)
        readiness=_readiness(unreleased,maturity,inflection,obs,research_blocked)
        lifecycle=_lifecycle(pressure,transmission,maturity,unreleased,readiness,inflection,obs,lifecycle_history)
        blockers=[]
        if veto: blockers.append({'type':'P02_RECOMPUTE_REQUIRED','reason':'NEW_OR_REPLACEMENT_CAUSAL_DRIVER_AGAINST_FROZEN_PRESSURE','groups':sorted(veto)})
        if missing=='DECISION_CRITICAL': blockers.append({'type':'MISSING_DRIVER_DECISION_CRITICAL','reason':'P03_UNMODELED_DRIVER_RISK_UNRESOLVED'})
        if missing=='RESEARCH_ESCALATION': blockers.append({'type':'RESEARCH_ESCALATION','reason':'P03_DISAGREEMENT_REQUIRES_RESEARCH','blocking':False})
        conf_inputs=[unreleased.get('confidence'),maturity.get('confidence'),(transmission.get('transmission_confidence') or {}).get('class')]
        if research_blocked: conf='LOW'
        elif conf_inputs.count('HIGH')>=2: conf='HIGH'
        elif 'LOW' in conf_inputs: conf='LOW'
        else: conf='MEDIUM'
        out={
          'schema_version':'1.0.0','phase':PHASE,'version':VERSION,'deployment':DEPLOYMENT,'status':'PASS',
          'as_of_utc':as_of.isoformat().replace('+00:00','Z'),'active_horizon':h,
          'upstream_pressure_reference':{'fingerprint':pfp,'class':(pressure.get('pressure_core') or {}).get('class'),'sign':(pressure.get('pressure_core') or {}).get('sign'),'immutable':True},
          'upstream_transmission_reference':{'fingerprint':_transmission_fingerprint(transmission),'state':(transmission.get('transmission_state') or {}).get('state'),'immutable':True},
          'evidence_summary':_summary(obs),
          'unreleased_pressure':unreleased,
          'opposing_move_maturity':maturity,
          'transmission_inflection':inflection,
          'latent_causal_reserve':reserve,
          'release_readiness':readiness,
          'release_lifecycle':lifecycle,
          'liquidity_hypotheses':{
             'absorption':_hypothesis(obs,'ABSORPTION_EVIDENCE'),
             'liquidity_sweep':_hypothesis(obs,'LIQUIDITY_SWEEP_EVIDENCE'),
             'definitive_confirmation_allowed':False
          },
          'research_blockers':blockers,
          'confidence':{'class':conf,'not_probability':True},
          'integrity':{
             'status':'PASS','pressure_mutated':False,'transmission_mutated':False,'target_price_used_as_independent_evidence':False,
             'price_distance_used_for_maturity':False,'time_elapsed_used_for_maturity':False,'release_from_price_alone':False,
             'trade_permission_granted':False,'broker_authority':'NONE','anti_storytelling_pass':True
          }
        }
        return out
    except Exception as e:
        return {'schema_version':'1.0.0','phase':PHASE,'version':VERSION,'deployment':DEPLOYMENT,'status':'FAIL_CLOSED','integrity':{'status':'FAIL_CLOSED','pressure_mutated':False,'transmission_mutated':False,'target_price_used_as_independent_evidence':False,'release_from_price_alone':False,'trade_permission_granted':False,'broker_authority':'NONE','anti_storytelling_pass':True,'diagnostics':[str(e)]}}

def stable_latent_release_fingerprint(state):
    obj={k:state.get(k) for k in ['upstream_pressure_reference','upstream_transmission_reference','unreleased_pressure','opposing_move_maturity','transmission_inflection','latent_causal_reserve','release_readiness','release_lifecycle','liquidity_hypotheses','research_blockers']}
    return _stable_hash(obj)
