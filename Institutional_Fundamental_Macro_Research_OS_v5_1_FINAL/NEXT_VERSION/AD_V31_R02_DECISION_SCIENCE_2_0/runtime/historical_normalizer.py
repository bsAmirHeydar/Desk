from __future__ import annotations
from statistics import mean,pstdev
from .common import cfg,parse_dt

def normalize(value,history,as_of=None):
    pol=cfg('historical_normalization_policy.json'); cutoff=parse_dt(as_of) if as_of else None; vals=[]
    for item in history or []:
        if not isinstance(item,dict) or not isinstance(item.get('value'),(int,float)):continue
        t=item.get('timestamp') or item.get('as_of') or item.get('reference_time')
        if cutoff is not None and t:
            dt=parse_dt(t)
            if dt>=cutoff: raise ValueError('R02_LOOKAHEAD_HISTORY_REJECTED')
        vals.append(float(item['value']))
    if len(vals)<int(pol['minimum_history']):return {'state':'INSUFFICIENT_HISTORY','history_size':len(vals),'z_score':None}
    sd=pstdev(vals)
    if sd<=1e-12:return {'state':'ZERO_VARIANCE','history_size':len(vals),'z_score':None}
    z=(float(value)-mean(vals))/sd
    return {'state':'AVAILABLE','history_size':len(vals),'z_score':z,'mean':mean(vals),'std':sd}
