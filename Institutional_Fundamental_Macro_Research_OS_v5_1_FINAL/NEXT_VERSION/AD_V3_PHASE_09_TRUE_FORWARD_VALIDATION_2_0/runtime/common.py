from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, os, tempfile
PHASE=Path(__file__).resolve().parents[1]; NEXT=PHASE.parent; VAULT=NEXT.parent; REPO=VAULT.parent
P03=NEXT/'AD_V3_PHASE_03_CAUSAL_GOLD_BRAIN_DECISION_ENGINE'; P04=NEXT/'AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING'; P05=NEXT/'AD_V3_PHASE_05_INTEGRITY_ARCHITECTURE_CONSOLIDATION'; P06=NEXT/'AD_V3_PHASE_06_GOVERNED_SEMANTIC_INTELLIGENCE'; P07=NEXT/'AD_V3_PHASE_07_LIVE_INTRADAY_GOLD_DATA_KERNEL'; P08=NEXT/'AD_V3_PHASE_08_DECISION_SCIENCE_CALIBRATION'
VERSION='3.9.0-true-forward-validation-2.0'
def iso(dt=None):
    if isinstance(dt,str):
        dt=parse_dt(dt)
    dt=dt or datetime.now(timezone.utc)
    if dt.tzinfo is None: dt=dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat().replace('+00:00','Z')
def parse_dt(v):
    if isinstance(v,datetime):
        return (v if v.tzinfo else v.replace(tzinfo=timezone.utc)).astimezone(timezone.utc)
    if not v:return None
    try:
        x=datetime.fromisoformat(str(v).replace('Z','+00:00'))
        if x.tzinfo is None:x=x.replace(tzinfo=timezone.utc)
        return x.astimezone(timezone.utc)
    except Exception:return None
def load(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def atomic_write(p,obj):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);data=(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    fd,tmp=tempfile.mkstemp(prefix=p.name+'.',suffix='.tmp',dir=str(p.parent))
    try:
        with os.fdopen(fd,'wb') as f:f.write(data);f.flush();os.fsync(f.fileno())
        os.replace(tmp,p)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)
    return p
def canonical_hash(obj): return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')).hexdigest()
def sha_file(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def stable_id(prefix,obj): return prefix+'_'+canonical_hash(obj)[:24].upper()
def cfg(name): return load(PHASE/'config'/name)
def state_dir(root=None): return Path(root) if root else PHASE/'artifacts'/'state'
