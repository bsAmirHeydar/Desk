#!/usr/bin/env python3
import argparse,json,datetime,hashlib,sys
from pathlib import Path
p=argparse.ArgumentParser(); sub=p.add_subparsers(dest='cmd',required=True)
q=sub.add_parser('prepare'); q.add_argument('--input',required=True); q.add_argument('--output',required=True)
q=sub.add_parser('validate'); q.add_argument('--pack',required=True); q.add_argument('--now-utc')
q=sub.add_parser('release'); q.add_argument('--pack',required=True); q.add_argument('--release-input',required=True); q.add_argument('--output',required=True)
a=p.parse_args()
def dt(x): return datetime.datetime.fromisoformat(str(x).replace('Z','+00:00'))
def digest(o):
    z=dict(o); z.pop('pack_sha256',None); return hashlib.sha256(json.dumps(z,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def env_digest(o):
    z=dict(o); z.pop('release_artifact_sha256',None); return hashlib.sha256(json.dumps(z,sort_keys=True,separators=(',',':')).encode()).hexdigest()
if a.cmd=='prepare':
    x=json.loads(Path(a.input).read_text(encoding='utf-8')); req=['event_id','event_time_utc','prepared_at_utc','consensus_vintage_utc','scenario_tree','surprise_dimensions','causal_leaders','required_cross_assets','invalidations','source_ids']
    miss=[k for k in req if k not in x]
    if miss: print(json.dumps({'status':'FAIL','missing':miss})); sys.exit(2)
    if dt(x['prepared_at_utc'])>=dt(x['event_time_utc']) or dt(x['consensus_vintage_utc'])>dt(x['prepared_at_utc']): print(json.dumps({'status':'FAIL','error':'invalid temporal ordering'})); sys.exit(2)
    x['pack_sha256']=digest(x); Path(a.output).write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8'); print(x['pack_sha256'])
elif a.cmd=='validate':
    x=json.loads(Path(a.pack).read_text(encoding='utf-8')); now=dt(a.now_utc) if a.now_utc else datetime.datetime.now(datetime.timezone.utc); errors=[]
    if x.get('pack_sha256')!=digest(x): errors.append('PACK_HASH_MISMATCH')
    try:
        if dt(x['prepared_at_utc'])>=dt(x['event_time_utc']): errors.append('PREPARED_AFTER_EVENT')
        if x.get('max_pack_age_seconds') is not None and (dt(x['event_time_utc'])-dt(x['prepared_at_utc'])).total_seconds()>float(x['max_pack_age_seconds']): errors.append('PACK_TOO_OLD_FOR_POLICY')
    except: errors.append('TIME_PARSE_ERROR')
    phase='PRE_EVENT' if now<dt(x['event_time_utc']) else 'RELEASE_OR_POST_EVENT'
    print(json.dumps({'status':'PASS' if not errors else 'UNDETERMINED','errors':errors,'phase':phase,'now_utc':now.isoformat()},indent=2)); sys.exit(0 if not errors else 2)
else:
    x=json.loads(Path(a.pack).read_text(encoding='utf-8')); u=json.loads(Path(a.release_input).read_text(encoding='utf-8'))
    if x.get('pack_sha256')!=digest(x): print('pack hash mismatch'); sys.exit(2)
    if u.get('revision_state') not in {'FIRST_RELEASE','OFFICIAL_FIRST_RELEASE'}: print('release update must be first release'); sys.exit(2)
    env={'event_id':x['event_id'],'pre_event_pack_sha256':x['pack_sha256'],'pre_event_pack_path':str(Path(a.pack)),'release_update':u}
    env['release_artifact_sha256']=env_digest(env)
    Path(a.output).write_text(json.dumps(env,indent=2)+'\n',encoding='utf-8'); print(env['release_artifact_sha256'])
