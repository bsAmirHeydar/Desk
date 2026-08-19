from __future__ import annotations
import hashlib,json,os
from datetime import datetime,timezone
from pathlib import Path

PHASE=Path(__file__).resolve().parents[1]
NEXT=PHASE.parent
REPO=NEXT.parents[1]
VERSION='3.1.4-institutional-data-edge'

def load_json(path, default=None):
    p=Path(path)
    if not p.exists(): return default
    return json.loads(p.read_text(encoding='utf-8'))

def save_json(path,obj):
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True),encoding='utf-8')

def canonical_json(obj): return json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(',',':'),default=str)
def canonical_hash(obj): return hashlib.sha256(canonical_json(obj).encode()).hexdigest()
def file_hash(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def utcnow(): return datetime.now(timezone.utc)
def iso(dt=None): return (dt or utcnow()).astimezone(timezone.utc).isoformat().replace('+00:00','Z')
def parse_dt(v):
    if isinstance(v,datetime): return v.astimezone(timezone.utc) if v.tzinfo else v.replace(tzinfo=timezone.utc)
    if not v:return None
    try:return datetime.fromisoformat(str(v).replace('Z','+00:00')).astimezone(timezone.utc)
    except Exception:return None

def env_present(name): return bool(os.getenv(name))
