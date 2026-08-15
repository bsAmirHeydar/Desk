from pathlib import Path
from contextlib import contextmanager
import json,hashlib,os

def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,default=str)
def hsh(x):return 'sha256:'+hashlib.sha256(canon(x).encode()).hexdigest()
def root(data_root):p=Path(data_root)/'alpha_desk_v2/p09_learning';p.mkdir(parents=True,exist_ok=True);return p
@contextmanager
def lock(p):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
 try:
  fd=os.open(str(p),os.O_CREAT|os.O_EXCL|os.O_WRONLY);os.close(fd);yield
 finally:
  try:p.unlink()
  except FileNotFoundError:pass
def append(p,obj):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
 with lock(str(p)+'.lock'):
  with p.open('a',encoding='utf-8',newline='\n') as f:f.write(canon(obj)+'\n');f.flush();os.fsync(f.fileno())
def create(p,obj):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists():raise RuntimeError('immutable record exists: '+str(p))
 with lock(str(p)+'.lock'):
  if p.exists():raise RuntimeError('immutable record exists: '+str(p))
  tmp=p.with_suffix(p.suffix+'.tmp');tmp.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');os.replace(tmp,p)
def read_jsonl(p):
 p=Path(p);out=[]
 if not p.is_file():return out
 for line in p.read_text(encoding='utf-8').splitlines():
  if not line.strip():continue
  try:out.append(json.loads(line))
  except:pass
 return out
