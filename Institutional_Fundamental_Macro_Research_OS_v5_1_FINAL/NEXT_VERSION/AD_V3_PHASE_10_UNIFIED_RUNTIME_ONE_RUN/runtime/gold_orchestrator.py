from __future__ import annotations
import json,pathlib,sys,time,traceback
from contextlib import contextmanager
from .common import iso,stable_id,atomic_json,atomic_text,load,sha_obj,sha_file
from .artifact_manager import ArtifactManager,build_seal,RuntimeLocked
from .control_room_input import build as build_cr_input
from AD_V3_PHASE_07_LIVE_INTRADAY_GOLD_DATA_KERNEL.runtime.acquisition_planner import build_plan
from AD_V3_PHASE_07_LIVE_INTRADAY_GOLD_DATA_KERNEL.runtime.kernel_runtime import run_kernel
from AD_V3_PHASE_03_CAUSAL_GOLD_BRAIN_DECISION_ENGINE.runtime.engine import execute as p03_execute
from AD_V3_PHASE_03_CAUSAL_GOLD_BRAIN_DECISION_ENGINE.runtime.loader import observation_history,current_previous_for_receipt
from AD_V3_PHASE_03_CAUSAL_GOLD_BRAIN_DECISION_ENGINE.runtime.semantic_packet import build_semantic_evidence_packet
from AD_V3_PHASE_06_GOVERNED_SEMANTIC_INTELLIGENCE.runtime.semantic_runtime import run_semantics
from AD_V3_PHASE_08_DECISION_SCIENCE_CALIBRATION.runtime.decision_runtime import calibrate as calibrate_decision
from AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0.runtime.forward_runtime import observe_and_evaluate as p09_observe_and_evaluate,precommit_current as p09_precommit_current,status as p09_status
from AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0.runtime.forward_ledger import load_state as p09_load_state,save_state as p09_save_state
from AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0.runtime.outcome_data import observation_from_anchor,add_observation
from AD_V31_R01_FORWARD_QUALITY_PROMOTION_SCIENCE.runtime.qualification_engine import qualify as r01_qualify
from AD_V31_R03_ANTIFRAGILE_MULTI_SCENARIO_PERSPECTIVE.runtime.perspective_runtime import run as run_r03_perspective, fail_closed as r03_fail_closed
from AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING.runtime.promotion import load_state as load_promotion
from AD_V3_PHASE_11_FINAL_INSTITUTIONAL_GOLD_CONTROL_ROOM.runtime.report_runtime import render_report as render_p11_report
from AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING.runtime.capsule import build as build_p04_capsule

VERSION='3.10.1-r03-perspective-stage'
STAGE_ORDER=['PRECHECK','FORWARD_EVALUATION','ACQUISITION_PLAN','ACQUISITION','PRE_SEMANTIC','SEMANTIC','FINAL_CAUSAL','DECISION_CALIBRATION','PERSPECTIVE_OVERLAY','FORWARD_PRECOMMIT','CONTROL_MODEL','REPORT','SEAL']

def _paths(repo):
    repo=pathlib.Path(repo);n=repo/'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL'/'NEXT_VERSION'
    return {k:n/v for k,v in {'p02':'AD_V3_PHASE_02_TOTAL_LIVE_DATA_OBSERVABILITY_FABRIC','p03':'AD_V3_PHASE_03_CAUSAL_GOLD_BRAIN_DECISION_ENGINE','p04':'AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING','p06':'AD_V3_PHASE_06_GOVERNED_SEMANTIC_INTELLIGENCE','p07':'AD_V3_PHASE_07_LIVE_INTRADAY_GOLD_DATA_KERNEL','p08':'AD_V3_PHASE_08_DECISION_SCIENCE_CALIBRATION','p09':'AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0','p10':'AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN','p11':'AD_V3_PHASE_11_FINAL_INSTITUTIONAL_GOLD_CONTROL_ROOM','r03':'AD_V31_R03_ANTIFRAGILE_MULTI_SCENARIO_PERSPECTIVE'}.items()}
def _progress(msg,quiet=False):
    if not quiet: print(msg,file=sys.stderr,flush=True)
def _obs(data_root,fact_id,run_id):
    p=pathlib.Path(data_root)/'observations/gold_fact_observations.jsonl';hit=None
    if not p.exists():return None
    for line in p.read_text(encoding='utf-8-sig').splitlines():
        try:o=json.loads(line)
        except Exception:continue
        if o.get('fact_id')==fact_id and o.get('acquisition_run_id')==run_id:hit=o
    return hit
def _price_anchor(data_root,run_id):
    for fact,kind,proxy in [('XAUUSD_SPOT_PRICE','SPOT_DIRECT',False),('GC_FUTURES_PRICE','GC_FUTURES_PROXY',True)]:
        o=_obs(data_root,fact,run_id)
        if not o or not isinstance(o.get('value'),(int,float)):continue
        if fact=='XAUUSD_SPOT_PRICE' and (o.get('directness')=='PROXY' or o.get('epistemic_state')=='PUBLIC_PROXY'):kind='SPOT_PUBLIC_PROXY';proxy=True
        meta=o.get('metadata') or {};sel=meta.get('selected_contract') or {}
        return {'value':float(o['value']),'economic_marker':o.get('reference_period') or o.get('event_time') or o.get('published_at') or o.get('retrieved_at'),'reference_period':o.get('reference_period'),'event_time':o.get('event_time'),'published_at':o.get('published_at'),'retrieved_at':o.get('retrieved_at'),'observation_id':o.get('observation_id'),'acquisition_run_id':run_id,'source_fact_id':fact,'source_id':o.get('source_id'),'anchor_kind':kind,'proxy_for_xauusd':proxy,'transmission_only':True,'causal_direction_authority':False,'instrument_key':sel.get('contract') if isinstance(sel,dict) else None}
    return None

def _evidence_index(data_root,run_id):
    p=pathlib.Path(data_root)/'observations/gold_fact_observations.jsonl';rows=[]
    if p.exists():
        for line in p.read_text(encoding='utf-8-sig').splitlines():
            try:o=json.loads(line)
            except Exception:continue
            if o.get('acquisition_run_id')!=run_id:continue
            rows.append({k:o.get(k) for k in ('fact_id','observation_id','value','value_type','unit','source_id','provenance_ref','directness','epistemic_state','reference_period','event_time','published_at','retrieved_at','metadata','warnings')})
    rows.sort(key=lambda x:str(x.get('fact_id') or ''))
    return {'record_type':'AD_V3_P11_EVIDENCE_INDEX','schema_version':'1.0.0','acquisition_run_id':run_id,'observation_count':len(rows),'observations':rows,'presentation_only':True,'scientific_authority':False}

def _record_price_only(anchor,state_root):
    if not anchor:return
    st=p09_load_state(state_root);obs=observation_from_anchor(anchor);add_observation(st,obs);p09_save_state(st,state_root)
def _versions(paths):
    out={}
    for k in ('p03','p06','p07','p08','p09','p10','p11','r03'):
        m=load(paths[k]/'DEVELOPMENT_MANIFEST.json',{}) or {};out[k.upper()]=m.get('version') or m.get('revision') or m.get('phase') or 'UNKNOWN'
    return out

def _classify(admission,decision):
    if admission in {'BLOCK','BLOCKED'}:return 'BLOCKED'
    action=((decision or {}).get('permission') or {}).get('research_action_candidate') or (decision or {}).get('permission_candidate')
    direction=(decision or {}).get('causal_direction')
    if admission in {'DEGRADED','DEGRADED_ALLOW'}:return 'SUCCESS_DEGRADED'
    if action in {None,'WAIT','WAIT_CANDIDATE'} or direction in {None,'UNKNOWN','MIXED'}:return 'SUCCESS_NONACTIONABLE'
    return 'SUCCESS'

def run_gold(repo_root,horizon='SESSION_1_6H',authority_mode='SHADOW',acquisition_mode='NORMAL',semantic_bundle_path=None,p02_data_root_override=None,artifact_root_override=None,kernel_fixture_dir=None,kernel_output_root_override=None,p09_state_root_override=None,r01_state_root_override=None,as_of_utc=None,fixture_mode=False,update_latest=True,fail_stage=None,quiet=False):
    repo=pathlib.Path(repo_root);paths=_paths(repo);decision_time=as_of_utc or iso();run_id=stable_id('P10RUN',{'t':decision_time,'h':horizon,'a':authority_mode,'m':acquisition_mode,'fixture':bool(fixture_mode)})
    root=pathlib.Path(artifact_root_override) if artifact_root_override else paths['p10']/'artifacts';am=ArtifactManager(root);stages=[];warnings=[];started=time.perf_counter();rd=None
    def stage(sid,status='PASS',t0=None,detail=None,artifacts=None,error=None):
        rec={'stage_id':sid,'run_id':run_id,'decision_time':decision_time,'status':status,'duration_ms':round((time.perf_counter()-t0)*1000,3) if t0 else 0,'detail':detail or {},'artifacts':artifacts or [],'error':error};stages.append(rec)
        if rd: atomic_json(rd/f'stage_{len(stages):02d}_{sid.lower()}.json',rec)
        return rec
    try:
        am.acquire(run_id);rd=am.run_dir(run_id)
        attempt={'record_type':'AD_V3_P10_RUN_POINTER','run_id':run_id,'status':'RUNNING','decision_time':decision_time,'authority_mode':authority_mode,'run_dir':str(rd)}
        if update_latest and not fixture_mode:am.publish_attempt(attempt)
        _progress('');_progress('============================================================',quiet);_progress(' ALPHA DESK V3 - UNIFIED GOLD RUNTIME',quiet);_progress('============================================================',quiet);_progress('Run ID: '+run_id,quiet)
        p04=paths['p04'];promotion=load_promotion(p04)
        # PRECHECK
        t=time.perf_counter();
        if str(authority_mode).upper() not in {'SHADOW','PRODUCTION','REPLAY','FIXTURE'}:raise RuntimeError('INVALID_AUTHORITY_MODE')
        p09s=p09_status(paths['p09'],state_root=p09_state_root_override)
        if p09s.get('cohort_change_required'):raise RuntimeError('P09_COHORT_CHANGE_REQUIRED')
        if fail_stage=='PRECHECK':raise RuntimeError('FORCED_STAGE_FAILURE:PRECHECK')
        stage('PRECHECK',t0=t,detail={'promotion_state':promotion.get('state'),'p09_forward_state':(p09s.get('statistics') or {}).get('forward_evidence_state'),'fixture_mode':fixture_mode})
        # P09 mature evaluation BEFORE current analysis. Uses already journaled fixed-maturity observations only.
        _progress('[1/10] Forward maturity',quiet);t=time.perf_counter();p09_eval=p09_observe_and_evaluate(paths['p09'],None,now=decision_time,state_root=p09_state_root_override);stage('FORWARD_EVALUATION',t0=t,detail={'new_outcomes':len(p09_eval.get('new_outcomes') or []),'forward_state':p09_eval.get('statistics',{}).get('forward_evidence_state')})
        # Plan first.
        _progress('[2/10] Gold data plan',quiet);t=time.perf_counter();plan=build_plan(horizon,acquisition_mode,decision_time);atomic_json(rd/'p07_acquisition_plan.json',plan);stage('ACQUISITION_PLAN',t0=t,detail={'plan_id':plan.get('plan_id'),'fact_universe_count':plan.get('fact_universe_count')},artifacts=['p07_acquisition_plan.json'])
        # Acquisition remains P07/P02 authority.
        _progress('[3/10] Gold data acquisition',quiet);t=time.perf_counter();data=pathlib.Path(p02_data_root_override) if p02_data_root_override else paths['p02']/'artifacts/live_store';kout=pathlib.Path(kernel_output_root_override) if kernel_output_root_override else paths['p07']/'artifacts';kernel=run_kernel(repo,horizon,acquisition_mode,decision_time,data,kout,kernel_fixture_dir);atomic_json(rd/'p07_kernel_receipt.json',kernel);cov=load(kernel['governed_coverage_path']);atomic_json(rd/'p07_governed_coverage.json',cov);adm=kernel.get('analysis_admission') or cov.get('analysis_admission');stage('ACQUISITION',status='DEGRADED' if adm in {'DEGRADED','DEGRADED_ALLOW'} else ('BLOCKED' if adm in {'BLOCK','BLOCKED'} else 'PASS'),t0=t,detail={'admission':adm,'kernel_health':kernel.get('kernel_health'),'performance':kernel.get('performance')},artifacts=['p07_kernel_receipt.json','p07_governed_coverage.json'])
        current_anchor=_price_anchor(data,kernel.get('p02_acquisition_run_id'));_record_price_only(current_anchor,p09_state_root_override)
        if fail_stage=='ACQUISITION':raise RuntimeError('FORCED_STAGE_FAILURE:ACQUISITION')
        if adm in {'BLOCK','BLOCKED'} or not cov.get('analysis_may_start',True):
            eidx=_evidence_index(data,kernel.get('p02_acquisition_run_id'));run_meta={'run_id':run_id,'subject':'Gold','decision_time':decision_time,'horizon':horizon,'authority_mode':authority_mode,'runtime_version':VERSION};blocked_decision={'record_type':'AD_V3_P08_BLOCKED_PRESENTATION_STATE','causal_direction':'UNKNOWN','raw_p03_causal_direction':'UNKNOWN','pressure_strength':'UNKNOWN','dominance_state':'UNKNOWN','dominant_root':None,'supporting_roots':[],'opposing_roots':[],'breadth':'NONE','fragility':'HIGH','fragility_reasons':['ANALYSIS_BLOCKED'],'contradiction':'UNKNOWN','consumption':'UNKNOWN','missing_driver_risk':'UNKNOWN','edge_state':'NO_EDGE','permission_candidate':'NO_AUTHORITY','blockers':['ANALYSIS_BLOCKED'],'calibrated_roots':[],'invalidation_conditions':[]}
            cri=build_cr_input(run_meta,kernel,{}, {'item_count':0,'items':[]},{'bundle':{'adjudication_mode':'CONSERVATIVE_EVIDENCE_ONLY','items':[]},'validation_receipt':{'status':'NOT_RUN_BLOCKED','validated_count':0,'unknown_count':0,'rejected_count':0,'fallback_count':0}}, {},blocked_decision,p09_eval,{'prediction':None,'statistics':p09_eval.get('statistics'),'cohort':p09s.get('active_cohort') or {}},promotion,['ANALYSIS_BLOCKED'],{},eidx,stages);atomic_json(rd/'control_room_input.json',cri)
            t=time.perf_counter();report=render_p11_report(cri,rd,None,fixture=fixture_mode);atomic_json(rd/'control_room.json',report['view_model']);stage('CONTROL_MODEL',status='BLOCKED',t0=t,detail={'phase':'AD-V3-P11','analysis_blocked':True},artifacts=['control_room_input.json','control_room_view_model.json','control_room.json']);stage('REPORT',status='PASS',t0=time.perf_counter(),detail={'phase':'AD-V3-P11','html':str(rd/'control_room.html')},artifacts=['control_room.html','p11_report_receipt.json','brief.txt'])
            result={'record_type':'AD_V3_P10_RUN_RESULT','schema_version':'1.0.0','run_id':run_id,'subject':'Gold','runtime_version':VERSION,'authority_mode':authority_mode,'decision_time':decision_time,'horizon':horizon,'overall_status':'BLOCKED','analysis_admission':'BLOCK','stage_receipts':stages,'data_state':kernel,'semantic_state':None,'causal_state':None,'decision_state':{'permission':{'research_action_candidate':'WAIT','official_permission':'NO_AUTHORITY'}},'forward_state':p09_eval.get('statistics'),'report_state':'P11_DIAGNOSTIC','promotion_state':promotion.get('state'),'trade_execution_authority':'NONE','versions':_versions(paths),'warnings':['ANALYSIS_BLOCKED']}
            atomic_json(rd/'run_result.json',result);caps={'record_type':'AD_V3_P10_RUN_CAPSULE','run_id':run_id,'status':'BLOCKED','result_sha256':sha_file(rd/'run_result.json'),'control_room_input_sha256':sha_file(rd/'control_room_input.json'),'p11_view_model_sha256':sha_file(rd/'control_room_view_model.json'),'p11_report_receipt_sha256':sha_file(rd/'p11_report_receipt.json'),'control_room_html_sha256':sha_file(rd/'control_room.html')};stage('SEAL',t0=time.perf_counter(),detail={'seal_pending':True},artifacts=['run_capsule.json','run_seal.json']);result['stage_receipts']=stages;atomic_json(rd/'run_result.json',result);caps['result_sha256']=sha_file(rd/'run_result.json');atomic_json(rd/'run_capsule.json',caps);seal=build_seal(rd)
            if update_latest and not fixture_mode:am.publish_attempt({**attempt,'status':'BLOCKED','completed_at':iso(),'run_result':str(rd/'run_result.json'),'html':str(rd/'control_room.html')})
            return result
        # P03 pre-semantic direct API.
        _progress('[4/10] Causal brain',quiet);t=time.perf_counter();covpath=rd/'p07_governed_coverage.json';pre=p03_execute(paths['p03'],data,covpath,None,horizon);atomic_json(rd/'p03_pre_semantic.json',pre);hist=observation_history(data,None);pairs,_=current_previous_for_receipt(hist,cov);reg=load(paths['p03']/'config/fact_reasoning_registry.json');cmap={x['fact_id']:x for x in reg['contracts']};packet=build_semantic_evidence_packet(pre,pairs,cmap,cov);atomic_json(rd/'semantic_evidence_packet.json',packet);stage('PRE_SEMANTIC',t0=t,detail={'handoff':pre.get('handoff_integrity'),'semantic_requests':packet.get('item_count',len(packet.get('items') or []))},artifacts=['p03_pre_semantic.json','semantic_evidence_packet.json'])
        # Semantic.
        _progress('[5/10] Semantic adjudication',quiet);t=time.perf_counter();sem=run_semantics(repo,packet,external_bundle_path=semantic_bundle_path,artifact_dir=rd);bundle=sem['bundle'];semrec=sem['validation_receipt'];atomic_json(rd/'semantic_adjudication_bundle.json',bundle);stage('SEMANTIC',status='DEGRADED' if semrec.get('fallback_count',0) else 'PASS',t0=t,detail={'mode':bundle.get('adjudication_mode'),'validation':semrec},artifacts=['semantic_adjudication_bundle.json'])
        # Final causal.
        _progress('[6/10] Final causal reconciliation',quiet);t=time.perf_counter();bundle_path=rd/'semantic_adjudication_bundle.json';final=p03_execute(paths['p03'],data,covpath,bundle_path,horizon);atomic_json(rd/'p03_final.json',final);stage('FINAL_CAUSAL',t0=t,detail={'direction':(final.get('shadow_decision') or {}).get('direction_candidate')},artifacts=['p03_final.json'])
        # P08.
        _progress('[7/10] Decision calibration',quiet);t=time.perf_counter();last=am.read_pointer('last_success.json') if update_latest and not fixture_mode else None;prev=None
        if last and last.get('run_dir') and (pathlib.Path(last['run_dir'])/'p08_decision_calibration.json').exists():prev=load(pathlib.Path(last['run_dir'])/'p08_decision_calibration.json')
        er=paths['p08']/'artifacts/state/empirical_calibration_registry.json';cal=calibrate_decision(final,kernel=kernel,previous=prev,promotion_state=promotion,empirical_registry_path=er if er.exists() else None);atomic_json(rd/'p08_decision_calibration.json',cal);stage('DECISION_CALIBRATION',t0=t,detail={'direction':cal.get('causal_direction'),'strength':cal.get('pressure_strength'),'dominance':cal.get('dominance_state'),'edge':cal.get('edge_state'),'permission':cal.get('permission_candidate')},artifacts=['p08_decision_calibration.json'])
        # R03 perspective-only monotonic authority defense.
        _progress('[8/11] Antifragile perspective',quiet);t=time.perf_counter();event_context=(final.get('event_context') or kernel.get('event_context') or {'events':[]}) if isinstance(final,dict) and isinstance(kernel,dict) else {'events':[]}
        try:
            perspective=run_r03_perspective(cal,final,kernel,bundle,event_context,decision_time)
        except Exception as r03e:
            perspective=r03_fail_closed(cal,'R03_RUNTIME_FAILURE:'+type(r03e).__name__);warnings.append('R03_FAIL_CLOSED')
        atomic_json(rd/'r03_perspective_state.json',perspective);stage('PERSPECTIVE_OVERLAY',status='DEGRADED' if ((perspective.get('audit') or {}).get('fail_closed')) else 'PASS',t0=t,detail={'scenario_count':((perspective.get('scenario_packet') or {}).get('scenario_count')),'thesis_resilience':perspective.get('thesis_resilience'),'unknown_envelope':((perspective.get('unknown_state') or {}).get('unknown_envelope')),'overlay':((perspective.get('perspective_overlay') or {}).get('overlay')),'final_permission':perspective.get('final_permission')},artifacts=['r03_perspective_state.json'])
        # P09 precommit persists the effective post-R03 permission while retaining upstream P08 state.
        _progress('[9/11] Forward precommit',quiet);t=time.perf_counter();p09c=p09_precommit_current(paths['p09'],run_id,cal,final,kernel,bundle,current_anchor,now=decision_time,state_root=p09_state_root_override,event_context=event_context,perspective=perspective);pred=p09c['prediction'];atomic_json(rd/'p09_forward_precommit.json',pred);atomic_json(rd/'p09_forward_statistics.json',p09c['statistics']);stage('FORWARD_PRECOMMIT',t0=t,detail={'prediction_id':pred.get('prediction_id'),'episode_id':pred.get('episode_id'),'forward_state':p09c['statistics'].get('forward_evidence_state'),'r03_overlay':((perspective.get('perspective_overlay') or {}).get('overlay'))},artifacts=['p09_forward_precommit.json','p09_forward_statistics.json'])
        # Stable ControlRoomInputV3 -> canonical P11 presentation.
        _progress('[10/11] Control Room',quiet);t=time.perf_counter();run_meta={'run_id':run_id,'subject':'Gold','decision_time':decision_time,'horizon':horizon,'authority_mode':authority_mode,'runtime_version':VERSION};lineage={'p07_plan_sha256':sha_file(rd/'p07_acquisition_plan.json'),'p07_kernel_sha256':sha_file(rd/'p07_kernel_receipt.json'),'p03_final_sha256':sha_file(rd/'p03_final.json'),'p08_sha256':sha_file(rd/'p08_decision_calibration.json'),'r03_perspective_sha256':sha_file(rd/'r03_perspective_state.json'),'p09_precommit_sha256':sha_file(rd/'p09_forward_precommit.json')};eidx=_evidence_index(data,kernel.get('p02_acquisition_run_id'));prev_input=None
        last=am.read_pointer('last_success.json') if update_latest and not fixture_mode else None
        if last and last.get('run_dir') and (pathlib.Path(last['run_dir'])/'control_room_input.json').exists():prev_input=load(pathlib.Path(last['run_dir'])/'control_room_input.json')
        qualification=r01_qualify(p09_state_root_override,r01_state_root_override);cri=build_cr_input(run_meta,kernel,pre,packet,sem,final,cal,p09_eval,p09c,promotion,warnings,lineage,eidx,stages,qualification,perspective);atomic_json(rd/'control_room_input.json',cri);report=render_p11_report(cri,rd,previous_input=prev_input,fixture=fixture_mode);atomic_json(rd/'control_room.json',report['view_model']);stage('CONTROL_MODEL',t0=t,detail={'phase':'AD-V3-P11','executive':report['view_model'].get('executive')},artifacts=['control_room_input.json','control_room_view_model.json','control_room.json'])
        stage('REPORT',t0=time.perf_counter(),detail={'phase':'AD-V3-P11','html':str(rd/'control_room.html'),'report_version':report['receipt'].get('version')},artifacts=['control_room.html','p11_report_receipt.json','brief.txt'])
        # P04 capsule retained as underlying artifact; P10 capsule is canonical index.
        build_p04_capsule(run_id,rd,pred,promotion.get('state')=='PRODUCTION_V3')
        effective_for_classification=dict(cal);effective_for_classification['permission_candidate']=perspective.get('final_permission',cal.get('permission_candidate'));effective_for_classification['edge_state']=perspective.get('final_edge',cal.get('edge_state'));overall=_classify(adm,effective_for_classification);result={'record_type':'AD_V3_P10_RUN_RESULT','schema_version':'1.0.0','run_id':run_id,'subject':'Gold','runtime_version':VERSION,'authority_mode':authority_mode,'decision_time':decision_time,'horizon':horizon,'overall_status':overall,'analysis_admission':adm,'data_state':{'kernel_health':kernel.get('kernel_health'),'performance':kernel.get('performance'),'run_id':kernel.get('run_id')},'semantic_state':{'mode':bundle.get('adjudication_mode'),'validation_status':semrec.get('status'),'unknown_count':semrec.get('unknown_count'),'fallback_count':semrec.get('fallback_count')},'causal_state':{'raw_direction':(final.get('shadow_decision') or {}).get('direction_candidate')},'decision_state':cal,'perspective_state':perspective,'effective_permission':perspective.get('final_permission'),'effective_edge':perspective.get('final_edge'),'forward_state':p09c['statistics'],'report_state':'P11_GENERATED','promotion_state':promotion.get('state'),'trade_execution_authority':'NONE','stage_receipts':stages,'artifact_lineage':lineage,'versions':_versions(paths),'warnings':warnings,'total_runtime_ms':round((time.perf_counter()-started)*1000,3)};atomic_json(rd/'run_result.json',result);caps={'record_type':'AD_V3_P10_RUN_CAPSULE','run_id':run_id,'result_sha256':sha_file(rd/'run_result.json'),'control_room_input_sha256':sha_file(rd/'control_room_input.json'),'p11_view_model_sha256':sha_file(rd/'control_room_view_model.json'),'p11_report_receipt_sha256':sha_file(rd/'p11_report_receipt.json'),'control_room_html_sha256':sha_file(rd/'control_room.html'),'phase_artifacts':lineage};stage('SEAL',t0=time.perf_counter(),detail={'seal_pending':True},artifacts=['run_capsule.json','run_seal.json']);result['stage_receipts']=stages;atomic_json(rd/'run_result.json',result);caps['result_sha256']=sha_file(rd/'run_result.json');atomic_json(rd/'run_capsule.json',caps);seal=build_seal(rd)
        completed={'record_type':'AD_V3_P10_RUN_POINTER','run_id':run_id,'status':overall,'decision_time':decision_time,'completed_at':iso(),'authority_mode':authority_mode,'run_dir':str(rd),'run_result':str(rd/'run_result.json'),'html':str(rd/'control_room.html')}
        if update_latest and not fixture_mode:am.publish_attempt(completed);am.publish_success(completed,rd)
        _progress('[11/11] Seal',quiet);_progress('============================================================',quiet);_progress(' GOLD UNIFIED RUNTIME - '+overall,quiet);_progress('============================================================',quiet);_progress('Direction : '+str(cal.get('causal_direction')),quiet);_progress('Action    : '+str(perspective.get('final_permission') or (cal.get('permission') or {}).get('research_action_candidate')),quiet);_progress('HTML      : '+str(rd/'control_room.html'),quiet)
        return result
    except Exception as e:
        err={'record_type':'AD_V3_P10_FAILED_RUN','run_id':run_id,'status':'FAILED_RUNTIME','decision_time':decision_time,'error_type':type(e).__name__,'error':str(e),'stage_receipts':stages,'traceback':traceback.format_exc()}
        if rd:
            atomic_json(rd/'failure_receipt.json',err)
        if update_latest and not fixture_mode:am.publish_attempt({'record_type':'AD_V3_P10_RUN_POINTER','run_id':run_id,'status':'FAILED_RUNTIME','decision_time':decision_time,'completed_at':iso(),'run_dir':str(rd) if rd else None,'failure_receipt':str(rd/'failure_receipt.json') if rd else None})
        raise
    finally:
        am.release()
