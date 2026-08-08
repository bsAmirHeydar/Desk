#!/usr/bin/env python3
import argparse,json,datetime,sys
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('--state',required=True); a=p.parse_args(); x=json.loads(Path(a.state).read_text(encoding='utf-8')); errors=[]
U=['XAUUSD','NASDAQ100','SP500','DJIA','EURUSD','USDJPY']; enums={
'fundamental_force_state':{'ACTIVE','PARTIAL','WEAK','FRAGMENTED','UNDETERMINED'},'narrative_clearance':{'ALIGNED_DOMINANT','ALIGNED_EMERGING','NEUTRAL','CONFLICTED','OPPOSING','UNDETERMINED'},'evidence_clearance':{'CLEAR','CLEAR_WITH_CONFIDENCE_CAP','HOLD','BLOCK'},'timing_clearance':{'CLEAR','CLEAR_WITH_CONSTRAINTS','HOLD','VETO','UNDETERMINED_MATERIAL','CLOSED'},'research_edge':{'EDGE_ACTIVE','EDGE_CONDITIONAL','EDGE_RELATIVE','BIAS_ONLY','NO_EDGE','EVENT_OR_FRAGMENTED','INSUFFICIENT_EVIDENCE'},'permission':{'BUY','SELL','NO_TRADE'}}
def isdt(v):
    try: datetime.datetime.fromisoformat(str(v).replace('Z','+00:00')); return True
    except: return False
if not isdt(x.get('generated_at_utc')): errors.append('generated_at_utc invalid')
mk=x.get('markets',{});
if list(mk.keys())!=U and set(mk.keys())!=set(U): errors.append('market universe mismatch')
for s in U:
    m=mk.get(s)
    if not isinstance(m,dict): errors.append(s+' missing'); continue
    for k,vals in enums.items():
        if m.get(k) not in vals: errors.append(f'{s}.{k} invalid')
    for k in ['valid_until_utc','next_review_utc']:
        if not isdt(m.get(k)): errors.append(f'{s}.{k} invalid datetime')
    if m.get('research_edge')=='EDGE_ACTIVE':
        if m.get('fundamental_force_state')!='ACTIVE': errors.append(s+' active edge without active fundamental force')
        if m.get('narrative_clearance') not in {'ALIGNED_DOMINANT','ALIGNED_EMERGING'}: errors.append(s+' active edge without narrative alignment')
        if m.get('timing_clearance') not in {'CLEAR','CLEAR_WITH_CONSTRAINTS'}: errors.append(s+' active edge without timing clearance')
print(json.dumps({'status':'PASS' if not errors else 'FAIL','errors':errors},indent=2)); sys.exit(0 if not errors else 2)
