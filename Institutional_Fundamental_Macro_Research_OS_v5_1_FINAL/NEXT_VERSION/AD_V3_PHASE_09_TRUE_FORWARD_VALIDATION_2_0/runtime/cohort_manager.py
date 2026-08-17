from __future__ import annotations
from pathlib import Path
from .common import PHASE,NEXT,cfg,sha_file,canonical_hash,stable_id,iso

def bound_hashes():
    pol=cfg('cohort_policy.json'); out={}
    for rel in pol['bound_surfaces']:
        p=(PHASE/'config'/rel).resolve() if not rel.startswith('../') and '/' not in rel else (PHASE/rel).resolve()
        # config filenames without slash live in P09 config
        if not rel.startswith('../') and '/' not in rel:p=PHASE/'config'/rel
        if not p.exists():raise RuntimeError('COHORT_BOUND_SURFACE_MISSING:'+str(p))
        out[str(rel)]=sha_file(p)
    return out

def current_fingerprint():return canonical_hash(bound_hashes())
def ensure_cohort(state,now=None):
    fp=current_fingerprint(); active=next((x for x in reversed(state['cohorts']) if x.get('state')=='OPEN'),None)
    if active and active.get('fingerprint')==fp:return state,active,False
    if active:
        active['state']='SUPERSEDED';active['closed_at_utc']=iso(now);active['close_reason']='BOUND_POLICY_FINGERPRINT_CHANGED'
    seq=max([int(x.get('sequence',0)) for x in state['cohorts']] or [0])+1
    obj={'record_type':'AD_V3_P09_FORWARD_COHORT','sequence':seq,'cohort_id':f'COHORT_{seq:03d}','state':'OPEN','opened_at_utc':iso(now),'fingerprint':fp,'bound_hashes':bound_hashes(),'prospective_only':True,'replay_counts_as_prospective':False,'fixture_samples_count_as_prospective':False}
    state['cohorts'].append(obj);return state,obj,True
