#!/usr/bin/env python3
import argparse,json,statistics
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('--outcomes',required=True); p.add_argument('--policy',required=True); p.add_argument('--output',required=True); a=p.parse_args()
pol=json.loads(Path(a.policy).read_text(encoding='utf-8')); rows=[]
for line in Path(a.outcomes).read_text(encoding='utf-8').splitlines():
 if line.strip():
  x=json.loads(line)
  if x.get('matured') and x.get('realized_r') is not None: rows.append(x)
keys=['symbol','horizon','core_direction','timing_gate','driver_family','narrative_family']
groups={}
for x in rows:
 k=tuple(x.get(z,'UNKNOWN') for z in keys); groups.setdefault(k,[]).append(x)
res=[]
for k,v in groups.items():
 vals=[float(x['realized_r']) for x in v]; roots={x.get('root_event_id',x.get('run_id')) for x in v}; regimes={x.get('regime_label','UNKNOWN') for x in v}; hold=[x for x in v if x.get('is_holdout')]
 ok=(len(roots)>=pol['min_independent_matured_observations'] and len(v)>=pol['min_total_matured_observations'] and len(regimes)>=pol['min_distinct_regime_labels'] and len(hold)>=pol['min_holdout_observations'])
 status='ELIGIBLE_FOR_CALIBRATION' if ok else ('DEVELOPING' if len(roots)>=pol['min_independent_matured_observations'] else 'COLD_START')
 item=dict(zip(keys,k)); item.update({'n':len(vals),'independent_root_events':len(roots),'distinct_regimes':len(regimes),'holdout_n':len(hold),'status':status,'mean_r':sum(vals)/len(vals),'median_r':statistics.median(vals),'positive_r_rate_descriptive':sum(z>0 for z in vals)/len(vals)})
 for fld in ['mfe_r','mae_r','time_to_trigger_seconds','time_to_mfe_seconds','cost_r']:
  z=[float(x[fld]) for x in v if x.get(fld) is not None]; item['mean_'+fld]=sum(z)/len(z) if z else None
 res.append(item)
out={'policy_version':pol['version'],'mode':pol['mode'],'groups':res,'note':'Positive-R rate is descriptive. Numeric predictive probability is not authorized merely by this file; promotion and validation are separate.'}
Path(a.output).write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8'); print(json.dumps({'matured_rows':len(rows),'groups':len(res),'eligible_groups':sum(x['status']=='ELIGIBLE_FOR_CALIBRATION' for x in res)}))
