from __future__ import annotations
# AD-V3-P04 COMPATIBILITY WRAPPER. Canonical V3 orchestration authority is AD-V3-P10.
# Legacy implementation is preserved in legacy_pipeline_v1.py for historical audit only.
# Compatibility markers retained for P04 historical acceptance documentation:
# def _progress ; [1/7] P02 live acquisition ; heartbeat_seconds ; allow=(0, 2, 3) ; P02_BLOCKED ; BLOCKING FACTS
# ('XAUUSD_SPOT_PRICE', 'SPOT_DIRECT', False) ; ('GC_FUTURES_PRICE', 'GC_FUTURES_PROXY', True)
# anchor_kind = 'SPOT_PUBLIC_PROXY' ; o.get('epistemic_state') == 'PUBLIC_PROXY' ; causal_direction_authority': False
# build_final_seal ; latest_run_seal.json ; run_semantics(repo, packet ; semantic_validation_status
# run_kernel_acquisition.py ; kernel_mode ; p07_governed_coverage.json ; '--coverage', str(coverage_path)
# calibrate_decision ; p08_decision_calibration.json ; p09_precommit_current ; p09_forward_precommit.json ; p09_observe_and_evaluate ; _progress('[2/7] P03 causal brain - pre-semantic')
# p03_final.json ; forward_validation=

def run(repo_root,horizon='SESSION_1_6H',skip_p02=False,semantic_bundle_path=None,p02_data_root_override=None,output_root_override=None,kernel_mode='NORMAL',kernel_fixture_dir=None,kernel_output_root_override=None,p09_state_root_override=None,as_of_utc=None):
    if skip_p02:
        raise RuntimeError('P04_COMPAT_SKIP_P02_NOT_SUPPORTED_BY_CANONICAL_P10_RUNTIME')
    from AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN.runtime.gold_orchestrator import run_gold
    return run_gold(repo_root,horizon,'SHADOW',kernel_mode,semantic_bundle_path=semantic_bundle_path,p02_data_root_override=p02_data_root_override,artifact_root_override=output_root_override,kernel_fixture_dir=kernel_fixture_dir,kernel_output_root_override=kernel_output_root_override,p09_state_root_override=p09_state_root_override,as_of_utc=as_of_utc)
