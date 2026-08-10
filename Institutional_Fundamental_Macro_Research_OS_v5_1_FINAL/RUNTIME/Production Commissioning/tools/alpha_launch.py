from pathlib import Path
import sys,json,argparse
HERE=Path(__file__).resolve();C1=HERE.parent.parent
if str(C1) not in sys.path:sys.path.insert(0,str(C1))
from alpha_commissioning.launcher import main as launch

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--vault-root',required=True);ap.add_argument('args',nargs=argparse.REMAINDER);a=ap.parse_args();out=launch(a.vault_root,a.args);print(json.dumps(out,ensure_ascii=False,indent=2));return 0
if __name__=='__main__':raise SystemExit(main())
