#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
from contextlib import contextmanager
import json,os,hashlib
PHASE='AD-V2-P07'
def _canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,default=str)
def _root(data_root):p=Path(data_root)/'alpha_desk_v2/p07_validation';p.mkdir(parents=True,exist_ok=True);return p
@contextmanager
def _lock(p):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);fd=None
    try:
        fd=os.open(str(p),os.O_CREAT|os.O_EXCL|os.O_WRONLY);os.close(fd);fd=None;yield
    finally:
        try:p.unlink()
        except FileNotFoundError:pass
def _append(p,obj):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    with _lock(str(p)+'.lock'):
        with p.open('a',encoding='utf-8',newline='\n') as f:f.write(_canon(obj)+'\n');f.flush();os.fsync(f.fileno())
def _create(p,obj):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():raise RuntimeError('immutable record already exists: '+str(p))
    with _lock(str(p)+'.lock'):
        if p.exists():raise RuntimeError('immutable record already exists: '+str(p))
        tmp=p.with_suffix(p.suffix+'.tmp');tmp.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');os.replace(tmp,p)
def persist_commitment(data_root,c):
    r=_root(data_root);p=r/'commitments'/c['commitment_id']/ 'commitment.json';_create(p,c);_append(r/'commitments/index.jsonl',{'commitment_id':c['commitment_id'],'run_id':c['run_id'],'sample_provenance':c['sample_provenance'],'true_forward_eligible':c['true_forward_eligible'],'independent_episode_key':c['independent_episode_key'],'trading_day':c['trading_day'],'regime':c.get('regime'),'path':str(p),'commitment_hash':c['commitment_hash']});return {'status':'PASS','path':str(p)}
def persist_outcome_link(data_root,o):
    r=_root(data_root);p=r/'outcomes'/o['outcome_link_id']/ 'outcome_link.json';_create(p,o);_append(r/'outcomes/index.jsonl',{'outcome_link_id':o['outcome_link_id'],'commitment_id':o['commitment_id'],'run_id':o['run_id'],'sample_provenance':o['sample_provenance'],'maturity_state':o['maturity_state'],'independent_episode_key':o['independent_episode_key'],'trading_day':o['trading_day'],'regime':o.get('regime'),'path':str(p),'outcome_link_hash':o['outcome_link_hash']});return {'status':'PASS','path':str(p)}
def read_jsonl(p):
    p=Path(p);out=[]
    if not p.is_file():return out
    for line in p.read_text(encoding='utf-8').splitlines():
        try:out.append(json.loads(line))
        except:pass
    return out
def load_links(data_root):
    r=_root(data_root);rows=[]
    for x in read_jsonl(r/'outcomes/index.jsonl'):
        p=Path(x.get('path',''))
        if p.is_file():
            try:rows.append(json.loads(p.read_text(encoding='utf-8')))
            except:pass
    return rows
def status(data_root):
    r=_root(data_root);c=read_jsonl(r/'commitments/index.jsonl');o=read_jsonl(r/'outcomes/index.jsonl');tf=[x for x in c if x.get('sample_provenance')=='TRUE_FORWARD' and x.get('true_forward_eligible')];m=[x for x in o if x.get('sample_provenance')=='TRUE_FORWARD' and x.get('maturity_state')=='MATURE'];linked=set(x.get('commitment_id') for x in o);pending=[x for x in tf if x.get('commitment_id') not in linked];return {'schema_version':'1.0.0','phase':PHASE,'status':'PASS','commitments_total':len(c),'true_forward_commitments':len(tf),'outcome_links_total':len(o),'mature_true_forward':len(m),'mature_true_forward_independent_episodes':len(set(x.get('independent_episode_key') for x in m if x.get('independent_episode_key'))),'mature_true_forward_trading_days':len(set(x.get('trading_day') for x in m if x.get('trading_day'))),'pending_true_forward':len(pending),'deployment':'SHADOW_ONLY','authority':{'trade_permission':'V1_INHERITED','broker':'NONE'}}
