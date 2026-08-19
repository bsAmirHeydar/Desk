from __future__ import annotations
from .common import PHASE,load_json,parse_dt,iso
from .pit_store import query

def recover_from_store(store_path,series_id,start,end):
    rows=query(store_path,series_id,start,end,record_classes=['LIVE_CAPTURED','HISTORICAL_REFERENCE','BACKFILLED_REFERENCE'])
    return [normalize_row(r) for r in rows]

def normalize_row(r):
    return {'record_type':'AD_V31_R04_HISTORICAL_MARKET_OBSERVATION','observed_at_utc':r['economic_time'],'value':float(r['value']),'provider_id':r['provider_id'],'scientific_series_id':r['series_id'],'instrument_key':r.get('instrument'),'fact_id':r.get('fact_id'),'record_class':r.get('record_class'),'outcome_acquisition_mode':'HISTORICALLY_RECOVERED','quality':r.get('quality'),'directness':r.get('directness'),'record_checksum':r.get('record_checksum'),'metadata':r.get('metadata') or {}}
