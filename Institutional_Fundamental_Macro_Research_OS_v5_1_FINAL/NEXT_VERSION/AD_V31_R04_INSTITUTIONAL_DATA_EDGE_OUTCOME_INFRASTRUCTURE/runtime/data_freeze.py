from __future__ import annotations
import glob
from pathlib import Path
from .common import PHASE,REPO,file_hash,canonical_hash,load_json,save_json

def surfaces():
    pats=['config/*.json','runtime/*.py','providers/*.py','schemas/*.json']
    out=[]
    for pat in pats:out += [Path(x) for x in glob.glob(str(PHASE/pat))]
    return sorted([p for p in out if p.name!='__pycache__'])
def build_manifest(path=None):
    files={str(p.relative_to(REPO)).replace('\\','/'):file_hash(p) for p in surfaces()}
    obj={'record_type':'AD_V31_R04_DATA_FREEZE','schema_version':'1.0.0','files':files,'file_count':len(files),'data_contract_fingerprint':'R04DATA_'+canonical_hash(files).upper(),'status':'PASS'}
    save_json(path or PHASE/'qualification/R04_DATA_FREEZE_MANIFEST.json',obj);return obj
def verify_manifest(path=None):
    m=load_json(path or PHASE/'qualification/R04_DATA_FREEZE_MANIFEST.json',{}) or {};bad=[]
    for rel,h in m.get('files',{}).items():
        p=REPO/rel
        if not p.exists() or file_hash(p)!=h:bad.append(rel)
    return {'status':'FAIL' if bad else 'PASS','drift':bad,'file_count':len(m.get('files',{})),'data_contract_fingerprint':m.get('data_contract_fingerprint')}
