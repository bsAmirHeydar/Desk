import argparse,json,sys
from pathlib import Path
def _imports(vault,data_root=None):
    v=Path(vault).resolve()
    for p in (str(v/'RUNTIME'/'R1 Foundation'),str(v/'RUNTIME'/'R2 Prompt Execution OS')):
        if p not in sys.path:sys.path.insert(0,p)
    from alpha_runtime.runtime import AlphaRuntime
    from alpha_prompt_runtime.orchestrator import R2Orchestrator
    rt=AlphaRuntime(v,data_root);r2=R2Orchestrator(rt);from .catalog_ext import init_r3;init_r3(rt.catalog);return v,rt,r2
def _make_run(v,rt,r2,L,args,req):
    if req.get('run_mode')=='REPRODUCTION_REPLAY':
        raise RuntimeError('REPRODUCTION_REPLAY execution requires the dedicated frozen-source reproduction path; R3 exposes reproduction-plan only and R4 certifies full parity.')
    live_intake=None
    from .host import make_host
    from .retrieval import RetrievalRuntime
    hp=json.loads((v/'RUNTIME'/'R3 Operational Execution and Learning OS'/'config'/'host_policy.json').read_text(encoding='utf-8'));binding=hp['bindings'][args.host_binding]
    if req['run_mode'] in ('LIVE','SHADOW_LIVE'):
        host=make_host(binding,rt.data_root,production=True);retriever=host.retrieve if 'EVIDENCE_RETRIEVAL' in binding.get('optional_capabilities',[])+binding.get('required_capabilities',[]) else None
        live_intake=RetrievalRuntime(v,rt).prefetch_live(req['instrument'],req['active_horizon'],retriever,req.get('allow_private_sources',False));req=dict(req);req['analysis_cutoff']=live_intake['cutoff_utc'];req['tags']=list(req.get('tags') or [])+['live-intake:'+live_intake['intake_id']]
    launch=L.create_request(req);rid=launch['run_id'];r2.bootstrap(rid,req['coverage_mode'],req['research_depth']);from .driver import RunDriver;seal=RunDriver(v,rt,r2,args.host_binding,live_intake=live_intake).run_to_decision(rid,production=True);return rid,seal
def main(argv=None):
    ap=argparse.ArgumentParser(prog='alpha');ap.add_argument('--vault-root',required=True);ap.add_argument('--data-root');sp=ap.add_subparsers(dest='cmd',required=True);sp.add_parser('preflight');sp.add_parser('selftest')
    p=sp.add_parser('run');p.add_argument('instrument');p.add_argument('--mode',default='LIVE');p.add_argument('--at');p.add_argument('--horizon',default='DAILY_OPEN_TO_CLOSE');p.add_argument('--coverage',default='STRICT_FULL');p.add_argument('--depth',default='AUTO');p.add_argument('--output-depth',default='FULL');p.add_argument('--execution-profile',default='PERMISSION_ONLY_V1');p.add_argument('--host-binding',default='PRODUCTION_COMMAND');p.add_argument('--decision-only',action='store_true');p.add_argument('--allow-private-sources',action='store_true')
    p=sp.add_parser('daily-six-plan');p.add_argument('--mode',default='LIVE');p.add_argument('--at');p.add_argument('--horizon',default='DAILY_OPEN_TO_CLOSE')
    p=sp.add_parser('bulk-plan');p.add_argument('instrument');p.add_argument('--cutoffs-file',required=True);p.add_argument('--mode',default='HISTORICAL_REPLAY');p.add_argument('--horizon',default='DAILY_OPEN_TO_CLOSE')
    p=sp.add_parser('reproduction-plan');p.add_argument('--source-run-id',required=True)
    p=sp.add_parser('handoff');p.add_argument('--run-id',required=True);p=sp.add_parser('ingest-execution');p.add_argument('--file',required=True);p=sp.add_parser('outcome');p.add_argument('--run-id',required=True);p.add_argument('--execution-file');p.add_argument('--price-path-file');p=sp.add_parser('counterfactual-plan');p.add_argument('--run-id',required=True);p=sp.add_parser('counterfactual-unscorable');p.add_argument('--run-id',required=True);p=sp.add_parser('counterfactual-ingest');p.add_argument('--run-id',required=True);p.add_argument('--file',required=True);p=sp.add_parser('warehouse');p.add_argument('--run-id');p.add_argument('--export-jsonl',action='store_true');p.add_argument('--counterfactual-summary',action='store_true');p.add_argument('--instrument');p.add_argument('--branch');p=sp.add_parser('calibrate');p.add_argument('--file',required=True);p=sp.add_parser('report');p.add_argument('--run-id',required=True);p.add_argument('--depth',default='FULL');p=sp.add_parser('event-plan');p.add_argument('--name',required=True);p.add_argument('--time',required=True);p.add_argument('--instruments',nargs='+',required=True);p.add_argument('--mode',default='HISTORICAL_REPLAY')
    p=sp.add_parser('run-plan');p.add_argument('--file',required=True);p.add_argument('--host-binding',default='PRODUCTION_COMMAND');p.add_argument('--decision-only',action='store_true')
    p=sp.add_parser('daily-six-run');p.add_argument('--mode',default='LIVE');p.add_argument('--at');p.add_argument('--horizon',default='DAILY_OPEN_TO_CLOSE');p.add_argument('--host-binding',default='PRODUCTION_COMMAND');p.add_argument('--decision-only',action='store_true')
    p=sp.add_parser('meta-reconcile');p.add_argument('--run-ids',nargs='+',required=True)
    a=ap.parse_args(argv);v=Path(a.vault_root).resolve()
    if a.cmd=='preflight':from .preflight import run;out=run(v);print(json.dumps(out,ensure_ascii=False,indent=2));return 0 if out['status']=='PASS' else 2
    if a.cmd=='selftest':from .selftest import run;out=run(v);print(json.dumps(out,ensure_ascii=False,indent=2));return 0 if out['status']=='PASS' else 2
    v,rt,r2=_imports(v,a.data_root);from .launcher import Launcher;L=Launcher(v,rt)
    if a.cmd=='run':
        req=L.compile_request(a.instrument,a.mode,a.at,a.horizon,a.coverage,a.depth,a.output_depth,a.execution_profile,allow_private_sources=a.allow_private_sources);rid,seal=_make_run(v,rt,r2,L,a,req);out={'run_id':rid,'decision_seal':seal};from .forward import ForwardObservationRecorder;out['forward_observation']=ForwardObservationRecorder(v,rt).build(rid)
        if not a.decision_only:from .execution import ExecutionManager;out['execution_handoff']=ExecutionManager(v,rt).handoff(rid)
        print(json.dumps(out,ensure_ascii=False,indent=2));return 0
    if a.cmd=='run-plan':
        plan=json.loads(Path(a.file).read_text(encoding='utf-8'));reqs=plan.get('requests') if isinstance(plan,dict) else plan
        if not isinstance(reqs,list) or not reqs:raise RuntimeError('run-plan requires a non-empty requests list')
        results=[]
        for req in reqs:
            rid,seal=_make_run(v,rt,r2,L,a,req);item={'run_id':rid,'decision_seal':seal}
            from .forward import ForwardObservationRecorder;item['forward_observation']=ForwardObservationRecorder(v,rt).build(rid)
            if not a.decision_only:
                from .execution import ExecutionManager;item['execution_handoff']=ExecutionManager(v,rt).handoff(rid)
            results.append(item)
        out={'plan_id':plan.get('plan_id') if isinstance(plan,dict) else None,'episode_id':plan.get('episode_id') if isinstance(plan,dict) else None,'count':len(results),'results':results}
    elif a.cmd=='daily-six-run':
        ep,reqs=L.daily_six_requests(a.mode,a.at,a.horizon);results=[];rids=[]
        for req in reqs:
            rid,seal=_make_run(v,rt,r2,L,a,req);rids.append(rid);item={'run_id':rid,'decision_seal':seal}
            from .forward import ForwardObservationRecorder;item['forward_observation']=ForwardObservationRecorder(v,rt).build(rid)
            if not a.decision_only:
                from .execution import ExecutionManager;item['execution_handoff']=ExecutionManager(v,rt).handoff(rid)
            results.append(item)
        from .meta import MetaReconciler;out={'episode_id':ep,'count':len(results),'results':results,'meta_reconciliation':MetaReconciler(rt).reconcile(rids)}
    elif a.cmd=='meta-reconcile':
        from .meta import MetaReconciler;out=MetaReconciler(rt).reconcile(a.run_ids)
    elif a.cmd=='daily-six-plan':ep,reqs=L.daily_six_requests(a.mode,a.at,a.horizon);out={'episode_id':ep,'requests':reqs}
    elif a.cmd=='bulk-plan':cuts=json.loads(Path(a.cutoffs_file).read_text(encoding='utf-8'));out=L.bulk_requests(a.instrument,cuts,a.mode,a.horizon)
    elif a.cmd=='reproduction-plan':out=L.reproduction_request(a.source_run_id)
    elif a.cmd=='handoff':from .execution import ExecutionManager;out=ExecutionManager(v,rt).handoff(a.run_id)
    elif a.cmd=='ingest-execution':from .execution import ExecutionManager;out=ExecutionManager(v,rt).ingest_receipt(json.loads(Path(a.file).read_text(encoding='utf-8')))
    elif a.cmd=='outcome':from .outcome import OutcomeEngine;ex=json.loads(Path(a.execution_file).read_text(encoding='utf-8')) if a.execution_file else None;pp=json.loads(Path(a.price_path_file).read_text(encoding='utf-8')) if a.price_path_file else None;out=OutcomeEngine(v,rt).build(a.run_id,ex,pp)
    elif a.cmd=='counterfactual-plan':from .counterfactual import CounterfactualEngine;out=CounterfactualEngine(v,rt).plan(a.run_id)
    elif a.cmd=='counterfactual-unscorable':from .counterfactual import CounterfactualEngine;out=CounterfactualEngine(v,rt).attach_unscorable(a.run_id)
    elif a.cmd=='counterfactual-ingest':from .counterfactual import CounterfactualEngine;out=CounterfactualEngine(v,rt).ingest_scored(a.run_id,json.loads(Path(a.file).read_text(encoding='utf-8')))
    elif a.cmd=='warehouse':
        from .warehouse import Warehouse;w=Warehouse(v,rt)
        if a.counterfactual_summary:out=w.counterfactual_summary(a.instrument,a.branch)
        else:out=w.upsert_run(a.run_id) if a.run_id else w.accelerator_status()
        if a.export_jsonl:out={'result':out,'export':w.export_jsonl()}
    elif a.cmd=='calibrate':from .calibration import Calibrator;from .ledger import D4Ledger;out=Calibrator(v,rt).run(json.loads(Path(a.file).read_text(encoding='utf-8')));D4Ledger(rt).append('CALIBRATION_REPORT',out,None)
    elif a.cmd=='report':from .report import Reporter;out=Reporter(v,rt).render(a.run_id,a.depth)
    elif a.cmd=='event-plan':ep,reqs=L.event_requests(a.name,a.time,a.instruments,run_mode=a.mode);out={'episode_id':ep,'requests':reqs}
    print(json.dumps(out,ensure_ascii=False,indent=2));return 0
if __name__=='__main__':raise SystemExit(main())
