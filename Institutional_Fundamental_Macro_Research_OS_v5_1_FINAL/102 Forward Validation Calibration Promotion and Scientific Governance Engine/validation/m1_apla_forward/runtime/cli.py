import argparse,json,sys
from pathlib import Path
from .preflight import run as preflight
from .engine import run_suite
from .acceptance import run as acceptance
from .ledger import append,validate
from .util import sha,now

def main(argv=None):
    p=argparse.ArgumentParser(prog='alphalab-m1-apla-forward-validate');p.add_argument('--vault-root',required=True);sp=p.add_subparsers(dest='cmd',required=True)
    sp.add_parser('preflight');sp.add_parser('selftest');sp.add_parser('suite');sp.add_parser('acceptance');q=sp.add_parser('ledger-validate');q.add_argument('--ledger',required=True);q=sp.add_parser('append-suite');q.add_argument('--ledger',required=True);q=sp.add_parser('commit-forward');q.add_argument('--ledger',required=True);q.add_argument('--run-id',required=True);q.add_argument('--analysis-cutoff-utc',required=True);q.add_argument('--payload',required=True);q.add_argument('--truth-state',choices=['SHADOW_LIVE','TRUE_FORWARD_VALIDATION'],required=True)
    a=p.parse_args(argv);v=Path(a.vault_root).resolve()
    if a.cmd=='preflight':out=preflight(v)
    elif a.cmd=='selftest':
        from .selftest import run as selftest;out=selftest(v)
    elif a.cmd=='suite':out=run_suite(v)
    elif a.cmd=='acceptance':out=acceptance(v)
    elif a.cmd=='ledger-validate':out=validate(a.ledger)
    elif a.cmd=='append-suite':
        s=run_suite(v);out={'status':'PASS','appended':[]}
        for r in s['records']:out['appended'].append(append(a.ledger,r))
    else:
        payload=json.loads(Path(a.payload).read_text(encoding='utf-8'));rec={'schema_version':'1.0.0','validation_version':'FV1.0.0','record_id':'FV1_COMMIT_'+a.run_id,'case_id':a.run_id,'truth_state':a.truth_state,'m1':{'status':'PRE_OUTCOME'},'apl_a':{'mode':'SHADOW_ONLY'},'interaction':'NONE','authority':{'direction_mutated':False,'permission_mutated':False},'analysis_cutoff_utc':a.analysis_cutoff_utc,'payload_hash':sha(payload),'created_at_utc':now()};out=append(a.ledger,rec)
    print(json.dumps(out,ensure_ascii=False,indent=2));return 0 if out.get('status')=='PASS' else 2
if __name__=='__main__':raise SystemExit(main())
