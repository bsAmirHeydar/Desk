#!/usr/bin/env python3
import argparse,json,csv,statistics,math,random,hashlib,datetime
from pathlib import Path
def mean(x):return statistics.fmean(x) if x else None
def med(x):return statistics.median(x) if x else None
def pf(x):
    pos=sum(v for v in x if v>0);neg=-sum(v for v in x if v<0);return None if neg==0 else pos/neg
def tail(x,p=.05):
    if not x:return None
    y=sorted(x);k=max(1,math.ceil(len(y)*p));return mean(y[:k])
def qtile(x,q):
    if not x:return None
    y=sorted(x);i=min(len(y)-1,max(0,int(round(q*(len(y)-1)))));return y[i]
def fnum(v):
    try:return float(v) if v not in ('',None) else None
    except:return None
def cluster_boot(rows,value_field,preferred='independent_root_id',fallback='trading_day',it=2000,seed=17):
    vals=[(r,fnum(r.get(value_field))) for r in rows];vals=[x for x in vals if x[1] is not None]
    if not vals:return {'interval':[None,None],'unit':'NONE','cluster_n':0,'observation_n':0}
    key=None
    if any(r.get(preferred) for r,_ in vals):key=preferred
    elif any(r.get(fallback) for r,_ in vals):key=fallback
    if key:
        g={}
        for r,v in vals:g.setdefault(r.get(key) or '__MISSING__',[]).append(v)
        units=[mean(vs) for vs in g.values()];unit=key
    else:units=[v for _,v in vals];unit='OBSERVATION_FALLBACK'
    if len(units)<2:return {'interval':[None,None],'unit':unit,'cluster_n':len(units),'observation_n':len(vals)}
    rr=random.Random(seed);bs=[]
    for _ in range(it):bs.append(mean([units[rr.randrange(len(units))] for __ in range(len(units))]))
    bs.sort();return {'interval':[bs[int(.025*(it-1))],bs[int(.975*(it-1))]],'unit':unit,'cluster_n':len(units),'observation_n':len(vals)}
def group_mean(rows,field,group):
    out={}
    for r in rows:
        v=fnum(r.get(field));g=r.get(group)
        if v is None or not g:continue
        out.setdefault(g,[]).append(v)
    return {k:{'n':len(v),'mean':mean(v),'median':med(v)} for k,v in sorted(out.items())}
p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--modifier-id',required=True);p.add_argument('--output');p.add_argument('--split-field',default='sample_split');p.add_argument('--policy');a=p.parse_args()
rows=list(csv.DictReader(open(a.input,encoding='utf-8-sig')));rows=[r for r in rows if r.get('modifier_id')==a.modifier_id]
policy={}
if a.policy:policy=json.loads(Path(a.policy).read_text())
else:
    pp=Path(__file__).resolve().parent.parent/'config/calibration_policy.json'
    if pp.exists():policy=json.loads(pp.read_text())
it=int((policy.get('bootstrap') or {}).get('iterations',2000));pref=(policy.get('bootstrap') or {}).get('preferred_cluster_key','independent_root_id');fallback=(policy.get('bootstrap') or {}).get('fallback_cluster_key','trading_day')
def part(label):
    rr=[r for r in rows if (r.get(a.split_field) or label)==label]
    realized=[r for r in rr if (r.get('outcome_status') or 'REALIZED') not in {'NOT_TRIGGERED','CENSORED','EXPIRED_WITHOUT_TRIGGER'}]
    deltas=[fnum(r.get('delta_r')) for r in realized];deltas=[v for v in deltas if v is not None]
    actual=[fnum(r.get('actual_r')) for r in realized];actual=[v for v in actual if v is not None]
    cf=[fnum(r.get('counterfactual_r')) for r in realized];cf=[v for v in cf if v is not None]
    roots=len(set(r.get('independent_root_id') for r in rr if r.get('independent_root_id')));days=len(set(r.get('trading_day') for r in rr if r.get('trading_day')));runs=len(set(r.get('run_id') for r in rr if r.get('run_id')));regs=len(set(r.get('regime') for r in rr if r.get('regime')))
    boot=cluster_boot(realized,'delta_r',pref,fallback,it);regime=group_mean(realized,'delta_r','regime');signs=[1 if v['mean']>0 else -1 if v['mean']<0 else 0 for v in regime.values() if v['mean'] is not None];stable=None if not signs else (all(s>=0 for s in signs) or all(s<=0 for s in signs))
    tail_actual=tail(actual);tail_cf=tail(cf);tail_delta=None if tail_actual is None or tail_cf is None else tail_actual-tail_cf;censored=len(rr)-len(realized)
    return {'raw_n':len(rr),'realized_n':len(realized),'censored_or_not_triggered_n':censored,'censored_or_not_triggered_rate':None if not rr else censored/len(rr),'unique_runs':runs,'unique_trading_days':days,'independent_roots':roots,'distinct_regimes':regs,'mean_delta_r':mean(deltas),'median_delta_r':med(deltas),'delta_r_95pct_cluster_bootstrap':boot['interval'],'resampling_unit':boot['unit'],'resampling_cluster_n':boot['cluster_n'],'mean_actual_r':mean(actual),'median_actual_r':med(actual),'profit_factor_actual':pf(actual),'lower_tail_mean_actual_r_5pct':tail_actual,'lower_tail_mean_counterfactual_r_5pct':tail_cf,'lower_tail_delta_r_5pct':tail_delta,'mae_r_95pct':qtile([fnum(r.get('mae_r')) for r in realized if fnum(r.get('mae_r')) is not None],.95),'mfe_r_median':med([fnum(r.get('mfe_r')) for r in realized if fnum(r.get('mfe_r')) is not None]),'regime_effects':regime,'effect_sign_stable_across_observed_regimes':stable}
dev=part('DEVELOPMENT');ho=part('HOLDOUT');hf=sorted(set(r.get('hypothesis_family_id') for r in rows if r.get('hypothesis_family_id')));refclasses=sorted(set(r.get('reference_class_id') for r in rows if r.get('reference_class_id')))
mt_counts=[]
for r in rows:
    try:
        if r.get('hypotheses_tested_in_family'):mt_counts.append(int(r['hypotheses_tested_in_family']))
    except:pass
reason=[]
if not rows:elig='INSUFFICIENT_EVIDENCE';reason.append('NO_MATCHING_ROWS')
elif dev['realized_n']==0 or ho['realized_n']==0:elig='INSUFFICIENT_EVIDENCE';reason.append('NO_REALIZED_DEVELOPMENT_OR_HOLDOUT')
elif not all((r.get('chronological_split_attested') or '').lower() in {'true','1','yes'} for r in rows):elig='NOT_ELIGIBLE';reason.append('CHRONOLOGICAL_SPLIT_NOT_ATTESTED')
elif dev['resampling_unit']=='OBSERVATION_FALLBACK' or ho['resampling_unit']=='OBSERVATION_FALLBACK':elig='NOT_ELIGIBLE';reason.append('DEPENDENCE_AWARE_RESAMPLING_UNAVAILABLE')
elif ho['mean_delta_r'] is None:elig='INSUFFICIENT_EVIDENCE';reason.append('HOLDOUT_DELTA_UNAVAILABLE')
elif ho['mean_delta_r']<=0:elig='VALIDATION_FAILED';reason.append('NONPOSITIVE_HOLDOUT_DELTA')
else:elig='ELIGIBLE_FOR_REVIEW';reason.append('PASSED_CALIBRATOR_REVIEW_FLOOR_NOT_PROMOTED')
chron=all((r.get('chronological_split_attested') or '').lower() in {'true','1','yes'} for r in rows) if rows else False
seed_obj={'modifier_id':a.modifier_id,'run_ids':sorted(set(r.get('run_id') for r in rows if r.get('run_id'))),'policy_version':policy.get('version','1.2.0')};calid='CAL_'+hashlib.sha256(json.dumps(seed_obj,sort_keys=True).encode()).hexdigest()[:20].upper()
out={'record_type':'CALIBRATION_REPORT','calibration_id':calid,'calibration_version':'1.2.0','policy_version':policy.get('version','1.2.0'),'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'modifier_id':a.modifier_id,'hypothesis_family_ids':hf,'reference_class_ids':refclasses,'development':dev,'holdout':ho,'dependence':{'preferred_cluster_key':pref,'fallback_cluster_key':fallback,'development_resampling_unit':dev['resampling_unit'],'holdout_resampling_unit':ho['resampling_unit'],'observation_level_bootstrap_used':dev['resampling_unit']=='OBSERVATION_FALLBACK' or ho['resampling_unit']=='OBSERVATION_FALLBACK'},'tail_risk':{'development_lower_tail_delta_r_5pct':dev['lower_tail_delta_r_5pct'],'holdout_lower_tail_delta_r_5pct':ho['lower_tail_delta_r_5pct'],'comparison_available':ho['lower_tail_delta_r_5pct'] is not None},'regime_stability':{'development':dev['regime_effects'],'holdout':ho['regime_effects'],'holdout_sign_stable':ho['effect_sign_stable_across_observed_regimes']},'multiple_testing':{'hypothesis_family_ids':hf,'max_declared_hypotheses_tested':max(mt_counts) if mt_counts else None,'disclosure_complete':bool(hf) and bool(mt_counts)},'chronological_split_attested':chron,'execution_profiles':sorted(set(r.get('execution_profile') for r in rows if r.get('execution_profile'))),'promotion_eligibility':elig,'promotion_eligibility_reason_codes':reason,'note':'Dependence-aware descriptive policy-effect calibration. ELIGIBLE_FOR_REVIEW is not a promotion; independent validation, tail/multiplicity/stability review and registry governance remain mandatory.'}
s=json.dumps(out,indent=2);print(s)
if a.output:Path(a.output).write_text(s+'\n',encoding='utf-8')
