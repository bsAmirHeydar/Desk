from __future__ import annotations
from pathlib import Path
import json,hashlib,datetime
HERE=Path(__file__).resolve(); PH=HERE.parents[1]; NXT=PH.parent
P03=NXT/'AD_V3_PHASE_03_CAUSAL_GOLD_BRAIN_DECISION_ENGINE'; P04=NXT/'AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING'; P06=NXT/'AD_V3_PHASE_06_GOVERNED_SEMANTIC_INTELLIGENCE'; P07=NXT/'AD_V3_PHASE_07_LIVE_INTRADAY_GOLD_DATA_KERNEL'
def load(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def config(name): return load(PH/'config'/name)
def iso(): return datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00','Z')
def stable_id(prefix,obj):
    raw=json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8'); return prefix+'_'+hashlib.sha256(raw).hexdigest()[:24].upper()
def sha256_file(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def clamp_edge(edge,max_edge):
    order=['NO_EDGE','LOW_EDGE','CONDITIONAL_EDGE','ACTIONABLE_EDGE']; return order[min(order.index(edge),order.index(max_edge))]
