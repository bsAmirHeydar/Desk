#!/usr/bin/env python3
from pathlib import Path
import argparse, json, hashlib, sys

PHASE_REL = Path("NEXT_VERSION/AD_V2_PHASE_00_PRESSURE_PRICE_CONSTITUTION")

def sha256_file(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for chunk in iter(lambda:f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()

def load(p):
    return json.loads(p.read_text(encoding='utf-8'))

def fail(errors, msg):
    errors.append(msg)

def locate_vault(repo_root):
    direct = repo_root / "Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL"
    if direct.is_dir(): return direct
    if (repo_root / "CURRENT_PRODUCTION_MANIFEST.json").is_file(): return repo_root
    raise FileNotFoundError("VAULT_ROOT_NOT_FOUND")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--repo-root', required=True)
    ap.add_argument('--json', action='store_true')
    args=ap.parse_args()
    repo=Path(args.repo_root).resolve()
    vault=locate_vault(repo)
    phase=vault/PHASE_REL
    errors=[]; checks=[]
    def check(name, cond, detail=None):
        checks.append({"name":name,"pass":bool(cond),"detail":detail})
        if not cond: fail(errors, name + (f":{detail}" if detail else ""))

    required=[
      'DEVELOPMENT_MANIFEST.json','config/pressure_price_constitution.json','config/authority_graph.json',
      'schemas/AlphaDesk_V2_PressurePriceConstitution.schema.json','tests/pressure_price_attack_cases.json',
      'baseline/V1_CRITICAL_SURFACE_FINGERPRINT.json'
    ]
    for r in required: check('required_file:'+r, (phase/r).is_file())
    if errors:
        out={"status":"FAIL","errors":errors,"checks":checks}; print(json.dumps(out,indent=2)); return 2

    manifest=load(phase/'DEVELOPMENT_MANIFEST.json')
    c=load(phase/'config/pressure_price_constitution.json')
    graph=load(phase/'config/authority_graph.json')
    attacks=load(phase/'tests/pressure_price_attack_cases.json')
    fp=load(phase/'baseline/V1_CRITICAL_SURFACE_FINGERPRINT.json')

    check('phase_shadow_only', manifest.get('status')=='SHADOW_ONLY')
    check('production_manifest_not_modified_declared', manifest.get('active_production_manifest_modified') is False)
    check('no_active_production_files_modified', manifest.get('active_production_files_modified')==[])
    check('v1_stack_baseline', manifest.get('v1_baseline',{}).get('scientific_stack')=='V21.3.0')
    check('v1_runtime_baseline', manifest.get('v1_baseline',{}).get('runtime')=='R4.0.0')

    current=load(vault/'CURRENT_PRODUCTION_MANIFEST.json')
    check('current_production_still_v21_3', current.get('current_stack')=='V21.3.0', current.get('current_stack'))
    cog=current.get('cognitive_hardening',{})
    check('v1_market_price_direction_authority_false', cog.get('market_price_direction_authority') is False)
    check('v1_market_price_model_diagnostic_true', cog.get('market_price_model_diagnostic') is True)
    r4=load(vault/'RUNTIME/R4 Scientific Certification and Reproducibility Hardening/R4_MANIFEST.json')
    check('r4_runtime_version', r4.get('runtime_version')=='R4.0.0', r4.get('runtime_version'))
    check('r4_scientific_stack', r4.get('scientific_stack')=='V21.3.0', r4.get('scientific_stack'))

    # Baseline source integrity: all critical V1 files must remain byte-identical.
    for row in fp.get('critical_files',[]):
        p=vault/row['path']; ok=p.is_file() and sha256_file(p)==row['sha256']
        check('v1_critical_unchanged:'+row['path'], ok)

    p=c.get('pressure',{}); t=c.get('target_price',{}); cons=c.get('consumption',{}); latent=c.get('latent_state',{}); exe=c.get('execution',{}); frozen=c.get('frozen_record',{})
    check('pressure_owner_module89', p.get('owner')=='MODULE_89')
    check('target_price_no_direct_pressure_authority', p.get('target_price_direct_authority') is False)
    check('target_price_no_direct_pressure_mutation', p.get('target_price_may_change_pressure_directly') is False)
    check('price_can_lower_model_completeness_not_pressure', p.get('target_price_may_lower_pressure_confidence_directly') is False and p.get('target_price_may_lower_model_completeness_confidence') is True)
    check('direct_price_to_pressure_edge_forbidden', c.get('audit_callback',{}).get('direct_price_to_pressure_edge') is False)
    check('driver_vs_price_consumption_separate', cons.get('driver_consumption_separate_from_price_consumption') is True)
    check('price_distance_not_driver_consumption', cons.get('target_price_distance_sufficient_for_driver_consumption') is False)
    check('latent_not_implemented', latent.get('phase00_authority')=='RESERVED_NOT_IMPLEMENTED')
    check('no_fake_latent_probability', latent.get('unreleased_pressure_probability_allowed') is False)
    check('price_alone_not_absorption_proof', latent.get('price_shape_alone_can_confirm_absorption') is False)
    check('price_alone_not_liquidity_sweep_proof', latent.get('price_shape_alone_can_confirm_liquidity_sweep') is False)
    check('technical_no_pressure_authority', exe.get('technical_can_change_fundamental_pressure') is False)
    check('high_pressure_not_forced_trade', exe.get('high_pressure_implies_trade') is False)
    check('future_outcome_no_historical_rewrite', frozen.get('future_outcome_can_rewrite_historical_pressure') is False)

    forbidden_edges={tuple(x) for x in graph.get('forbidden_edges',[])}
    check('graph_forbids_price_to_pressure', ('TARGET_PRICE_TRANSMISSION','DIRECTIONAL_PRESSURE') in forbidden_edges)
    check('graph_forbids_technical_to_pressure', ('TECHNICAL_EXECUTION_TIMING','DIRECTIONAL_PRESSURE') in forbidden_edges)
    callback={tuple(x) for x in graph.get('controlled_callback_edges',[])}
    check('graph_has_research_callback_only', ('RESEARCH_ESCALATION','D1_CAUSAL_EVIDENCE') in callback)

    # Declarative semantic attack checks.
    kinds={x.get('kind'):x for x in attacks.get('cases',[])}
    required_kinds=['PRICE_CONTAMINATION','MOMENTUM_TIEBREAKER','PRICE_CONSUMPTION','HIDDEN_STATE_STORY','CAUSAL_DRIVER_CHANGE','RESEARCH_CALLBACK_NO_NEW_EVIDENCE','RESEARCH_CALLBACK_WITH_NEW_EVIDENCE','D4_RETROACTIVE','TECHNICAL_BOUNDARY','CONFIDENCE_SEPARATION','CROSS_ASSET_CAUSAL_NUANCE','NO_FORCED_TRADE']
    for k in required_kinds: check('attack_case_present:'+k, k in kinds)
    if 'PRICE_CONTAMINATION' in kinds: check('attack_price_contamination_expected', kinds['PRICE_CONTAMINATION']['expected'].get('pressure_equal') is True)
    if 'MOMENTUM_TIEBREAKER' in kinds: check('attack_momentum_not_pressure', kinds['MOMENTUM_TIEBREAKER']['expected'].get('momentum_may_set_pressure') is False)
    if 'HIDDEN_STATE_STORY' in kinds: check('attack_hidden_state_unconfirmed', kinds['HIDDEN_STATE_STORY']['expected'].get('confirmed_absorption') is False)
    if 'RESEARCH_CALLBACK_NO_NEW_EVIDENCE' in kinds: check('attack_callback_no_direct_mutation', kinds['RESEARCH_CALLBACK_NO_NEW_EVIDENCE']['expected'].get('direct_pressure_mutation') is False)
    if 'D4_RETROACTIVE' in kinds: check('attack_d4_no_rewrite', kinds['D4_RETROACTIVE']['expected'].get('historical_pressure_rewrite') is False)

    out={"status":"PASS" if not errors else "FAIL","phase":"AD-V2-P00","checks_total":len(checks),"checks_passed":sum(1 for x in checks if x['pass']),"errors":errors}
    if args.json: print(json.dumps(out,indent=2))
    else:
        print(f"PHASE 00 VALIDATION: {out['status']}")
        print(f"Checks: {out['checks_passed']}/{out['checks_total']}")
        if errors:
            for e in errors: print(' -',e)
    return 0 if not errors else 2

if __name__=='__main__':
    sys.exit(main())
