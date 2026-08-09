import argparse,json
from pathlib import Path
from .certification import run as certify
from .preflight import run as preflight
from .environment import inspect as envinspect

def main(argv=None):
    ap=argparse.ArgumentParser(prog='alpha-certify');ap.add_argument('--vault-root',required=True);sub=ap.add_subparsers(dest='cmd',required=True)
    c=sub.add_parser('certify');c.add_argument('--profile',choices=['CORE','FULL','ENVIRONMENT'],default='CORE');c.add_argument('--out')
    sub.add_parser('preflight');sub.add_parser('environment')
    a=ap.parse_args(argv);v=Path(a.vault_root)
    if a.cmd=='certify':out=certify(v,a.profile)
    elif a.cmd=='preflight':out=preflight(v)
    else:out=envinspect(v)
    s=json.dumps(out,ensure_ascii=False,indent=2)
    print(s)
    if getattr(a,'out',None):Path(a.out).write_text(s+'\n',encoding='utf-8',newline='\n')
    if a.cmd=='environment':return 0
    return 0 if out.get('status') in ('PASS','PENDING') else 2
