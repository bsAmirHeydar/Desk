#!/usr/bin/env python3
import argparse,json,csv,statistics,math,random
from pathlib import Path

def mean(x):return statistics.fmean(x) if x else None
def med(x):return statistics.median(x) if x else None
def pf(x):
    pos=sum(v for v in x if v>0);neg=-sum(v for v in x if v<0)
    return None if neg==0 else pos/neg
def tail(x,p=.05):
    if not x:return None
    y=sorted(x);k=max(1,math.ceil(len(y)*p));return mean(y[:k])
def boot(x,it=1000,seed=17):
    if len(x)<2:return [None,None]
    r=random.Random(seed);vals=[]
    for _ in range(it):vals.append(mean([x[r.randrange(len(x))] for __ in range(len(x))]))
    vals.sort();return [vals[int(.025*(it-1))],vals[int(.975*(it-1))]]
p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--modifier-id',required=True);p.add_argument('--output');p.add_argument('--split-field',default='sample_split');a=p.parse_args()
rows=list(csv.DictReader(open(a.input,encoding='utf-8-sig')));rows=[r for r in rows if r.get('modifier_id')==a.modifier_id]
def part(label):
    rr=[r for r in rows if r.get(a.split_field,label)==label]
    deltas=[float(r['delta_r']) for r in rr if r.get('delta_r') not in ('',None)]
    actual=[float(r['actual_r']) for r in rr if r.get('actual_r') not in ('',None)]
    roots=len(set(r.get('independent_root_id') for r in rr if r.get('independent_root_id')))
    regs=len(set(r.get('regime') for r in rr if r.get('regime')))
    return {'n':len(rr),'independent_roots':roots,'distinct_regimes':regs,'mean_delta_r':mean(deltas),'median_delta_r':med(deltas),'delta_r_95pct_bootstrap':boot(deltas),'mean_actual_r':mean(actual),'profit_factor_actual':pf(actual),'lower_tail_mean_actual_r_5pct':tail(actual)}
out={'record_type':'CALIBRATION_REPORT','modifier_id':a.modifier_id,'development':part('DEVELOPMENT'),'holdout':part('HOLDOUT'),'note':'Descriptive policy-effect calibration; promotion still requires governance/validator review.'}
s=json.dumps(out,indent=2);print(s)
if a.output:Path(a.output).write_text(s+'\n',encoding='utf-8')
