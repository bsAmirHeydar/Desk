from __future__ import annotations
import json, hashlib
from datetime import datetime, timezone
from pathlib import Path

def iso(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def load_json(path,default=None):
    p=Path(path)
    if not p.exists(): return {} if default is None else default
    return json.loads(p.read_text(encoding='utf-8-sig'))
def write_json(path,obj):
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    return p
def stable_id(prefix,obj):
    raw=json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')
    return prefix+'_'+hashlib.sha256(raw).hexdigest()[:24].upper()
def sha256_file(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()
def human_effect(x):
    return {'BULLISH_GOLD':'به نفع طلا','BEARISH_GOLD':'به ضرر طلا','MIXED':'متناقض','UNKNOWN':'اثبات‌نشده','NEUTRAL':'بدون فشار تازه','NO_DIRECTION':'بدون جهت قابل اتکا'}.get(x,str(x or 'UNKNOWN'))
