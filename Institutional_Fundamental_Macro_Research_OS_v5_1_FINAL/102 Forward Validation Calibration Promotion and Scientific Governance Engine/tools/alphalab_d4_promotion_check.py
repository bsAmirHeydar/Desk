#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--report',required=True);p.add_argument('--authority-class',required=True);p.add_argument('--policy',required=True);a=p.parse_args();r=json.loads(Path(a.report).read_text());pol=json.loads(Path(a.policy).read_text())
cls=a.authority_class
bucket='risk_reducing_or_constraint'
if cls=='RESTORE_EXISTING_DIRECTION_PERMISSION':bucket='positive_permission_restore'
if cls=='CREATE_PERMISSION_WITH_EXISTING_FUNDAMENTAL_DIRECTION':bucket='positive_permission_create'
f=pol['governance_floors'][bucket];dev=r.get('development',{});ho=r.get('holdout',{})
checks={
 'development_observations':dev.get('n',0)>=f['min_observations'],
 'development_independent_roots':dev.get('independent_roots',0)>=f['min_independent_roots'],
 'holdout_independent_roots':ho.get('independent_roots',0)>=f['min_holdout_roots'],
 'distinct_regimes':max(dev.get('distinct_regimes',0),ho.get('distinct_regimes',0))>=f['min_distinct_regimes'],
 'holdout_delta_positive':ho.get('mean_delta_r') is not None and ho.get('mean_delta_r')>0}
status='ELIGIBLE_FOR_REVIEW' if all(checks.values()) else 'NOT_ELIGIBLE'
out={'status':status,'authority_class':cls,'floor_bucket':bucket,'checks':checks,'warning':'Eligibility is not promotion. Tail-risk, multiplicity, stability and independent validation remain mandatory.'};print(json.dumps(out,indent=2));sys.exit(0)
