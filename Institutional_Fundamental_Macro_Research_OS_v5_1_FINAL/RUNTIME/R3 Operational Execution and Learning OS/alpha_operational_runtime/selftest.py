from pathlib import Path
import tempfile,json,sys
from .launcher import Launcher,LaunchError
from .catalog_ext import init_r3
from .warehouse import Warehouse
from .ledger import D4Ledger
from .host import make_host,HostError
from .forward import ForwardObservationRecorder
from .calibration import Calibrator
from .retrieval import RetrievalRuntime
from .meta import MetaReconciler

def run(vault_root):
    v=Path(vault_root);checks=[];errors=[];rm=json.loads((v/'RUNTIME'/'RUNTIME_MANIFEST.json').read_text(encoding='utf-8'));checks += [('runtime_r3_active',rm.get('runtime_version')=='R3.0.0'),('scientific_stack_v213',rm.get('scientific_stack')=='V21.3.0'),('operational_gate_block_only',rm.get('operational_execution',{}).get('authority')=='BLOCK_ONLY')]
    for p in (str(v/'RUNTIME'/'R1 Foundation'),str(v/'RUNTIME'/'R2 Prompt Execution OS')):
        if p not in sys.path:sys.path.insert(0,p)
    from alpha_runtime.runtime import AlphaRuntime
    with tempfile.TemporaryDirectory(prefix='alphalab_r3_') as td:
        rt=AlphaRuntime(v,td);init_r3(rt.catalog);L=Launcher(v,rt);a=L.compile_request('NAS100','LIVE');b=L.compile_request('NASDAQ100','HISTORICAL_REPLAY','2026-07-01T12:00:00Z');checks += [('alias_resolution',a['subject']=='NASDAQ100'),('live_cutoff_now',a['analysis_cutoff']=='NOW'),('historical_explicit_cutoff',b['analysis_cutoff']=='2026-07-01T12:00:00Z'),('same_run_contract_shape',set(a)==set(b))]
        ep,daily=L.daily_six_requests('HISTORICAL_REPLAY','2026-07-01T12:00:00Z');checks += [('daily_six_count',len(daily)==6),('daily_six_common_historical_cutoff',len({x['analysis_cutoff'] for x in daily})==1)];bulk=L.bulk_requests('NAS100',['2026-07-01T12:00:00Z','2026-07-02T12:00:00Z']);checks.append(('bulk_plan_count',bulk['count']==2))
        try:L.compile_request('UNKNOWN','LIVE');ok=False
        except LaunchError:ok=True
        checks.append(('unknown_alias_fail_closed',ok));hp=json.loads((v/'RUNTIME'/'R3 Operational Execution and Learning OS'/'config'/'host_policy.json').read_text(encoding='utf-8'))
        try:make_host(hp['bindings']['FIXTURE_TEST'],td,fixture=lambda x:{},production=True);ok=False
        except HostError:ok=True
        checks.append(('fixture_forbidden_production',ok))
        rr=RetrievalRuntime(v,rt);captured_requests=[]
        def fake_retrieve(req):
            captured_requests.append(req);return []
        intake=rr.prefetch_live('NASDAQ100','DAILY_OPEN_TO_CLOSE',fake_retrieve,False)
        checks += [('live_preintake_has_no_fake_future_cutoff',all(x.get('analysis_cutoff_utc') is None and x.get('capture_mode')=='LIVE_PRE_RUN' for x in captured_requests)),('live_intake_cutoff_semantics',intake.get('cutoff_semantics')=='INTAKE_COMPLETION_UTC' and intake.get('atomic_snapshot_claim') is False)]
        m,_=rt.create_run(a,vault_commit='SELFTEST_COMMIT',run_id='RUN_R3_SELFTEST');rid=m['run_id'];rt.lifecycle.transition(rid,'INPUTS_RESOLVED');rt.lifecycle.transition(rid,'SNAPSHOT_FROZEN');rt.lifecycle.transition(rid,'EVIDENCE_FROZEN')
        rt.store.put_artifact(rid,'final_permission','DECISION','DECISION',{'schema_version':'1.0.0','instrument':'NASDAQ100','active_horizon':'DAILY_OPEN_TO_CLOSE','direction_authority':'FUNDAMENTAL_ONLY','permission':'NO_TRADE','validity':{},'review_trigger':{},'invalidation_triggers':[],'outside_strategy_edges_permission_effect':'NONE','operational_execution_gate':'R3_PENDING'},'application/json');rt.store.put_artifact(rid,'research_intent','DECISION','DECISION',{'fundamental_direction':'BULLISH','edge_state':'NO_EDGE','active_horizon':'DAILY_OPEN_TO_CLOSE'},'application/json');rt.store.put_artifact(rid,'cognitive_adjudication','DECISION','DECISION',{'fundamental_direction':'BULLISH'},'application/json');rt.store.put_artifact(rid,'d3_adjudication','DECISION','DECISION',{'pre_d3_permission':'NO_TRADE','final_permission':'NO_TRADE','d3_edge_quality':'CONSTRAINED','deduplicated_root_ids':['ROOT_A']},'application/json');rt.store.put_artifact(rid,'d4_authority_receipt','DECISION','DECISION',{'registry_version':'1.0.0','v19_d3_permission':'NO_TRADE','final_v20_permission':'NO_TRADE','applied_promotion_ids':[],'shadow_candidate_ids':[]},'application/json');rt.store.put_artifact(rid,'global_reconciliation','DECISION','DECISION',{'schema_version':'1.0.0','state':'CONSISTENT'},'application/json');rt.lifecycle.transition(rid,'COGNITION_FROZEN')
        from alpha_runtime.seal_safe import create_decision_seal
        create_decision_seal(rid,rt);checks.append(('decision_seal_required_worlds',bool(rt.store.load_manifest(rid).get('decision_seal_hash'))));fo=ForwardObservationRecorder(v,rt).build(rid);checks += [('forward_observation_created',fo['record_type']=='FORWARD_OBSERVATION'),('forward_observation_pinned',fo['vault_commit']=='SELFTEST_COMMIT')];from .util import validate_scientific_schema;checks.append(('d4_forward_schema_valid',bool(validate_scientific_schema(v,'102 Forward Validation Calibration Promotion and Scientific Governance Engine/schemas/AlphaLab_D4_Forward_Observation.schema.json',fo))))
        wh=Warehouse(v,rt);row=wh.upsert_run(rid);checks += [('warehouse_sqlite_row',row['run_id']==rid),('warehouse_accelerator_non_authoritative',wh.accelerator_status()['precision_loss_if_unavailable'] is False)]
        led=D4Ledger(rt);x=led.append('OUTCOME',{'run_id':rid,'state':'TEST'},rid);ok,n=led.verify();checks.append(('ledger_hash_chain_and_payload',ok and n==2));# forward + test outcome
        # Tamper JSONL projection; strong verify must reject it, then rebuild.
        with open(led.path,'a',encoding='utf-8') as f:f.write('{}\n')
        ok2,_=led.verify();checks.append(('ledger_jsonl_tamper_detected',not ok2));led.rebuild_jsonl();checks.append(('ledger_rebuild_verifies',led.verify()[0]));meta=MetaReconciler(rt).reconcile([rid,rid]);checks += [('meta_cutoff_disclosed',meta['temporal_alignment']=='EXACT' and len(meta['component_cutoffs_utc'])==1),('meta_has_no_permission_authority',meta['permission_effect']=='NONE_DIRECT')];rt.catalog.checkpoint()
    lp=json.loads((v/'RUNTIME'/'R3 Operational Execution and Learning OS'/'config'/'launcher_profiles.json').read_text(encoding='utf-8'));checks.append(('six_production_instruments',len(lp['production_instruments'])==6));rp=json.loads((v/'RUNTIME'/'R3 Operational Execution and Learning OS'/'config'/'retrieval_runtime_policy.json').read_text(encoding='utf-8'));checks += [('historical_current_only_forbidden',rp['historical_current_only']=='FORBIDDEN'),('live_postcutoff_retrieval_forbidden',rp['live_on_demand_after_cutoff']=='FORBIDDEN')]
    errors += [n for n,ok in checks if not ok];return {'status':'PASS' if not errors else 'FAIL','passed':sum(1 for _,x in checks if x),'total':len(checks),'checks':[{'name':n,'pass':ok} for n,ok in checks],'errors':errors}
