import argparse,json,sys
from pathlib import Path

def _r1_import(vault):
    p=str(Path(vault)/'RUNTIME'/'R1 Foundation')
    if p not in sys.path: sys.path.insert(0,p)
    from alpha_runtime.runtime import AlphaRuntime
    return AlphaRuntime

def main(argv=None):
    ap=argparse.ArgumentParser(); sp=ap.add_subparsers(dest='cmd',required=True)
    p=sp.add_parser('preflight'); p.add_argument('--vault-root',required=True)
    p=sp.add_parser('selftest'); p.add_argument('--vault-root',required=True)
    p=sp.add_parser('bootstrap'); p.add_argument('--vault-root',required=True); p.add_argument('--data-root'); p.add_argument('--run-id',required=True); p.add_argument('--coverage-mode',default='STRICT_FULL'); p.add_argument('--research-depth',default='AUTO')
    p=sp.add_parser('plan'); p.add_argument('--vault-root',required=True); p.add_argument('--data-root'); p.add_argument('--run-id',required=True)
    p=sp.add_parser('status'); p.add_argument('--vault-root',required=True); p.add_argument('--data-root'); p.add_argument('--run-id',required=True)
    p=sp.add_parser('start'); p.add_argument('--vault-root',required=True); p.add_argument('--data-root'); p.add_argument('--run-id',required=True); p.add_argument('--process-id',required=True); p.add_argument('--job-hash')
    p=sp.add_parser('complete'); p.add_argument('--vault-root',required=True); p.add_argument('--data-root'); p.add_argument('--run-id',required=True); p.add_argument('--process-id',required=True); p.add_argument('--file',required=True)
    p=sp.add_parser('finalize-decision'); p.add_argument('--vault-root',required=True); p.add_argument('--data-root'); p.add_argument('--run-id',required=True)
    p=sp.add_parser('gate'); p.add_argument('--vault-root',required=True); p.add_argument('--data-root'); p.add_argument('--run-id',required=True); p.add_argument('--gate-id',required=True)
    args=ap.parse_args(argv)
    if args.cmd=='preflight':
        from .preflight import run; out=run(args.vault_root); print(json.dumps(out,indent=2)); return 0 if out['status']=='PASS' else 2
    if args.cmd=='selftest':
        from .selftest import run; out=run(args.vault_root); print(json.dumps(out,indent=2)); return 0 if out['status']=='PASS' else 2
    AlphaRuntime=_r1_import(args.vault_root); rt=AlphaRuntime(args.vault_root,getattr(args,'data_root',None))
    from .orchestrator import R2Orchestrator; r2=R2Orchestrator(rt)
    if args.cmd=='bootstrap': out=r2.bootstrap(args.run_id,args.coverage_mode,args.research_depth)
    elif args.cmd=='plan': out=r2.ready_jobs(args.run_id)
    elif args.cmd=='status': out=r2.status(args.run_id)
    elif args.cmd=='start': r2.start(args.run_id,args.process_id,args.job_hash); out=r2.status(args.run_id)
    elif args.cmd=='complete': out=r2.complete(args.run_id,args.process_id,json.loads(Path(args.file).read_text(encoding='utf-8')))
    elif args.cmd=='finalize-decision': out=r2.finalize_decision(args.run_id)
    elif args.cmd=='gate': out=r2.gate(args.run_id,args.gate_id,store_receipt=False)
    print(json.dumps(out,ensure_ascii=False,indent=2)); return 0
