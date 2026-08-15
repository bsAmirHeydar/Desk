#!/usr/bin/env python3
from pathlib import Path
import argparse, hashlib, importlib.util, json, sys, copy
sys.dont_write_bytecode=True

def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for c in iter(lambda:f.read(1024*1024),b''): h.update(c)
    return h.hexdigest()

def load_module(p):
    spec=importlib.util.spec_from_file_location('ad_v2_p01_semantic',p); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def check(cond,name,detail,rows): rows.append({'name':name,'pass':bool(cond),'detail':detail}); return bool(cond)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--repo-root',required=True); ap.add_argument('--json',action='store_true'); a=ap.parse_args()
    repo=Path(a.repo_root).resolve(); vault=repo/'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL'; phase=vault/'NEXT_VERSION/AD_V2_PHASE_01_RUNTIME_SEMANTIC_REPAIR'; rows=[]
    p00=vault/'NEXT_VERSION/AD_V2_PHASE_00_PRESSURE_PRICE_CONSTITUTION/DEVELOPMENT_MANIFEST.json'
    check(p00.is_file(),'p00_present',str(p00),rows)
    if p00.is_file():
        try: m0=json.loads(p00.read_text(encoding='utf-8')); check(m0.get('phase_id')=='AD-V2-P00' and m0.get('status')=='SHADOW_ONLY','p00_identity',m0.get('phase_id'),rows)
        except Exception as e: check(False,'p00_identity',str(e),rows)

    fp=json.loads((phase/'baseline/V1_RUNTIME_SEMANTIC_SURFACE_FINGERPRINT.json').read_text(encoding='utf-8'))
    bad=[]
    for r in fp['critical_files']:
        p=vault/r['path']
        if not p.is_file() or sha(p)!=r['sha256']: bad.append(r['path'])
    check(not bad,'v1_closed_runtime_fingerprint',bad,rows)

    own=json.loads((phase/'config/semantic_ownership_registry.json').read_text(encoding='utf-8'))
    required={'fundamental_direction','fundamental_force','fundamental_consumption','cognitive_consumption','remaining_fundamental_pressure','persistence','reversal_risk','driver_transition'}
    check(required.issubset(set(own.get('fields',{}))),'ownership_registry_complete',sorted(required-set(own.get('fields',{}))),rows)
    forbidden=own.get('forbidden_substitutions',[])
    check(any(x.get('from')=='driver_transition.state' and x.get('to')=='fundamental_force' for x in forbidden),'forbid_driver_state_to_force',None,rows)
    check(any('remaining_asymmetry' in x.get('from','') and x.get('to')=='remaining_fundamental_pressure' for x in forbidden),'forbid_asymmetry_to_remaining_pressure',None,rows)

    mod=load_module(phase/'runtime/semantic_lifecycle.py')
    fixture=json.loads((phase/'tests/fixtures/semantic_valid_gold.json').read_text(encoding='utf-8'))
    art=fixture['artifacts']; h=fixture['active_horizon']; n=mod.normalize_v1_artifacts(art,h)
    check(n['semantic_integrity']['status']=='PASS','valid_fixture_integrity',n['semantic_integrity'],rows)
    check(n['fundamental_direction']['value']=='BULLISH','active_horizon_direction',n['fundamental_direction'],rows)
    check(n['fundamental_force']['owner']=='MODULE_89' and n['fundamental_force']['active_horizon_range']=={'low':52,'high':72,'unit':'ordinal_score'},'force_owner_and_range',n['fundamental_force'],rows)
    check(n['fundamental_force']['force_class']=='UNMAPPED_IN_P01','no_invented_force_class',n['fundamental_force']['force_class'],rows)
    check(n['fundamental_consumption']['value']=='PARTIALLY_ABSORBED' and n['cognitive_consumption']['value']=='FLOW_PROPAGATION','consumption_separation',{'fundamental':n['fundamental_consumption'],'cognitive':n['cognitive_consumption']},rows)
    check(n['remaining_fundamental_pressure']['value']=='MODERATE','remaining_pressure_owner',n['remaining_fundamental_pressure'],rows)
    check(n['remaining_asymmetry']['research_intent']['value']=='HIGHLY_FAVORABLE','asymmetry_separate',n['remaining_asymmetry'],rows)
    check(n['persistence']['value']=='MULTI_DAY','persistence_owner',n['persistence'],rows)
    check(n['driver_transition']['state']=='TAKEOVER' and n['fundamental_force']['active_horizon_range']!="TAKEOVER",'driver_transition_not_force',n['driver_transition'],rows)
    check(n['semantic_integrity']['substitutions_used']==[],'no_substitutions',n['semantic_integrity']['substitutions_used'],rows)

    # Attack: missing exact horizon must fail closed, not borrow session row.
    a5=copy.deepcopy(art); a5['fundamental_state']['v11_fundamental_state']['horizon_states']=[x for x in a5['fundamental_state']['v11_fundamental_state']['horizon_states'] if x['horizon']!=h]
    n5=mod.normalize_v1_artifacts(a5,h)
    check(n5['semantic_integrity']['status']=='FAIL_CLOSED' and n5['fundamental_direction']['value'] is None,'no_horizon_fallback',n5['semantic_integrity'],rows)

    # Attack: missing force range must not become TAKEOVER.
    a6=copy.deepcopy(art); [x.pop('force_range',None) for x in a6['fundamental_state']['v11_fundamental_state']['horizon_states'] if x['horizon']==h]
    n6=mod.normalize_v1_artifacts(a6,h)
    check(n6['semantic_integrity']['status']=='FAIL_CLOSED' and n6['fundamental_force']['active_horizon_range'] is None and n6['driver_transition']['state']=='TAKEOVER','no_force_fallback',n6['fundamental_force'],rows)

    # Attack: missing remaining pressure cannot use HIGHLY_FAVORABLE asymmetry.
    a7=copy.deepcopy(art); a7['fundamental_state']['v11_fundamental_state']['remaining_pressure_v2'].pop('aggregate_class',None)
    n7=mod.normalize_v1_artifacts(a7,h)
    check(n7['semantic_integrity']['status']=='FAIL_CLOSED' and n7['remaining_fundamental_pressure']['value'] is None and n7['remaining_asymmetry']['research_intent']['value']=='HIGHLY_FAVORABLE','no_remaining_pressure_fallback',n7['remaining_fundamental_pressure'],rows)

    # Attack: persistence missing cannot use transition or review trigger.
    a8=copy.deepcopy(art); [x.pop('persistence_class',None) for x in a8['fundamental_state']['v11_fundamental_state']['horizon_states'] if x['horizon']==h]
    n8=mod.normalize_v1_artifacts(a8,h)
    check(n8['semantic_integrity']['status']=='FAIL_CLOSED' and n8['persistence']['value'] is None,'no_persistence_fallback',n8['persistence'],rows)

    out={'status':'PASS' if all(x['pass'] for x in rows) else 'FAIL','phase':'AD-V2-P01','tests':len(rows),'passed':sum(1 for x in rows if x['pass']),'checks':rows}
    print(json.dumps(out,indent=2) if a.json else f"PHASE 01 VALIDATION: {out['status']} ({out['passed']}/{out['tests']})")
    return 0 if out['status']=='PASS' else 3
if __name__=='__main__': sys.exit(main())
