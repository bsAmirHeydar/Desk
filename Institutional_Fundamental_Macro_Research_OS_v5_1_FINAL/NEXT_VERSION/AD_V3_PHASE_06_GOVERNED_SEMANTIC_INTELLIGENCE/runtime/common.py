from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json

def load_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))

def write_json(path,obj):
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=False)+'\n',encoding='utf-8')
    return p

def canonical_bytes(obj):
    return json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')

def sha256_obj(obj): return hashlib.sha256(canonical_bytes(obj)).hexdigest()
def sha256_file(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def stable_id(prefix,obj,n=24): return prefix+'_'+sha256_obj(obj)[:n].upper()
def iso(): return datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
