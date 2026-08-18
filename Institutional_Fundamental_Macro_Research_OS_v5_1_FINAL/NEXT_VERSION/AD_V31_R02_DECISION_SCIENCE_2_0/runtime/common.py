from __future__ import annotations
from pathlib import Path
import json,hashlib,datetime
HERE=Path(__file__).resolve(); PH=HERE.parents[1]; NEXT=PH.parent
P03=NEXT/'AD_V3_PHASE_03_CAUSAL_GOLD_BRAIN_DECISION_ENGINE'; P08=NEXT/'AD_V3_PHASE_08_DECISION_SCIENCE_CALIBRATION'; P09=NEXT/'AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0'; R01=NEXT/'AD_V31_R01_FORWARD_QUALITY_PROMOTION_SCIENCE'
def load(p,default=None):
    p=Path(p)
    if not p.exists(): return default
    return json.loads(p.read_text(encoding='utf-8-sig'))
def cfg(name):return load(PH/'config'/name)
def sha_obj(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def sha_file(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def iso(dt=None):
    x=dt or datetime.datetime.now(datetime.timezone.utc)
    if isinstance(x,str):x=parse_dt(x)
    if x.tzinfo is None:x=x.replace(tzinfo=datetime.timezone.utc)
    return x.astimezone(datetime.timezone.utc).isoformat().replace('+00:00','Z')
def parse_dt(v):
    if isinstance(v,datetime.datetime):
        return v if v.tzinfo else v.replace(tzinfo=datetime.timezone.utc)
    return datetime.datetime.fromisoformat(str(v).replace('Z','+00:00'))
def stable_id(prefix,obj):return prefix+'_'+sha_obj(obj)[:24].upper()
