from __future__ import annotations
from .common import state_dir,atomic_json,load,iso,PHASE,sha_obj
from .qualification_freeze import verify_manifest

def path(root=None):return state_dir(root)/'qualification_cohort.json'
def load_cohort(root=None):return load(path(root),None)
def initialize(p09_status,root=None,now=None,baseline_commit=None):
    old=load_cohort(root);fr=verify_manifest();fp=fr.get('policy_fingerprint')
    active=(p09_status or {}).get('active_cohort') or {};p09fp=(p09_status or {}).get('current_fingerprint')
    if old and old.get('state')=='OPEN' and old.get('policy_fingerprint')==fp and old.get('p09_fingerprint')==p09fp:return old
    if old and old.get('state')=='OPEN':
        old=dict(old);old['state']='SUPERSEDED';old['closed_at_utc']=iso(now);atomic_json(path(root).with_name('qualification_cohort_superseded.json'),old)
    obj={'record_type':'AD_V31_R01_QUALIFICATION_COHORT','schema_version':'1.0.0','qualification_cohort_id':'R01Q_'+sha_obj({'t':iso(now),'p':fp,'p09':p09fp})[:20].upper(),'state':'OPEN','started_at_utc':iso(now),'policy_fingerprint':fp,'p09_cohort_id':active.get('cohort_id'),'p09_fingerprint':p09fp,'baseline_commit':baseline_commit,'pre_r01_episodes_primary_qualification_authority':False,'existing_p09_history_preserved':True}
    atomic_json(path(root),obj);return obj
