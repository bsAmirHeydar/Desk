#!/usr/bin/env python3
from pathlib import Path
import argparse,json,datetime,sys
p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--output');a=p.parse_args();x=json.loads(Path(a.input).read_text(encoding='utf-8'));tr=x.get('candidate_triggers') or []
def parse(s):
    if not s:return None
    try:return datetime.datetime.fromisoformat(s.replace('Z','+00:00'))
    except:return None
rank={'DECISION_CRITICAL':0,'MATERIAL':1,'SUPPORTING':2,'CONTEXTUAL':3}
valid=[]
for t in tr:
    dt=parse(t.get('time_utc'));valid.append((rank.get(t.get('materiality'),9),dt,t))
# Earliest timed decision-material trigger wins; if none, highest-material condition.
timed=[z for z in valid if z[1] is not None and z[0]<=1]
if timed:chosen=sorted(timed,key=lambda z:(z[1],z[0]))[0][2]
elif valid:chosen=sorted(valid,key=lambda z:z[0])[0][2]
else:chosen={'trigger_type':'STATE_REVIEW','condition':'NEXT_DECISION_MATERIAL_CAUSAL_TRIGGER','time_utc':None,'materiality':'MATERIAL'}
out={'next_review_trigger':chosen,'fixed_interval_fallback_used':False if tr else True}
s=json.dumps(out,indent=2);print(s)
if a.output:Path(a.output).write_text(s+'\n',encoding='utf-8')
