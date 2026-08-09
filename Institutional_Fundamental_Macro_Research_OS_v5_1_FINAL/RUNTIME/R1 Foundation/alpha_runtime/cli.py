import argparse, json, sys, os
from pathlib import Path
from .runtime import AlphaRuntime
from .visibility import build_receipt
from .seal_safe import create_decision_seal, verify_decision_seal, create_close_seal, verify_close_seal
from .preflight import run as preflight
from .selftest import run as selftest
from .timeutil import local_to_utc
from .canonical import load_json, dump_json


def main(argv=None):
    p=argparse.ArgumentParser(prog='alpha_runtime'); p.add_argument('--vault-root',required=True); p.add_argument('--data-root')
    sub=p.add_subparsers(dest='cmd',required=True)
    sub.add_parser('init')
    c=sub.add_parser('create-run'); c.add_argument('--request',required=True); c.add_argument('--vault-commit'); c.add_argument('--run-id')
    t=sub.add_parser('transition'); t.add_argument('--run-id',required=True); t.add_argument('--to',required=True)
    a=sub.add_parser('put-json'); a.add_argument('--run-id',required=True); a.add_argument('--logical-name',required=True); a.add_argument('--world',required=True); a.add_argument('--stage',required=True); a.add_argument('--file',required=True)
    v=sub.add_parser('build-visibility'); v.add_argument('--run-id',required=True); v.add_argument('--requirements',required=True); v.add_argument('--snapshots',required=True); v.add_argument('--mode')
    s=sub.add_parser('seal-decision'); s.add_argument('--run-id',required=True)
    sv=sub.add_parser('verify-decision'); sv.add_argument('--run-id',required=True)
    sc=sub.add_parser('seal-close'); sc.add_argument('--run-id',required=True)
    vc=sub.add_parser('verify-close'); vc.add_argument('--run-id',required=True)
    rp=sub.add_parser('reproduce-visibility'); rp.add_argument('--source-run-id',required=True); rp.add_argument('--requirements',required=True); rp.add_argument('--new-run-id')
    n=sub.add_parser('normalize-local-time'); n.add_argument('--local',required=True); n.add_argument('--zone',required=True); n.add_argument('--fold',type=int,choices=[0,1])
    sub.add_parser('selftest'); sub.add_parser('preflight')
    args=p.parse_args(argv)
    if args.cmd=='selftest':
        out=selftest(args.vault_root); print(json.dumps(out,indent=2)); return 0 if out['status']=='PASS' else 2
    if args.cmd=='preflight':
        out=preflight(args.vault_root); print(json.dumps(out,indent=2)); return 0 if out['status']=='PASS' else 2
    if args.cmd=='normalize-local-time': print(local_to_utc(args.local,args.zone,args.fold)); return 0
    rt=AlphaRuntime(args.vault_root,args.data_root)
    if args.cmd=='init': print(json.dumps({'status':'PASS','data_root':str(rt.data_root),'runtime':'R1.0.0'},indent=2)); return 0
    if args.cmd=='create-run':
        m,reused=rt.create_run(load_json(args.request),args.vault_commit,args.run_id); print(json.dumps({'status':'PASS','reused':reused,'manifest':m},indent=2)); return 0
    if args.cmd=='transition': print(json.dumps(rt.lifecycle.transition(args.run_id,args.to),indent=2)); return 0
    if args.cmd=='put-json': print(json.dumps(rt.store.put_artifact(args.run_id,args.logical_name,args.world,args.stage,load_json(args.file)),indent=2)); return 0
    if args.cmd=='build-visibility':
        m=rt.store.load_manifest(args.run_id); req=load_json(args.requirements); sn=load_json(args.snapshots); mode=args.mode or m['run_mode']; receipt=build_receipt(args.run_id,m['analysis_cutoff_utc'],mode,req if isinstance(req,list) else req['requirements'],sn if isinstance(sn,list) else sn['snapshots']); print(json.dumps(receipt,indent=2)); return 0
    if args.cmd=='seal-decision': print(json.dumps(create_decision_seal(args.run_id,rt),indent=2)); return 0
    if args.cmd=='verify-decision': print(json.dumps({'status':'PASS' if verify_decision_seal(args.run_id,rt) else 'FAIL'},indent=2)); return 0
    if args.cmd=='seal-close': print(json.dumps(create_close_seal(args.run_id,rt),indent=2)); return 0
    if args.cmd=='verify-close': print(json.dumps({'status':'PASS' if verify_close_seal(args.run_id,rt) else 'FAIL'},indent=2)); return 0
    if args.cmd=='reproduce-visibility':
        req=load_json(args.requirements); req=req if isinstance(req,list) else req['requirements']; m,meta=rt.reproduce_visibility_run(args.source_run_id,req,args.new_run_id); print(json.dumps({'status':'PASS','manifest':m,'replay_receipt':meta},indent=2)); return 0
    return 1
