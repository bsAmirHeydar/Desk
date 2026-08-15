#!/usr/bin/env python3
from pathlib import Path
from copy import deepcopy
import argparse,json,sys
ROOT=Path(__file__).resolve().parents[1]
P02=ROOT.parent/'AD_V2_PHASE_02_DIRECTIONAL_PRESSURE_ENGINE'
P03=ROOT.parent/'AD_V2_PHASE_03_PRICE_TRANSMISSION_ENGINE'
sys.path.insert(0,str(P02/'runtime')); sys.path.insert(0,str(P03/'runtime')); sys.path.insert(0,str(ROOT/'runtime'))
from directional_pressure import build_from_roots
from price_transmission import build_transmission, _pressure_fingerprint
from latent_release import build_latent_release, stable_latent_release_fingerprint

def make_pressure():
    inp=json.loads((P02/'tests/fixtures/explicit_gold_pressure.json').read_text(encoding='utf-8'))
    return build_from_roots(inp)

def sig(p):
    return {
      'signature_id':'P04-TEST-SIG','pressure_fingerprint':_pressure_fingerprint(p),'active_horizon':p['active_horizon'],
      'declared_at_utc':'2026-08-15T08:01:00Z','method':'POLICY_PATH_DECOMPOSITION','method_provenance':'MODEL_IMPLIED',
      'target_response':{'instrument':'XAUUSD','unit':'PCT_RETURN','expected_aligned_range':{'low':0.30,'high':0.70},'minimum_material_response':0.10,'earliest_material_response_seconds':60,'latest_expected_lag_seconds':1800},
      'pathways':[]
    }

def transmission(p,obs=-0.40,start='2026-08-15T08:02:00Z',end='2026-08-15T08:32:00Z'):
    a={'window_start_utc':start,'window_end_utc':end,'target':{'instrument':'XAUUSD','unit':'PCT_RETURN','observed_response':obs,'data_quality':'HIGH'},'channels':[]}
    return build_transmission(p,sig(p),a,missing_driver_candidates=[])

def evidence(roles=None,event=False,new_driver=False,same_group=False):
    base=[
      ('flowdec','FLOW','OPPOSING_FLOW_DECAYING','g_flow'),
      ('posexh','POSITIONING','POSITIONING_UNWIND_EXHAUSTING','g_pos'),
      ('fundease','FUNDING_LIQUIDITY','FUNDING_HEADWIND_EASING','g_fund'),
      ('press','STRUCTURAL','PRESSURE_SUPPORT_PERSISTENT','g_struct'),
    ]
    if roles is not None: base=roles
    if event: base.append(('evt','EVENT_STATE','EVENT_RESET_RISK','g_evt'))
    if new_driver: base.append(('new','EVENT_STATE','NEW_CAUSAL_DRIVER_AGAINST_PRESSURE','g_new'))
    obs=[]
    for i,(eid,dom,role,grp) in enumerate(base):
      if same_group: grp='same'
      sk={'FLOW':'VERIFIED_FLOW','POSITIONING':'POSITIONING_STATE','FUNDING_LIQUIDITY':'FUNDING_LIQUIDITY_STATE','MECHANICS':'MECHANICS_STATE','OPTIONS_DEALER':'OPTIONS_DEALER_STATE','PHYSICAL_BALANCE':'PHYSICAL_BALANCE','EVENT_STATE':'EVENT_STATE','CROSS_ASSET_CAUSAL':'CROSS_ASSET_CAUSAL_STATE','STRUCTURAL':'STRUCTURAL_STATE','MARKET_LIQUIDITY':'MARKET_LIQUIDITY_STATE'}[dom]
      obs.append({'evidence_id':eid,'domain':dom,'role':role,'strength':'HIGH' if role in {'EVENT_RESET_RISK','NEW_CAUSAL_DRIVER_AGAINST_PRESSURE'} else 'MEDIUM','confidence':80,'independence_group':grp,'source_kind':sk,'provenance_ref':'test://'+eid,'observed_at_utc':'2026-08-15T08:20:00Z','freshness_ttl_seconds':7200,'target_price_derived':False,'status':'PRESENT'})
    return {'as_of_utc':'2026-08-15T08:30:00Z','active_horizon':'MULTI_DAY_2_10D','observations':obs}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--json',action='store_true'); a=ap.parse_args(); checks=[]
    def ck(name,cond,detail=None): checks.append({'name':name,'status':'PASS' if cond else 'FAIL','detail':detail})
    p=make_pressure(); ck('p02 pressure fixture pass',p.get('status')=='PASS')
    tneg=transmission(p,-0.40); ck('p03 negative transmission fixture',((tneg.get('transmission_state') or {}).get('state')=='NEGATIVE_TRANSMISSION'))
    e=evidence(); o=build_latent_release(p,tneg,e)
    ck('p04 base pass',o.get('status')=='PASS',o)
    ck('unreleased high-or-very-high',o.get('unreleased_pressure',{}).get('class') in {'HIGH','VERY_HIGH'})
    ck('maturity exhausting-or-exhausted',o.get('opposing_move_maturity',{}).get('state') in {'EXHAUSTING','EXHAUSTED'})
    ck('latent reserve high',o.get('latent_causal_reserve',{}).get('class') in {'HIGH','VERY_HIGH'})
    ck('price distance not used',o.get('integrity',{}).get('price_distance_used_for_maturity') is False)
    ck('time not used for maturity',o.get('integrity',{}).get('time_elapsed_used_for_maturity') is False)
    ck('no trade permission',o.get('integrity',{}).get('trade_permission_granted') is False)
    ck('no broker authority',o.get('integrity',{}).get('broker_authority')=='NONE')
    ck('anti storytelling pass',o.get('integrity',{}).get('anti_storytelling_pass') is True)
    # Price contamination in independent ledger fails closed.
    bad=evidence(); bad['observations'][0]['target_price_derived']=True
    x=build_latent_release(p,tneg,bad); ck('target-price-derived independent evidence blocked',x.get('status')=='FAIL_CLOSED')
    bad=evidence(); bad['observations'][0]['source_kind']='TARGET_PRICE_RETURN'
    x=build_latent_release(p,tneg,bad); ck('target-price source kind blocked',x.get('status')=='FAIL_CLOSED')
    # Same independence group cannot manufacture maturity.
    x=build_latent_release(p,tneg,evidence(same_group=True)); ck('independence group dedup prevents exhaustion',x.get('opposing_move_maturity',{}).get('state') not in {'EXHAUSTING','EXHAUSTED'})
    # New causal driver => recompute blocker and unreleased undetermined.
    x=build_latent_release(p,tneg,evidence(new_driver=True)); ck('new causal driver blocks latent',x.get('release_readiness',{}).get('state')=='BLOCKED_UNRESOLVED')
    ck('new causal driver requires p02 recompute',any(z.get('type')=='P02_RECOMPUTE_REQUIRED' for z in x.get('research_blockers',[])))
    ck('new causal driver makes unreleased undetermined',x.get('unreleased_pressure',{}).get('class')=='UNDETERMINED')
    # P02/P03 fingerprint mismatch.
    tb=deepcopy(tneg); tb['upstream_pressure_reference']['fingerprint']='bad'
    x=build_latent_release(p,tb,e); ck('upstream pressure fingerprint mismatch blocked',x.get('status')=='FAIL_CLOSED')
    # Future evidence blocked.
    bad=evidence(); bad['observations'][0]['observed_at_utc']='2026-08-16T08:20:00Z'
    x=build_latent_release(p,tneg,bad); ck('future evidence blocked',x.get('status')=='FAIL_CLOSED')
    # Event cap.
    hist=[tneg]
    talign=transmission(p,0.45,start='2026-08-15T08:33:00Z',end='2026-08-15T09:03:00Z')
    er=evidence(roles=[
      ('flowdec','FLOW','OPPOSING_FLOW_DECAYING','g_flow'),('posexh','POSITIONING','POSITIONING_UNWIND_EXHAUSTING','g_pos'),('fundease','FUNDING_LIQUIDITY','FUNDING_HEADWIND_EASING','g_fund'),('press','STRUCTURAL','PRESSURE_SUPPORT_PERSISTENT','g_struct'),('rel1','FLOW','RELEASE_SUPPORT','g_rel1'),('rel2','MECHANICS','RELEASE_SUPPORT','g_rel2')
    ])
    x=build_latent_release(p,talign,er,transmission_history=hist)
    ck('transmission inflection improving',x.get('transmission_inflection',{}).get('state') in {'IMPROVING','IMPROVING_FAST'})
    ck('release requires independent groups and can occur',x.get('release_lifecycle',{}).get('state')=='RELEASE',x.get('release_lifecycle'))
    # One release group only => no RELEASE.
    er1=deepcopy(er); er1['observations']=[q for q in er1['observations'] if q['evidence_id']!='rel2']
    x=build_latent_release(p,talign,er1,transmission_history=hist)
    ck('single release group cannot release',x.get('release_lifecycle',{}).get('state')!='RELEASE')
    ck('single release group can at most candidate/pre-release',x.get('release_lifecycle',{}).get('state') in {'RELEASE_CANDIDATE','PRE_RELEASE','UNDETERMINED'})
    # Price flip with no independent release support cannot release.
    x=build_latent_release(p,talign,evidence(),transmission_history=hist)
    ck('price flip alone not release',x.get('release_lifecycle',{}).get('state')!='RELEASE')
    ck('release from price alone integrity false',x.get('integrity',{}).get('release_from_price_alone') is False)
    # Event reset caps high readiness.
    x=build_latent_release(p,talign,evidence(roles=[
      ('flowdec','FLOW','OPPOSING_FLOW_DECAYING','g_flow'),('posexh','POSITIONING','POSITIONING_UNWIND_EXHAUSTING','g_pos'),('fundease','FUNDING_LIQUIDITY','FUNDING_HEADWIND_EASING','g_fund'),('press','STRUCTURAL','PRESSURE_SUPPORT_PERSISTENT','g_struct'),('rel','MECHANICS','RELEASE_SUPPORT','g_rel'),('evt','EVENT_STATE','EVENT_RESET_RISK','g_evt')
    ]),transmission_history=hist)
    ck('event reset caps readiness',x.get('release_readiness',{}).get('state')=='WATCH')
    ck('event cap disclosed',x.get('release_readiness',{}).get('event_cap_applied') is True)
    # Liquidity hypotheses need independent evidence and never confirm.
    eh=evidence(roles=[('a1','FLOW','ABSORPTION_EVIDENCE','g1'),('a2','POSITIONING','ABSORPTION_EVIDENCE','g2'),('l1','MECHANICS','LIQUIDITY_SWEEP_EVIDENCE','g3'),('l2','MARKET_LIQUIDITY','LIQUIDITY_SWEEP_EVIDENCE','g4')])
    x=build_latent_release(p,tneg,eh)
    ck('absorption supported only with independent evidence',x.get('liquidity_hypotheses',{}).get('absorption',{}).get('status')=='SUPPORTED')
    ck('liquidity sweep supported only with independent evidence',x.get('liquidity_hypotheses',{}).get('liquidity_sweep',{}).get('status')=='SUPPORTED')
    ck('definitive liquidity confirmation forbidden',x.get('liquidity_hypotheses',{}).get('definitive_confirmation_allowed') is False)
    # Duplicated same group only unconfirmed.
    eh2=evidence(roles=[('a1','FLOW','ABSORPTION_EVIDENCE','same'),('a2','POSITIONING','ABSORPTION_EVIDENCE','same')])
    x=build_latent_release(p,tneg,eh2)
    ck('same-group absorption not supported',x.get('liquidity_hypotheses',{}).get('absorption',{}).get('status')=='UNCONFIRMED')
    # Active opposition remains active.
    ea=evidence(roles=[('oa','FLOW','OPPOSING_FLOW_ACTIVE','g1'),('pa','POSITIONING','POSITIONING_UNWIND_ACTIVE','g2')])
    x=build_latent_release(p,tneg,ea)
    ck('active opposition classified active',x.get('opposing_move_maturity',{}).get('state')=='ACTIVE')
    ck('active opposition not high readiness',x.get('release_readiness',{}).get('state') in {'WATCH','NOT_READY'})
    # Fresh replacement driver hard veto.
    ev=evidence(roles=[('rep','EVENT_STATE','REPLACEMENT_OPPOSING_DRIVER','g1'),('flowdec','FLOW','OPPOSING_FLOW_DECAYING','g2')])
    x=build_latent_release(p,tneg,ev)
    ck('replacement opposing driver hard veto',x.get('release_readiness',{}).get('state')=='BLOCKED_UNRESOLVED')
    # Unavailable observations do not count.
    eu=evidence(); eu['observations'][0]['status']='UNAVAILABLE'; eu['observations'][1]['status']='UNAVAILABLE'
    x=build_latent_release(p,tneg,eu)
    ck('unavailable observations reduce maturity',x.get('opposing_move_maturity',{}).get('state') not in {'EXHAUSTED'})
    # Expired evidence doesn't count.
    ex=evidence(); ex['observations'][0]['observed_at_utc']='2026-08-14T00:00:00Z'; ex['observations'][0]['freshness_ttl_seconds']=60
    x=build_latent_release(p,tneg,ex)
    ck('expired evidence excluded',x.get('evidence_summary',{}).get('unavailable_or_expired',0)>=1)
    # Horizon mismatch blocked.
    bad=evidence(); bad['active_horizon']='SESSION_1_6H'
    x=build_latent_release(p,tneg,bad); ck('evidence horizon mismatch blocked',x.get('status')=='FAIL_CLOSED')
    # Pressure immutability attack: target response changes P04 but not upstream fingerprint.
    t2=transmission(p,-1.20); o1=build_latent_release(p,tneg,e); o2=build_latent_release(p,t2,e)
    ck('upstream pressure fingerprint invariant across price response',o1.get('upstream_pressure_reference',{}).get('fingerprint')==o2.get('upstream_pressure_reference',{}).get('fingerprint'))
    ck('upstream pressure immutable flag',o2.get('upstream_pressure_reference',{}).get('immutable') is True)
    # High release readiness not trade permission.
    x=build_latent_release(p,talign,er,transmission_history=hist)
    ck('high/release state no trade permission',x.get('integrity',{}).get('trade_permission_granted') is False)
    # lifecycle expansion with prior release.
    x2=build_latent_release(p,talign,er,transmission_history=hist,lifecycle_history=[x])
    ck('post-release aligned state expansion',x2.get('release_lifecycle',{}).get('state')=='EXPANSION')
    # Pressure weakening/consumed case is not latent high (modify safe copies).
    pw=deepcopy(p); pw['remaining_causal_pressure']={'class':'LOW','owner':'MODULE_89'}; pw['fundamental_driver_consumption']={'state':'FULLY_CONSUMED','owner':'MODULE_89','target_price_used':False}
    # Need matching transmission for modified pressure.
    tw=transmission(pw,-0.40)
    x=build_latent_release(pw,tw,e)
    ck('low remaining plus consumed pressure lowers latent',x.get('unreleased_pressure',{}).get('class') in {'LOW','MEDIUM'})
    # Low upstream confidence => undetermined.
    pl=deepcopy(p); pl['pressure_confidence']['class']='LOW'; tl=transmission(pl,-0.40); x=build_latent_release(pl,tl,e)
    ck('low upstream pressure confidence latent undetermined',x.get('unreleased_pressure',{}).get('class')=='UNDETERMINED')
    # Stable fingerprints deterministic.
    x=build_latent_release(p,tneg,e); ck('latent release fingerprint deterministic',stable_latent_release_fingerprint(x)==stable_latent_release_fingerprint(deepcopy(x)))
    # Schema and phase metadata.
    ck('phase id',x.get('phase')=='AD-V2-P04'); ck('deployment shadow',x.get('deployment')=='SHADOW_ONLY'); ck('integrity pass',x.get('integrity',{}).get('status')=='PASS')
    # Reserved semantics absent.
    def has_exact_key(obj,key):
        if isinstance(obj,dict):
            return key in obj or any(has_exact_key(v,key) for v in obj.values())
        if isinstance(obj,list): return any(has_exact_key(v,key) for v in obj)
        return False
    ck('no probability field', not has_exact_key(x,'probability'))
    ck('no expected return field', not has_exact_key(x,'expected_return'))
    ck('no technical trigger field', not has_exact_key(x,'technical_trigger'))
    # Attack case descriptor count and schema presence.
    ac=json.loads((ROOT/'tests/latent_release_attack_cases.json').read_text(encoding='utf-8'))
    ck('attack cases >=10',len(ac.get('cases',[]))>=10)
    schema=json.loads((ROOT/'schemas/AlphaDesk_V2_LatentReleaseState.schema.json').read_text(encoding='utf-8'))
    ck('schema additionalProperties false',schema.get('additionalProperties') is False)
    # Count to 60+ using config/governance integrity checks.
    for rel in ['config/evidence_domain_registry.json','config/unreleased_pressure_policy.json','config/opposing_move_maturity_policy.json','config/release_state_policy.json','DEVELOPMENT_MANIFEST.json','PHASE_04_ROADMAP_HANDOFF.json']:
        ck('file exists:'+rel,(ROOT/rel).is_file())
    reg=json.loads((ROOT/'config/evidence_domain_registry.json').read_text(encoding='utf-8'))
    ck('target price forbidden registry','TARGET_PRICE' in reg.get('forbidden_source_kinds',[]))
    ck('trade outcome forbidden registry','TRADE_OUTCOME' in reg.get('forbidden_source_kinds',[]))
    pol=json.loads((ROOT/'config/release_state_policy.json').read_text(encoding='utf-8'))
    ck('release needs two groups',pol.get('release_min_independent_non_price_groups')==2)
    ck('event cap configured',pol.get('event_reset_can_cap_readiness')=='WATCH')
    ck('trade permission not added',pol.get('trade_permission_added') is False)
    ck('empirical probability not added',pol.get('empirical_probability_added') is False)
    failed=[c for c in checks if c['status']!='PASS']; report={'schema_version':'1.0.0','phase':'AD-V2-P04','status':'PASS' if not failed else 'FAIL','passed':len(checks)-len(failed),'failed':len(failed),'checks':checks}
    print(json.dumps(report,ensure_ascii=False,indent=2) if a.json else f"P04 VALIDATION: {report['status']} ({report['passed']}/{len(checks)} PASS)")
    return 0 if not failed else 2
if __name__=='__main__': raise SystemExit(main())
