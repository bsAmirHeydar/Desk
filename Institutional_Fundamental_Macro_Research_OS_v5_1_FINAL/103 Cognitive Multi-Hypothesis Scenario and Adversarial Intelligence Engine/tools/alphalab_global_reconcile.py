#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys
p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--output');a=p.parse_args();x=json.loads(Path(a.input).read_text(encoding='utf-8'));markets=x.get('market_intents') or [];inc=[];roots={}
for m in markets:
    for r in m.get('implied_root_ids') or []:roots.setdefault(r,[]).append((m.get('instrument'),m.get('direction'),m.get('local_explanation')))
for rid,vals in roots.items():
    dirs={v[1] for v in vals if v[1] not in {None,'NEUTRAL','UNRESOLVED'}}
    # Opposite asset directions are not automatically inconsistent; require explicit expected-root-direction claims.
    claims=[]
    for m in markets:
        for c in m.get('root_direction_claims') or []:
            if c.get('root_id')==rid:claims.append((m.get('instrument'),c.get('root_state')))
    states={s for _,s in claims if s}
    if len(states)>1:inc.append({'root_id':rid,'claims':claims,'reason':'same root has incompatible stated global condition'})
state='COHERENT'
if inc:state='INCONSISTENT'
elif len({r for m in markets for r in (m.get('implied_root_ids') or [])})>3:state='MULTI_DRIVER_BUT_COHERENT'
out={'state':state,'market_intents':markets,'implied_global_roots':sorted(roots),'inconsistencies':inc,'resolution_actions':['REVIEW_SAME_ROOT_CLAIMS'] if inc else [],'direction_override_applied':False}
s=json.dumps(out,indent=2,ensure_ascii=False);print(s)
if a.output:Path(a.output).write_text(s+'\n',encoding='utf-8')
