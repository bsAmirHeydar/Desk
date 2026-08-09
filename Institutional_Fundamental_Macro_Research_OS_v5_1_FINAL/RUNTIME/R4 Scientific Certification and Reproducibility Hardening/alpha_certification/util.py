from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, os, sys, subprocess, uuid
TEXT_EXT={'.md','.json','.yaml','.yml','.txt','.csv','.py','.sql','.ps1','.cmd'}
def now(): return datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00','Z')
def uid(prefix): return prefix+'_'+uuid.uuid4().hex[:20].upper()
def load_json(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def canonical_bytes(p):
    p=Path(p);b=p.read_bytes()
    if p.suffix.lower() not in TEXT_EXT:return b
    try:s=b.decode('utf-8-sig')
    except UnicodeDecodeError:return b
    return s.replace('\r\n','\n').replace('\r','\n').encode('utf-8')
def chash(p): return 'sha256:'+hashlib.sha256(canonical_bytes(p)).hexdigest()
def sha256_bytes(b): return 'sha256:'+hashlib.sha256(b).hexdigest()
def sha256_obj(x): return sha256_bytes(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8'))
def add_runtime_paths(v):
    v=Path(v)
    for rel in ('RUNTIME/R1 Foundation','RUNTIME/R2 Prompt Execution OS','RUNTIME/R3 Operational Execution and Learning OS','RUNTIME/R4 Scientific Certification and Reproducibility Hardening'):
        p=str(v/rel)
        if p not in sys.path:sys.path.insert(0,p)
def run_tool(cmd):
    return subprocess.run(cmd,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
def case(case_id,category,status,detail=None,hard=True): return {'case_id':case_id,'category':category,'hard':bool(hard),'status':status,'detail':detail}
def check_hash_bytes(actual,expected,label='content'):
    h=sha256_bytes(actual)
    if h!=expected: raise RuntimeError(label+' drift: expected '+str(expected)+' got '+h)
    return True
