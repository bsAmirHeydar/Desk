from __future__ import annotations
from pathlib import Path
from .common import PHASE,REPO,load_json,sha_file,sha_obj

def build(repo=REPO):
    pol=load_json(PHASE/'config/r05_freeze_policy.json',{}) or {}
    rows=[];seen=set()
    for pat in pol.get('immutable_patterns',[]):
        for f in sorted(Path(repo).glob(pat)):
            if f.is_file() and f not in seen:
                seen.add(f); rows.append({'path':f.relative_to(repo).as_posix(),'sha256':sha_file(f)})
    core={'record_type':'AD_V31_R05_IMPLEMENTATION_FREEZE','schema_version':'1.0.0','version':'3.1.5-operations-human-intelligence','surfaces':rows,'scientific_authority':False,'r04_cohort_reset':False}
    core['fingerprint']='V31R05_'+sha_obj(rows).upper()
    return core

def verify(repo=REPO,manifest=None):
    m=manifest or load_json(PHASE/'qualification/R05_IMPLEMENTATION_FREEZE.json',{}) or {}
    drift=[]
    for r in m.get('surfaces',[]):
        p=Path(repo)/r['path']; got=sha_file(p) if p.exists() else None
        if got!=r['sha256']: drift.append({'path':r['path'],'expected':r['sha256'],'actual':got})
    return {'status':'PASS' if not drift and bool(m.get('surfaces')) else 'FAIL','drift':drift,'surface_count':len(m.get('surfaces',[])),'fingerprint':m.get('fingerprint')}

def verify_science(next_root=None):
    nr=Path(next_root) if next_root else PHASE.parent
    b=load_json(PHASE/'baseline/PRE_R05_SCIENCE_HASHES.json',{}) or {}; drift=[]
    for rel,expected in (b.get('hashes') or {}).items():
        p=nr/rel; got=sha_file(p) if p.exists() else None
        if got!=expected: drift.append({'path':rel,'expected':expected,'actual':got})
    return {'status':'PASS' if not drift else 'FAIL','drift':drift,'surface_count':len(b.get('hashes') or {}),'baseline_commit':b.get('baseline_commit')}
