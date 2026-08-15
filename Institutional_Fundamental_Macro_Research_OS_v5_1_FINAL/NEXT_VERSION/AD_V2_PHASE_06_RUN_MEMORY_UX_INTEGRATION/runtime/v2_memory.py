#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
from contextlib import contextmanager
from datetime import datetime,timezone
import hashlib,json,os,tempfile

PHASE='AD-V2-P06'; VERSION='0.6.0'
FORBIDDEN=('OPENAI_API_KEY','API_KEY','ACCESS_TOKEN','AUTHORIZATION','COOKIE','REFRESH_TOKEN','SECRET_KEY')

def _canon(x): return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def _sha(x): return 'sha256:'+hashlib.sha256(_canon(x).encode()).hexdigest()
def _dt(s):
    if not s: return datetime.min.replace(tzinfo=timezone.utc)
    try:
        d=datetime.fromisoformat(str(s).replace('Z','+00:00')); return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
    except Exception: return datetime.min.replace(tzinfo=timezone.utc)
def _safe(s): return ''.join(c if c.isalnum() or c in '-_.' else '_' for c in str(s or 'UNKNOWN'))
def _root(data_root): p=Path(data_root)/'alpha_desk_v2'; p.mkdir(parents=True,exist_ok=True); return p
@contextmanager
def _lock(p):
    p=Path(p); p.parent.mkdir(parents=True,exist_ok=True); fd=None
    try:
        fd=os.open(str(p),os.O_CREAT|os.O_EXCL|os.O_WRONLY); os.write(fd,b'LOCK\n'); os.close(fd); fd=None; yield
    finally:
        try:
            if fd is not None: os.close(fd)
        except Exception: pass
        try: p.unlink()
        except FileNotFoundError: pass

def _atomic_create(path,obj):
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists(): raise RuntimeError('immutable V2 capsule already exists: '+str(p))
    with _lock(p.parent/'.v2_capsule.lock'):
        if p.exists(): raise RuntimeError('immutable V2 capsule already exists: '+str(p))
        fd,tmp=tempfile.mkstemp(prefix='.'+p.name+'.',suffix='.tmp',dir=str(p.parent)); os.close(fd); t=Path(tmp)
        try:
            data=(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+'\n').encode()
            with t.open('wb') as f: f.write(data); f.flush(); os.fsync(f.fileno())
            os.replace(t,p)
        finally:
            if t.exists(): t.unlink()

def _append(path,obj):
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    with _lock(str(p)+'.lock'):
        with p.open('a',encoding='utf-8',newline='\n') as f: f.write(_canon(obj)+'\n'); f.flush(); os.fsync(f.fileno())

def _secret_scan(obj,path=''):
    bad=[]
    if isinstance(obj,dict):
        for k,v in obj.items():
            kp=(path+'.'+str(k)).strip('.')
            if any(x in str(k).upper() for x in FORBIDDEN): bad.append(kp)
            bad.extend(_secret_scan(v,kp))
    elif isinstance(obj,list):
        for i,v in enumerate(obj): bad.extend(_secret_scan(v,f'{path}[{i}]'))
    return bad

def read_index(data_root):
    p=_root(data_root)/'runs/index.jsonl'; out=[]
    if not p.is_file(): return out
    for line in p.read_text(encoding='utf-8').splitlines():
        if not line.strip(): continue
        try: out.append(json.loads(line))
        except Exception: out.append({'integrity':'INVALID_JSON_LINE'})
    return out

def find_previous(data_root,subject,mode,horizon):
    rows=[r for r in read_index(data_root) if r.get('subject')==subject and r.get('mode')==mode and r.get('horizon')==horizon and r.get('quality_status') in {'PASS','PASS_WITH_WARNINGS','PARTIAL'}]
    rows.sort(key=lambda x:_dt(x.get('as_of')),reverse=True)
    for r in rows:
        p=Path(r.get('path',''))
        if p.is_file():
            try:
                o=json.loads(p.read_text(encoding='utf-8')); return o.get('canonical_v2_state') or o
            except Exception: pass
    return None

def build_extension(state,quality=None):
    if not isinstance(state,dict) or state.get('status')!='PASS' or ((state.get('integrity') or {}).get('status')!='PASS'): raise RuntimeError('valid P06 state required')
    q=quality or {'status':('PASS_WITH_WARNINGS' if (((state.get('science_v2') or {}).get('latent_release') or {}).get('research_blockers')) else 'PASS')}
    ext={'schema_version':'1.0.0','phase':PHASE,'version':VERSION,'deployment':'SHADOW_ONLY','run_id':state.get('run_id'),'subject':state.get('subject'),'as_of':state.get('as_of'),'horizon':state.get('horizon'),'mode':state.get('mode'),'base_run':state.get('base_run'),'upstream_fingerprints':{
      'pressure':hashlib.sha256(_canon(((state.get('science_v2') or {}).get('pressure'))).encode()).hexdigest(),
      'transmission':hashlib.sha256(_canon(((state.get('science_v2') or {}).get('transmission'))).encode()).hexdigest(),
      'latent_release':hashlib.sha256(_canon(((state.get('science_v2') or {}).get('latent_release'))).encode()).hexdigest(),
      'gold_intelligence':hashlib.sha256(_canon(((state.get('science_v2') or {}).get('gold_intelligence'))).encode()).hexdigest()},
      'canonical_v2_state':state,'canonical_v2_state_hash':state.get('canonical_v2_state_hash'),'change_set':state.get('change_set'),'portable_memory':state.get('portable_memory'),'quality_status':q.get('status'),'p06_quality_receipt':q,'authority':state.get('authority'),'created_at_utc':datetime.now(timezone.utc).isoformat().replace('+00:00','Z')}
    ext['capsule_extension_hash']=_sha(ext)
    return ext

def persist(data_root,extension):
    bad=_secret_scan(extension)
    if bad: raise RuntimeError('secret-like fields forbidden: '+','.join(bad[:8]))
    dt=_dt(extension.get('as_of')); yr=f'{dt.year:04d}' if dt.year>1 else 'UNKNOWN'; mo=f'{dt.month:02d}' if dt.year>1 else '00'; root=_root(data_root)
    p=root/'runs'/extension['subject']/yr/mo/_safe(extension['run_id'])/'capsule_extension.json'; _atomic_create(p,extension)
    v=verify(p)
    if v.get('status')!='PASS': raise RuntimeError('post-write V2 capsule verification failed')
    row={'run_id':extension['run_id'],'subject':extension['subject'],'as_of':extension['as_of'],'horizon':extension['horizon'],'mode':extension['mode'],'quality_status':extension['quality_status'],'pressure_class':((((extension.get('canonical_v2_state') or {}).get('science_v2') or {}).get('pressure') or {}).get('pressure_core') or {}).get('class'),'transmission_state':((((extension.get('canonical_v2_state') or {}).get('science_v2') or {}).get('transmission') or {}).get('transmission_state') or {}).get('state'),'release_readiness':((((extension.get('canonical_v2_state') or {}).get('science_v2') or {}).get('latent_release') or {}).get('release_readiness') or {}).get('state'),'release_lifecycle':((((extension.get('canonical_v2_state') or {}).get('science_v2') or {}).get('latent_release') or {}).get('release_lifecycle') or {}).get('state'),'permission':((extension.get('canonical_v2_state') or {}).get('execution') or {}).get('permission'),'capsule_extension_hash':extension['capsule_extension_hash'],'path':str(p),'created_at_utc':extension['created_at_utc']}
    _append(root/'runs/index.jsonl',row); _append(root/'runs/events.jsonl',{'event':'V2_CAPSULE_EXTENSION_SEALED','run_id':extension['run_id'],'capsule_extension_hash':extension['capsule_extension_hash'],'path':str(p),'at':extension['created_at_utc']})
    hp=root/'history'/extension['subject']/(_safe(extension['horizon'])+'.jsonl')
    _append(hp,{**row,'change_set':extension.get('change_set'),'portable_memory':extension.get('portable_memory')})
    return {'status':'PASS','path':str(p),'index':str(root/'runs/index.jsonl'),'events':str(root/'runs/events.jsonl'),'history':str(hp),'capsule_extension_hash':extension['capsule_extension_hash']}

def verify(path):
    p=Path(path)
    try:
        o=json.loads(p.read_text(encoding='utf-8')); h=o.pop('capsule_extension_hash',None); ok=h==_sha(o)
        return {'status':'PASS' if ok else 'FAIL','path':str(p),'capsule_extension_hash':h,'errors':[] if ok else ['CAPSULE_EXTENSION_HASH_MISMATCH']}
    except Exception as e: return {'status':'FAIL','path':str(p),'errors':[str(e)]}

def status(data_root):
    rows=[r for r in read_index(data_root) if r.get('integrity')!='INVALID_JSON_LINE']; last=rows[-1] if rows else None; vr=verify(last['path']) if last else None
    return {'schema_version':'1.0.0','phase':PHASE,'status':'PASS' if vr is None or vr.get('status')=='PASS' else 'FAIL','runs':len(rows),'latest':last,'latest_integrity':vr,'root':str(_root(data_root)),'authority':{'trade_permission':'V1_INHERITED','broker':'NONE','deployment':'SHADOW_ONLY'}}
