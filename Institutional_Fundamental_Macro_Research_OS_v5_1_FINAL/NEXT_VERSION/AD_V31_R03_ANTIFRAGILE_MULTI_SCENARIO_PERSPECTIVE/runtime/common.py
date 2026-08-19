from __future__ import annotations
from pathlib import Path
import json,hashlib,datetime,os,tempfile
HERE=Path(__file__).resolve();PH=HERE.parents[1];NEXT=PH.parent
R02=NEXT/'AD_V31_R02_DECISION_SCIENCE_2_0';P09=NEXT/'AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0';R01=NEXT/'AD_V31_R01_FORWARD_QUALITY_PROMOTION_SCIENCE'
def load(p,default=None):
    p=Path(p)
    if not p.exists():return default
    return json.loads(p.read_text(encoding='utf-8-sig'))
def cfg(name):return load(PH/'config'/name,{})
def sha_obj(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=False,default=str).encode()).hexdigest()
def sha_file(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def iso(dt=None):
    x=dt or datetime.datetime.now(datetime.timezone.utc)
    if isinstance(x,str):return x
    if x.tzinfo is None:x=x.replace(tzinfo=datetime.timezone.utc)
    return x.astimezone(datetime.timezone.utc).isoformat().replace('+00:00','Z')
def stable_id(prefix,obj):return prefix+'_'+sha_obj(obj)[:24].upper()
def atomic_json(path,obj):
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True);fd,tmp=tempfile.mkstemp(prefix=p.name+'.',suffix='.tmp',dir=str(p.parent));os.close(fd)
    try:Path(tmp).write_text(json.dumps(obj,indent=2,ensure_ascii=False,default=str)+'\n',encoding='utf-8');os.replace(tmp,p)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)
