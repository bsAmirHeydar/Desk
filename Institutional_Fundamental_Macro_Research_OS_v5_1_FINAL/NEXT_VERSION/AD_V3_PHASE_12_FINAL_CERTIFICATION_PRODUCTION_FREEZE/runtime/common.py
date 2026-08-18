from __future__ import annotations
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,tempfile,subprocess
PHASE=Path(__file__).resolve().parents[1];NEXT=PHASE.parent;VAULT=NEXT.parent;REPO=VAULT.parent
VERSION='3.12.1-v31-r01-qualified'
def iso():return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def load(p,default=None):
 p=Path(p)
 if not p.exists():return default
 return json.loads(p.read_text(encoding='utf-8-sig'))
def atomic_json(p,obj):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);fd,tmp=tempfile.mkstemp(prefix=p.name+'.',suffix='.tmp',dir=str(p.parent));os.close(fd)
 try:Path(tmp).write_text(json.dumps(obj,ensure_ascii=False,indent=2,default=str)+'\n',encoding='utf-8');os.replace(tmp,p)
 finally:
  if os.path.exists(tmp):os.unlink(tmp)
def sha_file(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def sha_obj(o):return hashlib.sha256(json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False,default=str).encode()).hexdigest()
def git_commit(repo=REPO):
 try:
  cp=subprocess.run(['git','-C',str(repo),'rev-parse','--short','HEAD'],capture_output=True,text=True,timeout=5)
  return cp.stdout.strip() if cp.returncode==0 else None
 except Exception:return None
