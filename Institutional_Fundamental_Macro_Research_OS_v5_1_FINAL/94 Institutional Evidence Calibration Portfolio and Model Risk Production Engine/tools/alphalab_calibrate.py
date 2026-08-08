#!/usr/bin/env python3
import argparse,json,statistics,math
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('--outcomes',required=True); p.add_argument('--policy',required=True); p.add_argument('--output',required=True); a=p.parse_args()
pol=json.loads(Path(a.policy).read_text(encoding='utf-8')); rows=[]
for line in Path(a.outcomes).read_text(encoding='utf-8').splitlines():
    if line.strip():
        x=json.loads(line)
        if x.get('matured') and x.get('realized_r') is not None: rows.append(x)

def stats(v):
    if not v: return {'n':0,'mean_r':None,'median_r':None,'positive_r_rate_descriptive':None,'mean_r_approx_95_interval':None}
    vals=[float(x['realized_r']) for x in v]; n=len(vals); mean=sum(vals)/n; sd=statistics.stdev(vals) if n>1 else 0.0; sem=sd/math.sqrt(n) if n else 0.0
    return {'n':n,'mean_r':mean,'median_r':statistics.median(vals),'positive_r_rate_descriptive':sum(z>0 for z in vals)/n,'mean_r_approx_95_interval':[mean-1.96*sem,mean+1.96*sem] if n>1 else None}

def build_level(level,keys):
    groups={}
    for x in rows:
        k=tuple(x.get(z,'UNKNOWN') for z in keys); groups.setdefault(k,[]).append(x)
    res=[]
    for k,v in groups.items():
        train=[x for x in v if not x.get('is_holdout')]; hold=[x for x in v if x.get('is_holdout')]
        roots={x.get('root_event_id') for x in v}; regimes={x.get('regime_label','UNKNOWN') for x in v}
        floors=(len(roots)>=pol['min_independent_matured_observations'] and len(v)>=pol['min_total_matured_observations'] and len(regimes)>=pol['min_distinct_regime_labels'] and len(hold)>=pol['min_holdout_observations'])
        status='ELIGIBLE_FOR_CALIBRATION' if floors else ('DEVELOPING' if len(v)>0 and (len(roots)>=max(5,pol['min_independent_matured_observations']//3) or len(v)>=max(10,pol['min_total_matured_observations']//3)) else 'COLD_START')
        item={'cohort_level':level,**dict(zip(keys,k)),'n':len(v),'independent_root_events':len(roots),'distinct_regimes':len(regimes),'status':status,'train':stats(train),'holdout':stats(hold)}
        for fld in ['mfe_r','mae_r','time_to_trigger_seconds','time_to_mfe_seconds','cost_r']:
            z=[float(x[fld]) for x in v if x.get(fld) is not None]; item['mean_'+fld]=sum(z)/len(z) if z else None
        exp=[x.get('expired_without_trigger') for x in v if x.get('expired_without_trigger') is not None]; item['expiry_without_trigger_rate']=sum(bool(x) for x in exp)/len(exp) if exp else None
        surv=[x.get('state_survived') for x in v if x.get('state_survived') is not None]; item['state_survival_rate']=sum(bool(x) for x in surv)/len(surv) if surv else None
        reg={rg:stats([x for x in v if x.get('regime_label','UNKNOWN')==rg]) for rg in regimes}; item['per_regime']=reg
        overall=stats(v)['mean_r']; osign=1 if overall and overall>0 else (-1 if overall and overall<0 else 0)
        signs=[1 if z['mean_r']>0 else (-1 if z['mean_r']<0 else 0) for z in reg.values() if z['mean_r'] is not None]
        item['regime_sign_consistency']=sum(z==osign for z in signs)/len(signs) if signs and osign else None
        flags=[]
        if train and hold and item['train']['mean_r'] is not None and item['holdout']['mean_r'] is not None and item['train']['mean_r']*item['holdout']['mean_r']<0: flags.append('TRAIN_HOLDOUT_SIGN_FLIP')
        if len(regimes)<pol['min_distinct_regime_labels']: flags.append('REGIME_DIVERSITY_BELOW_FLOOR')
        item['stability_review_flags']=flags
        item['promotion_note']='Sample floors create review eligibility only. No predictive probability or enforcement follows automatically.'
        res.append(item)
    return res
levels=[]
for level,keys in pol['cohort_levels'].items(): levels.extend(build_level(level,keys))
out={'policy_version':pol['version'],'mode':pol['mode'],'backoff_rule':pol['backoff_rule'],'cohorts':levels,'note':'Broader cohorts are explicit backoff views, never silently pooled into an exact cohort. All rates/intervals are descriptive unless separately validated/promoted.'}
Path(a.output).write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8'); print(json.dumps({'matured_rows':len(rows),'cohorts':len(levels),'eligible_cohorts':sum(x['status']=='ELIGIBLE_FOR_CALIBRATION' for x in levels)}))
