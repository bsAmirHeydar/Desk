#!/usr/bin/env python3
from __future__ import annotations
from datetime import datetime,timezone
from pathlib import Path
import hashlib,json
from .store import root,atomic_create,append,read_jsonl,canon,hsh
class ProfileError(ValueError):pass

def dt(s):
    d=datetime.fromisoformat(str(s).replace('Z','+00:00'));return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
def validate(p):
    if not isinstance(p,dict) or p.get('record_type')!='P08_EVALUATION_PROFILE':raise ProfileError('P08_EVALUATION_PROFILE required')
    if p.get('subject')!='XAUUSD':raise ProfileError('profile subject must be XAUUSD')
    if not p.get('profile_id') or not p.get('horizon'):raise ProfileError('profile_id and horizon required')
    for k in ['maturity_seconds','reference_capture_seconds','max_observation_gap_seconds']:
        try:v=int(p.get(k))
        except:raise ProfileError(k+' must be integer')
        if v<=0:raise ProfileError(k+' must be positive')
    try:r=float(p.get('one_r_price_distance'))
    except:raise ProfileError('one_r_price_distance required')
    if r<=0:raise ProfileError('one_r_price_distance must be positive')
    if not p.get('sealed_at_utc'):raise ProfileError('sealed_at_utc required')
    if p.get('profile_kind') not in {'COUNTERFACTUAL_RESEARCH','REALIZED_EXECUTION'}:raise ProfileError('profile_kind invalid')
    out=dict(p);out['one_r_price_distance']=r;x=dict(out);x.pop('profile_hash',None);out['profile_hash']=hsh(x);return out

def register(data_root,p):
    x=validate(p);rt=root(data_root);path=rt/'profiles'/x['profile_id']/ 'profile.json'
    if path.exists():
        old=json.loads(path.read_text(encoding='utf-8'))
        if old.get('profile_hash')==x.get('profile_hash'):return {'status':'PASS','mode':'ALREADY_PRESENT_IDENTICAL','path':str(path),'profile_hash':x['profile_hash']}
        raise ProfileError('profile_id already exists with different content')
    atomic_create(path,x);append(rt/'profiles/index.jsonl',{'profile_id':x['profile_id'],'subject':x['subject'],'horizon':x['horizon'],'sealed_at_utc':x['sealed_at_utc'],'active_from_utc':x.get('active_from_utc') or x['sealed_at_utc'],'path':str(path),'profile_hash':x['profile_hash']});return {'status':'PASS','mode':'CREATED','path':str(path),'profile_hash':x['profile_hash']}

def active_for(data_root,horizon,commitment_sealed_at):
    rows=read_jsonl(root(data_root)/'profiles/index.jsonl');candidates=[];ct=dt(commitment_sealed_at)
    for r in rows:
        if r.get('subject')!='XAUUSD' or r.get('horizon')!=horizon:continue
        p=Path(r.get('path',''))
        if not p.is_file():continue
        try:o=json.loads(p.read_text(encoding='utf-8'));o=validate(o)
        except:continue
        if dt(o['sealed_at_utc'])>ct:continue
        af=dt(o.get('active_from_utc') or o['sealed_at_utc'])
        if af>ct:continue
        candidates.append(o)
    candidates.sort(key=lambda x:dt(x['sealed_at_utc']),reverse=True)
    return candidates[0] if candidates else None
