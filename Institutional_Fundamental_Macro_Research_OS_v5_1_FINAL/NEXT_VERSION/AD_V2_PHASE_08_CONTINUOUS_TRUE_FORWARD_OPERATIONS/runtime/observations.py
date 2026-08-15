#!/usr/bin/env python3
from __future__ import annotations
from datetime import datetime,timezone
from pathlib import Path
import hashlib,json
from .store import root,append,read_jsonl,canon,hsh
class ObservationError(ValueError):pass

def dt(s):
    d=datetime.fromisoformat(str(s).replace('Z','+00:00'));return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
def _id(o):
    seed={k:o.get(k) for k in ['subject','observed_at_utc','source_id','provider_id','price','provenance_ref']};return 'GOBS_'+hashlib.sha256(canon(seed).encode()).hexdigest()[:24].upper()
def validate(o,policy,now_utc=None):
    if not isinstance(o,dict) or o.get('record_type')!='GOLD_MARKET_OBSERVATION':raise ObservationError('GOLD_MARKET_OBSERVATION required')
    if o.get('subject')!='XAUUSD':raise ObservationError('P08 observations currently certify XAUUSD only')
    if not o.get('source_id') or not o.get('provenance_ref'):raise ObservationError('source_id and provenance_ref required')
    if o.get('quality_status') not in set(policy['allowed_quality']):raise ObservationError('invalid quality_status')
    try:price=float(o.get('price'))
    except:raise ObservationError('numeric price required')
    if price<=0:raise ObservationError('positive price required')
    when=dt(o.get('observed_at_utc'));now=dt(now_utc) if now_utc else datetime.now(timezone.utc)
    if (when-now).total_seconds()>policy['max_future_clock_skew_seconds']:raise ObservationError('future observation beyond clock-skew tolerance')
    out=dict(o);out['price']=price;out['observation_id']=out.get('observation_id') or _id(out);x=dict(out);x.pop('observation_hash',None);out['observation_hash']=hsh(x);return out

def ingest(data_root,observations,policy,now_utc=None):
    p=root(data_root)/'observations/XAUUSD.jsonl';existing=read_jsonl(p);by_key={(x.get('source_id'),x.get('observed_at_utc')):x for x in existing if x.get('source_id') and x.get('observed_at_utc')};added=0;dupe=0
    for raw in observations:
        o=validate(raw,policy,now_utc=now_utc);k=(o['source_id'],o['observed_at_utc'])
        if k in by_key:
            if by_key[k].get('observation_hash')==o.get('observation_hash'):dupe+=1;continue
            raise ObservationError('conflicting observation for source/timestamp: '+str(k))
        append(p,o);by_key[k]=o;added+=1
    return {'status':'PASS','added':added,'identical_duplicates':dupe,'path':str(p)}

def load(data_root,start_utc=None,end_utc=None):
    rows=[x for x in read_jsonl(root(data_root)/'observations/XAUUSD.jsonl') if x.get('record_type')=='GOLD_MARKET_OBSERVATION']
    if start_utc:rows=[x for x in rows if dt(x['observed_at_utc'])>=dt(start_utc)]
    if end_utc:rows=[x for x in rows if dt(x['observed_at_utc'])<=dt(end_utc)]
    return sorted(rows,key=lambda x:dt(x['observed_at_utc']))
