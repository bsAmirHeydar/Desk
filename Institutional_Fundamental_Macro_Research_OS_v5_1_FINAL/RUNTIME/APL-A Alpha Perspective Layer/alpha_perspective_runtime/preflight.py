from pathlib import Path
from .selftest import run as selftest
from .parity import run as parity
from .acceptance import run as acceptance
from .util import load_json


def run(vault):
    v = Path(vault)
    checks = []

    def ck(n, x, d=None):
        checks.append({'name': n, 'pass': bool(x), 'detail': d})

    try:
        pm = load_json(v / 'CURRENT_PRODUCTION_MANIFEST.json')
        rm = load_json(v / 'RUNTIME/RUNTIME_MANIFEST.json')
        ck('scientific_v213', pm.get('current_stack') == 'V21.3.0')
        ck('runtime_r4', rm.get('runtime_version') == 'R4.0.0')
        ck('commissioning_c1', rm.get('commissioning', {}).get('version') == 'C1.0.0')
        ck('apl_a_manifest', (v / 'RUNTIME/APL-A Alpha Perspective Layer/APL_A_MANIFEST.json').is_file())
        st = selftest(v)
        ck('apl_a_selftest', st['status'] == 'PASS', st)
        pa = parity(v)
        ck('apl_a_data_parity', pa['status'] == 'PASS', pa)
        ac = acceptance(v, pa)
        ck('apl_a_behavioral_acceptance', ac['status'] == 'PASS', ac)
    except Exception as e:
        ck('exception', False, str(e))

    return {
        'status': 'PASS' if all(x['pass'] for x in checks) else 'FAIL',
        'checks': checks,
        'errors': [x for x in checks if not x['pass']],
    }
