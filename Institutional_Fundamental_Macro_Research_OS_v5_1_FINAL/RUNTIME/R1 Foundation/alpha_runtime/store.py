from pathlib import Path
import os, json, mimetypes
from .canonical import sha256_bytes, canonical_json_bytes, dump_json, load_json
from .timeutil import utc_now
from .locking import FileLock

WORLD_DIR={"DECISION":"decision_world","OUTCOME":"outcome_world","LEARNING":"learning_world","META":"meta"}
STAGE_DIR={"META":"","EVIDENCE":"10_evidence","MARKET_STATE":"20_market_state","COGNITION":"30_cognition","DECISION":"40_decision","EXECUTION":"50_execution","OUTCOME":"60_outcome","LEARNING":"70_learning"}

class RuntimeStoreError(RuntimeError): pass

class ArtifactStore:
    def __init__(self,data_root): self.root=Path(data_root); self.obj=self.root/"objects"/"sha256"; self.tmp=self.root/"tmp"
    def put_bytes(self,data:bytes,media_type="application/octet-stream"):
        h=sha256_bytes(data); hexh=h.split(":",1)[1]; rel=Path("objects")/"sha256"/hexh[:2]/hexh[2:4]/hexh
        p=self.root/rel; p.parent.mkdir(parents=True,exist_ok=True); self.tmp.mkdir(parents=True,exist_ok=True)
        if not p.exists():
            t=self.tmp/(hexh+"."+str(os.getpid())+".tmp"); t.write_bytes(data); os.replace(t,p)
        elif sha256_bytes(p.read_bytes())!=h: raise RuntimeStoreError("content-address collision/hash drift")
        return h,rel.as_posix(),len(data)
    def get_bytes(self,artifact_hash):
        hexh=artifact_hash.split(":",1)[1]; p=self.root/"objects"/"sha256"/hexh[:2]/hexh[2:4]/hexh
        b=p.read_bytes()
        if sha256_bytes(b)!=artifact_hash: raise RuntimeStoreError("artifact hash mismatch")
        return b

class RunStore:
    def __init__(self,data_root,catalog): self.root=Path(data_root); self.catalog=catalog; self.objects=ArtifactStore(data_root)
    def run_dir(self,run): return self.root/run['run_relpath']
    def _lock(self,run_id): return FileLock(self.root/"locks"/(run_id+".lock"))
    def init_dirs(self,run):
        rd=self.run_dir(run)
        for p in [rd/"meta"/"manifest_history",rd/"decision_world"/"10_evidence",rd/"decision_world"/"20_market_state",rd/"decision_world"/"30_cognition",rd/"decision_world"/"40_decision",rd/"outcome_world"/"50_execution",rd/"outcome_world"/"60_outcome",rd/"learning_world"/"70_learning",rd/"seals"]: p.mkdir(parents=True,exist_ok=True)
    def write_manifest(self,manifest):
        rd=self.run_dir(manifest); self.init_dirs(manifest); rev=int(manifest['manifest_revision']); hist=rd/"meta"/"manifest_history"/(f"manifest_{rev:06d}.json")
        dump_json(hist,manifest); dump_json(rd/"meta"/"manifest.json",manifest)
    def load_manifest(self,run_id):
        r=self.catalog.get_run(run_id)
        if not r: raise RuntimeStoreError("run not found")
        return load_json(self.root/r['run_relpath']/"meta"/"manifest.json")
    def put_artifact(self,run_id,logical_name,world,stage,data,media_type="application/json",original_filename=None,producer_process_id=None,producer_version=None):
        run=self.catalog.get_run(run_id)
        if not run: raise RuntimeStoreError("run not found")
        m=self.load_manifest(run_id)
        if m.get('run_close_seal_hash') and world in ("DECISION","OUTCOME","LEARNING"): raise RuntimeStoreError("run is close-sealed")
        if world=="DECISION" and m.get('decision_seal_hash'): raise RuntimeStoreError("decision world is sealed")
        if world in ("OUTCOME","LEARNING") and not m.get('decision_seal_hash'): raise RuntimeStoreError("outcome firewall: decision seal required")
        b=canonical_json_bytes(data) if isinstance(data,(dict,list)) else (data.encode('utf-8') if isinstance(data,str) else bytes(data))
        h,orel,n=self.objects.put_bytes(b,media_type)
        ref={"schema_version":"1.0.0","artifact_hash":h,"logical_name":logical_name,"world":world,"stage":stage,"media_type":media_type,"original_filename":original_filename,"byte_length":n,"object_relpath":orel,"producer_process_id":producer_process_id,"producer_version":producer_version,"created_at_utc":utc_now()}
        self.catalog.upsert_artifact(ref)
        wd=WORLD_DIR[world]; sd=STAGE_DIR[stage]; refdir=self.root/run['run_relpath']/wd
        if sd: refdir=refdir/sd
        refdir.mkdir(parents=True,exist_ok=True); refpath=refdir/(logical_name+".ref.json")
        relref=refpath.relative_to(self.root).as_posix()
        with self._lock(run_id):
            if refpath.exists(): raise RuntimeStoreError(f"logical artifact already exists: {logical_name}")
            dump_json(refpath,ref); self.catalog.register_run_artifact(run_id,ref,relref,0); self._refresh_index(run_id)
        return ref
    def _refresh_index(self,run_id):
        run=self.catalog.get_run(run_id); rows=self.catalog.list_artifacts(run_id); obj={"schema_version":"1.0.0","run_id":run_id,"artifacts":rows,"updated_at_utc":utc_now()}; dump_json(self.root/run['run_relpath']/"meta"/"artifact_index.json",obj)
    def load_artifact_json(self,run_id,logical_name):
        rows=[r for r in self.catalog.list_artifacts(run_id) if r['logical_name']==logical_name]
        if not rows: raise RuntimeStoreError("artifact not found")
        return json.loads(self.objects.get_bytes(rows[0]['artifact_hash']).decode('utf-8'))
