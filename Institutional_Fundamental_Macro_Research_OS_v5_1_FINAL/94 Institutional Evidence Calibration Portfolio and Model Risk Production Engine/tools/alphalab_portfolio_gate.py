#!/usr/bin/env python3
import argparse,json
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('--candidates',required=True); p.add_argument('--policy',required=True); p.add_argument('--output',required=True); a=p.parse_args()
c=json.loads(Path(a.candidates).read_text(encoding='utf-8')); pol=json.loads(Path(a.policy).read_text(encoding='utf-8')); mp=pol['loading_map']; agg={}; roots={}; unknown=[]
for x in c.get('candidates',[]):
 risk=float(x.get('risk_units',1.0)); sym=x.get('symbol')
 for f,cl in (x.get('factor_loadings') or {}).items():
  if cl=='UNKNOWN': unknown.append([sym,f]); continue
  agg[f]=agg.get(f,0.0)+risk*mp[cl]
 for f in x.get('root_factors',[]): roots.setdefault(f,[]).append(sym)
viol=[]
for f,val in agg.items():
 if abs(val)>float(pol['max_abs_factor_risk_units']): viol.append({'type':'FACTOR_CAP','factor':f,'value':val})
for f,syms in roots.items():
 if len(syms)>int(pol['max_same_root_factor_trades']): viol.append({'type':'ROOT_COUNT','factor':f,'symbols':syms})
status='BLOCK' if pol['mode']=='ENFORCED' and viol else 'ALLOW'
out={'mode':pol['mode'],'status':status,'aggregate_factor_risk_units':agg,'unknown_material_exposures':unknown,'violations':viol,'shadow_would_block':bool(viol)}
Path(a.output).write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8'); print(json.dumps(out))
