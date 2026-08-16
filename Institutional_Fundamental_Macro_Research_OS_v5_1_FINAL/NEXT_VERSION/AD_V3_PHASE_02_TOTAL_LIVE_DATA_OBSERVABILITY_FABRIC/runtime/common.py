from __future__ import annotations
import hashlib, json, re
from datetime import datetime, timezone
from pathlib import Path

ISO_Z = "%Y-%m-%dT%H:%M:%SZ"

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

def iso(dt: datetime | None = None) -> str:
    dt = dt or utc_now()
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).strftime(ISO_Z)

def parse_iso(v: str | None) -> datetime | None:
    if not v:
        return None
    s = str(v).strip()
    for z in (s, s.replace('Z','+00:00')):
        try:
            d=datetime.fromisoformat(z)
            if d.tzinfo is None: d=d.replace(tzinfo=timezone.utc)
            return d.astimezone(timezone.utc)
        except Exception:
            pass
    return None

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def canon(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",",":"), ensure_ascii=False)

def stable_id(prefix: str, obj) -> str:
    return f"{prefix}_{hashlib.sha256(canon(obj).encode('utf-8')).hexdigest()[:24].upper()}"

def load_json(p: Path):
    return json.loads(p.read_text(encoding='utf-8'))

def write_json(p: Path, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+"\n",encoding='utf-8')

def append_jsonl(p: Path, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('a',encoding='utf-8',newline='\n') as f:
        f.write(json.dumps(obj,ensure_ascii=False,sort_keys=True)+"\n")

def slug(s: str) -> str:
    return re.sub(r'[^A-Za-z0-9_.-]+','_',str(s)).strip('_') or 'item'
