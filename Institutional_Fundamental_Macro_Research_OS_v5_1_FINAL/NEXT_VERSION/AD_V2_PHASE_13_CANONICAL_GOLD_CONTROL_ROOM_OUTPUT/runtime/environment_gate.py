from __future__ import annotations
from pathlib import Path
import json, os, sys

from .common import dump_json


class EnvironmentGateError(RuntimeError):
    pass


def _commissioning_paths(vault: Path):
    p = vault / 'RUNTIME' / 'Production Commissioning'
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
    return p


def _p11_root(vault: Path):
    return vault / 'NEXT_VERSION' / 'AD_V2_PHASE_11_UNIFIED_COMMAND_RESEARCH_ORCHESTRATION'


def _receipt_path(data_root: Path):
    return Path(data_root) / 'commissioning' / 'environment_receipt.json'


def _load_json(path: Path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def _surface(vault: Path):
    _commissioning_paths(vault)
    from alpha_commissioning.util import current_certification_surface
    return current_certification_surface(vault)


def environment_status(vault: Path, data_root: Path):
    vault = Path(vault).resolve()
    data_root = Path(data_root).resolve()
    p = _receipt_path(data_root)
    surface = _surface(vault)
    if not p.is_file():
        return {
            'schema_version': '1.0.0',
            'status': 'MISSING',
            'classification': 'NOT_CERTIFIED',
            'receipt_path': str(p),
            'current_certification_surface': surface,
            'api_key_present': bool(os.environ.get('OPENAI_API_KEY')),
        }
    try:
        r = _load_json(p)
    except Exception as e:
        return {
            'schema_version': '1.0.0',
            'status': 'INVALID',
            'classification': 'NOT_CERTIFIED',
            'receipt_path': str(p),
            'current_certification_surface': surface,
            'api_key_present': bool(os.environ.get('OPENAI_API_KEY')),
            'error': str(e),
        }
    if r.get('status') != 'PASS' or r.get('classification') != 'ENVIRONMENT_CERTIFIED':
        state = 'FAILED'
    elif r.get('certification_surface_fingerprint') != surface:
        state = 'STALE'
    else:
        state = 'PASS'
    return {
        'schema_version': '1.0.0',
        'status': state,
        'classification': r.get('classification'),
        'receipt_path': str(p),
        'current_certification_surface': surface,
        'receipt_certification_surface': r.get('certification_surface_fingerprint'),
        'created_at_utc': r.get('created_at_utc'),
        'api_key_present': bool(os.environ.get('OPENAI_API_KEY')),
        'certification_profile': r.get('certification_profile'),
        'errors': r.get('errors') or [],
    }


def _verify_direct_v1_binding(repo: Path, vault: Path):
    p11 = _p11_root(vault)
    runtime_parent = vault / 'NEXT_VERSION'
    if str(runtime_parent) not in sys.path:
        sys.path.insert(0, str(runtime_parent))
    from AD_V2_PHASE_11_UNIFIED_COMMAND_RESEARCH_ORCHESTRATION.runtime.v1_launcher_guard import (
        load_policy,
        verify_v1_root_launcher,
    )
    return verify_v1_root_launcher(repo, load_policy(p11))


def reconcile_doctor(repo: Path, vault: Path, doctor_result: dict):
    """Reconcile the legacy C1 root-wrapper check with the governed P11 direct-runtime bridge.

    No other C1 doctor failure is waived. This only supersedes the obsolete requirement that
    AlphaLab.ps1/AlphaLab_Commission.ps1 exist at repository root when P11's frozen direct V1
    runtime authority binding is valid.
    """
    rows = [dict(x) for x in (doctor_result.get('checks') or [])]
    errors = list(doctor_result.get('errors') or [])
    failed_names = {x.get('name') for x in rows if not x.get('pass')}
    allowed_legacy_failure = 'root_launchers_match_certified_templates'
    other_failed = sorted(x for x in failed_names if x != allowed_legacy_failure)
    other_errors = [x for x in errors if x != allowed_legacy_failure]
    if other_failed or other_errors:
        return {
            'status': 'FAIL',
            'checks': rows,
            'errors': sorted(set(other_errors + other_failed)),
            'legacy_root_launcher_reconciled': False,
            'v1_direct_binding': None,
        }
    binding = _verify_direct_v1_binding(Path(repo).resolve(), Path(vault).resolve())
    if binding.get('status') != 'PASS':
        return {
            'status': 'FAIL',
            'checks': rows,
            'errors': ['P11 direct V1 authority binding failed'],
            'legacy_root_launcher_reconciled': False,
            'v1_direct_binding': binding,
        }
    out_rows = []
    for row in rows:
        if row.get('name') == allowed_legacy_failure:
            out_rows.append({
                'name': 'legacy_root_launchers_superseded_by_p11_direct_v1_binding',
                'pass': True,
                'original_check': allowed_legacy_failure,
            })
        else:
            out_rows.append(row)
    out_rows.append({'name': 'p11_direct_v1_authority_binding', 'pass': True})
    return {
        'status': 'PASS',
        'checks': out_rows,
        'errors': [],
        'legacy_root_launcher_reconciled': allowed_legacy_failure in failed_names,
        'v1_direct_binding': {
            'status': binding.get('status'),
            'launcher_presence': binding.get('launcher_presence'),
            'bridge_mode': binding.get('bridge_mode'),
            'canonical_sha256': binding.get('canonical_sha256'),
            'git_blob': binding.get('git_blob'),
            'p00_commit': binding.get('p00_commit'),
        },
    }


def certify_environment(repo: Path, vault: Path, data_root: Path):
    repo = Path(repo).resolve()
    vault = Path(vault).resolve()
    data_root = Path(data_root).resolve()
    _commissioning_paths(vault)
    from alpha_commissioning.environment import doctor
    from alpha_commissioning.openai_api import OpenAIResponsesClient, output_text, web_sources
    from alpha_commissioning.util import current_certification_surface, load_json, now

    d = doctor(vault)
    compat = reconcile_doctor(repo, vault, d)
    checks = list(compat.get('checks') or [])
    errors = list(compat.get('errors') or [])
    p = _receipt_path(data_root)
    if compat.get('status') != 'PASS':
        out = {
            'schema_version': '1.0.0',
            'status': 'FAIL',
            'classification': 'NOT_CERTIFIED',
            'certification_profile': 'P13_P11_DIRECT_RUNTIME_COMPATIBLE_C1',
            'checks': checks,
            'errors': errors,
            'v1_direct_binding': compat.get('v1_direct_binding'),
            'created_at_utc': now(),
        }
        dump_json(p, out)
        return out

    if not os.environ.get('OPENAI_API_KEY'):
        out = {
            'schema_version': '1.0.0',
            'status': 'FAIL',
            'classification': 'NOT_CERTIFIED',
            'certification_profile': 'P13_P11_DIRECT_RUNTIME_COMPATIBLE_C1',
            'checks': checks + [{'name': 'openai_api_key_present', 'pass': False}],
            'errors': ['OPENAI_API_KEY is not set in the current environment'],
            'v1_direct_binding': compat.get('v1_direct_binding'),
            'created_at_utc': now(),
        }
        dump_json(p, out)
        return out

    surface = current_certification_surface(vault)
    cfg = load_json(vault / 'RUNTIME' / 'Production Commissioning' / 'config' / 'model_bindings.json')
    client = OpenAIResponsesClient(timeout=600, max_attempts=2)
    hp = cfg['health_profile']
    model_receipt = {}
    web_receipt = {}

    try:
        schema = {
            'type': 'object',
            'required': ['ok'],
            'properties': {'ok': {'type': 'boolean'}},
            'additionalProperties': False,
        }
        resp = client.create({
            'model': hp['model'],
            'reasoning': hp['reasoning'],
            'store': False,
            'input': 'Return {"ok":true}. This is an Alpha Desk production environment capability attestation.',
            'max_output_tokens': 200,
            'text': {'format': {'type': 'json_schema', 'name': 'alphadesk_health', 'strict': True, 'schema': schema}},
        })
        obj = json.loads(output_text(resp))
        ok = obj.get('ok') is True and bool(resp.get('id')) and bool(resp.get('model'))
        checks.append({'name': 'openai_gpt_5_6_sol_responses_health', 'pass': ok})
        if not ok:
            errors.append('model health response invalid')
        model_receipt = {
            'response_id': resp.get('id'),
            'configured_model': hp['model'],
            'returned_model': resp.get('model'),
            'status': resp.get('status'),
            'reasoning_requested': hp['reasoning'],
            'usage': resp.get('usage'),
            'store': False,
        }
    except Exception as e:
        checks.append({'name': 'openai_gpt_5_6_sol_responses_health', 'pass': False})
        errors.append('model health: ' + str(e))

    try:
        resp = client.create({
            'model': hp['model'],
            'reasoning': {'mode': 'pro', 'effort': 'high', 'context': 'current_turn'},
            'store': False,
            'tools': [{
                'type': 'web_search',
                'filters': {'allowed_domains': ['developers.openai.com']},
                'search_context_size': 'low',
            }],
            'tool_choice': 'required',
            'include': ['web_search_call.action.sources'],
            'input': 'Find the OpenAI API documentation page for web search and return its title in one sentence.',
            'max_output_tokens': 500,
        })
        src = web_sources(resp)
        ok = bool(src) and all('developers.openai.com' in (x.get('url') or '') for x in src)
        checks.append({'name': 'openai_web_search_domain_filter_health', 'pass': ok})
        if not ok:
            errors.append('web search did not return domain-filtered source evidence')
        web_receipt = {
            'response_id': resp.get('id'),
            'returned_model': resp.get('model'),
            'sources': src,
            'usage': resp.get('usage'),
            'store': False,
        }
    except Exception as e:
        checks.append({'name': 'openai_web_search_domain_filter_health', 'pass': False})
        errors.append('web search health: ' + str(e))

    status = 'PASS' if not errors and all(x.get('pass') for x in checks) else 'FAIL'
    out = {
        'schema_version': '1.0.0',
        'status': status,
        'classification': 'ENVIRONMENT_CERTIFIED' if status == 'PASS' else 'NOT_CERTIFIED',
        'certification_profile': 'P13_P11_DIRECT_RUNTIME_COMPATIBLE_C1',
        'checks': checks,
        'model_receipt': model_receipt,
        'web_search_receipt': web_receipt,
        'source_scope_note': 'Licensed/subscription/private feeds are not claimed connected by this environment attestation.',
        'data_root': str(data_root),
        'certification_surface_fingerprint': surface,
        'v1_direct_binding': compat.get('v1_direct_binding'),
        'legacy_root_launcher_reconciled': compat.get('legacy_root_launcher_reconciled'),
        'created_at_utc': now(),
        'errors': errors,
    }
    dump_json(p, out)
    return out


def ensure_environment(repo: Path, vault: Path, data_root: Path, auto_certify=True):
    st = environment_status(vault, data_root)
    if st.get('status') == 'PASS':
        return st
    if not auto_certify:
        raise EnvironmentGateError('Alpha Desk environment is not certified: ' + st.get('status', 'UNKNOWN'))
    if not os.environ.get('OPENAI_API_KEY'):
        raise EnvironmentGateError(
            'Alpha Desk environment certification is required before Run Gold. '
            'OPENAI_API_KEY is not set in this PowerShell environment. '
            'Set the key outside the repository, then run: .\\AlphaDesk.ps1 environment-certify'
        )
    rec = certify_environment(repo, vault, data_root)
    if rec.get('status') != 'PASS' or rec.get('classification') != 'ENVIRONMENT_CERTIFIED':
        raise EnvironmentGateError(
            'Alpha Desk environment certification failed: ' + '; '.join(rec.get('errors') or ['unknown error'])
        )
    return environment_status(vault, data_root)
