import argparse,json,sys
from pathlib import Path
from .util import add_paths

def _rt(vault,data_root=None):
    add_paths(vault); from alpha_runtime.runtime import AlphaRuntime; return AlphaRuntime(vault,data_root)

def main(argv=None):
    ap=argparse.ArgumentParser(prog='alpha-method'); ap.add_argument('--vault-root',required=True); ap.add_argument('--data-root'); sp=ap.add_subparsers(dest='cmd',required=True)
    sp.add_parser('preflight'); sp.add_parser('selftest'); sp.add_parser('parity'); sp.add_parser('acceptance')
    p=sp.add_parser('plan'); p.add_argument('--run-id',required=True)
    p=sp.add_parser('validate'); p.add_argument('--run-id',required=True); p.add_argument('--phase',choices=['EVIDENCE','COGNITION','PRE_DECISION','AD_HOC'],default='PRE_DECISION'); p.add_argument('--no-store',action='store_true'); p.add_argument('--no-block',action='store_true')
    a=ap.parse_args(argv); v=Path(a.vault_root).resolve()
    if a.cmd=='preflight': from .preflight import run; out=run(v)
    elif a.cmd in ('selftest','acceptance'): from .selftest import run; out=run(v)
    elif a.cmd=='parity': from .parity import run; out=run(v)
    else:
        rt=_rt(v,a.data_root); from .integration import ensure_plan,validate_phase
        if a.cmd=='plan': out=ensure_plan(v,rt,a.run_id)
        else: out=validate_phase(v,rt,a.run_id,a.phase,store=not a.no_store,raise_hard=not a.no_block)
    print(json.dumps(out,ensure_ascii=False,indent=2)); return 0 if out.get('status','PASS') not in ('FAIL','METHOD_INVALID','OUTPUT_QUARANTINED') else 2
