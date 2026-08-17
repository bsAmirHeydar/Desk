from __future__ import annotations
from pathlib import Path
from .common import state_dir,atomic_write,load,iso,canonical_hash
class ForwardLedgerCorrupt(RuntimeError):pass

def path(root=None):return state_dir(root)/'forward_state.json'
def empty_state():return {'record_type':'AD_V3_P09_FORWARD_STATE','schema_version':'1.0.0','updated_at_utc':iso(),'predictions':[],'outcomes':[],'episodes':[],'cohorts':[],'market_observations':[],'integrity_failures':0,'test_fixture_samples_included':False}
def load_state(root=None):
    p=path(root)
    if not p.exists():return empty_state()
    try:s=load(p)
    except Exception as e:raise ForwardLedgerCorrupt('P09_FORWARD_LEDGER_CORRUPT:'+type(e).__name__)
    required=('predictions','outcomes','episodes','cohorts','market_observations')
    if not isinstance(s,dict) or any(not isinstance(s.get(k),list) for k in required):raise ForwardLedgerCorrupt('P09_FORWARD_LEDGER_SCHEMA_CORRUPT')
    return s
def save_state(s,root=None):s=dict(s);s['updated_at_utc']=iso();atomic_write(path(root),s);return s
def append_unique(s,key,obj,id_key):
    oid=obj[id_key]
    old=next((x for x in s[key] if x.get(id_key)==oid),None)
    if old:
        if canonical_hash(old)!=canonical_hash(obj):raise ForwardLedgerCorrupt('IMMUTABLE_RECORD_MUTATION:'+oid)
        return False
    s[key].append(obj);return True
