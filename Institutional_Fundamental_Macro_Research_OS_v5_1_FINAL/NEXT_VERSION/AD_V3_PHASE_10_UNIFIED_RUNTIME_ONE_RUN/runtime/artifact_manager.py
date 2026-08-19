from __future__ import annotations
import os,pathlib,shutil,time,json,socket,datetime
from .common import atomic_json,atomic_text,load,sha_file,sha_obj,iso
class RuntimeLocked(RuntimeError): pass
class ArtifactManager:
    def __init__(self,root,create=True):
        self.root=pathlib.Path(root);self.runs=self.root/'runs';self.latest=self.root/'latest';self.state=self.root/'state'
        if create:
            for d in (self.runs,self.latest,self.state):d.mkdir(parents=True,exist_ok=True)
        self.lock=self.state/'runtime.lock';self.locked=False;self.lock_run_id=None
    def _read_lock(self):
        if not self.lock.exists():return None
        try:
            txt=self.lock.read_text(encoding='utf-8-sig').strip();o=json.loads(txt)
            return o if isinstance(o,dict) else {'legacy':txt}
        except Exception:
            try:return {'legacy':self.lock.read_text(encoding='utf-8-sig').strip()}
            except Exception:return {'corrupt':True}
    def classify_lock(self,stale_after_seconds=7200):
        o=self._read_lock()
        if o is None:return {'state':'UNLOCKED','locked':False,'lock_path':str(self.lock)}
        if o.get('corrupt'):return {'state':'CORRUPT','locked':True,'lock_path':str(self.lock),'metadata':o}
        if 'legacy' in o:return {'state':'AMBIGUOUS','locked':True,'lock_path':str(self.lock),'metadata':o}
        try:
            s=str(o.get('started_at_utc') or '').replace('Z','+00:00');dt=datetime.datetime.fromisoformat(s);age=(datetime.datetime.now(datetime.timezone.utc)-dt.astimezone(datetime.timezone.utc)).total_seconds()
        except Exception:age=None
        host=o.get('host');same_host=(not host) or host==socket.gethostname()
        state='ACTIVE'
        if age is not None and age>stale_after_seconds and same_host:state='STALE_RECOVERABLE'
        elif not same_host:state='AMBIGUOUS'
        return {'state':state,'locked':True,'lock_path':str(self.lock),'metadata':o,'age_seconds':age}
    def recover_stale_lock(self):
        st=self.classify_lock()
        if st.get('state')!='STALE_RECOVERABLE':return False
        try:self.lock.unlink();return True
        except FileNotFoundError:return True
    def acquire(self,run_id,mode='UNKNOWN'):
        if self.lock.exists():
            st=self.classify_lock()
            if st.get('state')=='STALE_RECOVERABLE':self.recover_stale_lock()
            else:raise RuntimeLocked('RUNTIME_LOCKED:'+st.get('state','UNKNOWN'))
        meta={'run_id':run_id,'pid':os.getpid(),'host':socket.gethostname(),'mode':mode,'started_at_utc':iso()}
        try:
            fd=os.open(str(self.lock),os.O_CREAT|os.O_EXCL|os.O_WRONLY);os.write(fd,(json.dumps(meta,sort_keys=True)+'\n').encode());os.close(fd);self.locked=True;self.lock_run_id=run_id
        except FileExistsError:raise RuntimeLocked('RUNTIME_LOCKED:RACE')
    def release(self):
        if self.locked:
            try:
                cur=self._read_lock() or {}
                if cur.get('run_id') in (None,self.lock_run_id):self.lock.unlink()
            except FileNotFoundError:pass
            self.locked=False;self.lock_run_id=None
    def run_dir(self,run_id):
        d=self.runs/run_id;d.mkdir(parents=True,exist_ok=False);return d
    def pointer(self,name,obj): atomic_json(self.latest/name,obj)
    def read_pointer(self,name): return load(self.latest/name)
    def publish_attempt(self,receipt): self.pointer('last_attempt.json',receipt)
    def publish_success(self,receipt,rd):
        self.pointer('last_success.json',receipt)
        mapping={'run_result.json':'latest_run.json','control_room.html':'latest_control_room.html','control_room.json':'latest_control_room.json','control_room_view_model.json':'latest_control_room_view_model.json','p11_report_receipt.json':'latest_p11_report_receipt.json','run_capsule.json':'latest_capsule.json','run_seal.json':'latest_seal.json','control_room_input.json':'latest_control_room_input.json','r05_operations_receipt.json':'latest_operations_receipt.json'}
        for src,name in mapping.items():
            p=rd/src
            if p.exists():
                tmp=self.latest/(name+'.tmp');shutil.copy2(p,tmp);os.replace(tmp,self.latest/name)
    def lock_state(self): return self.classify_lock()

def build_seal(rd):
    rd=pathlib.Path(rd);names=['run_result.json','control_room.html','control_room_view_model.json','p11_report_receipt.json','run_capsule.json','control_room_input.json','r05_operations_receipt.json'];hashes={n:sha_file(rd/n) for n in names if (rd/n).exists()};seal={'record_type':'AD_V3_P10_RUN_SEAL','sealed_at_utc':iso(),'sealed_hashes':hashes,'seal_id':'P10SEAL_'+sha_obj(hashes)[:24].upper()};atomic_json(rd/'run_seal.json',seal);return seal

def verify_seal(rd):
    rd=pathlib.Path(rd);s=load(rd/'run_seal.json');
    if not s:return False
    return all((rd/n).exists() and sha_file(rd/n)==h for n,h in (s.get('sealed_hashes') or {}).items())
