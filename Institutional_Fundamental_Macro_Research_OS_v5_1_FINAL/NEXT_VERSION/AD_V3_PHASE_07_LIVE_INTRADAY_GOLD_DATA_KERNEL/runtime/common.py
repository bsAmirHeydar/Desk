from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone, date
import json, hashlib

PHASE=Path(__file__).resolve().parents[1]
NEXT=PHASE.parent
VAULT=NEXT.parent
REPO=VAULT.parent
P01=NEXT/'AD_V3_PHASE_01_TOTAL_GOLD_KNOWLEDGE_SCIENCE_FOUNDATION'
P02=NEXT/'AD_V3_PHASE_02_TOTAL_LIVE_DATA_OBSERVABILITY_FABRIC'
P03=NEXT/'AD_V3_PHASE_03_CAUSAL_GOLD_BRAIN_DECISION_ENGINE'
P04=NEXT/'AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING'
P05=NEXT/'AD_V3_PHASE_05_INTEGRITY_ARCHITECTURE_CONSOLIDATION'
P06=NEXT/'AD_V3_PHASE_06_GOVERNED_SEMANTIC_INTELLIGENCE'
VERSION='3.7.0-live-intraday-gold-kernel'

def iso(dt=None):
    dt=dt or datetime.now(timezone.utc)
    if dt.tzinfo is None: dt=dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat().replace('+00:00','Z')

def parse_dt(v):
    if v in (None,''): return None
    s=str(v).strip()
    try:
        if len(s)==10 and s[4]=='-' and s[7]=='-':
            return datetime.fromisoformat(s+'T00:00:00+00:00')
        x=datetime.fromisoformat(s.replace('Z','+00:00'))
        if x.tzinfo is None: x=x.replace(tzinfo=timezone.utc)
        return x.astimezone(timezone.utc)
    except Exception:
        return None

def load(path): return json.loads(Path(path).read_text(encoding='utf-8-sig'))
def write(path,obj):
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return p

def digest_bytes(b): return hashlib.sha256(b).hexdigest()
def digest(path): return digest_bytes(Path(path).read_bytes())
def canonical_hash(obj): return digest_bytes(json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8'))
def stable_id(prefix,obj): return prefix+'_'+canonical_hash(obj)[:24].upper()
def rel(path): return Path(path).resolve().relative_to(REPO.resolve()).as_posix()

def config(name): return load(PHASE/'config'/name)
