from pathlib import Path
import os, json, uuid, hashlib, subprocess
from .canonical import sha256_obj, dump_json, canonical_json_bytes
from .timeutil import utc_now, to_utc_z
from .catalog import Catalog
from .store import RunStore, RuntimeStoreError
from .lifecycle import Lifecycle

class AlphaRuntime:
    def __init__(self,vault_root,data_root=None):
        self.vault=Path(vault_root).resolve(); self.r1=self.vault/'RUNTIME'/'R1 Foundation'; self.policy=json.loads((self.r1/'config'/'runtime_policy.json').read_text(encoding='utf-8')); self.storage_policy=json.loads((self.r1/'config'/'storage_policy.json').read_text(encoding='utf-8')); self.lifecycle_policy=json.loads((self.r1/'config'/'lifecycle_policy.json').read_text(encoding='utf-8'))
        default_root=self._default_data_root()
        self.data_root=Path(data_root or os.environ.get('ALPHALAB_DATA_ROOT') or default_root).resolve(); self.catalog=Catalog(self.data_root,self.r1/'sql'/'catalog_schema.sql',self.storage_policy['busy_timeout_ms']); self.catalog.init(); self.store=RunStore(self.data_root,self.catalog); self.lifecycle=Lifecycle(self.store,self.catalog,self.lifecycle_policy); self._init_dirs()
    def _default_data_root(self):
        try:
            q=subprocess.run(['git','-C',str(self.vault),'rev-parse','--show-toplevel'],capture_output=True,text=True,timeout=5)
            if q.returncode==0 and q.stdout.strip():
                return Path(q.stdout.strip()).resolve().parent/'AlphaLab_Data'
        except Exception:
            pass
        return self.vault.parent/'AlphaLab_Data'
    def _init_dirs(self):
        for x in ['objects/sha256','runs','catalog','locks','tmp','warehouse/parquet']:(self.data_root/x).mkdir(parents=True,exist_ok=True)
        with self.catalog.connect() as c:
            c.execute("INSERT OR REPLACE INTO runtime_metadata(key,value) VALUES('runtime_version','R1.0.0')")
            c.execute("INSERT OR REPLACE INTO runtime_metadata(key,value) VALUES('scientific_stack','V21.3.0')")
    def resolved_request(self,req):
        r=dict(req); cutoff=r.get('analysis_cutoff')
        if cutoff=='NOW': cutoff=utc_now()
        r['analysis_cutoff_utc']=to_utc_z(cutoff); return r
    def create_run(self,req,vault_commit=None,run_id=None):
        r=self.resolved_request(req); fp=sha256_obj({k:v for k,v in r.items() if k!='run_id'}); idem=r.get('idempotency_policy','REUSE_EXACT')
        if idem=='REUSE_EXACT':
            old=self.catalog.find_request(fp)
            if old: return self.store.load_manifest(old['run_id']),True
        now=utc_now(); rid=run_id or ('RUN_'+now.replace('-','').replace(':','').replace('T','_').replace('Z','')+'_'+uuid.uuid4().hex[:8].upper()); ep=r.get('episode_id')
        if ep:
            with self.catalog.connect() as c: c.execute("INSERT OR IGNORE INTO episodes(episode_id,research_program_id,episode_type,subject,created_at_utc) VALUES(?,?,?,?,?)",(ep,r['research_program_id'],'MANUAL',r.get('subject'),now))
        date=r['analysis_cutoff_utc'][:10].replace('-','/'); scope=r['run_scope']; subj=''.join(c if c.isalnum() or c in '._-' else '_' for c in r['subject']); episode=ep or '_NO_EPISODE'; rel=(Path('runs')/date/scope/subj/episode/rid).as_posix()
        manifest={"schema_version":"1.0.0","run_id":rid,"episode_id":ep,"request_fingerprint":fp,"run_fingerprint":None,"run_scope":scope,"subject":r['subject'],"run_mode":r['run_mode'],"analysis_cutoff_utc":r['analysis_cutoff_utc'],"state":"REQUESTED","manifest_revision":1,"vault_stack":"V21.3.0","vault_commit":vault_commit,"runtime_version":"R1.0.0","prompt_pack_version":None,"model_profile_set":None,"snapshot_manifest_hash":None,"decision_seal_hash":None,"run_close_seal_hash":None,"run_relpath":rel,"created_at_utc":now,"updated_at_utc":now}
        self.store.init_dirs(manifest); req_ref=self.store.objects.put_bytes(canonical_json_bytes(r),'application/json'); req_obj={"schema_version":"1.0.0","artifact_hash":req_ref[0],"logical_name":"run_request","world":"META","stage":"META","media_type":"application/json","original_filename":"request.json","byte_length":req_ref[2],"object_relpath":req_ref[1],"producer_process_id":"R1_RUNTIME","producer_version":"R1.0.0","created_at_utc":now}; self.catalog.upsert_artifact(req_obj)
        with self.catalog.connect() as c:
            c.execute("INSERT INTO runs(run_id,episode_id,research_program_id,run_scope,subject,run_mode,analysis_cutoff_utc,state,request_fingerprint,run_fingerprint,run_relpath,vault_stack,runtime_version,manifest_revision,created_at_utc,updated_at_utc) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(rid,ep,r['research_program_id'],scope,r['subject'],r['run_mode'],r['analysis_cutoff_utc'],'REQUESTED',fp,None,rel,'V21.3.0','R1.0.0',1,now,now))
            c.execute("INSERT INTO run_artifacts(run_id,logical_name,world,stage,artifact_hash,ref_relpath,immutable,created_at_utc) VALUES(?,?,?,?,?,?,?,?)",(rid,'run_request','META','META',req_obj['artifact_hash'],(Path(rel)/'meta'/'request.ref.json').as_posix(),1,now))
            c.execute("INSERT INTO run_events(run_id,sequence,event_type,from_state,to_state,occurred_at_utc,details_json) VALUES(?,?,?,?,?,?,?)",(rid,1,'RUN_CREATED',None,'REQUESTED',now,'{}'))
        dump_json(self.data_root/rel/'meta'/'request.ref.json',req_obj); self.store.write_manifest(manifest); self.store._refresh_index(rid)
        with open(self.data_root/rel/'meta'/'events.jsonl','a',encoding='utf-8',newline='\n') as f: f.write(json.dumps({"schema_version":"1.0.0","run_id":rid,"sequence":1,"event_type":"RUN_CREATED","from_state":None,"to_state":"REQUESTED","occurred_at_utc":now,"details":{}},sort_keys=True,separators=(',',':'))+'\n')
        return manifest,False
    def freeze_snapshot_manifest(self,run_id,snapshot_manifest):
        m=self.store.load_manifest(run_id); ref=self.store.put_artifact(run_id,'snapshot_manifest','DECISION','EVIDENCE',snapshot_manifest,'application/json',producer_process_id='R1_SNAPSHOT',producer_version='R1.0.0'); m['snapshot_manifest_hash']=ref['artifact_hash']; m['run_fingerprint']=sha256_obj({"request_fingerprint":m['request_fingerprint'],"snapshot_manifest_hash":ref['artifact_hash'],"vault_stack":m['vault_stack'],"vault_commit":m.get('vault_commit'),"runtime_version":m['runtime_version'],"prompt_pack_version":m.get('prompt_pack_version'),"model_profile_set":m.get('model_profile_set')}); m['manifest_revision']+=1; m['updated_at_utc']=utc_now(); self.store.write_manifest(m)
        with self.catalog.connect() as c: c.execute("UPDATE runs SET run_fingerprint=?,manifest_revision=?,updated_at_utc=? WHERE run_id=?",(m['run_fingerprint'],m['manifest_revision'],m['updated_at_utc'],run_id))
        return ref,m
    def reproduce_visibility_run(self,source_run_id,requirements,new_run_id=None):
        from .replay import reproduce_visibility
        srcm=self.store.load_manifest(source_run_id)
        src_req=self.store.load_artifact_json(source_run_id,'run_request')
        src_sm=self.store.load_artifact_json(source_run_id,'snapshot_manifest')
        src_vr=self.store.load_artifact_json(source_run_id,'visibility_receipt')
        req=dict(src_req); req['run_mode']='REPRODUCTION_REPLAY'; req['analysis_cutoff']=srcm['analysis_cutoff_utc']; req['idempotency_policy']='NEW_RUN'; req['tags']=list(req.get('tags') or [])+['reproduction:'+source_run_id]
        m,_=self.create_run(req,vault_commit=srcm.get('vault_commit'),run_id=new_run_id)
        self.lifecycle.transition(m['run_id'],'INPUTS_RESOLVED')
        self.store.put_artifact(m['run_id'],'coverage_requirements','DECISION','EVIDENCE',requirements,'application/json',producer_process_id='R1_REPLAY',producer_version='R1.0.0')
        replay_sm=dict(src_sm); replay_sm['run_id']=m['run_id']; replay_sm['source_run_id']=source_run_id; replay_sm['source_manifest_hash']=srcm.get('snapshot_manifest_hash'); replay_sm['created_at_utc']=utc_now(); replay_sm['manifest_hash']=None; replay_sm['manifest_hash']=sha256_obj({k:v for k,v in replay_sm.items() if k not in ('created_at_utc','manifest_hash')})
        self.freeze_snapshot_manifest(m['run_id'],replay_sm)
        self.lifecycle.transition(m['run_id'],'SNAPSHOT_FROZEN')
        receipt,meta=reproduce_visibility(srcm,src_sm,src_vr,m['run_id'],requirements)
        self.store.put_artifact(m['run_id'],'visibility_receipt','DECISION','EVIDENCE',receipt,'application/json',producer_process_id='R1_REPLAY',producer_version='R1.0.0')
        self.store.put_artifact(m['run_id'],'replay_receipt','DECISION','EVIDENCE',meta,'application/json',producer_process_id='R1_REPLAY',producer_version='R1.0.0')
        self.lifecycle.transition(m['run_id'],'EVIDENCE_FROZEN')
        with self.catalog.connect() as c:
            c.execute("INSERT INTO replay_links(source_run_id,replay_run_id,replay_mode,visibility_parity,created_at_utc) VALUES(?,?,?,?,?)",(source_run_id,m['run_id'],'REPRODUCTION_REPLAY',int(meta['visibility_parity']),utc_now()))
        return self.store.load_manifest(m['run_id']),meta

