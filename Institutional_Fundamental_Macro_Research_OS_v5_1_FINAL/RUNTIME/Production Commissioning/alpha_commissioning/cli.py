from pathlib import Path
import argparse,json,sys
from .selftest import run as selftest
from .environment import doctor,certify as env_certify
from .shadow import certify as shadow_certify
from .readiness import evaluate as readiness
from .launcher import main as launch

def main(argv=None):
    ap=argparse.ArgumentParser(prog='alpha-commission');ap.add_argument('--vault-root',required=True);sp=ap.add_subparsers(dest='cmd',required=True)
    sp.add_parser('selftest');sp.add_parser('doctor');sp.add_parser('environment')
    p=sp.add_parser('shadow');p.add_argument('--runs-per-instrument',type=int,default=None)
    p=sp.add_parser('readiness');p.add_argument('--signoff',action='store_true')
    p=sp.add_parser('launch');p.add_argument('launch_args',nargs=argparse.REMAINDER)
    a=ap.parse_args(argv);v=Path(a.vault_root).resolve()
    if a.cmd=='selftest':out=selftest(v)
    elif a.cmd=='doctor':out=doctor(v)
    elif a.cmd=='environment':out=env_certify(v)
    elif a.cmd=='shadow':out=shadow_certify(v,a.runs_per_instrument)
    elif a.cmd=='readiness':out=readiness(v,a.signoff)
    elif a.cmd=='launch':out=launch(v,a.launch_args)
    print(json.dumps(out,ensure_ascii=False,indent=2));return 0 if out.get('status') in ('PASS','PENDING') else 2
if __name__=='__main__':raise SystemExit(main())
