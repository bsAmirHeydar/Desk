import argparse,json,sys
from pathlib import Path
from .compiler import compile_request
from .executor import execute
from .selftest import run as selftest
from .acceptance import run as acceptance

def _request_from_args(a):
    if a.request_file:return json.loads(Path(a.request_file).read_text(encoding='utf-8'))
    return {'schema_version':'1.0.0','subject':a.subject,'request_text':a.request,'mode':a.mode,'as_of':a.as_of,'horizon':a.horizon,'depth':a.depth,'output_profile':a.output,'locale':a.locale,'research_class':a.research_class,'intent_tags':a.tag or []}
def main(argv=None):
    ap=argparse.ArgumentParser(prog='alpha-research');ap.add_argument('--vault-root',required=True);ap.add_argument('--data-root');sp=ap.add_subparsers(dest='cmd',required=True)
    for name in ('compile','run'):
        p=sp.add_parser(name);p.add_argument('--request-file');p.add_argument('--subject');p.add_argument('--request');p.add_argument('--mode',default='LIVE');p.add_argument('--as-of');p.add_argument('--horizon');p.add_argument('--depth',default='AUTO');p.add_argument('--output',default='EXPLORER');p.add_argument('--locale');p.add_argument('--research-class');p.add_argument('--tag',action='append');
        if name=='run':p.add_argument('--truth-state',choices=['SHADOW_LIVE','TRUE_FORWARD'])
    sp.add_parser('selftest');sp.add_parser('acceptance')
    a=ap.parse_args(argv);v=Path(a.vault_root).resolve()
    if a.cmd=='selftest':out=selftest(v)
    elif a.cmd=='acceptance':out=acceptance(v)
    else:
        req=_request_from_args(a)
        if not req.get('subject') or not req.get('request_text'):raise RuntimeError('subject and request are required')
        comp=compile_request(v,req);out=comp if a.cmd=='compile' else execute(v,comp,a.data_root,a.truth_state)
    print(json.dumps(out,ensure_ascii=False,indent=2));return 0 if out.get('status','PASS') in ('PASS','PLAN_ONLY') else 2
if __name__=='__main__':raise SystemExit(main())
