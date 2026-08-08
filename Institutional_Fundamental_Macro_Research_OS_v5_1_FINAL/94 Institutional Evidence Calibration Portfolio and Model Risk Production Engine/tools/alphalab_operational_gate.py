#!/usr/bin/env python3
import argparse,json,datetime
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('--state',required=True); p.add_argument('--policy',required=True); p.add_argument('--output',required=True); a=p.parse_args()
s=json.loads(Path(a.state).read_text(encoding='utf-8')); pol=json.loads(Path(a.policy).read_text(encoding='utf-8')); reasons=[]
now=datetime.datetime.now(datetime.timezone.utc)
def dt(x): return datetime.datetime.fromisoformat(x.replace('Z','+00:00'))
if not s.get('symbol_mapping_valid',False): reasons.append('SYMBOL_MAPPING_INVALID')
if not s.get('market_state_known',False): reasons.append('MARKET_STATE_UNKNOWN')
if s.get('permission_valid_until_utc'):
 try:
  if dt(s['permission_valid_until_utc'])<=now: reasons.append('PERMISSION_EXPIRED')
 except: reasons.append('PERMISSION_EXPIRY_MALFORMED')
else: reasons.append('PERMISSION_EXPIRY_MISSING')
if abs(float(s.get('clock_drift_seconds',0)))>float(pol['permission_max_clock_drift_seconds']): reasons.append('CLOCK_DRIFT')
for x in s.get('hard_incidents',[]): reasons.append(str(x))
out={'generated_at_utc':now.isoformat(),'status':'BLOCK_NEW_ENTRY' if reasons else 'CLEAR','hard_block':bool(reasons),'reasons':reasons}
Path(a.output).write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8'); print(json.dumps(out))
