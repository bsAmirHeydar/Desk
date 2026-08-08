#!/usr/bin/env python3
from pathlib import Path
import argparse,json,datetime
p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--output');a=p.parse_args();x=json.loads(Path(a.input).read_text(encoding='utf-8'));tr=x.get('candidate_triggers') or []
def parse(s):
 try:return datetime.datetime.fromisoformat((s or '').replace('Z','+00:00')) if s else None
 except:return None
cut=parse(x.get('analysis_cutoff_utc')) or datetime.datetime.now(datetime.timezone.utc)
rank={'DECISION_CRITICAL':0,'MATERIAL':1,'SUPPORTING':2,'CONTEXTUAL':3};haz={'VERY_HIGH':0,'HIGH':1,'MODERATE':2,'LOW':3,'UNDETERMINED':4,None:4}
future=[];conditional=[];ignored=[]
for t in tr:
 dt=parse(t.get('time_utc'));key=(rank.get(t.get('materiality'),9),haz.get(t.get('state_change_hazard'),4))
 if dt is not None:
  if dt>cut:future.append((dt,key,t))
  else:ignored.append(t)
 else:conditional.append((key,t))
if future:
 # earliest material event; hazard resolves ties/near-equal scheduling without fabricating probabilities
 chosen=sorted(future,key=lambda z:(z[0],z[1]))[0][2]
elif conditional:chosen=sorted(conditional,key=lambda z:z[0])[0][1]
else:chosen={'trigger_type':'STATE_REVIEW','condition':'NEXT_DECISION_MATERIAL_CAUSAL_TRIGGER','time_utc':None,'materiality':'MATERIAL','state_change_hazard':'UNDETERMINED'}
out={'analysis_cutoff_utc':cut.isoformat().replace('+00:00','Z'),'next_review_trigger':chosen,'ignored_past_trigger_count':len(ignored),'fixed_interval_fallback_used':not bool(tr)};s=json.dumps(out,indent=2);print(s)
if a.output:Path(a.output).write_text(s+'\n',encoding='utf-8')
