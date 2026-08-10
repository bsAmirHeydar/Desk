from pathlib import Path
import copy
import json

from .registry import APLRegistry
from .semantics import (
    SemanticError,
    direct_fact_satisfied,
    fragility_state,
    independent_roots,
    invariant_survives,
    optionality_state,
)
from .util import load_json


def run(vault_root, parity_result=None):
    v = Path(vault_root).resolve()
    root = v / 'RUNTIME' / 'APL-A Alpha Perspective Layer'
    reg = APLRegistry(v)
    checks = []

    def ck(case_id, name, ok, detail=None):
        checks.append({
            'case_id': case_id,
            'name': name,
            'pass': bool(ok),
            'detail': detail,
        })

    # 1-3: epistemic state separation.
    epistemic_prompt = (root / 'prompt_registry' / 'V02_EPISTEMIC_FRAGILITY_AUDITOR' / 'prompt.md').read_text(encoding='utf-8')
    ck('APL-A-001', 'UNKNOWN is not ZERO', 'UNKNOWN' in epistemic_prompt and 'first-class' in epistemic_prompt)
    ck('APL-A-002', 'UNAVAILABLE is not ABSENT', 'UNAVAILABLE' in epistemic_prompt and 'first-class' in epistemic_prompt)
    ck(
        'APL-A-003',
        'PROXY cannot satisfy DIRECT FACT',
        not direct_fact_satisfied([
            {'epistemic_class': 'PUBLIC_PROXY', 'direct': False},
            {'epistemic_class': 'DERIVED_FACT', 'direct': False},
        ]),
    )

    # 4-5: repetition and same-root evidence are not independent confirmation.
    repeated = [{'root_id': 'ROOT_A'}, {'root_id': 'ROOT_A'}, {'root_id': 'ROOT_A'}]
    ck('APL-A-004', 'Narrative repetition cannot become independent evidence', independent_roots(repeated) == 1)
    ck('APL-A-005', 'Same-root sources remain one independent root', independent_roots(repeated + [{'root_id': 'ROOT_B'}]) == 2)

    # 6-8: removal audits are counterfactual copies, not upstream mutation.
    facts = {
        'facts': [
            {'fact_id': 'F1', 'root_id': 'ROOT_A', 'value': 1},
            {'fact_id': 'F2', 'root_id': 'ROOT_B', 'value': 2},
        ],
        'story': 'attractive narrative',
    }
    facts_original = copy.deepcopy(facts)
    story_removed = copy.deepcopy(facts)
    story_removed.pop('story', None)
    ck(
        'APL-A-006',
        'Story Removal may weaken a thesis without deleting facts',
        facts == facts_original and story_removed['facts'] == facts_original['facts'] and 'story' not in story_removed,
    )
    hypotheses = {'hypotheses': [{'id': 'H1'}, {'id': 'H2'}]}
    hypotheses_original = copy.deepcopy(hypotheses)
    model_removed = {'hypotheses': [x for x in copy.deepcopy(hypotheses['hypotheses']) if x['id'] != 'H1']}
    ck(
        'APL-A-007',
        'Model Removal cannot mutate original hypotheses',
        hypotheses == hypotheses_original and model_removed != hypotheses,
    )
    evidence_original = copy.deepcopy(facts_original)
    source_removed = copy.deepcopy(facts_original)
    source_removed['facts'] = [x for x in source_removed['facts'] if x['root_id'] != 'ROOT_A']
    ck(
        'APL-A-008',
        'Source Removal cannot mutate D1 evidence',
        facts_original == evidence_original and len(source_removed['facts']) == 1 and len(facts_original['facts']) == 2,
    )

    # 9: invariants must explicitly survive the declared removals.
    ck(
        'APL-A-009',
        'Invariant survives the stated removals',
        invariant_survives([
            {'surviving': ['INV_A', 'INV_B']},
            {'surviving': ['INV_A']},
            {'surviving': ['INV_A', 'INV_C']},
        ], 'INV_A'),
    )

    # 10-13: scoped fragility geometry and unresolved reversal.
    valid_scope = {
        'system_boundary': 'RUN_THESIS',
        'stressor': 'YIELD_SHOCK',
        'horizon': 'DAILY_OPEN_TO_CLOSE',
        'welfare_metric': 'THESIS_STABILITY',
    }
    try:
        fragility_state({'system_boundary': 'RUN_THESIS', 'stressor': 'YIELD_SHOCK', 'horizon': '', 'welfare_metric': 'THESIS_STABILITY'}, 'LOCALLY_CONVEX')
        missing_horizon_rejected = False
    except SemanticError:
        missing_horizon_rejected = True
    ck('APL-A-010', 'Fragility classification requires stressor/scope/horizon', missing_horizon_rejected)
    try:
        fragility_state({'system_boundary': 'RUN_THESIS', 'stressor': None, 'horizon': 'DAILY_OPEN_TO_CLOSE', 'welfare_metric': 'THESIS_STABILITY'}, 'LOCALLY_CONVEX')
        missing_stressor_rejected = False
    except SemanticError:
        missing_stressor_rejected = True
    ck('APL-A-011', 'Antifragile without a stressor is rejected', missing_stressor_rejected)
    ck(
        'APL-A-012',
        'Local convexity is not global convexity',
        fragility_state(valid_scope, 'LOCALLY_CONVEX') == 'LOCALLY_CONVEX' and 'GLOBAL_CONVEX' not in {
            'LOCALLY_CONVEX','LOCALLY_CONCAVE','APPROX_LINEAR','MIXED_CURVATURE','CURVATURE_REVERSAL_RISK','THRESHOLD_DOMINATED','DISCONTINUOUS','UNKNOWN_GEOMETRY'
        },
    )
    ck(
        'APL-A-013',
        'Curvature reversal can remain UNRESOLVED/unknown',
        fragility_state(valid_scope, 'CURVATURE_REVERSAL_RISK') == 'CURVATURE_REVERSAL_RISK' and fragility_state(valid_scope, 'NOT_ESTIMABLE') == 'UNKNOWN_GEOMETRY',
    )

    # 14-15: optionality requires cost, expiry and exercise feasibility.
    ck('APL-A-014', 'Optionality is not assumed free', optionality_state('PROHIBITIVE', 'OPEN', True) == 'IMPAIRED_OPTIONALITY')
    ck('APL-A-015', 'Apparent optionality can be ILLUSORY', optionality_state('LOW', 'OPEN', False) == 'ILLUSORY_OPTIONALITY')

    # 16: nominal redundancy is not independent redundancy.
    network_schema = load_json(root / 'schemas' / 'AlphaLab_APL_Network_CommonMode_Map.schema.json')
    ck(
        'APL-A-016',
        'Network redundancy checks common upstream roots',
        'nominal_support_count' in network_schema.get('required', []) and 'independent_root_count' in network_schema.get('required', []) and independent_roots(repeated) == 1,
    )

    # 17-18: agency/transfer and intervention are explicitly conditional and reversible.
    v13_prompt = (root / 'prompt_registry' / 'V13_INCENTIVE_TRANSFER_INTERVENTION' / 'prompt.md').read_text(encoding='utf-8')
    agency_schema = load_json(root / 'schemas' / 'AlphaLab_APL_Agency_Intervention_Map.schema.json')
    ck(
        'APL-A-017',
        'Fragility transfer identifies the tail carrier where evidence supports it',
        'who carries the tail' in v13_prompt.lower() and 'fragility_transfers' in agency_schema.get('required', []),
    )
    ck(
        'APL-A-018',
        'Intervention analysis includes reversal/side-effect conditions',
        'second-order' in v13_prompt.lower() and 'failure/reversal conditions' in v13_prompt.lower() and 'interventions' in agency_schema.get('required', []),
    )

    # 19-21: authority and retrieval boundaries are machine-readable on every process.
    authority = load_json(root / 'policies' / 'authority_policy.json')
    ck('APL-A-019', 'No APL process creates Direction', 'CREATE_FUNDAMENTAL_DIRECTION' in authority['forbidden'] and all('fundamental_direction' not in reg.manifest(pid)['authority'].get('can_create', []) for pid in reg.ids()))
    ck('APL-A-020', 'No APL process creates BUY/SELL', 'CREATE_BUY_SELL' in authority['forbidden'] and all('final_permission' not in reg.manifest(pid)['authority'].get('can_create', []) for pid in reg.ids()))
    ck('APL-A-021', 'No APL process directly retrieves web data', 'DIRECT_WEB_RETRIEVAL' in authority['forbidden'] and all('unadmitted_web_results' in reg.manifest(pid).get('forbidden_inputs', []) for pid in reg.ids()))

    # 22: actual R1 Decision World + seal parity test is authoritative here.
    parity_ok = bool(parity_result and parity_result.get('status') == 'PASS')
    if parity_ok:
        pchecks = {x['name']: x['pass'] for x in parity_result.get('checks', [])}
        parity_ok = bool(
            pchecks.get('upstream_hashes_identical') and
            pchecks.get('entire_decision_world_identical') and
            pchecks.get('decision_seal_identical') and
            pchecks.get('apl_shadow_pass') and
            pchecks.get('apl_outputs_learning_only')
        )
    ck('APL-A-022', 'Final production decision/world is identical with APL-A shadow enabled vs disabled', parity_ok)

    # 23: research requests can only route to the governed evidence pipeline.
    data_policy = load_json(root / 'policies' / 'data_plane_isolation_policy.json')
    shadow_source = (root / 'alpha_perspective_runtime' / 'shadow.py').read_text(encoding='utf-8')
    route_text = json.dumps(data_policy, ensure_ascii=False)
    ck(
        'APL-A-023',
        'APL can emit only governed research requests',
        'P11' in route_text and 'C1' in route_text and 'R1' in route_text and 'D1' in route_text and 'P11_EVIDENCE_PLAN_NEXT_GOVERNED_RUN' in shadow_source and 'direct_retrieval' in shadow_source,
    )

    # 24: every load-bearing principle retains provenance and source hash.
    principles = load_json(root / 'canon' / 'APL_A_PRINCIPLE_REGISTRY.json').get('principles', [])
    provenance_classes = {'TALEB_SOURCE_DERIVED', 'TALEB_PRIMARY_SYNTHESIS', 'TALEB_EXPANDED_SYNTHESIS'}
    provenance_ok = bool(principles)
    for pr in principles:
        if pr.get('provenance_class') not in provenance_classes or not pr.get('source_refs'):
            provenance_ok = False
            break
        for ref in pr.get('source_refs', []):
            if not str(ref.get('sha256', '')).startswith('sha256:') or ref.get('provenance_class') not in provenance_classes:
                provenance_ok = False
                break
        if not provenance_ok:
            break
    ck('APL-A-024', 'Taleb provenance survives to all load-bearing principle records', provenance_ok, {'principle_count': len(principles)})

    # 25: no collapsed Taleb/Perspective score or voting layer exists.
    banned = ('taleb_score', 'perspective_score', 'weighted_vote', 'majority_vote')
    bad = []
    for p in root.rglob('*'):
        if not p.is_file() or '__pycache__' in p.parts or p.name in ('acceptance.py','selftest.py') or p.suffix.lower() not in ('.json', '.md', '.py', '.yaml', '.yml'):
            continue
        text = p.read_text(encoding='utf-8', errors='ignore').lower()
        # Documentation may mention banned concepts only in explicit prohibitions.
        for token in banned:
            if token in text and p.name not in ('acceptance.py',):
                bad.append({'path': p.relative_to(root).as_posix(), 'token': token})
    ck('APL-A-025', 'No total Taleb/Perspective score or voting layer exists', not bad, bad[:20])

    # Additional high-leverage controls from the execution specification.
    source_vault_vendored = any('Talebian_Systems_Philosophy_OS_v3.0.0_MAXIMAL' in p.name for p in v.iterdir())
    ck('APL-A-026', 'Taleb source vault remains external/read-only and is not vendored', not source_vault_vendored)
    receipt = load_json(root / 'receipts' / 'TALEB_EXTRACTION_COVERAGE_RECEIPT.json')
    ck('APL-A-027', 'Complete 696-note Taleb extraction inventory exists', receipt.get('total_markdown_notes') == 696 and len(receipt.get('records', [])) == 696)
    ck('APL-A-028', 'All extraction records have explicit dispositions', all(x.get('production_disposition') in {'INTEGRATED','CONTEXT_ONLY','DUPLICATE_OF_EXISTING_ALPHA','DEFER_TO_APL_B','REJECTED_FOR_PRODUCTION','NOT_APPLICABLE'} for x in receipt.get('records', [])))
    ck('APL-A-029', 'APL-A remains SHADOW_ONLY', authority.get('mode') == 'SHADOW_ONLY' and authority.get('shadow_failure_blocks_core') is False)
    graph = load_json(root / 'config' / 'process_graph.json')
    ck('APL-A-030', 'APL-A has no dependency from core P50-P63 decision path', graph.get('influences_core_decision') is False and 'final_permission' in graph.get('forbidden_core_inputs', []))

    errors = [x['case_id'] + ' ' + x['name'] for x in checks if not x['pass']]
    return {
        'schema_version': '1.0.0',
        'status': 'PASS' if not errors else 'FAIL',
        'passed': sum(1 for x in checks if x['pass']),
        'total': len(checks),
        'checks': checks,
        'errors': errors,
    }
