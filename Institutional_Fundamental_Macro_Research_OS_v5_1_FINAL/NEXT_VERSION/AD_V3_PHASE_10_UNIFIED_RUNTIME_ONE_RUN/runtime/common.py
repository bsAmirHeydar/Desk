from __future__ import annotations
import hashlib,json,os,pathlib,tempfile
from datetime import datetime,timezone

def iso(dt=None):
    dt=dt or datetime.now(timezone.utc)
    if isinstance(dt,str): return dt
    return dt.astimezone(timezone.utc).isoformat().replace('+00:00','Z')

def load(path,default=None):
    p=pathlib.Path(path)
    if not p.exists(): return default
    return json.loads(p.read_text(encoding='utf-8-sig'))

def canonical_bytes(obj): return json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=False,default=str).encode('utf-8')
def sha_obj(obj): return hashlib.sha256(canonical_bytes(obj)).hexdigest()
def sha_file(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()
def stable_id(prefix,obj): return prefix+'_'+sha_obj(obj)[:24].upper()
def atomic_json(path,obj):
    p=pathlib.Path(path);p.parent.mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(prefix=p.name+'.',suffix='.tmp',dir=str(p.parent));os.close(fd)
    try:
        pathlib.Path(tmp).write_text(json.dumps(obj,indent=2,ensure_ascii=False,default=str)+'\n',encoding='utf-8')
        os.replace(tmp,p)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)
def atomic_text(path,text):
    p=pathlib.Path(path);p.parent.mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(prefix=p.name+'.',suffix='.tmp',dir=str(p.parent));os.close(fd)
    try:
        pathlib.Path(tmp).write_text(text,encoding='utf-8');os.replace(tmp,p)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)
