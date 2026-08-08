#!/usr/bin/env python3
import argparse,json,datetime,math
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('--state',required=True); p.add_argument('--policy',required=True); p.add_argument('--output',required=True); a=p.parse_args()
s=json.loads(Path(a.state).read_text(encoding='utf-8')); pol=json.loads(Path(a.policy).read_text(encoding='utf-8')); reasons=[]; info=[]; now=datetime.datetime.now(datetime.timezone.utc)
def dt(x): return datetime.datetime.fromisoformat(str(x).replace('Z','+00:00'))
def req(name):
    if name not in s or s[name] is None: reasons.append('MISSING_'+name.upper()); return False
    return True
stage=s.get('stage','PERMISSION_INGEST'); permission=s.get('permission')
if stage not in {'PERMISSION_INGEST','ENTRY_TRIGGER'}: reasons.append('INVALID_STAGE')
if permission not in {'BUY','SELL','NO_TRADE'}: reasons.append('PERMISSION_INVALID')
# A valid NO_TRADE requests no new exposure. Do not manufacture operational alarms that cannot increase risk.
entry_requested=permission in {'BUY','SELL'}
if entry_requested:
    for f in pol.get('required_ingest_fields',[]): req(f)
    if s.get('symbol_mapping_valid') is not True: reasons.append('SYMBOL_MAPPING_INVALID')
    if s.get('market_state_known') is not True: reasons.append('MARKET_STATE_UNKNOWN')
    if s.get('market_open') is not True: reasons.append('MARKET_CLOSED')
    if s.get('state_checksum_valid') is not True: reasons.append('STATE_CHECKSUM_INVALID')
    if 'clock_drift_seconds' in s and s.get('clock_drift_seconds') is not None:
        try:
            if abs(float(s['clock_drift_seconds']))>float(pol['permission_max_clock_drift_seconds']): reasons.append('CLOCK_DRIFT')
        except: reasons.append('CLOCK_DRIFT_MALFORMED')
    if s.get('permission_valid_until_utc'):
        try:
            if dt(s['permission_valid_until_utc'])<=now: reasons.append('PERMISSION_EXPIRED')
        except: reasons.append('PERMISSION_EXPIRY_MALFORMED')
    for x in s.get('hard_incidents',[]): reasons.append('INCIDENT_'+str(x))
    if stage=='ENTRY_TRIGGER':
        for f in pol.get('required_entry_fields',[]): req(f)
        if s.get('feed_connected') is not True: reasons.append('FEED_DISCONNECTED')
        if s.get('quote_timestamp_utc'):
            try:
                age=(now-dt(s['quote_timestamp_utc'])).total_seconds()
                if age< -2: reasons.append('QUOTE_TIMESTAMP_FUTURE')
                if age>float(pol['entry_quote_max_age_seconds']): reasons.append('QUOTE_STALE')
            except: reasons.append('QUOTE_TIMESTAMP_MALFORMED')
        for name in ['price','atr']:
            if name in s and s.get(name) is not None:
                try:
                    v=float(s[name])
                    if not math.isfinite(v) or v<=0: reasons.append(name.upper()+'_INVALID')
                except: reasons.append(name.upper()+'_INVALID')
        if s.get('spread_hard_limit_breached') is not False: reasons.append('SPREAD_LIMIT_OR_UNKNOWN')
        if s.get('duplicate_order_detected') is not False: reasons.append('DUPLICATE_ORDER_OR_UNKNOWN')
        if s.get('position_sync_valid') is not True: reasons.append('POSITION_SYNC_INVALID')
else:
    info.append('NO_ENTRY_REQUESTED')
seen=set(); reasons=[x for x in reasons if not (x in seen or seen.add(x))]
out={'generated_at_utc':now.isoformat(),'stage':stage,'entry_requested':entry_requested,'status':'BLOCK_NEW_ENTRY' if reasons else 'CLEAR','hard_block':bool(reasons),'reasons':reasons,'info':info}
Path(a.output).write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8'); print(json.dumps(out))
