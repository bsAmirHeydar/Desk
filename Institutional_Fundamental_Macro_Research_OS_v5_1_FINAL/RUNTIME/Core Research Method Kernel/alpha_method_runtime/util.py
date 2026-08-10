from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, sys

def now(): return datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00','Z')
def load_json(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def dump_json(p,x):
    p=Path(p); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(x,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
def canonical_bytes(x): return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def sha256_obj(x): return 'sha256:'+hashlib.sha256(canonical_bytes(x)).hexdigest()
def parse_utc(x):
    if not x: return None
    try:
        d=datetime.fromisoformat(str(x).replace('Z','+00:00'))
        if d.tzinfo is None: return None
        return d.astimezone(timezone.utc)
    except Exception: return None

def add_paths(vault):
    v=Path(vault).resolve()
    for rel in ('RUNTIME/R1 Foundation','RUNTIME/R2 Prompt Execution OS','RUNTIME/R3 Operational Execution and Learning OS','RUNTIME/Core Research Method Kernel'):
        p=str(v/rel)
        if p not in sys.path: sys.path.insert(0,p)

def validate_schema(vault_root, rel, payload):
    try: import jsonschema
    except Exception as e: raise RuntimeError('jsonschema required for method validation') from e
    p=Path(vault_root)/rel; s=load_json(p)
    jsonschema.Draft202012Validator(s).validate(payload); return True
