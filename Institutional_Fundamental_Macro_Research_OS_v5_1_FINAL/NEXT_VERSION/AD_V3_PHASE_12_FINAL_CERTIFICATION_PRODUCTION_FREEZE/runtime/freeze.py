from __future__ import annotations
from pathlib import Path
from .common import PHASE,REPO,load,sha_file,sha_obj

def expand_policy(repo=REPO):
 pol=load(PHASE/'config/final_freeze_policy.json',{});classes={}
 for cls,patterns in (pol.get('immutable_classes') or {}).items():
  rows=[];seen=set()
  for pat in patterns:
   for f in sorted(Path(repo).glob(pat)):
    if f.is_file() and f not in seen:
     seen.add(f);rows.append({'path':f.relative_to(repo).as_posix(),'sha256':sha_file(f)})
  classes[cls]=rows
 return classes

def make_manifest(repo=REPO):
 classes=expand_policy(repo);core={'record_type':'AD_V3_P12_FINAL_FREEZE_MANIFEST','schema_version':'1.0.0','classes':classes,'mutable_exclusions':load(PHASE/'config/final_freeze_policy.json',{}).get('mutable_classes',{})};core['release_fingerprint']='V3REL_'+sha_obj(classes).upper();return core

def verify_manifest(repo=REPO,manifest=None):
 m=manifest or load(PHASE/'release/FINAL_FREEZE_MANIFEST.json',{});by_class={};drift=[]
 for cls,rows in (m.get('classes') or {}).items():
  bad=[]
  for r in rows:
   p=Path(repo)/r['path'];got=sha_file(p) if p.exists() else None
   if got!=r['sha256']:bad.append({'path':r['path'],'expected':r['sha256'],'actual':got})
  by_class[cls]={'status':'PASS' if not bad else 'FAIL','drift':bad};drift+=bad
 return {'status':'PASS' if not drift else 'FAIL','classes':by_class,'drift':drift,'release_fingerprint':m.get('release_fingerprint')}
