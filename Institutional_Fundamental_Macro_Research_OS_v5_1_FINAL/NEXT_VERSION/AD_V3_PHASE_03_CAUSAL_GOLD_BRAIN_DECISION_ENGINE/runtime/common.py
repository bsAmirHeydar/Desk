from __future__ import annotations
import json, hashlib
from pathlib import Path
from datetime import datetime, timezone

def load_json(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def canon(o): return json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def stable_id(prefix,o): return prefix+'_'+hashlib.sha256(canon(o).encode()).hexdigest()[:24].upper()
def iso(): return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
def rank_strength(v): return {'UNKNOWN':0,'LOW':1,'MEDIUM':2,'HIGH':3}.get(v,0)
def max_strength(vals):
    vals=list(vals); return max(vals,key=rank_strength) if vals else 'UNKNOWN'
def effect_sign(e): return 1 if e=='BULLISH_GOLD' else -1 if e=='BEARISH_GOLD' else 0
