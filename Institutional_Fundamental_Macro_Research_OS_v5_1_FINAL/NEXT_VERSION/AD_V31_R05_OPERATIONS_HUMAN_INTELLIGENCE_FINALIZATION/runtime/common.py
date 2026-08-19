from __future__ import annotations
from pathlib import Path
import json,hashlib,os,datetime
PHASE=Path(__file__).resolve().parents[1]
NEXT=PHASE.parent
REPO=NEXT.parents[1]
def load_json(p,default=None):
    p=Path(p)
    if not p.exists(): return default
    try:return json.loads(p.read_text(encoding='utf-8-sig'))
    except Exception:return default
def atomic_json(p,obj):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);tmp=p.with_name(p.name+'.tmp')
    with open(tmp,'w',encoding='utf-8',newline='\n') as f:
        json.dump(obj,f,ensure_ascii=False,indent=2);f.write('\n');f.flush()
        try:os.fsync(f.fileno())
        except Exception:pass
    os.replace(tmp,p)
def iso(dt=None):
    dt=dt or datetime.datetime.now(datetime.timezone.utc)
    if isinstance(dt,str):return dt
    if dt.tzinfo is None:dt=dt.replace(tzinfo=datetime.timezone.utc)
    return dt.astimezone(datetime.timezone.utc).isoformat().replace('+00:00','Z')
def sha_file(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def sha_obj(o):return hashlib.sha256(json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def cfg(name):return load_json(PHASE/'config'/name,{}) or {}
