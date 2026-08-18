from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, tempfile
PHASE=Path(__file__).resolve().parents[1]; NEXT=PHASE.parent; VAULT=NEXT.parent; REPO=VAULT.parent
P09=NEXT/'AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0'; P12=NEXT/'AD_V3_PHASE_12_FINAL_CERTIFICATION_PRODUCTION_FREEZE'
VERSION='3.1.1-forward-quality'
def iso(dt=None):
    dt=dt or datetime.now(timezone.utc)
    if isinstance(dt,str): dt=datetime.fromisoformat(dt.replace('Z','+00:00'))
    if dt.tzinfo is None: dt=dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat().replace('+00:00','Z')
def parse_dt(v):
    if not v:return None
    if isinstance(v,datetime):return (v if v.tzinfo else v.replace(tzinfo=timezone.utc)).astimezone(timezone.utc)
    try:
        x=datetime.fromisoformat(str(v).replace('Z','+00:00'));return (x if x.tzinfo else x.replace(tzinfo=timezone.utc)).astimezone(timezone.utc)
    except Exception:return None
def load(p,default=None):
    p=Path(p)
    if not p.exists():return default
    return json.loads(p.read_text(encoding='utf-8-sig'))
def atomic_json(p,obj):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);fd,tmp=tempfile.mkstemp(prefix=p.name+'.',suffix='.tmp',dir=str(p.parent));os.close(fd)
    try:Path(tmp).write_text(json.dumps(obj,ensure_ascii=False,indent=2,default=str)+'\n',encoding='utf-8');os.replace(tmp,p)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)
def sha_file(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def sha_obj(o):return hashlib.sha256(json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False,default=str).encode()).hexdigest()
def cfg(name):return load(PHASE/'config'/name,{}) or {}
def state_dir(root=None):return Path(root) if root else PHASE/'artifacts/state'
