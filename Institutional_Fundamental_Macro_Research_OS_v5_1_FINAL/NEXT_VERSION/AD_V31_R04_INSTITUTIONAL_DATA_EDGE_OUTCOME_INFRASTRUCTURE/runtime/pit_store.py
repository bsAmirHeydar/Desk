from __future__ import annotations
import sqlite3,json
from pathlib import Path
from .common import canonical_hash,iso,parse_dt

SCHEMA_VERSION='1.0.0'
DDL='''
CREATE TABLE IF NOT EXISTS observations(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 series_id TEXT NOT NULL,
 instrument TEXT,
 fact_id TEXT,
 provider_id TEXT NOT NULL,
 economic_time TEXT NOT NULL,
 release_time TEXT,
 market_time TEXT,
 fetch_time TEXT,
 ingest_time TEXT NOT NULL,
 first_seen_time TEXT NOT NULL,
 revision_time TEXT,
 value REAL,
 unit TEXT,
 quality TEXT,
 directness TEXT,
 revision INTEGER NOT NULL DEFAULT 0,
 record_class TEXT NOT NULL,
 raw_reference TEXT,
 metadata_json TEXT NOT NULL,
 record_checksum TEXT NOT NULL,
 UNIQUE(series_id,provider_id,economic_time,revision)
);
CREATE INDEX IF NOT EXISTS ix_obs_series_time ON observations(series_id,economic_time);
CREATE TABLE IF NOT EXISTS metadata(k TEXT PRIMARY KEY,v TEXT NOT NULL);
'''

def _connect(path):
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True);c=sqlite3.connect(p);c.row_factory=sqlite3.Row;c.executescript(DDL);c.execute("INSERT OR REPLACE INTO metadata(k,v) VALUES('schema_version',?)",(SCHEMA_VERSION,));c.commit();return c

def _core(r):
    keys=['series_id','instrument','fact_id','provider_id','economic_time','release_time','market_time','revision_time','value','unit','quality','directness','revision','record_class','raw_reference','metadata']
    return {k:r.get(k) for k in keys}

def put(path,record):
    r=dict(record)
    et=parse_dt(r.get('economic_time') or r.get('market_time'))
    if not et:raise ValueError('PIT_ECONOMIC_TIME_REQUIRED')
    r['economic_time']=iso(et);r.setdefault('market_time',r['economic_time']);r.setdefault('ingest_time',iso());r.setdefault('first_seen_time',r['ingest_time']);r.setdefault('revision',0);r.setdefault('record_class','LIVE_CAPTURED');r.setdefault('metadata',{})
    r['record_checksum']=canonical_hash(_core(r))
    with _connect(path) as c:
        old=c.execute('SELECT * FROM observations WHERE series_id=? AND provider_id=? AND economic_time=? AND revision=?',(r['series_id'],r['provider_id'],r['economic_time'],r['revision'])).fetchone()
        if old:
            if old['record_checksum']!=r['record_checksum']:raise RuntimeError('PIT_IMMUTABLE_RECORD_CONFLICT')
            return dict(old),False
        c.execute('''INSERT INTO observations(series_id,instrument,fact_id,provider_id,economic_time,release_time,market_time,fetch_time,ingest_time,first_seen_time,revision_time,value,unit,quality,directness,revision,record_class,raw_reference,metadata_json,record_checksum) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',(
            r['series_id'],r.get('instrument'),r.get('fact_id'),r['provider_id'],r['economic_time'],r.get('release_time'),r.get('market_time'),r.get('fetch_time'),r['ingest_time'],r['first_seen_time'],r.get('revision_time'),r.get('value'),r.get('unit'),r.get('quality'),r.get('directness'),r['revision'],r['record_class'],r.get('raw_reference'),json.dumps(r.get('metadata') or {},sort_keys=True),r['record_checksum']))
        c.commit(); row=c.execute('SELECT * FROM observations WHERE id=last_insert_rowid()').fetchone();return dict(row),True

def query(path,series_id,start=None,end=None,provider_id=None,record_classes=None):
    if not Path(path).exists():return []
    sql='SELECT * FROM observations WHERE series_id=?';args=[series_id]
    if start:sql+=' AND economic_time>=?';args.append(iso(parse_dt(start)))
    if end:sql+=' AND economic_time<=?';args.append(iso(parse_dt(end)))
    if provider_id:sql+=' AND provider_id=?';args.append(provider_id)
    if record_classes:
        sql+=' AND record_class IN ('+','.join('?' for _ in record_classes)+')';args+=list(record_classes)
    sql+=' ORDER BY economic_time ASC, provider_id ASC, revision ASC'
    with _connect(path) as c:
        rows=[dict(r) for r in c.execute(sql,args).fetchall()]
    for r in rows:r['metadata']=json.loads(r.pop('metadata_json') or '{}')
    return rows

def verify(path):
    if not Path(path).exists():return {'status':'PASS','records':0,'schema_version':SCHEMA_VERSION}
    bad=[];total=0
    with _connect(path) as c:
        for row in c.execute('SELECT * FROM observations'):
            total+=1;r=dict(row);r['metadata']=json.loads(r.pop('metadata_json') or '{}')
            chk=r.pop('record_checksum');r.pop('id',None)
            if canonical_hash(_core(r))!=chk:bad.append({'series_id':r['series_id'],'economic_time':r['economic_time'],'provider_id':r['provider_id']})
    return {'status':'FAIL' if bad else 'PASS','records':total,'integrity_failures':bad,'schema_version':SCHEMA_VERSION}

def nearest(path,series_id,target,tolerance_seconds,providers=None):
    t=parse_dt(target); start=iso(tolerance_dt(t,-tolerance_seconds));end=iso(tolerance_dt(t,tolerance_seconds))
    rows=query(path,series_id,start,end)
    if providers:rows=[r for r in rows if r['provider_id'] in providers]
    if not rows:return None
    # deterministic: nearest absolute time; tie -> earlier; then provider id
    rows.sort(key=lambda r:(abs((parse_dt(r['economic_time'])-t).total_seconds()),0 if parse_dt(r['economic_time'])<=t else 1,r['economic_time'],r['provider_id']))
    return rows[0]

def tolerance_dt(dt,seconds):
    from datetime import timedelta
    return dt+timedelta(seconds=seconds)
