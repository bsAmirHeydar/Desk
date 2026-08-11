from pathlib import Path
import sys
from .util import load_json,now
from .result import build as build_result
from .report_model import build as build_report
from .render import render_files,render_pdf_from_html
from .quality import pre_run,evaluate,set_gate,report_fidelity
from .memory import find_previous,build_capsule,persist

def _paths(v):
    for p in [v/'RUNTIME'/'R1 Foundation',v/'RUNTIME'/'R2 Prompt Execution OS',v/'RUNTIME'/'R3 Operational Execution and Learning OS',v/'RUNTIME'/'Production Commissioning',v/'RUNTIME'/'Core Research Method Kernel']:
        if str(p) not in sys.path:sys.path.insert(0,str(p))

def execute(vault_root,compiled,data_root=None,truth_state=None):
    v=Path(vault_root).resolve();_paths(v)
    pre=pre_run(v,compiled)
    if pre['status']=='BLOCKED':return {'status':'BLOCKED','classification':'RUN2_PRE_RUN_BLOCKED','compiled_intent':compiled,'run_quality_receipt':pre,'authority':{'direction':'UNCHANGED','broker_write':'NONE','apl_a':'SHADOW_ONLY'},'created_at_utc':now()}
    if compiled['execution_eligibility']!='CERTIFIED_RUNTIME':return {'status':'PLAN_ONLY','classification':compiled['execution_eligibility'],'compiled_intent':compiled,'run_quality_receipt':pre,'reason':'Subject is outside certified production runtime. NEW_ASSET_RESEARCH plan may proceed, but production execution is blocked.'}
    from alpha_commissioning.util import data_root as default_data_root
    from alpha_commissioning.launcher import _require_certification
    dr=Path(data_root).resolve() if data_root else default_data_root(v)
    mode=compiled['mode'];certmode='SHADOW' if mode=='SHADOW' else ('HISTORICAL' if mode in ('HISTORICAL','WALK_FORWARD','REPLAY') else 'LIVE')
    _require_certification(v,dr,certmode)
    from alpha_runtime.runtime import AlphaRuntime
    from alpha_prompt_runtime.orchestrator import R2Orchestrator
    from alpha_operational_runtime.catalog_ext import init_r3
    from alpha_operational_runtime.launcher import Launcher
    from alpha_operational_runtime.retrieval import RetrievalRuntime
    from alpha_operational_runtime.host import make_host
    from alpha_operational_runtime.driver import RunDriver
    rt=AlphaRuntime(v,dr);r2=R2Orchestrator(rt);init_r3(rt.catalog);L=Launcher(v,rt)
    hp=load_json(v/'RUNTIME'/'R3 Operational Execution and Learning OS'/'config'/'host_policy.json');binding=hp['bindings']['PRODUCTION_COMMAND']
    results=[]
    for sub in compiled['resolved_subjects']:
        inst=sub['canonical'];previous=find_previous(dr,compiled,inst);tags=list(compiled['intent_tags'])+['run_quality:RUN2.0.0','persistence:ON'];coverage='EVENT_FAST_STRICT' if compiled['primary_research_class']=='EVENT_ANALYSIS' else ('DEEP_ESCALATION' if compiled['depth'] in ('DEEP','CRITICAL') else 'STRICT_FULL')
        rdepth='DEEP' if compiled['depth'] in ('DEEP','CRITICAL') else ('STANDARD' if compiled['depth'] in ('LIGHT','STANDARD') else 'AUTO')
        profile='SHADOW_ONLY_V1' if compiled['r3_run_mode']=='SHADOW_LIVE' else 'PERMISSION_ONLY_V1'
        req=L.compile_request(inst,compiled['r3_run_mode'],compiled['analysis_cutoff'],compiled['active_horizon'],coverage,rdepth,'FULL',profile,tags=tags)
        live_intake=None
        if req['run_mode'] in ('LIVE','SHADOW_LIVE'):
            host=make_host(binding,dr,production=True);retriever=host.retrieve if 'EVIDENCE_RETRIEVAL' in binding.get('optional_capabilities',[])+binding.get('required_capabilities',[]) else None
            live_intake=RetrievalRuntime(v,rt).prefetch_live(req['instrument'],req['active_horizon'],retriever,req.get('allow_private_sources',False));req=dict(req);req['analysis_cutoff']=live_intake['cutoff_utc'];req['tags']=list(req.get('tags') or [])+['live-intake:'+live_intake['intake_id']]
        launch=L.create_request(req);rid=launch['run_id']
        rt.store.put_artifact(rid,'unified_request','META','META',compiled['original_request'],'application/json',producer_process_id='RUN2_REQUEST',producer_version='RUN2.0.0')
        rt.store.put_artifact(rid,'compiled_intent','META','META',compiled,'application/json',producer_process_id='RUN2_COMPILER',producer_version='RUN2.0.0')
        rt.store.put_artifact(rid,'run2_pre_run_receipt','META','META',pre,'application/json',producer_process_id='RUN2_QUALITY',producer_version='RUN2.0.0')
        r2.bootstrap(rid,req['coverage_mode'],req['research_depth']);seal=RunDriver(v,rt,r2,'PRODUCTION_COMMAND',live_intake=live_intake).run_to_decision(rid,production=True)
        can=build_result(rt,rid,compiled['request_id']);rt.store.put_artifact(rid,'canonical_scientific_result','META','OUTCOME',can,'application/json',producer_process_id='UI_RESULT',producer_version='UX3.0.0')
        quality=evaluate(rt,rid,compiled,can)
        preliminary=build_report(rt,rid,can,compiled,quality,None,None);fid=report_fidelity(can,preliminary);quality=set_gate(quality,'REPORT_FIDELITY','PASS' if fid['status']=='PASS' else 'FAIL',fid)
        cap0=build_capsule(rt,rid,compiled,can,quality,previous=previous);cap,persist_receipt=persist(dr,cap0);quality=cap['run_quality_receipt']
        rt.store.put_artifact(rid,'run_quality_receipt','META','OUTCOME',quality,'application/json',producer_process_id='RUN2_QUALITY',producer_version='RUN2.0.0')
        rt.store.put_artifact(rid,'run_capsule','META','OUTCOME',cap,'application/json',producer_process_id='RUN2_MEMORY',producer_version='RUN2.0.0')
        rt.store.put_artifact(rid,'run_persistence_receipt','META','OUTCOME',persist_receipt,'application/json',producer_process_id='RUN2_MEMORY',producer_version='RUN2.0.0')
        rm=build_report(rt,rid,can,compiled,quality,cap,cap.get('changes_since_previous'));rt.store.put_artifact(rid,'canonical_report_model','META','OUTCOME',rm,'application/json',producer_process_id='UI_REPORT_MODEL',producer_version='UX3.0.0')
        outdir=dr/'reports'/'unified';files=render_files(outdir,rm,compiled['output_profile'])
        if compiled['output_profile']=='ARCHIVE_PDF':files['pdf']=render_pdf_from_html(files['html_path'],str(Path(files['html_path']).with_suffix('.pdf')))
        commitment=None
        if compiled['r3_run_mode']=='SHADOW_LIVE':
            from alpha_commissioning.true_forward import seal_run
            commitment=seal_run(v,rid,truth_state or 'SHADOW_LIVE')
        results.append({'run_id':rid,'decision_seal_hash':seal.get('decision_seal_hash'),'canonical_result':can,'run_quality_receipt':quality,'run_capsule':{'path':persist_receipt['path'],'capsule_hash':cap['capsule_hash'],'quality_status':cap['quality_status'],'reproducibility_state':cap['reproducibility_state']},'changes_since_previous':cap.get('changes_since_previous'),'report':files,'forward_commitment':commitment})
    overall='PASS' if all(x['run_quality_receipt']['status'] in ('PASS','PASS_WITH_WARNINGS') for x in results) else ('PARTIAL' if all(x['run_quality_receipt']['status']!='BLOCKED' for x in results) else 'BLOCKED')
    return {'schema_version':'1.0.0','status':overall,'interface_version':'UX3.0.0','run_contract_version':'RUN2.0.0','request_id':compiled['request_id'],'compiled_intent':compiled,'results':results,'authority':{'direction':'UNCHANGED','broker_write':'NONE','apl_a':'SHADOW_ONLY'},'created_at_utc':now()}
