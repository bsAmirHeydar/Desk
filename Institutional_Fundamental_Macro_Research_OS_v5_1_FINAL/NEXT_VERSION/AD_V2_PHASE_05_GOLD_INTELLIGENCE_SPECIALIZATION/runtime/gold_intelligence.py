#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
from copy import deepcopy
from datetime import datetime, timezone
import json, hashlib

PHASE='AD-V2-P05'; VERSION='0.5.0'; DEPLOYMENT='SHADOW_ONLY'
P04_SOURCE_KIND_BY_DOMAIN={
 'FLOW':'VERIFIED_FLOW','POSITIONING':'POSITIONING_STATE','FUNDING_LIQUIDITY':'FUNDING_LIQUIDITY_STATE',
 'MECHANICS':'MECHANICS_STATE','OPTIONS_DEALER':'OPTIONS_DEALER_STATE','PHYSICAL_BALANCE':'PHYSICAL_BALANCE',
 'EVENT_STATE':'EVENT_STATE','CROSS_ASSET_CAUSAL':'CROSS_ASSET_CAUSAL_STATE','STRUCTURAL':'STRUCTURAL_STATE','MARKET_LIQUIDITY':'MARKET_LIQUIDITY_STATE'}
P04_DOMAIN_FOR_METRIC={
 'ETF_HOLDINGS_FLOW':'FLOW','ETF_SPONSOR_SHARES_HOLDINGS':'FLOW','CFTC_GOLD_POSITIONING':'POSITIONING',
 'GC_SIGNED_TRADE_IMBALANCE':'FLOW','GC_DEPTH_RESILIENCY':'MARKET_LIQUIDITY','GC_DEALER_CONVEXITY_MODEL':'OPTIONS_DEALER',
 'COMEX_STOCKS_DELIVERIES':'PHYSICAL_BALANCE','ASIA_PHYSICAL_BALANCE':'PHYSICAL_BALANCE','USD_FUNDING_STATE':'FUNDING_LIQUIDITY',
 'DEALER_BALANCE_SHEET_STATE':'FUNDING_LIQUIDITY','TREASURY_AUCTION_EVENT':'EVENT_STATE','US_MACRO_EVENT':'EVENT_STATE',
 'RETAIL_SALES_EVENT':'EVENT_STATE','GEOPOLITICAL_RISK_STATE':'EVENT_STATE','GOLD_FINANCING_STATE':'FUNDING_LIQUIDITY'}

class GoldSpecializationError(ValueError): pass

def _dt(s):
    if not s: return None
    try:
        x=str(s).replace('Z','+00:00'); d=datetime.fromisoformat(x)
        if d.tzinfo is None: d=d.replace(tzinfo=timezone.utc)
        return d.astimezone(timezone.utc)
    except Exception: return None

def _hash(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':'),default=str).encode()).hexdigest()

def _base(): return Path(__file__).resolve().parents[1]/'config'

def load_registries():
    b=_base(); names=['gold_source_registry','gold_instrument_ontology','gold_pressure_root_registry','gold_evidence_role_registry','gold_transmission_pathway_registry','gold_independence_registry','gold_event_window_registry','gold_observability_matrix','gold_release_evidence_policy','gold_missing_driver_search_registry']
    return {n:json.loads((b/(n+'.json')).read_text(encoding='utf-8')) for n in names}

def _indexes(reg):
    src={x['source_id']:x for x in reg['gold_source_registry']['sources']}
    met={x['metric_id']:x for x in reg['gold_evidence_role_registry']['metrics']}
    roots={x['root_id']:x for x in reg['gold_pressure_root_registry']['root_families']}
    return src,met,roots

def _fresh(obs,metric,as_of):
    od=_dt(obs.get('observed_at_utc')); ttl=obs.get('freshness_ttl_seconds',metric.get('ttl_seconds'))
    if od is None: raise GoldSpecializationError('observed_at_utc required: '+str(obs.get('observation_id')))
    if od>as_of: raise GoldSpecializationError('future observation forbidden: '+str(obs.get('observation_id')))
    if not isinstance(ttl,(int,float)) or ttl<0: raise GoldSpecializationError('invalid freshness ttl')
    age=max(0,(as_of-od).total_seconds())
    return {'age_seconds':round(age,3),'ttl_seconds':float(ttl),'state':'FRESH' if age<=float(ttl) else 'EXPIRED'}

def _runtime_provider_required(source,obs):
    if source.get('access')=='RUNTIME_PROVIDER_REQUIRED' and not str(obs.get('provider_id','')).strip():
        raise GoldSpecializationError('runtime market feed requires provider_id: '+source['source_id'])

def _normalize(observations,as_of,horizon,src,met):
    out=[]; ids=set()
    for raw in observations:
        if not isinstance(raw,dict): raise GoldSpecializationError('observation must be object')
        o=deepcopy(raw); oid=o.get('observation_id'); mid=o.get('metric_id'); sid=o.get('source_id')
        if not oid or oid in ids: raise GoldSpecializationError('duplicate/missing observation_id')
        ids.add(oid)
        if mid not in met: raise GoldSpecializationError('unregistered metric_id: '+str(mid))
        m=met[mid]
        if sid!=m.get('source_id') or sid not in src: raise GoldSpecializationError('metric/source mismatch: '+str(oid))
        s=src[sid]; _runtime_provider_required(s,o)
        if horizon not in m.get('horizons',[]): raise GoldSpecializationError('metric horizon mismatch: '+str(mid))
        st=str(o.get('status','AVAILABLE')).upper()
        if st not in {'AVAILABLE','UNAVAILABLE','LICENSED_REQUIRED','NOT_APPLICABLE'}: raise GoldSpecializationError('invalid observation status')
        fr=_fresh(o,m,as_of) if st=='AVAILABLE' else {'age_seconds':None,'ttl_seconds':m.get('ttl_seconds'),'state':'UNAVAILABLE'}
        # Model lineage for dealer/convexity claims is mandatory.
        if m.get('requires_model_ref') and st=='AVAILABLE' and not str(o.get('model_ref','')).strip():
            raise GoldSpecializationError('model_ref required for '+str(mid))
        # No role override: registry owns semantic authority.
        if 'roles' in o or 'p04_role' in o or 'p02_policy' in o:
            raise GoldSpecializationError('observation role override forbidden: '+str(oid))
        o['_metric']=m; o['_source']=s; o['freshness']=fr
        out.append(o)
    return out

def _p02_candidates(obs,roots,horizon):
    bundles={}
    for o in obs:
        m=o['_metric']; pol=m.get('p02_policy')
        if pol!='EXPLICIT_ROOT_ONLY' or o.get('status','AVAILABLE')!='AVAILABLE' or o['freshness']['state']!='FRESH': continue
        rid=m.get('root_id'); rr=roots.get(rid)
        if not rid or rr is None: raise GoldSpecializationError('unregistered P02 root '+str(rid))
        interp=o.get('causal_interpretation')
        if not isinstance(interp,dict): continue
        polarity=str(interp.get('polarity','')).upper(); mr=interp.get('magnitude_range')
        if polarity not in {'BUY','SELL','NEUTRAL','UNKNOWN'}: raise GoldSpecializationError('invalid causal polarity')
        if polarity in {'BUY','SELL'}:
            if not isinstance(mr,dict) or not isinstance(mr.get('low'),(int,float)) or not isinstance(mr.get('high'),(int,float)): raise GoldSpecializationError('magnitude_range required for root')
            if not (0<=float(mr['low'])<=float(mr['high'])<=100): raise GoldSpecializationError('invalid root magnitude_range')
        mechanism=str(interp.get('mechanism','')).strip()
        if not mechanism: raise GoldSpecializationError('root mechanism required')
        if m.get('target_price_derived'): raise GoldSpecializationError('target-price-derived root forbidden')
        entry={'observation_id':o['observation_id'],'metric_id':m['metric_id'],'source_id':o['source_id'],'root_id':rid,'active_horizon':horizon,'polarity':polarity,'magnitude_range':mr,'source_kind':m.get('source_kind'),'mechanism':mechanism,'provenance_ref':o.get('provenance_ref'),'freshness':o['freshness'],'independence_group':m.get('independence_group'),'eligible_for_p02':True}
        bundles.setdefault(rid,[]).append(entry)
    # Do not aggregate competing observations locally. P02/root-owner adjudication remains downstream.
    return [{'root_id':rid,'candidate_observations':xs,'requires_root_owner_adjudication':len(xs)>1} for rid,xs in sorted(bundles.items())]

def _p03_candidates(obs):
    target=[]; channels=[]; proxies=[]
    for o in obs:
        if o.get('status','AVAILABLE')!='AVAILABLE' or o['freshness']['state']!='FRESH': continue
        m=o['_metric']; roles=set(m.get('roles',[])); x={'observation_id':o['observation_id'],'metric_id':m['metric_id'],'source_id':o['source_id'],'independence_group':m.get('independence_group'),'provider_id':o.get('provider_id'),'observed_at_utc':o.get('observed_at_utc')}
        if 'P03_TARGET_RESPONSE' in roles: target.append(x)
        if 'P03_PATHWAY_CHANNEL' in roles: channels.append(x)
        if 'P03_TARGET_PROXY' in roles or 'P03_CROSS_ASSET_DIAGNOSTIC' in roles: proxies.append(x)
    return {'target_response_candidates':target,'pathway_channel_candidates':channels,'diagnostic_proxy_candidates':proxies,'target_and_gc_price_same_independence_group':True}

def _p04_packet(obs,horizon,as_of):
    rows=[]; excluded=[]
    for o in obs:
        m=o['_metric']; policy=m.get('p04_policy')
        if o.get('status','AVAILABLE')!='AVAILABLE' or o['freshness']['state']!='FRESH':
            excluded.append({'observation_id':o['observation_id'],'reason':'UNAVAILABLE_OR_EXPIRED'}); continue
        if m.get('target_price_derived') or policy in {'FORBIDDEN','NO_RELEASE_COUNT','ACTIVITY_ONLY','CONTEXT_ONLY','STRUCTURAL_PERSISTENCE_ONLY'}:
            excluded.append({'observation_id':o['observation_id'],'reason':policy or 'NOT_P04_EVIDENCE'}); continue
        if policy=='EVENT_ONLY':
            if str(o.get('state_code','')).upper() not in {'EVENT_RESET_RISK','NEW_CAUSAL_DRIVER','REPLACEMENT_OPPOSING_DRIVER'}:
                excluded.append({'observation_id':o['observation_id'],'reason':'EVENT_STATE_NOT_MAPPED'}); continue
            role=str(o.get('state_code')).upper()
        elif policy=='EVENT_OR_STRUCTURAL':
            sc=str(o.get('state_code','')).upper()
            role={'EVENT_RESET_RISK':'EVENT_RESET_RISK','NEW_CAUSAL_DRIVER':'NEW_CAUSAL_DRIVER','PRESSURE_SUPPORT':'PRESSURE_SUPPORT_PERSISTENT'}.get(sc)
            if not role: excluded.append({'observation_id':o['observation_id'],'reason':'STATE_NOT_MAPPED'}); continue
        elif policy=='STATE_MAPPED':
            sc=str(o.get('state_code','')).upper(); role=(m.get('allowed_p04_states') or {}).get(sc)
            if not role: excluded.append({'observation_id':o['observation_id'],'reason':'STATE_NOT_MAPPED'}); continue
        else:
            excluded.append({'observation_id':o['observation_id'],'reason':'POLICY_NOT_ADMITTED'}); continue
        dom=P04_DOMAIN_FOR_METRIC.get(m['metric_id'])
        if not dom: excluded.append({'observation_id':o['observation_id'],'reason':'NO_P04_DOMAIN'}); continue
        strength=str(o.get('strength','MEDIUM')).upper(); confidence=str(o.get('confidence','MEDIUM')).upper()
        if strength not in {'LOW','MEDIUM','HIGH'} or confidence not in {'LOW','MEDIUM','HIGH'}: raise GoldSpecializationError('invalid P04 strength/confidence')
        rows.append({'evidence_id':o['observation_id'],'domain':dom,'role':role,'strength':strength,'confidence':confidence,'independence_group':m.get('independence_group'),'source_kind':P04_SOURCE_KIND_BY_DOMAIN[dom],'source_id':o['source_id'],'provenance_ref':o.get('provenance_ref'),'observed_at_utc':o.get('observed_at_utc'),'freshness_ttl_seconds':m.get('ttl_seconds'),'target_price_derived':False,'status':'AVAILABLE'})
    return {'as_of_utc':as_of.isoformat().replace('+00:00','Z'),'active_horizon':horizon,'observations':rows,'excluded':excluded}

def _event_state(obs):
    ev=[]
    for o in obs:
        m=o['_metric']; roles=set(m.get('roles',[]))
        if 'EVENT_RESET' not in roles or o.get('status','AVAILABLE')!='AVAILABLE' or o['freshness']['state']!='FRESH': continue
        e=o.get('event')
        if not isinstance(e,dict): continue
        state=str(e.get('state','')).upper()
        if state not in {'UPCOMING','ACTIVE','COMPLETED','CANCELLED'}: raise GoldSpecializationError('invalid event state')
        ev.append({'observation_id':o['observation_id'],'metric_id':m['metric_id'],'state':state,'event_time_utc':e.get('event_time_utc'),'materiality':str(e.get('materiality','UNKNOWN')).upper(),'requires_post_event_recompute':bool(e.get('requires_post_event_recompute',True))})
    cap=any(x['state'] in {'UPCOMING','ACTIVE'} and x['materiality'] in {'HIGH','VERY_HIGH','CRITICAL'} for x in ev)
    return {'events':ev,'release_readiness_cap_recommended':'WATCH' if cap else None,'current_calendar_must_be_source_verified':True}

def _coverage(obs,reg):
    fam={x['family']:{'fresh':0,'unavailable':0,'expired':0} for x in reg['gold_observability_matrix']['matrix']}
    # Simple role-based families for runtime coverage receipt.
    mapping={'XAUUSD_RETURN':'TARGET_PRICE','GC_PRICE_RETURN':'TARGET_PRICE','DXY_STATE':'RATES_USD','UST2Y_STATE':'RATES_USD','UST10Y_TIPS_STATE':'RATES_USD','POLICY_REPRICING_STATE':'RATES_USD','ETF_HOLDINGS_FLOW':'ETF_FLOW','ETF_SPONSOR_SHARES_HOLDINGS':'ETF_FLOW','GOLD_DEMAND_TRENDS':'OFFICIAL_DEMAND','CFTC_GOLD_POSITIONING':'FUTURES_POSITIONING','GC_OPEN_INTEREST':'FUTURES_POSITIONING','GC_SIGNED_TRADE_IMBALANCE':'LISTED_ORDER_FLOW','GC_DEPTH_RESILIENCY':'LISTED_ORDER_FLOW','LBMA_TRADE_ACTIVITY':'LONDON_OTC_FLOW','ASIA_PHYSICAL_BALANCE':'PHYSICAL_ASIA','USD_FUNDING_STATE':'FUNDING_GOLD_FINANCING','GOLD_FINANCING_STATE':'FUNDING_GOLD_FINANCING','GC_DEALER_CONVEXITY_MODEL':'OPTIONS_DEALER','GC_OPTIONS_OI':'OPTIONS_DEALER','TREASURY_AUCTION_EVENT':'MECHANICS_EVENT','US_MACRO_EVENT':'MECHANICS_EVENT','RETAIL_SALES_EVENT':'MECHANICS_EVENT'}
    for o in obs:
        f=mapping.get(o['_metric']['metric_id']);
        if not f or f not in fam: continue
        if o.get('status','AVAILABLE')!='AVAILABLE': fam[f]['unavailable']+=1
        elif o['freshness']['state']=='FRESH': fam[f]['fresh']+=1
        else: fam[f]['expired']+=1
    return fam

def _missing_search(reg,transmission,latent):
    escalation=str((((transmission or {}).get('missing_driver_escalation') or {}).get('level')) or 'NONE').upper()
    blockers=(latent or {}).get('research_blockers') or []
    needed=escalation in {'RESEARCH_ESCALATION','DECISION_CRITICAL'} or any(x.get('type') in {'P02_RECOMPUTE_REQUIRED','MISSING_DRIVER_DECISION_CRITICAL'} for x in blockers if isinstance(x,dict))
    return {'required':needed,'trigger':escalation,'priorities':deepcopy(reg['gold_missing_driver_search_registry']['priorities']) if needed else [],'new_causal_driver_requires_p02_recompute':True}

def build_gold_intelligence(observations:list, *, as_of_utc:str, active_horizon:str, upstream_pressure=None, upstream_transmission=None, upstream_latent=None):
    try:
        reg=load_registries(); src,met,roots=_indexes(reg); as_of=_dt(as_of_utc)
        if as_of is None or not active_horizon: raise GoldSpecializationError('as_of_utc and active_horizon required')
        obs=_normalize(observations,as_of,active_horizon,src,met)
        p02=_p02_candidates(obs,roots,active_horizon); p03=_p03_candidates(obs); p04=_p04_packet(obs,active_horizon,as_of); evt=_event_state(obs); cov=_coverage(obs,reg); search=_missing_search(reg,upstream_transmission,upstream_latent)
        # Immutable upstream fingerprints; P05 never mutates upstream science.
        up={'pressure_fingerprint':_hash(upstream_pressure) if isinstance(upstream_pressure,dict) else None,'transmission_fingerprint':_hash(upstream_transmission) if isinstance(upstream_transmission,dict) else None,'latent_fingerprint':_hash(upstream_latent) if isinstance(upstream_latent,dict) else None}
        admitted=[]
        for o in obs:
            admitted.append({'observation_id':o['observation_id'],'metric_id':o['_metric']['metric_id'],'source_id':o['source_id'],'roles':o['_metric'].get('roles',[]),'independence_group':o['_metric'].get('independence_group'),'status':o.get('status','AVAILABLE'),'freshness':o['freshness'],'provider_id':o.get('provider_id')})
        out={'schema_version':'1.0.0','phase':PHASE,'version':VERSION,'deployment':DEPLOYMENT,'status':'PASS','subject':'XAUUSD','as_of_utc':as_of.isoformat().replace('+00:00','Z'),'active_horizon':active_horizon,
             'upstream_references':up,'instrument_topology':deepcopy(reg['gold_instrument_ontology']),'admitted_observations':admitted,'observability_coverage':cov,
             'p02_adapter':{'owner':'AD-V2-P02','root_candidate_bundles':p02,'aggregation_performed_by_p05':False},
             'p03_adapter':{'owner':'AD-V2-P03',**p03,'pathway_templates':deepcopy(reg['gold_transmission_pathway_registry']['pathways'])},
             'p04_adapter':{'owner':'AD-V2-P04','evidence_packet':p04,'release_policy':deepcopy(reg['gold_release_evidence_policy']['gold_rules'])},
             'event_reset':evt,'missing_driver_search':search,
             'coverage_gaps':{'otc_client_dealer_flow':'LICENSED_REQUIRED_OR_UNAVAILABLE','global_physical_financing':'PARTIAL','global_gold_single_venue_complete':False},
             'integrity':{'status':'PASS','p02_mutated':False,'p03_mutated':False,'p04_mutated':False,'target_price_used_as_pressure_root':False,'target_price_used_as_independent_release_evidence':False,'volume_treated_as_directional_flow':False,'oi_treated_as_directional_flow':False,'single_venue_equated_to_global_gold':False,'trade_permission_granted':False,'broker_authority':'NONE'}}
        return out
    except Exception as e:
        return {'schema_version':'1.0.0','phase':PHASE,'version':VERSION,'deployment':DEPLOYMENT,'status':'FAIL_CLOSED','subject':'XAUUSD','integrity':{'status':'FAIL_CLOSED','p02_mutated':False,'p03_mutated':False,'p04_mutated':False,'target_price_used_as_pressure_root':False,'target_price_used_as_independent_release_evidence':False,'volume_treated_as_directional_flow':False,'oi_treated_as_directional_flow':False,'single_venue_equated_to_global_gold':False,'trade_permission_granted':False,'broker_authority':'NONE','diagnostics':[str(e)]}}

def stable_gold_intelligence_fingerprint(state):
    obj={k:state.get(k) for k in ['subject','as_of_utc','active_horizon','upstream_references','admitted_observations','observability_coverage','p02_adapter','p03_adapter','p04_adapter','event_reset','missing_driver_search','coverage_gaps']}
    return _hash(obj)
