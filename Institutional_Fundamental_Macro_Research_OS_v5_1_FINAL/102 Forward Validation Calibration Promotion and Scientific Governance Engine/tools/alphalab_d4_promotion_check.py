#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--report',required=True);p.add_argument('--authority-class',required=True);p.add_argument('--policy',required=True);a=p.parse_args();r=json.loads(Path(a.report).read_text());pol=json.loads(Path(a.policy).read_text())
cls=a.authority_class;bucket='risk_reducing_or_constraint'
if cls=='RESTORE_EXISTING_DIRECTION_PERMISSION':bucket='positive_permission_restore'
if cls=='CREATE_PERMISSION_WITH_EXISTING_FUNDAMENTAL_DIRECTION':bucket='positive_permission_create'
f=pol['governance_floors'][bucket];dev=r.get('development',{});ho=r.get('holdout',{});dep=r.get('dependence',{});tail=r.get('tail_risk',{});reg=r.get('regime_stability',{});mt=r.get('multiple_testing',{})
checks={
 'development_observations':dev.get('raw_n',dev.get('n',0))>=f['min_observations'],
 'development_independent_roots':dev.get('independent_roots',0)>=f['min_independent_roots'],
 'holdout_independent_roots':ho.get('independent_roots',0)>=f['min_holdout_roots'],
 'distinct_regimes':max(dev.get('distinct_regimes',0),ho.get('distinct_regimes',0))>=f['min_distinct_regimes'],
 'holdout_delta_positive':ho.get('mean_delta_r') is not None and ho.get('mean_delta_r')>0,
 'dependence_aware_resampling':not dep.get('observation_level_bootstrap_used',True) if (dev.get('independent_roots',0)>0 or ho.get('independent_roots',0)>0) else True,
 'chronological_split_attested':r.get('chronological_split_attested') is True,
 'execution_profile_present':bool(r.get('execution_profiles'))}
positive=cls in {'RESTORE_EXISTING_DIRECTION_PERMISSION','CREATE_PERMISSION_WITH_EXISTING_FUNDAMENTAL_DIRECTION'}
if positive:
    checks['tail_risk_comparison_available']=tail.get('comparison_available') is True
    checks['regime_sign_stability_disclosed']=reg.get('holdout_sign_stable') is not None
    checks['multiple_testing_disclosed']=mt.get('disclosure_complete') is True
status='ELIGIBLE_FOR_INDEPENDENT_REVIEW' if all(checks.values()) else 'NOT_ELIGIBLE'
out={'status':status,'authority_class':cls,'floor_bucket':bucket,'checks':checks,'warning':'Eligibility is not promotion. V21 requires independent validator approval, explicit tail-harm judgement, stability/drift review and registry change control.'};print(json.dumps(out,indent=2));sys.exit(0)
