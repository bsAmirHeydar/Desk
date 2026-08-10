from pathlib import Path
import json
from datetime import datetime, timezone
from .registry import PromptRegistry
from .graph import ProcessGraph
from .catalog_ext import init_r2
from .context import ContextCompiler
from .jobs import make_job
from .validation import validate_json_schema
from .gates import GateEngine

R2_VERSION='R2.0.0'; PACK='ALPHALAB_PROMPT_PACK_1.1.0'; GRAPH='R2_PROCESS_GRAPH_1.0.0'; MODELS='R2_MODEL_PROFILES_1.0.0'
def now(): return datetime.now(timezone.utc).isoformat().replace('+00:00','Z')

class OrchestratorError(RuntimeError): pass

class R2Orchestrator:
    def __init__(self,rt):
        self.rt=rt; self.vault=rt.vault; self.registry=PromptRegistry(self.vault); self.graph=ProcessGraph(self.registry.graph); init_r2(rt.catalog); self.ctx=ContextCompiler(self.vault,rt,self.registry); self.gates=GateEngine(rt,self.registry)
        errs=self.registry.validate()+self.graph.validate()
        if errs: raise OrchestratorError('R2 registry/graph invalid: '+'; '.join(errs))
    def bootstrap(self,run_id,coverage_mode='STRICT_FULL',research_depth='AUTO'):
        m=self.rt.store.load_manifest(run_id)
        if m.get('decision_seal_hash'): raise OrchestratorError('cannot bootstrap R2 after decision seal')
        n=now()
        with self.rt.catalog.connect() as c:
            c.execute("INSERT OR REPLACE INTO r2_process_runs(run_id,prompt_pack_version,process_graph_version,model_profile_set,coverage_mode,research_depth,status,created_at_utc,updated_at_utc) VALUES(?,?,?,?,?,?,?,?,?)",(run_id,PACK,GRAPH,MODELS,coverage_mode,research_depth,'ACTIVE',n,n))
            for pid in self.registry.process_ids():
                pm=self.registry.manifest(pid)
                c.execute("INSERT OR IGNORE INTO r2_process_state(run_id,process_id,process_version,stage,status,attempt_count) VALUES(?,?,?,?,?,0)",(run_id,pid,pm['version'],pm['stage'],'PENDING'))
                c.execute("INSERT OR REPLACE INTO r2_prompt_pins(run_id,process_id,process_version,prompt_hash,model_profile) VALUES(?,?,?,?,?)",(run_id,pid,pm['version'],self.registry.prompt_hash(pid),pm['model_profile']))
        # pin R1 manifest; before snapshot so run_fingerprint includes pack/model profile
        m=self.rt.store.load_manifest(run_id); m['prompt_pack_version']=PACK; m['model_profile_set']=MODELS; m['manifest_revision']+=1; m['updated_at_utc']=n; self.rt.store.write_manifest(m)
        with self.rt.catalog.connect() as c:
            c.execute("UPDATE runs SET manifest_revision=?,updated_at_utc=? WHERE run_id=?",(m['manifest_revision'],n,run_id))
        self.rt.lifecycle.event(run_id,'R2_BOOTSTRAPPED',{'runtime':'R2.0.0','prompt_pack':PACK,'graph':GRAPH})
        return self.status(run_id)
    def status(self,run_id):
        with self.rt.catalog.connect() as c:
            c.row_factory=__import__('sqlite3').Row
            rows=[dict(x) for x in c.execute("SELECT * FROM r2_process_state WHERE run_id=? ORDER BY stage,process_id",(run_id,)).fetchall()]
            rr=c.execute("SELECT * FROM r2_process_runs WHERE run_id=?",(run_id,)).fetchone(); meta=dict(rr) if rr else None
        return {'run':meta,'processes':rows}
    def _status_map(self,run_id): return {x['process_id']:x['status'] for x in self.status(run_id)['processes']}
    def _assert_prompt_pin(self,run_id,pid):
        current=self.registry.prompt_hash(pid); pm=self.registry.manifest(pid)
        with self.rt.catalog.connect() as c:
            r=c.execute("SELECT process_version,prompt_hash,model_profile FROM r2_prompt_pins WHERE run_id=? AND process_id=?",(run_id,pid)).fetchone()
        if not r: raise OrchestratorError('prompt pin missing for '+pid)
        if r[0]!=pm['version'] or r[1]!=current or r[2]!=pm['model_profile']:
            raise OrchestratorError('PROMPT_OR_PROFILE_DRIFT_AFTER_PIN: '+pid)
        return True
    def ready_jobs(self,run_id):
        sm=self._status_map(run_id); ready=self.graph.ready(sm); jobs=[]
        for pid in ready:
            self._assert_prompt_pin(run_id,pid)
            context=self.ctx.compile(run_id,pid); jobs.append(make_job(run_id,pid,self.registry,context))
        return jobs
    def start(self,run_id,pid,job_hash=None):
        with self.rt.catalog.connect() as c:
            r=c.execute("SELECT status,attempt_count FROM r2_process_state WHERE run_id=? AND process_id=?",(run_id,pid)).fetchone()
            if not r: raise OrchestratorError('process not initialized')
            if r[0] not in ('PENDING','FAILED_RETRYABLE'): raise OrchestratorError('process not startable: '+r[0])
            c.execute("UPDATE r2_process_state SET status='RUNNING',attempt_count=attempt_count+1,last_job_hash=? WHERE run_id=? AND process_id=?",(job_hash,run_id,pid))
        self.rt.lifecycle.event(run_id,'R2_PROCESS_STARTED',{'process_id':pid,'job_hash':job_hash})
    def complete(self,run_id,pid,envelope):
        pm=self.registry.manifest(pid)
        if envelope.get('run_id')!=run_id or envelope.get('process_id')!=pid: raise OrchestratorError('output envelope identity mismatch')
        status=envelope.get('status')
        if status not in ('PRESENT','NOT_APPLICABLE','UNAVAILABLE','UNDETERMINED','ESCALATE','FAILED'): raise OrchestratorError('invalid output status')
        arts=envelope.get('artifacts') or {}
        if status=='PRESENT':
            expected={x['logical_name']:x for x in pm['outputs']}
            missing=[x for x in expected if x not in arts]
            if missing: raise OrchestratorError('missing expected output(s): '+','.join(missing))
            for name,payload in arts.items():
                if name not in expected: raise OrchestratorError('unexpected output: '+name)
                cfg=expected[name]; validate_json_schema(self.vault,cfg['schema_ref'],payload)
                if cfg.get('mode')=='R1_SNAPSHOT_MANIFEST':
                    self.rt.freeze_snapshot_manifest(run_id,payload)
                else:
                    self.rt.store.put_artifact(run_id,name,cfg['world'],cfg['artifact_stage'],payload,'application/json',producer_process_id=pid,producer_version=pm['version'])
        # non-present statuses still need typed applicability artifacts for expected scientific outputs; R2 records a process receipt and gates will fail if required output artifacts are absent
        final='COMPLETED' if status=='PRESENT' else status
        with self.rt.catalog.connect() as c:
            c.execute("UPDATE r2_process_state SET status=?,output_status=?,output_reason=?,completed_at_utc=? WHERE run_id=? AND process_id=?",(final,status,envelope.get('reason'),now(),run_id,pid))
        self.rt.lifecycle.event(run_id,'R2_PROCESS_COMPLETED',{'process_id':pid,'status':status})
        # lifecycle coupling
        m=self.rt.store.load_manifest(run_id)
        if pid=='P10_SCOPE' and m['state']=='REQUESTED': self.rt.lifecycle.transition(run_id,'INPUTS_RESOLVED','R2_SCOPE_RESOLVED',{})
        if pid=='W21_SNAPSHOT_AUDIT' and status=='PRESENT':
            m=self.rt.store.load_manifest(run_id)
            if m['state']=='INPUTS_RESOLVED': self.rt.lifecycle.transition(run_id,'SNAPSHOT_FROZEN','R2_SNAPSHOT_FROZEN',{})
        if pid=='W23_LINEAGE_VALIDATOR' and status=='PRESENT':
            m=self.rt.store.load_manifest(run_id)
            if m['state']=='SNAPSHOT_FROZEN': self.rt.lifecycle.transition(run_id,'EVIDENCE_FROZEN','R2_EVIDENCE_FROZEN',{})
        return self.status(run_id)
    def gate(self,run_id,gate_id,store_receipt=True):
        rec=self.gates.evaluate(run_id,gate_id,self._status_map(run_id))
        if store_receipt:
            logical='r2_gate_'+gate_id.lower()
            # unique gate receipt once only
            try: ref=self.rt.store.put_artifact(run_id,logical,'DECISION','DECISION',rec,'application/json',producer_process_id='R2_GATE',producer_version=R2_VERSION)
            except Exception: ref=None
            with self.rt.catalog.connect() as c:
                c.execute("INSERT OR REPLACE INTO r2_stage_gates(run_id,gate_id,status,receipt_hash,created_at_utc) VALUES(?,?,?,?,?)",(run_id,gate_id,rec['status'],ref['artifact_hash'] if ref else None,rec['created_at_utc']))
        return rec
    def finalize_decision(self,run_id):
        rec=self.gate(run_id,'G4_DECISION_COMPLETION',store_receipt=True)
        if rec['status']!='PASS': raise OrchestratorError('G4 decision completion failed')
        m=self.rt.store.load_manifest(run_id)
        if m['state']!='EVIDENCE_FROZEN': raise OrchestratorError('run must be EVIDENCE_FROZEN before cognition freeze')
        self.rt.lifecycle.transition(run_id,'COGNITION_FROZEN','R2_COGNITION_FROZEN',{})
        from alpha_runtime.seal_safe import create_decision_seal
        seal=create_decision_seal(run_id,self.rt)
        with self.rt.catalog.connect() as c: c.execute("UPDATE r2_process_runs SET status='DECISION_SEALED',updated_at_utc=? WHERE run_id=?",(now(),run_id))
        return seal
