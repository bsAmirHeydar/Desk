#!/usr/bin/env python3
import argparse,json
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('--input',required=True); p.add_argument('--q',type=float,default=0.05); p.add_argument('--output',required=True); a=p.parse_args()
x=json.loads(Path(a.input).read_text(encoding='utf-8')); tests=x['tests']; s=sorted(enumerate(tests),key=lambda z:z[1]['p_value']); m=len(s); kmax=-1
for rank,(idx,t) in enumerate(s,1):
 if float(t['p_value']) <= rank*a.q/m: kmax=rank
accepted=set(idx for rank,(idx,t) in enumerate(s,1) if kmax!=-1 and rank<=kmax)
out={'method':'Benjamini-Hochberg','q':a.q,'m':m,'results':[dict(t,discovery=(i in accepted)) for i,t in enumerate(tests)],'note':'This controls supplied p-values only; it does not create valid p-values or replace pre-registration/holdout.'}
Path(a.output).write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8'); print(sum(r['discovery'] for r in out['results']))
