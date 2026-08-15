#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
from contextlib import contextmanager
import json,hashlib,os,tempfile

def canon(x): return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,default=str)
def hsh(x): return 'sha256:'+hashlib.sha256(canon(x).encode()).hexdigest()
def root(data_root):
    p=Path(data_root)/'alpha_desk_v2/p08_operations';p.mkdir(parents=True,exist_ok=True);return p
@contextmanager
def lock(path):
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True);fd=None
    try:
        fd=os.open(str(p),os.O_CREAT|os.O_EXCL|os.O_WRONLY);os.write(fd,b'LOCK\n');os.close(fd);fd=None;yield
    finally:
        try:
            if fd is not None:os.close(fd)
        except:pass
        try:p.unlink()
        except FileNotFoundError:pass

def atomic_create(path,obj):
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():raise RuntimeError('immutable record exists: '+str(p))
    with lock(str(p)+'.lock'):
        if p.exists():raise RuntimeError('immutable record exists: '+str(p))
        fd,tmp=tempfile.mkstemp(prefix='.'+p.name+'.',suffix='.tmp',dir=str(p.parent));os.close(fd);t=Path(tmp)
        try:
            with t.open('w',encoding='utf-8',newline='\n') as f:json.dump(obj,f,ensure_ascii=False,indent=2,sort_keys=True);f.write('\n');f.flush();os.fsync(f.fileno())
            os.replace(t,p)
        finally:
            try:t.unlink()
            except FileNotFoundError:pass

def append(path,obj):
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
    with lock(str(p)+'.lock'):
        with p.open('a',encoding='utf-8',newline='\n') as f:f.write(canon(obj)+'\n');f.flush();os.fsync(f.fileno())

def read_jsonl(path):
    p=Path(path);out=[]
    if not p.is_file():return out
    for line in p.read_text(encoding='utf-8').splitlines():
        if not line.strip():continue
        try:out.append(json.loads(line))
        except:out.append({'integrity':'INVALID_JSON_LINE','raw':line[:120]})
    return out

def event(data_root,event_name,payload):append(root(data_root)/'events.jsonl',{'event':event_name,**payload})

def seal_cycle(data_root,receipt):
    rid=receipt['cycle_id'];p=root(data_root)/'cycles'/rid/'cycle_receipt.json';atomic_create(p,receipt);append(root(data_root)/'cycles/index.jsonl',{'cycle_id':rid,'started_at_utc':receipt.get('started_at_utc'),'finished_at_utc':receipt.get('finished_at_utc'),'status':receipt.get('status'),'path':str(p),'cycle_hash':receipt.get('cycle_hash')});return p
