from __future__ import annotations
from pathlib import Path
import json, shutil
from .common import PHASE,P02,load,write,digest,digest_bytes,canonical_hash,parse_dt,iso

_EXT={'html':'.html','json':'.json','csv':'.csv','xml':'.xml','txt':'.txt','pdf':'.pdf'}

def _source_fingerprint(source):
    return canonical_hash(source)

def _extractor_fingerprint():
    return digest(P02/'runtime'/'extractors.py')

def _cache_root(cache_root=None):
    return Path(cache_root) if cache_root else PHASE/'artifacts'/'context_cache'

def _entry_path(source_id,cache_root=None): return _cache_root(cache_root)/'index'/(source_id+'.json')
def _body_path(source_id,sha,fmt,cache_root=None): return _cache_root(cache_root)/'bodies'/source_id/(sha+_EXT.get(fmt,'.bin'))

def ttl_seconds(source,policy):
    return int((policy.get('cadence_ttl_seconds') or {}).get(source.get('cadence'),policy.get('default_ttl_seconds',0)))

def inspect_entry(source,as_of_utc,policy,cache_root=None):
    p=_entry_path(source['source_id'],cache_root)
    if not p.exists(): return {'status':'MISS','reason':'NO_ENTRY','entry':None}
    try: e=load(p)
    except Exception as ex: return {'status':'REJECTED','reason':'CORRUPT_INDEX:'+type(ex).__name__,'entry':None}
    body=_cache_root(cache_root)/e.get('body_rel','')
    if not body.exists(): return {'status':'REJECTED','reason':'BODY_MISSING','entry':e}
    try: got=digest(body)
    except Exception: return {'status':'REJECTED','reason':'BODY_UNREADABLE','entry':e}
    if got!=e.get('raw_sha256'): return {'status':'REJECTED','reason':'BODY_HASH_MISMATCH','entry':e}
    if e.get('source_contract_sha256')!=_source_fingerprint(source): return {'status':'REJECTED','reason':'SOURCE_CONTRACT_CHANGED','entry':e}
    if e.get('extractor_sha256')!=_extractor_fingerprint(): return {'status':'REJECTED','reason':'EXTRACTOR_CHANGED','entry':e}
    asof=parse_dt(as_of_utc); acquired=parse_dt(e.get('acquired_at'))
    if not asof or not acquired: return {'status':'REJECTED','reason':'INVALID_CLOCK','entry':e}
    if acquired>asof: return {'status':'REJECTED','reason':'FUTURE_ACQUISITION','entry':e}
    nxt=parse_dt(e.get('next_publication_utc'))
    if policy.get('invalidate_at_next_publication') and nxt and asof>=nxt:
        return {'status':'EXPIRED','reason':'PUBLICATION_WINDOW_PASSED','entry':e}
    for marker in e.get('economic_markers') or []:
        md=parse_dt(marker.get('value'))
        if md and md>asof and policy.get('reject_future_economic_marker',True):
            return {'status':'REJECTED','reason':'FUTURE_ECONOMIC_MARKER','entry':e}
    ttl=ttl_seconds(source,policy)
    if source.get('cadence') in set(policy.get('always_refresh_cadences') or []) or ttl<=0:
        return {'status':'EXPIRED','reason':'ALWAYS_REFRESH_CADENCE','entry':e}
    age=(asof-acquired).total_seconds()
    if age>ttl: return {'status':'EXPIRED','reason':'TTL_EXPIRED','age_seconds':age,'ttl_seconds':ttl,'entry':e}
    return {'status':'HIT','reason':'VALID_CONTEXT_CACHE','age_seconds':age,'ttl_seconds':ttl,'entry':e,'body_path':str(body)}

def store_source(source,attempt,observations,policy,cache_root=None,next_publication_utc=None):
    if not attempt or not attempt.get('ok'): return {'stored':False,'reason':'ATTEMPT_NOT_SUCCESS'}
    # Reusing cache must never reset the original acquisition clock.
    if str(attempt.get('url') or '').startswith('p07-cache://'):
        return {'stored':False,'reason':'CACHE_REUSE_NO_CLOCK_RESET'}
    raw=attempt.get('raw_path')
    if not raw or not Path(raw).exists(): return {'stored':False,'reason':'NO_RAW_BODY'}
    body=Path(raw).read_bytes(); sha=digest_bytes(body)
    dest=_body_path(source['source_id'],sha,source.get('format'),cache_root); dest.parent.mkdir(parents=True,exist_ok=True)
    if not dest.exists(): dest.write_bytes(body)
    markers=[]
    seen=set()
    for o in observations:
        if o.get('source_id')!=source['source_id']: continue
        for kind in ('reference_period','event_time','published_at'):
            v=o.get(kind)
            if v not in (None,'') and (kind,str(v)) not in seen:
                markers.append({'kind':kind,'value':str(v)}); seen.add((kind,str(v)))
    root=_cache_root(cache_root)
    e={
      'record_type':'AD_V3_P07_CONTEXT_CACHE_ENTRY','schema_version':'1.0.0','source_id':source['source_id'],
      'source_contract_sha256':_source_fingerprint(source),'extractor_sha256':_extractor_fingerprint(),
      'raw_sha256':sha,'body_rel':dest.relative_to(root).as_posix(),'format':source.get('format'),
      'cadence':source.get('cadence'),'publication_lag':source.get('publication_lag'),
      'acquired_at':attempt.get('retrieved_at') or iso(),'economic_markers':markers,
      'next_publication_utc':next_publication_utc,'safe_to_delete':True
    }
    write(_entry_path(source['source_id'],cache_root),e)
    return {'stored':True,'entry':e}

def cache_state(source_registry,policy,as_of_utc,cache_root=None):
    rows=[]
    for s in source_registry.get('sources') or []:
        r=inspect_entry(s,as_of_utc,policy,cache_root); rows.append({'source_id':s['source_id'],'status':r['status'],'reason':r.get('reason')})
    from collections import Counter
    return {'counts':dict(Counter(x['status'] for x in rows)),'rows':rows}
