from __future__ import annotations
import subprocess, sys, json, shutil, time
from pathlib import Path
from .common import load_json, write_json, stable_id, iso
from AD_V3_PHASE_06_GOVERNED_SEMANTIC_INTELLIGENCE.runtime.semantic_runtime import run_semantics
from .promotion import load_state as load_promotion
from .permission import evaluate as permission_eval
from .commissioning import build_precommit, update as update_commissioning
from .control_room_model import build as build_model
from .renderer import render, brief
from .capsule import build as build_capsule, build_final_seal


def _progress(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


def _current_fact_observation(data_root, fact_id, acquisition_run_id):
    obs = Path(data_root) / 'observations' / 'gold_fact_observations.jsonl'
    if not obs.exists():
        return None
    hit = None
    for line in obs.read_text(encoding='utf-8-sig').splitlines():
        if not line.strip():
            continue
        try:
            o = json.loads(line)
        except Exception:
            continue
        if o.get('fact_id') == fact_id and o.get('acquisition_run_id') == acquisition_run_id:
            hit = o
    return hit


def _price_anchor_from_store(data_root, p03):
    run_id = (p03.get('handoff_integrity') or {}).get('acquisition_run_id')
    candidates = [
        ('XAUUSD_SPOT_PRICE', 'SPOT_DIRECT', False),
        ('GC_FUTURES_PRICE', 'GC_FUTURES_PROXY', True),
    ]
    for fact_id, anchor_kind, proxy in candidates:
        o = _current_fact_observation(data_root, fact_id, run_id)
        if not o or not isinstance(o.get('value'), (int, float)):
            continue
        # XAUUSD_SPOT_PRICE may be supplied by a clearly-labelled public proxy fallback.
        # Preserve that epistemic status in the true-forward anchor; never relabel it direct.
        if fact_id == 'XAUUSD_SPOT_PRICE' and (o.get('directness') == 'PROXY' or o.get('epistemic_state') == 'PUBLIC_PROXY'):
            anchor_kind = 'SPOT_PUBLIC_PROXY'
            proxy = True
        marker = o.get('reference_period') or o.get('event_time') or o.get('published_at') or o.get('retrieved_at')
        meta = o.get('metadata') or {}
        selected = meta.get('selected_contract') or {}
        instrument_key = selected.get('contract') if isinstance(selected, dict) else None
        return {
            'value': float(o['value']),
            'economic_marker': marker,
            'reference_period': o.get('reference_period'),
            'event_time': o.get('event_time'),
            'published_at': o.get('published_at'),
            'retrieved_at': o.get('retrieved_at'),
            'observation_id': o.get('observation_id'),
            'acquisition_run_id': run_id,
            'source_fact_id': fact_id,
            'source_id': o.get('source_id'),
            'anchor_kind': anchor_kind,
            'proxy_for_xauusd': proxy,
            'transmission_only': True,
            'causal_direction_authority': False,
            'instrument_key': instrument_key,
        }
    return None


def _run_json(cmd, allow=(0,), label='subprocess', hard_timeout_seconds=900, heartbeat_seconds=20):
    """Run a JSON-producing child while keeping the operator informed.

    Child stdout remains machine-readable and is parsed only after exit. Progress is
    emitted by P04 on stderr, so the canonical JSON contract is preserved.
    """
    started = time.monotonic()
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding='utf-8',
        errors='replace',
    )
    out = err = ''
    while True:
        try:
            out, err = proc.communicate(timeout=heartbeat_seconds)
            break
        except subprocess.TimeoutExpired:
            elapsed = int(time.monotonic() - started)
            _progress(f'      {label}: running ({elapsed}s elapsed)')
            if elapsed >= hard_timeout_seconds:
                proc.kill()
                out, err = proc.communicate()
                raise RuntimeError(
                    f'{label.upper()}_TIMEOUT after {elapsed}s; child terminated safely.\n' + (err[-1200:] if err else '')
                )
    try:
        obj = json.loads((out or '').lstrip('\ufeff'))
    except Exception as e:
        raise RuntimeError(
            'JSON_OUTPUT_PARSE_FAILED ' + repr(e) + '\n' + (out[-1200:] if out else '') + '\n' + (err[-1200:] if err else '')
        )
    if proc.returncode not in allow:
        raise RuntimeError(
            'COMMAND_FAILED ' + str(proc.returncode) + '\n' + (err[-1200:] if err else '')
        )
    return proc.returncode, obj


def _blocking_fact_ids(coverage):
    ids = []
    for x in coverage.get('failed_blocking_facts') or []:
        if isinstance(x, dict) and x.get('fact_id'):
            ids.append(str(x['fact_id']))
        elif x:
            ids.append(str(x))
    for x in coverage.get('unattempted_blocking_facts') or []:
        if x:
            ids.append(str(x))
    return list(dict.fromkeys(ids))


def run(repo_root, horizon='SESSION_1_6H', skip_p02=False, semantic_bundle_path=None, p02_data_root_override=None, output_root_override=None, kernel_mode='NORMAL', kernel_fixture_dir=None, kernel_output_root_override=None):
    repo = Path(repo_root)
    nxt = repo / 'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL' / 'NEXT_VERSION'
    p02 = nxt / 'AD_V3_PHASE_02_TOTAL_LIVE_DATA_OBSERVABILITY_FABRIC'
    p03 = nxt / 'AD_V3_PHASE_03_CAUSAL_GOLD_BRAIN_DECISION_ENGINE'
    p04 = nxt / 'AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING'
    p07 = nxt / 'AD_V3_PHASE_07_LIVE_INTRADAY_GOLD_DATA_KERNEL'
    data = Path(p02_data_root_override) if p02_data_root_override else p02 / 'artifacts' / 'live_store'
    outroot = Path(output_root_override) if output_root_override else p04 / 'artifacts'
    runs = outroot / 'runs'
    runs.mkdir(parents=True, exist_ok=True)
    stamp = iso().replace('-', '').replace(':', '')
    run_id = stable_id('P04RUN', {'stamp': stamp, 'horizon': horizon, 'data': str(data)})
    rd = runs / run_id
    rd.mkdir(parents=True, exist_ok=False)

    _progress('')
    _progress('============================================================')
    _progress(' ALPHA DESK V3 - GOLD COMMISSIONING')
    _progress('============================================================')
    _progress(f'Run ID: {run_id}')

    kernel = None
    coverage_path = rd / 'p07_governed_coverage.json'
    if not skip_p02:
        _progress('[1/7] P02 live acquisition via P07 intraday Gold data kernel')
        cmd=[sys.executable, str(p07 / 'tools' / 'run_kernel_acquisition.py'), '--horizon', horizon, '--mode', kernel_mode, '--data-root', str(data), '--json']
        if kernel_fixture_dir:
            cmd += ['--fixture-network-dir', str(kernel_fixture_dir)]
        if kernel_output_root_override:
            cmd += ['--output-root', str(kernel_output_root_override)]
        code, kernel = _run_json(
            cmd, allow=(0, 2, 3), label='P07 Gold data kernel', hard_timeout_seconds=900, heartbeat_seconds=20,
        )
        source_cov=load_json(kernel['governed_coverage_path'])
        write_json(coverage_path, source_cov)
        write_json(rd / 'p07_kernel_receipt.json', kernel)
        cov=source_cov
    else:
        _progress('[1/7] P07 data kernel: SKIPPED (using latest governed kernel coverage)')
        latest_kernel=p07/'artifacts'/'latest'/'latest_kernel_receipt.json'
        latest_cov=p07/'artifacts'/'latest'/'latest_governed_coverage.json'
        if not latest_kernel.exists() or not latest_cov.exists():
            raise RuntimeError('NO_P07_KERNEL_RECEIPT')
        kernel=load_json(latest_kernel); cov=load_json(latest_cov); code=0
        write_json(coverage_path,cov); write_json(rd/'p07_kernel_receipt.json',kernel)

    admission = cov.get('analysis_admission')
    may_start = bool(cov.get('analysis_may_start'))
    kh=(kernel or {}).get('kernel_health') or {}
    _progress(f"      kernel: live {kh.get('live_kernel_fresh')}/{kh.get('live_kernel_total')} | context {kh.get('context_valid')}/{kh.get('context_total')} | admission={admission}")
    if code == 2 and may_start:
        _progress('      DEGRADED / NON-BLOCKED -> CONTINUE')
    if code == 3 or admission == 'BLOCKED' or not may_start:
        blockers = _blocking_fact_ids(cov)
        if blockers:
            _progress('      BLOCKING FACTS: ' + ', '.join(blockers))
        raise RuntimeError('P02_BLOCKED_BY_P07_KERNEL' + (': ' + ', '.join(blockers) if blockers else ''))

    _progress('[2/7] P03 causal brain - pre-semantic')
    _, pre = _run_json(
        [sys.executable, str(p03 / 'tools' / 'run_causal_brain.py'), '--p02-data-root', str(data), '--coverage', str(coverage_path), '--horizon', horizon, '--json'],
        label='P03 pre-semantic causal brain',
        hard_timeout_seconds=300,
        heartbeat_seconds=20,
    )
    write_json(rd / 'p03_pre_semantic.json', pre)
    handoff = pre.get('handoff_integrity') or {}
    _progress(f"      P03 handoff: {handoff.get('current_observations_loaded')}/{handoff.get('expected_current_observations')} complete={handoff.get('complete')}")

    _progress('[3/7] Semantic evidence packet')
    packet_path = rd / 'semantic_evidence_packet.json'
    sr = subprocess.run(
        [sys.executable, str(p03 / 'tools' / 'export_semantic_evidence_packet.py'), '--p02-data-root', str(data), '--coverage', str(coverage_path), '--horizon', horizon, '--output', str(packet_path)],
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace',
        timeout=300,
    )
    if sr.returncode != 0:
        raise RuntimeError('SEMANTIC_PACKET_EXPORT_FAILED ' + sr.stderr[-1000:])
    packet = load_json(packet_path)
    _progress(f"      semantic requests: {packet.get('item_count', len(packet.get('items') or []))}")

    _progress('[4/7] Governed semantic adjudication')
    semantic_run = run_semantics(repo, packet, external_bundle_path=semantic_bundle_path, artifact_dir=rd)
    bundle = semantic_run['bundle']
    sem_receipt = semantic_run['validation_receipt']
    write_json(rd / 'semantic_adjudication_bundle.json', bundle)
    _progress(f"      semantic mode: {bundle.get('adjudication_mode', 'GOVERNED_BUNDLE')}")
    _progress(f"      semantic validation: {sem_receipt.get('validated_count',0)} validated | {sem_receipt.get('unknown_count',0)} unknown | {sem_receipt.get('rejected_count',0)} rejected | {sem_receipt.get('fallback_count',0)} fallback")

    _progress('[5/7] P03 causal brain - final')
    _, final = _run_json(
        [sys.executable, str(p03 / 'tools' / 'run_causal_brain.py'), '--p02-data-root', str(data), '--coverage', str(coverage_path), '--horizon', horizon, '--adjudication', str(rd / 'semantic_adjudication_bundle.json'), '--json'],
        label='P03 final causal brain',
        hard_timeout_seconds=300,
        heartbeat_seconds=20,
    )
    write_json(rd / 'p03_final.json', final)

    promotion = load_promotion(p04)
    permission = permission_eval(final, promotion)
    write_json(rd / 'permission.json', permission)
    _progress(f"      direction: {permission.get('direction')} | action: {permission.get('research_action_candidate')} | official permission: {permission.get('official_permission')}")

    _progress('[6/7] True-forward precommit + Control Room')
    price_anchor = _price_anchor_from_store(data, final)
    if price_anchor:
        _progress(f"      price anchor: {price_anchor.get('source_fact_id')} {price_anchor.get('value')} ({price_anchor.get('anchor_kind')})")
    else:
        _progress('      price anchor: UNAVAILABLE (C3 directional outcomes would be unevaluable)')
    precommit = build_precommit(run_id, final, permission, price_anchor)
    write_json(rd / 'precommit.json', precommit)
    commissioning = update_commissioning(p04, precommit, price_anchor)
    write_json(rd / 'commissioning_snapshot.json', commissioning)
    latest_dir = outroot / 'latest'
    prev = None
    if (latest_dir / 'latest_control_room.json').exists():
        prev = load_json(latest_dir / 'latest_control_room.json')
    model = build_model(run_id, final, packet, bundle, permission, commissioning, promotion, prev, pre_semantic=pre, data_kernel=kernel)
    write_json(rd / 'control_room.json', model)
    helps = load_json(p04 / 'config' / 'help_registry.json')
    (rd / 'control_room.html').write_text(render(model, helps), encoding='utf-8')
    (rd / 'brief.txt').write_text(brief(model), encoding='utf-8')

    _progress('[7/7] Immutable capsule + publish latest outputs')
    cap = build_capsule(run_id, rd, precommit, promotion.get('state') == 'PRODUCTION_V3')
    latest_dir.mkdir(parents=True, exist_ok=True)
    for src, name in [
        (rd / 'control_room.json', 'latest_control_room.json'),
        (rd / 'control_room.html', 'latest_control_room.html'),
        (rd / 'brief.txt', 'latest_brief.txt'),
        (rd / 'capsule.json', 'latest_capsule.json'),
        (rd / 'precommit.json', 'latest_precommit.json'),
        (rd / 'p03_final.json', 'latest_p03_final.json'),
        (rd / 'semantic_evidence_packet.json', 'latest_semantic_evidence_packet.json'),
        (rd / 'semantic_request_packet.json', 'latest_semantic_request_packet.json'),
        (rd / 'semantic_validation_receipt.json', 'latest_semantic_validation_receipt.json'),
        (rd / 'semantic_validated_bundle.json', 'latest_semantic_validated_bundle.json'),
        (rd / 'semantic_run_capsule.json', 'latest_semantic_run_capsule.json'),
        (rd / 'p07_kernel_receipt.json', 'latest_p07_kernel_receipt.json'),
        (rd / 'p07_governed_coverage.json', 'latest_p07_governed_coverage.json'),
    ]:
        shutil.copy2(src, latest_dir / name)

    receipt = {
        'record_type': 'AD_V3_P04_PIPELINE_RECEIPT',
        'run_id': run_id,
        'generated_at_utc': iso(),
        'status': 'PASS',
        'p02_admission': cov.get('p02_original_analysis_admission', cov.get('analysis_admission')),
        'p07_admission': cov.get('analysis_admission'),
        'p02_degraded_nonblocking': code == 2 and bool(cov.get('analysis_may_start')),
        'p07_kernel_run_id': (kernel or {}).get('run_id'),
        'p07_live_kernel_health': ((kernel or {}).get('kernel_health') or {}).get('live_kernel_health'),
        'p07_live_kernel_fresh': ((kernel or {}).get('kernel_health') or {}).get('live_kernel_fresh'),
        'p07_live_kernel_total': ((kernel or {}).get('kernel_health') or {}).get('live_kernel_total'),
        'p07_context_valid': ((kernel or {}).get('kernel_health') or {}).get('context_valid'),
        'p07_context_total': ((kernel or {}).get('kernel_health') or {}).get('context_total'),
        'p07_network_requests': ((kernel or {}).get('performance') or {}).get('network_requests'),
        'p07_cache_hits': ((kernel or {}).get('performance') or {}).get('cache_hits'),
        'p07_duration_ms': ((kernel or {}).get('performance') or {}).get('total_p07_ms'),
        'p03_handoff_complete': bool((final.get('handoff_integrity') or {}).get('complete')),
        'direction_candidate': permission.get('direction'),
        'research_action_candidate': permission.get('research_action_candidate'),
        'official_permission': permission.get('official_permission'),
        'semantic_mode': bundle.get('adjudication_mode', 'GOVERNED_BUNDLE'),
        'semantic_validation_status': sem_receipt.get('status'),
        'semantic_request_count': sem_receipt.get('request_count',0),
        'semantic_validated_count': sem_receipt.get('validated_count',0),
        'semantic_unknown_count': sem_receipt.get('unknown_count',0),
        'semantic_rejected_count': sem_receipt.get('rejected_count',0),
        'semantic_fallback_count': sem_receipt.get('fallback_count',0),
        'semantic_model_host_state': (bundle.get('p06_semantic') or {}).get('model_host_state'),
        'semantic_prompt_version': (bundle.get('p06_semantic') or {}).get('prompt_version'),
        'semantic_prompt_sha256': (bundle.get('p06_semantic') or {}).get('prompt_sha256'),
        'semantic_capsule_id': (bundle.get('p06_semantic') or {}).get('capsule_id'),
        'control_room': str(rd / 'control_room.html'),
        'capsule_id': cap.get('capsule_id'),
        'production_authority': promotion.get('state') == 'PRODUCTION_V3',
    }
    write_json(rd / 'pipeline_receipt.json', receipt)
    write_json(latest_dir / 'latest_pipeline_receipt.json', receipt)
    seal = build_final_seal(run_id, rd, cap, receipt)
    shutil.copy2(rd / 'run_seal.json', latest_dir / 'latest_run_seal.json')

    _progress(f"Run seal  : {seal.get('seal_id')}")
    _progress('============================================================')
    _progress(' GOLD COMMISSIONING - PASS')
    _progress('============================================================')
    _progress(f"Direction : {receipt.get('direction_candidate')}")
    _progress(f"Action    : {receipt.get('research_action_candidate')}")
    _progress(f"HTML      : {receipt.get('control_room')}")
    return receipt
