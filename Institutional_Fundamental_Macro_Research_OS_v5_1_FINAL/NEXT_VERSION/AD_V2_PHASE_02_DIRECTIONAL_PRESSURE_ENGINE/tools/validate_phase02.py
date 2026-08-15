#!/usr/bin/env python3
from pathlib import Path
import argparse, copy, hashlib, importlib.util, json, sys
sys.dont_write_bytecode=True

def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for c in iter(lambda:f.read(1024*1024),b''): h.update(c)
    return h.hexdigest()

def load(p,name):
    spec=importlib.util.spec_from_file_location(name,p); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def ck(cond,name,detail,rows): rows.append({'name':name,'pass':bool(cond),'detail':detail}); return bool(cond)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--repo-root',required=True); ap.add_argument('--json',action='store_true'); a=ap.parse_args()
    repo=Path(a.repo_root).resolve(); vault=repo/'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL'; phase=vault/'NEXT_VERSION/AD_V2_PHASE_02_DIRECTIONAL_PRESSURE_ENGINE'; p00=vault/'NEXT_VERSION/AD_V2_PHASE_00_PRESSURE_PRICE_CONSTITUTION'; p01=vault/'NEXT_VERSION/AD_V2_PHASE_01_RUNTIME_SEMANTIC_REPAIR'; rows=[]
    deps=json.loads((phase/'baseline/P00_P01_DEPENDENCY_FINGERPRINT.json').read_text(encoding='utf-8'))
    for d in deps['requires']:
        p=vault/d['path']; ck(p.is_file() and sha(p)==d['sha256'],'dependency_'+d['phase'],d['path'],rows)
    pol=json.loads((phase/'config/pressure_classification_policy.json').read_text(encoding='utf-8'))
    ck(pol.get('scale_type')=='ANALYTICAL_ORDINAL_NOT_PROBABILITY','no_false_probability_scale',pol.get('scale_type'),rows)
    bands=pol.get('magnitude_bands',[]); ck([x['name'] for x in bands]==['VERY_LOW','LOW','MEDIUM','HIGH','VERY_HIGH','EXTREME'],'pressure_band_vocabulary',[x['name'] for x in bands],rows)
    src=json.loads((phase/'config/pressure_source_registry.json').read_text(encoding='utf-8'))
    ck('TARGET_PRICE' in src['forbidden_pressure_source_kinds'],'target_price_forbidden',src['forbidden_pressure_source_kinds'],rows)
    ck('CROSS_ASSET_CAUSAL_STATE' in src['allowed_source_kinds'],'cross_asset_causal_allowed',None,rows)
    mod=load(phase/'runtime/directional_pressure.py','ad_p02')
    fixture=json.loads((phase/'tests/fixtures/explicit_gold_pressure.json').read_text(encoding='utf-8'))
    out=mod.build_from_roots(fixture,history=[{'signed_midpoint':50},{'signed_midpoint':54}])
    ck(out['status']=='PASS','explicit_fixture_pass',out.get('integrity'),rows)
    ck(out['pressure_core']['sign']=='BUY','explicit_sign_buy',out['pressure_core'],rows)
    ck(out['pressure_core']['class']=='BUY_HIGH','explicit_class_buy_high',out['pressure_core'],rows)
    ck(out['pressure_core']['scale']=='ANALYTICAL_ORDINAL_NOT_PROBABILITY','explicit_not_probability',out['pressure_core'],rows)
    ck(out['pressure_dynamics']['trend']=='RISING','pressure_trend_from_pressure_history',out['pressure_dynamics'],rows)
    ck(out['pressure_dynamics']['acceleration']=='STEADY','pressure_acceleration',out['pressure_dynamics'],rows)
    ck(out['remaining_causal_pressure']['class']=='HIGH','remaining_causal_pressure_separate',out['remaining_causal_pressure'],rows)
    ck(out['fundamental_driver_consumption']['state']=='PARTIALLY_ABSORBED','driver_consumption_separate',out['fundamental_driver_consumption'],rows)
    ck(out['contradiction_load']['class']=='LOW','contradiction_preserved',out['contradiction_load'],rows)
    ck(all(r['normalized_weight']>0 for r in out['causal_root_ledger']),'root_weights_present',[r['normalized_weight'] for r in out['causal_root_ledger']],rows)
    ck(not any(k in out for k in ['price_transmission','unreleased_pressure','opposing_move_maturity','release_readiness']),'future_fields_absent',list(out),rows)

    # PRICE CONTAMINATION: price context is accepted by the function solely to prove it is ignored.
    a1=mod.build_from_roots(copy.deepcopy(fixture),history=[{'signed_midpoint':50},{'signed_midpoint':54}],target_price_context={'symbol':'XAUUSD','return_pct':+5.0,'price':5000})
    a2=mod.build_from_roots(copy.deepcopy(fixture),history=[{'signed_midpoint':50},{'signed_midpoint':54}],target_price_context={'symbol':'XAUUSD','return_pct':-5.0,'price':4000})
    ck(mod.pressure_core_fingerprint(a1)==mod.pressure_core_fingerprint(a2),'price_contamination_attack',{'up':mod.pressure_core_fingerprint(a1),'down':mod.pressure_core_fingerprint(a2)},rows)
    ck(a1['pressure_core']==a2['pressure_core'],'price_cannot_change_pressure_core',None,rows)

    # Forbidden source kind.
    x=copy.deepcopy(fixture); x['roots'][0]['source_kind']='TARGET_PRICE'; y=mod.build_from_roots(x)
    ck(y['status']=='FAIL_CLOSED','target_price_source_fail_closed',y['integrity'],rows)

    # DXY/cross-asset causal source remains legal with explicit mechanism.
    x=copy.deepcopy(fixture); x['roots']=[x['roots'][1]]; x['roots'][0]['weight']=1.0; y=mod.build_from_roots(x)
    ck(y['status']=='PASS' and y['pressure_core']['sign']=='BUY','cross_asset_causal_not_globally_banned',y.get('pressure_core'),rows)

    # Duplicate root.
    x=copy.deepcopy(fixture); x['roots'].append(copy.deepcopy(x['roots'][0])); y=mod.build_from_roots(x)
    ck(y['status']=='FAIL_CLOSED','duplicate_root_fail_closed',y['integrity'],rows)

    # Dependent root at top-level.
    x=copy.deepcopy(fixture); x['roots'][1]['depends_on_root_ids']=['POLICY_EXPECTATIONS']; y=mod.build_from_roots(x)
    ck(y['status']=='FAIL_CLOSED','dependent_root_double_count_fail',y['integrity'],rows)

    # Horizon mismatch.
    x=copy.deepcopy(fixture); x['roots'][0]['active_horizon']='SESSION_1_6H'; y=mod.build_from_roots(x)
    ck(y['status']=='FAIL_CLOSED','exact_horizon_required',y['integrity'],rows)

    # Unavailable applicable root widens interval and reduces coverage.
    x=copy.deepcopy(fixture); x['roots'][0]['applicability']='UNAVAILABLE'; y=mod.build_from_roots(x)
    ck(y['status']=='PASS' and y['freshness_and_coverage']['unknown_weight']>0,'unavailable_root_kept_as_uncertainty',{'core':y.get('pressure_core'),'coverage':y.get('freshness_and_coverage')},rows)
    ck(y['pressure_core']['signed_range']['low'] < out['pressure_core']['signed_range']['low'],'unavailable_root_widens_low_bound',{'base':out['pressure_core']['signed_range'],'attack':y['pressure_core']['signed_range']},rows)

    # N/A root removed/renormalized rather than becoming uncertainty.
    x=copy.deepcopy(fixture); x['roots'][-1]['applicability']='NOT_APPLICABLE'; y=mod.build_from_roots(x)
    ck(y['status']=='PASS' and abs(sum(r['normalized_weight'] for r in y['causal_root_ledger'])-1)<1e-7,'not_applicable_renormalizes',[r['normalized_weight'] for r in y['causal_root_ledger']],rows)
    ck(y['freshness_and_coverage']['unknown_weight']==0,'not_applicable_not_unknown',y['freshness_and_coverage'],rows)

    # Expired applicable root becomes unavailable.
    x=copy.deepcopy(fixture); x['roots'][0]['observed_at_utc']='2026-08-14T00:00:00Z'; x['roots'][0]['freshness_ttl_seconds']=3600; y=mod.build_from_roots(x)
    r0=next(r for r in y['causal_root_ledger'] if r['root_id']=='POLICY_EXPECTATIONS')
    ck(r0['freshness']['state']=='EXPIRED' and r0['effective_state']=='UNAVAILABLE','expired_root_not_carried',r0['freshness'],rows)

    # Empirical half-life requires validation ref.
    x=copy.deepcopy(fixture); x['roots'][0]['half_life']={'provenance':'EMPIRICAL','range':{'low':2,'high':4,'unit':'hours'}}; y=mod.build_from_roots(x)
    ck(y['status']=='FAIL_CLOSED','empirical_half_life_requires_validation',y['integrity'],rows)

    # P01 legacy-wrap mode.
    p01mod=load(p01/'runtime/semantic_lifecycle.py','ad_p01'); f=json.loads((p01/'tests/fixtures/semantic_valid_gold.json').read_text(encoding='utf-8')); n=p01mod.normalize_v1_artifacts(f['artifacts'],f['active_horizon'])
    leg=mod.build_from_p01(n,as_of_utc='2026-08-15T08:00:00Z',history=[{'signed_midpoint':48},{'signed_midpoint':54}],target_price_context={'return_pct':-12})
    ck(leg['status']=='PASS','legacy_wrap_pass',leg.get('integrity'),rows)
    ck(leg['pressure_core']['sign']=='BUY' and leg['pressure_core']['class']=='BUY_HIGH','legacy_wrap_signs_module89_force',leg['pressure_core'],rows)
    ck(leg['provenance']['target_price_used'] is False,'legacy_target_price_unused',leg['provenance'],rows)
    ck(leg['fundamental_driver_consumption']['value']=='PARTIALLY_ABSORBED','legacy_consumption_owner',leg['fundamental_driver_consumption'],rows)
    ck(leg['remaining_causal_pressure']['value']=='MODERATE','legacy_remaining_pressure_owner',leg['remaining_causal_pressure'],rows)

    # Invalid P01 integrity cannot be rescued.
    bad=copy.deepcopy(n); bad['semantic_integrity']['status']='FAIL_CLOSED'; y=mod.build_from_p01(bad,as_of_utc='2026-08-15T08:00:00Z')
    ck(y['status']=='FAIL_CLOSED','legacy_requires_p01_integrity',y['integrity'],rows)

    # Trend/acceleration must depend on pressure history only.
    y=mod.build_from_roots(fixture,history=[{'signed_midpoint':40,'target_price_return':+20},{'signed_midpoint':48,'target_price_return':-20}],target_price_context={'return_pct':-50})
    ck(y['pressure_dynamics']['trend'] in {'RISING','RISING_FAST'} and y['pressure_dynamics']['acceleration'] in {'STEADY','BUYWARD_ACCELERATION','SELLWARD_ACCELERATION'},'dynamics_pressure_only',y['pressure_dynamics'],rows)

    outj={'status':'PASS' if all(r['pass'] for r in rows) else 'FAIL','phase':'AD-V2-P02','tests':len(rows),'passed':sum(1 for r in rows if r['pass']),'checks':rows}
    print(json.dumps(outj,indent=2) if a.json else f"PHASE 02 VALIDATION: {outj['status']} ({outj['passed']}/{outj['tests']})")
    return 0 if outj['status']=='PASS' else 3
if __name__=='__main__': sys.exit(main())
