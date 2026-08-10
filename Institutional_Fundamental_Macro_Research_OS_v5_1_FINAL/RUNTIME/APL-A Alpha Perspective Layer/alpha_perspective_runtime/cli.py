import argparse
import json
from .preflight import run as preflight
from .selftest import run as selftest
from .parity import run as parity
from .acceptance import run as acceptance


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('--vault-root', required=True)
    p.add_argument('cmd', choices=['preflight', 'selftest', 'parity', 'acceptance'])
    a = p.parse_args(argv)
    if a.cmd == 'preflight':
        out = preflight(a.vault_root)
    elif a.cmd == 'selftest':
        out = selftest(a.vault_root)
    elif a.cmd == 'parity':
        out = parity(a.vault_root)
    else:
        pa = parity(a.vault_root)
        out = acceptance(a.vault_root, pa)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if out['status'] == 'PASS' else 2
