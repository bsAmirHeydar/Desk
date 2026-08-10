from pathlib import Path
import json,hashlib,datetime,statistics,time,sys

def now(): return datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def canon(x): return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def sha(x): return 'sha256:'+hashlib.sha256((x if isinstance(x,(bytes,bytearray)) else canon(x).encode('utf-8'))).hexdigest()
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def add_paths(vault):
    v=Path(vault).resolve()
    for p in [v/'RUNTIME'/'Core Research Method Kernel',v/'RUNTIME'/'APL-A Alpha Perspective Layer',v/'RUNTIME'/'R1 Foundation',v/'RUNTIME'/'R2 Prompt Execution OS',v/'RUNTIME'/'R3 Operational Execution and Learning OS']:
        s=str(p)
        if s not in sys.path: sys.path.insert(0,s)
def pct(vals,q):
    if not vals:return 0.0
    a=sorted(vals); idx=max(0,min(len(a)-1,int(round((len(a)-1)*q))))
    return a[idx]
