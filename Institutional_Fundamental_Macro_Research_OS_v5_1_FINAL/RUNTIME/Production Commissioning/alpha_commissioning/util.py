from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, os, sys, subprocess

TEXT_EXT={'.md','.json','.yaml','.yml','.txt','.csv','.py','.sql','.ps1','.cmd'}

def now(): return datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00','Z')
def load_json(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def dump_json(p,x):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
def sha256_bytes(b): return 'sha256:'+hashlib.sha256(b).hexdigest()
def sha256_obj(x): return sha256_bytes(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8'))
def canonical_bytes(p):
    p=Path(p);b=p.read_bytes()
    if p.suffix.lower() not in TEXT_EXT:return b
    try:s=b.decode('utf-8-sig')
    except UnicodeDecodeError:return b
    return s.replace('\r\n','\n').replace('\r','\n').encode('utf-8')
def chash(p): return sha256_bytes(canonical_bytes(p))
def data_root(vault):
    e=os.environ.get('ALPHALAB_DATA_ROOT')
    if e:return Path(e).expanduser().resolve()
    return Path(vault).resolve().parent/'AlphaLab_Data'
def add_runtime_paths(v):
    v=Path(v).resolve()
    for rel in ('RUNTIME/R1 Foundation','RUNTIME/R2 Prompt Execution OS','RUNTIME/R3 Operational Execution and Learning OS','RUNTIME/R4 Scientific Certification and Reproducibility Hardening','RUNTIME/Production Commissioning'):
        p=str(v/rel)
        if p not in sys.path:sys.path.insert(0,p)
def ensure_inside(vault,p):
    v=Path(vault).resolve();q=Path(p).resolve()
    if q!=v and v not in q.parents:raise RuntimeError('path escaped vault: '+str(p))
    return q
def host_command_json(vault):
    v=Path(vault).resolve();tool=v/'RUNTIME'/'Production Commissioning'/'tools'/'openai_host.py'
    return json.dumps([sys.executable,str(tool)],ensure_ascii=False,separators=(',',':'))


def current_certification_surface(vault):
    v=Path(vault).resolve();add_runtime_paths(v)
    from alpha_certification.fingerprint import verify
    r=verify(v)
    if not r.get('pass'):raise RuntimeError('R4 certification surface drift: '+json.dumps(r,ensure_ascii=False)[:4000])
    return r['actual_surface_hash']

def repo_git_state(vault):
    v=Path(vault).resolve();repo=v.parent
    q=subprocess.run(['git','-C',str(repo),'rev-parse','HEAD'],capture_output=True,text=True)
    if q.returncode:raise RuntimeError('cannot resolve Git HEAD')
    head=q.stdout.strip()
    q=subprocess.run(['git','-C',str(repo),'status','--porcelain','--untracked-files=no'],capture_output=True,text=True)
    if q.returncode:raise RuntimeError('cannot inspect Git working tree')
    return {'repo_root':str(repo),'head':head,'tracked_clean':not bool(q.stdout.strip())}
