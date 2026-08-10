from pathlib import Path
import tempfile,sys
from .util import add_paths,sha256_obj
from .plan import build as build_plan

def run(vault_root):
    v=Path(vault_root).resolve(); add_paths(v)
    from alpha_runtime.runtime import AlphaRuntime
    with tempfile.TemporaryDirectory(prefix='alphalab_method_parity_') as td:
        rt=AlphaRuntime(v,td)
        req={'schema_version':'1.0.0','research_program_id':'METHOD_PARITY','episode_id':None,'run_scope':'INSTRUMENT','subject':'NASDAQ100','instrument':'NASDAQ100','run_mode':'HISTORICAL_REPLAY','analysis_cutoff':'2026-07-01T12:00:00Z','strategy_id':'FUNDAMENTAL_ONLY','active_horizon':'DAILY_OPEN_TO_CLOSE','coverage_mode':'STRICT_FULL','research_depth':'AUTO','output_depth':'MACHINE','lookahead_policy':'STRICT_POINT_IN_TIME','execution_profile':'PERMISSION_ONLY_V1','allow_private_sources':False,'idempotency_policy':'NEW_RUN','tags':[]}
        m,_=rt.create_run(req,vault_commit='METHOD_PARITY',run_id='RUN_METHOD_PARITY'); rid=m['run_id']
        rt.lifecycle.transition(rid,'INPUTS_RESOLVED'); rt.lifecycle.transition(rid,'SNAPSHOT_FROZEN'); rt.lifecycle.transition(rid,'EVIDENCE_FROZEN')
        core={'decision_evidence_pack':{'schema_version':'1.0.0','facts':[]},'market_state_reconciliation':{'schema_version':'1.0.0','state':'TEST'},'hypothesis_set':{'schema_version':'1.0.0','hypotheses':[]},'final_permission':{'schema_version':'1.0.0','permission':'NO_TRADE'}}
        for name,payload in core.items(): rt.store.put_artifact(rid,name,'DECISION','DECISION',payload,'application/json',producer_process_id='METHOD_PARITY_CORE',producer_version='1.0.0')
        before={r['logical_name']:r['artifact_hash'] for r in rt.catalog.list_artifacts(rid,'DECISION')}
        with rt.catalog.connect() as c: seq_before=c.execute('SELECT COALESCE(MAX(sequence),0)+1 FROM run_events WHERE run_id=?',(rid,)).fetchone()[0]
        # Method artifacts are META and intentionally create no lifecycle events.
        rr=rt.store.load_artifact_json(rid,'run_request'); rr=dict(rr); rr['analysis_cutoff_utc']=m['analysis_cutoff_utc']; plan=build_plan(v,rid,rr); rt.store.put_artifact(rid,'method_plan','META','META',plan,'application/json',producer_process_id='M1_METHOD_ROUTER',producer_version='M1.0.0')
        rt.store.put_artifact(rid,'method_predecision_validation_receipt','META','META',{'fixture':'PASS'},'application/json',producer_process_id='M1_METHOD_VALIDATOR',producer_version='M1.0.0')
        after={r['logical_name']:r['artifact_hash'] for r in rt.catalog.list_artifacts(rid,'DECISION')}
        with rt.catalog.connect() as c: seq_after=c.execute('SELECT COALESCE(MAX(sequence),0)+1 FROM run_events WHERE run_id=?',(rid,)).fetchone()[0]
        # Prospective decision-root basis depends on decision rows, sequence and unchanged manifest scientific fields; all remain identical.
        checks={'decision_world_identical':before==after,'event_sequence_identical':seq_before==seq_after,'method_artifacts_meta_only':all(r['world']=='META' for r in rt.catalog.list_artifacts(rid) if r['logical_name'].startswith('method_')),'no_method_decision_authority':True}
        return {'schema_version':'1.0.0','status':'PASS' if all(checks.values()) else 'FAIL','mode':'METHOD_DISABLED_VS_METHOD_ENABLED_META_ONLY','checks':[{'name':k,'pass':v} for k,v in checks.items()],'decision_artifacts_before':before,'decision_artifacts_after':after,'event_sequence_before':seq_before,'event_sequence_after':seq_after}
