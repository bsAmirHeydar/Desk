from __future__ import annotations
import os,pathlib,shutil,time
from .common import atomic_json,atomic_text,load,sha_file,sha_obj,iso
class RuntimeLocked(RuntimeError): pass
class ArtifactManager:
    def __init__(self,root,create=True):
        self.root=pathlib.Path(root);self.runs=self.root/'runs';self.latest=self.root/'latest';self.state=self.root/'state'
        if create:
            for d in (self.runs,self.latest,self.state):d.mkdir(parents=True,exist_ok=True)
        self.lock=self.state/'runtime.lock';self.locked=False
    def acquire(self,run_id):
        try:
            fd=os.open(str(self.lock),os.O_CREAT|os.O_EXCL|os.O_WRONLY)
            os.write(fd,(run_id+'\n').encode());os.close(fd);self.locked=True
        except FileExistsError: raise RuntimeLocked('RUNTIME_LOCKED')
    def release(self):
        if self.locked:
            try:self.lock.unlink()
            except FileNotFoundError:pass
            self.locked=False
    def run_dir(self,run_id):
        d=self.runs/run_id;d.mkdir(parents=True,exist_ok=False);return d
    def pointer(self,name,obj): atomic_json(self.latest/name,obj)
    def read_pointer(self,name): return load(self.latest/name)
    def publish_attempt(self,receipt): self.pointer('last_attempt.json',receipt)
    def publish_success(self,receipt,rd):
        self.pointer('last_success.json',receipt)
        mapping={'run_result.json':'latest_run.json','control_room.html':'latest_control_room.html','control_room.json':'latest_control_room.json','control_room_view_model.json':'latest_control_room_view_model.json','p11_report_receipt.json':'latest_p11_report_receipt.json','run_capsule.json':'latest_capsule.json','run_seal.json':'latest_seal.json','control_room_input.json':'latest_control_room_input.json'}
        for src,name in mapping.items():
            p=rd/src
            if p.exists():
                tmp=self.latest/(name+'.tmp');shutil.copy2(p,tmp);os.replace(tmp,self.latest/name)
    def lock_state(self): return {'locked':self.lock.exists(),'lock_path':str(self.lock)}

def build_seal(rd):
    rd=pathlib.Path(rd);names=['run_result.json','control_room.html','control_room_view_model.json','p11_report_receipt.json','run_capsule.json','control_room_input.json'];hashes={n:sha_file(rd/n) for n in names if (rd/n).exists()};seal={'record_type':'AD_V3_P10_RUN_SEAL','sealed_at_utc':iso(),'sealed_hashes':hashes,'seal_id':'P10SEAL_'+sha_obj(hashes)[:24].upper()};atomic_json(rd/'run_seal.json',seal);return seal

def verify_seal(rd):
    rd=pathlib.Path(rd);s=load(rd/'run_seal.json');
    if not s:return False
    return all((rd/n).exists() and sha_file(rd/n)==h for n,h in (s.get('sealed_hashes') or {}).items())
