#!/usr/bin/env python3
import argparse,json
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('--candidates',required=True); p.add_argument('--policy',required=True); p.add_argument('--output',required=True); a=p.parse_args()
c=json.loads(Path(a.candidates).read_text(encoding='utf-8')); pol=json.loads(Path(a.policy).read_text(encoding='utf-8')); mp=pol['loading_map']; agg={}; unknown=[]; root_dir={}
for x in c.get('candidates',[]):
    risk=float(x.get('risk_units',1.0)); sym=x.get('symbol'); side=x.get('side'); mult=1 if side=='BUY' else (-1 if side=='SELL' else 0)
    if mult==0: unknown.append([sym,'SIDE']); continue
    for f,cl in (x.get('factor_loadings') or {}).items():
        if cl=='UNKNOWN': unknown.append([sym,f]); continue
        agg[f]=agg.get(f,0.0)+risk*mult*mp[cl]
    for f,cl in (x.get('root_factor_loadings') or {}).items():
        if cl=='UNKNOWN': unknown.append([sym,'ROOT:'+f]); continue
        v=risk*mult*mp[cl]; sign='POS' if v>0 else ('NEG' if v<0 else 'ZERO'); root_dir.setdefault(f,{}).setdefault(sign,[]).append(sym)
viol=[]; offsets=[]
for f,val in agg.items():
    if abs(val)>float(pol['max_abs_factor_risk_units']): viol.append({'type':'FACTOR_CAP','factor':f,'value':val})
for f,d in root_dir.items():
    if d.get('POS') and d.get('NEG'): offsets.append({'factor':f,'positive_symbols':d['POS'],'negative_symbols':d['NEG']})
    for sign in ['POS','NEG']:
        syms=d.get(sign,[])
        if len(syms)>int(pol['max_same_direction_root_factor_trades']): viol.append({'type':'ROOT_SAME_DIRECTION_COUNT','factor':f,'direction':sign,'symbols':syms})
status='BLOCK' if pol['mode']=='ENFORCED' and viol else 'ALLOW'
out={'mode':pol['mode'],'status':status,'aggregate_signed_factor_risk_units':agg,'unknown_material_exposures':unknown,'offsetting_root_exposures':offsets,'violations':viol,'shadow_would_block':bool(viol),'covariance_status':pol.get('covariance_status','UNAVAILABLE')}
Path(a.output).write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8'); print(json.dumps(out))
