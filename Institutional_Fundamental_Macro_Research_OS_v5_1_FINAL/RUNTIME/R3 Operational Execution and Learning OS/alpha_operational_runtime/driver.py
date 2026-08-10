from pathlib import Path
from .util import load_json
from .materialize import InvocationMaterializer
from .host import make_host,HostError
from .retrieval import RetrievalRuntime
class DriverError(RuntimeError):pass
GATE_AFTER={'P11_EVIDENCE_PLAN':'G1_SCOPE_EVIDENCE_PLAN','W23_LINEAGE_VALIDATOR':'G2_EVIDENCE_ADMISSION','P53_GLOBAL_RECONCILIATION':'G3_COGNITIVE_INTEGRITY'}
class RunDriver:
    def __init__(self,vault,rt,r2,host_binding='PRODUCTION_COMMAND',fixture=None,live_intake=None):
        self.vault=Path(vault);self.rt=rt;self.r2=r2;self.r3=self.vault/'RUNTIME'/'R3 Operational Execution and Learning OS';self.hp=load_json(self.r3/'config'/'host_policy.json');self.ep=load_json(self.vault/'RUNTIME'/'R2 Prompt Execution OS'/'config'/'execution_policy.json');self.binding_name=host_binding;self.binding=self.hp['bindings'][host_binding];self.materializer=InvocationMaterializer(vault,rt,r2);self.retrieval=RetrievalRuntime(vault,rt);self.fixture=fixture;self.live_intake=live_intake
    def host(self,production=True):return make_host(self.binding,self.rt.data_root,self.fixture,production=production)
    def _record_receipt(self,run_id,pid,job,receipt,status):
        try:ref=self.rt.store.put_artifact(run_id,'r3_host_receipt_'+pid.lower()+'_'+str(receipt['attempt']),'DECISION','EVIDENCE',receipt,'application/json',producer_process_id='R3_HOST',producer_version='R3.0.0')
        except Exception:ref=None
        with self.rt.catalog.connect() as c:c.execute("INSERT OR REPLACE INTO r3_model_invocations(invocation_id,run_id,process_id,job_hash,adapter,provider,model,model_version,request_hash,response_hash,status,attempt,started_at_utc,completed_at_utc,latency_ms,receipt_artifact_hash) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(receipt['invocation_id'],run_id,pid,job['job_hash'],receipt['adapter'],receipt.get('provider'),receipt.get('model'),receipt.get('model_version'),receipt['request_hash'],receipt.get('response_hash'),status,receipt['attempt'],receipt['started_at_utc'],receipt.get('completed_at_utc'),receipt.get('latency_ms'),ref['artifact_hash'] if ref else None))
    def _retryable(self,e):
        if isinstance(e,HostError):return e.category in ('TRANSIENT_ERROR','SCHEMA_REPAIRABLE','FORMAT_INVALID')
        s=str(e).lower();return any(x in s for x in ('schema validation failed','missing expected output','invalid output status','host missing process_output')) and not any(x in s for x in ('authority','lookahead','identity mismatch','forbidden future'))
    def _execute_job(self,job,production=True):
        maxa=int(self.ep['retry_policy']['max_attempts_per_node']);last=None
        for attempt in range(1,maxa+1):
            self.r2.start(job['run_id'],job['process_id'],job['job_hash'])
            try:
                out,rec=self.host(production).invoke(self.materializer.build(job,self.binding.get('payload_mode','FILE_REFERENCES')),attempt);self._record_receipt(job['run_id'],job['process_id'],job,rec,out.get('status','OK'))
                if out.get('status')!='OK':raise HostError(out.get('error') or 'host status '+str(out.get('status')),out.get('error_category','PERMANENT_ERROR'))
                env=out.get('process_output')
                if not isinstance(env,dict):raise HostError('host missing process_output','SCHEMA_REPAIRABLE')
                return self.r2.complete(job['run_id'],job['process_id'],env)
            except Exception as e:
                last=e;retry=attempt<maxa and self._retryable(e);state='FAILED_RETRYABLE' if retry else 'FAILED'
                with self.rt.catalog.connect() as c:c.execute("UPDATE r2_process_state SET status=?,output_status='FAILED',output_reason=? WHERE run_id=? AND process_id=?",(state,str(e),job['run_id'],job['process_id']))
                self.rt.lifecycle.event(job['run_id'],'R3_HOST_FAILURE',{'process_id':job['process_id'],'attempt':attempt,'retryable':retry,'error':str(e)})
                if not retry:raise DriverError(f"{job['process_id']} failed at attempt {attempt}: {e}") from e
        raise DriverError(str(last))
    def _ensure_retrieval(self,run_id,production=True):
        names={r['logical_name'] for r in self.rt.catalog.list_artifacts(run_id)}
        if 'r3_retrieval_receipt' in names:return
        h=self.host(production);retriever=h.retrieve if 'EVIDENCE_RETRIEVAL' in self.binding.get('optional_capabilities',[])+self.binding.get('required_capabilities',[]) else None
        self.retrieval.capture(run_id,host_retriever=retriever,live_intake=self.live_intake)
    def run_to_decision(self,run_id,production=True):
        st=self.r2.status(run_id)
        if not st['run']:self.r2.bootstrap(run_id)
        while True:
            m=self.rt.store.load_manifest(run_id)
            if m.get('decision_seal_hash'):return m
            jobs=self.r2.ready_jobs(run_id)
            if not jobs:raise DriverError('no ready jobs before decision seal; inspect R2 status/gates')
            # Deterministic serial scheduling is the accuracy-first baseline. The DAG remains parallelizable.
            for job in jobs:
                pid=job['process_id']
                if pid=='W21_SNAPSHOT_AUDIT':self._ensure_retrieval(run_id,production)
                self._execute_job(job,production)
                if pid in GATE_AFTER:
                    rec=self.r2.gate(run_id,GATE_AFTER[pid],store_receipt=True)
                    if rec['status']!='PASS':raise DriverError(GATE_AFTER[pid]+' failed: '+repr(rec.get('missing_artifacts')))
                if pid=='P63_FINAL_DECISION':
                    g=self.r2.gate(run_id,'G4_DECISION_COMPLETION',store_receipt=False)
                    if g['status']!='PASS':raise DriverError('G4 failed: '+repr(g.get('missing_artifacts')))
                    return self.r2.finalize_decision(run_id)
