from __future__ import annotations
from .common import PHASE,cfg,sha_file,sha_obj,load

def make_manifest():
    pol=cfg('qualification_freeze_policy.json');rows=[]
    for rel in pol.get('frozen_surfaces',[]):
        p=PHASE/rel
        if not p.exists():raise RuntimeError('R01_FREEZE_SURFACE_MISSING:'+rel)
        rows.append({'path':rel,'sha256':sha_file(p)})
    core={'record_type':'AD_V31_R01_QUALIFICATION_FREEZE','schema_version':'1.0.0','surfaces':rows,'parent_release':'ALPHA_DESK_V3_GOLD_RC1'}
    core['policy_fingerprint']='R01QPOL_'+sha_obj(rows).upper();return core

def verify_manifest(manifest=None):
    m=manifest or load(PHASE/'qualification/QUALIFICATION_FREEZE_MANIFEST.json',{}) or {};bad=[]
    for r in m.get('surfaces',[]):
        p=PHASE/r['path'];got=sha_file(p) if p.exists() else None
        if got!=r['sha256']:bad.append({'path':r['path'],'expected':r['sha256'],'actual':got})
    return {'status':'PASS' if not bad else 'FAIL','policy_fingerprint':m.get('policy_fingerprint'),'drift':bad,'surfaces':m.get('surfaces',[])}
