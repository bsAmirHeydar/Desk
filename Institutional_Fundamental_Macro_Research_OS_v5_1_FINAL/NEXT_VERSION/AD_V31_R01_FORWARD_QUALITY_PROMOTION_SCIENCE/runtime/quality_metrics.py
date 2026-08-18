from __future__ import annotations
from collections import Counter,defaultdict
from statistics import mean
from .common import cfg
from .benchmark_engine import rate,wilson_lower,direction_score

def _classify_dom(v):
    s=str(v or '')
    if 'DOMINANT' in s:return 'DOMINANT'
    if 'FRAGILE' in s:return 'FRAGILE'
    if s in ('BALANCED','TRUE_MIXED','MIXED'):return 'BALANCED'
    return s or 'UNKNOWN'
def _path_supported(o):return o.get('path_quality') in ('CLEAN','ACCEPTABLE')
def _path_adverse(o):return o.get('path_quality')=='ADVERSE'
def _usable_path(o):return ((o.get('path_coverage') or {}).get('path_metric_authority')=='AVAILABLE')
def primary_records(state,qualification_cohort):
    preds={p['prediction_id']:p for p in state.get('predictions',[])};outs={o['prediction_id']:o for o in state.get('outcomes',[])};rows=[]
    start=(qualification_cohort or {}).get('started_at_utc');bound=(qualification_cohort or {}).get('p09_cohort_id')
    for e in state.get('episodes',[]):
        pid=e.get('primary_prediction_id');p=preds.get(pid);o=outs.get(pid)
        if not p or not o or p.get('eligibility')!='VALIDATION_ELIGIBLE':continue
        if bound and p.get('cohort_id')!=bound:continue
        if start and str(e.get('start_time') or p.get('precommit_time') or '')<str(start):continue
        rows.append((p,o,e))
    return rows

def direction_quality(rows):
    pol=cfg('forward_quality_policy.json')['direction_quality'];drows=[(p,o) for p,o,_ in rows if p.get('causal_direction') in ('BULLISH_GOLD','BEARISH_GOLD') and o.get('direction_outcome') in ('ALIGNED','OPPOSED','NEUTRAL_BAND')]
    cnt=Counter(o.get('direction_outcome') for p,o in drows);n=len(drows);non=cnt['ALIGNED']+cnt['OPPOSED'];bull=[o for p,o in drows if p.get('causal_direction')=='BULLISH_GOLD'];bear=[o for p,o in drows if p.get('causal_direction')=='BEARISH_GOLD']
    def ar(z):
        a=sum(1 for o in z if o.get('direction_outcome')=='ALIGNED');q=sum(1 for o in z if o.get('direction_outcome')=='OPPOSED');return rate(a,a+q)
    br,ser=ar(bull),ar(bear);bal=(br+ser)/2 if br is not None and ser is not None else None;wl=wilson_lower(cnt['ALIGNED'],non);neutral=rate(cnt['NEUTRAL_BAND'],n)
    enough=n>=pol['min_evaluable_episodes'] and non>=pol['min_non_neutral_episodes'] and len(bull)>=pol['min_bull_episodes'] and len(bear)>=pol['min_bear_episodes']
    passed=bool(enough and bal is not None and bal>=pol['min_class_balanced_alignment_rate'] and wl is not None and wl>=pol['min_overall_wilson_lower_bound'] and neutral<=pol['max_neutral_share'])
    return {'state':'PASS' if passed else ('FAIL' if enough else 'INSUFFICIENT'),'n':n,'non_neutral_n':non,'bull_n':len(bull),'bear_n':len(bear),'counts':dict(cnt),'bull_alignment_rate':br,'bear_alignment_rate':ser,'class_balanced_alignment_rate':bal,'overall_wilson_lower_bound':wl,'neutral_share':neutral,'benchmark':'CLASS_BALANCED_50_50_NULL'}

def strength_calibration(rows):
    min_n=cfg('forward_quality_policy.json')['supporting_min_group_n'];tol=cfg('forward_quality_policy.json')['supporting_tolerance'];order=['WEAK','MODERATE','STRONG','DOMINANT'];g=defaultdict(list)
    for p,o,_ in rows:
        s=direction_score(o.get('direction_outcome'))
        if s is not None:g[str(p.get('pressure_strength'))].append(s)
    av={k:mean(v) for k,v in g.items() if len(v)>=min_n};seq=[(k,av[k]) for k in order if k in av]
    if len(seq)<2:return {'state':'INCONCLUSIVE','groups':{k:{'n':len(g[k]),'mean_direction_score':mean(g[k]) if g[k] else None} for k in g}}
    ok=all(seq[i+1][1]+tol>=seq[i][1] for i in range(len(seq)-1));return {'state':'PASS' if ok else 'FAIL','groups':{k:{'n':len(g[k]),'mean_direction_score':mean(g[k]) if g[k] else None} for k in g},'ordered_groups':seq}

def dominance_calibration(rows):
    min_n=cfg('forward_quality_policy.json')['supporting_min_group_n'];tol=cfg('forward_quality_policy.json')['supporting_tolerance'];g=defaultdict(list)
    for p,o,_ in rows:
        s=direction_score(o.get('direction_outcome'))
        if s is not None:g[_classify_dom(p.get('dominance_state'))].append(s)
    dom=g.get('DOMINANT',[]);other=g.get('FRAGILE',[])+g.get('BALANCED',[])
    if len(dom)<min_n or len(other)<min_n:return {'state':'INCONCLUSIVE','dominant_n':len(dom),'comparison_n':len(other),'dominant_mean':mean(dom) if dom else None,'comparison_mean':mean(other) if other else None}
    ok=mean(dom)+tol>=mean(other);return {'state':'PASS' if ok else 'FAIL','dominant_n':len(dom),'comparison_n':len(other),'dominant_mean':mean(dom),'comparison_mean':mean(other)}

def edge_separation(rows):
    pol=cfg('forward_quality_policy.json')['edge_separation'];a=[o for p,o,_ in rows if p.get('edge_state') in pol['actionable_states'] and _usable_path(o)];b=[o for p,o,_ in rows if p.get('edge_state') in pol['baseline_states'] and _usable_path(o)]
    ar=rate(sum(_path_supported(o) for o in a),len(a));br=rate(sum(_path_supported(o) for o in b),len(b));adv=rate(sum(_path_adverse(o) for o in a),len(a));enough=len(a)>=pol['min_actionable_path_samples'] and len(b)>=pol['min_baseline_path_samples'];sep=(ar-br) if ar is not None and br is not None else None
    ok=bool(enough and ar>=pol['min_actionable_supported_path_rate'] and sep>=pol['min_supported_path_rate_separation'] and adv<=pol['max_actionable_adverse_path_rate'])
    return {'state':'PASS' if ok else ('FAIL' if enough else 'INSUFFICIENT'),'actionable_n':len(a),'baseline_n':len(b),'actionable_supported_path_rate':ar,'baseline_supported_path_rate':br,'separation':sep,'actionable_adverse_rate':adv}

def permission_quality(rows):
    pol=cfg('forward_quality_policy.json')['permission_quality'];z=[o for p,o,_ in rows if p.get('permission_candidate') in ('BUY_CANDIDATE','SELL_CANDIDATE') and o.get('permission_outcome')!='UNRESOLVED'];c=Counter(o.get('permission_outcome') for o in z);n=len(z);sup=rate(c['SUPPORTED'],n);opp=rate(c['OPPOSED'],n);wl=wilson_lower(c['SUPPORTED'],n);enough=n>=pol['min_directional_permission_samples'];ok=bool(enough and sup>=pol['min_supported_rate'] and opp<=pol['max_opposed_rate'] and wl>=pol['min_supported_wilson_lower_bound'])
    return {'state':'PASS' if ok else ('FAIL' if enough else 'INSUFFICIENT'),'n':n,'counts':dict(c),'supported_rate':sup,'opposed_rate':opp,'supported_wilson_lower_bound':wl}

def wait_quality(rows):
    pol=cfg('forward_quality_policy.json')['wait_quality'];z=[o for p,o,_ in rows if p.get('permission_candidate')=='WAIT'];c=Counter(o.get('wait_outcome') for o in z);n=len(z);good=c['WAIT_PROTECTED']+c['WAIT_APPROPRIATE_UNCERTAINTY']+c['WAIT_CONSUMPTION_AVOIDED'];gr=rate(good,n);miss=rate(c['WAIT_MISSED_OPPORTUNITY'],n);unres=rate(c['WAIT_UNRESOLVED'],n);enough=n>=pol['min_wait_samples'];ok=bool(enough and gr>=pol['min_protective_or_appropriate_rate'] and miss<=pol['max_missed_opportunity_rate'] and unres<=pol['max_unresolved_rate'])
    return {'state':'PASS' if ok else ('FAIL' if enough else 'INSUFFICIENT'),'n':n,'counts':dict(c),'protective_or_appropriate_rate':gr,'missed_opportunity_rate':miss,'unresolved_rate':unres}

def path_completeness(rows):
    pol=cfg('forward_quality_policy.json')['path_completeness'];relevant=[o for p,o,_ in rows if p.get('edge_state')=='ACTIONABLE_EDGE' or p.get('permission_candidate') in ('BUY_CANDIDATE','SELL_CANDIDATE')];avail=sum(_usable_path(o) for o in relevant);share=rate(avail,len(relevant));enough=len(relevant)>=20;ok=bool(enough and share is not None and share>=pol['min_path_authority_share_for_edge_permission'])
    return {'state':'PASS' if ok else ('FAIL' if enough else 'INSUFFICIENT'),'relevant_n':len(relevant),'path_available_n':avail,'path_authority_share':share}

def consumption_validity(rows):
    min_n=cfg('forward_quality_policy.json')['supporting_min_group_n'];g=defaultdict(list)
    for p,o,_ in rows:
        if not _usable_path(o) or o.get('mfe_return') is None:continue
        band=o.get('neutral_band_return') or 0
        if band>0:g[str(p.get('consumption'))].append(o['mfe_return']/band)
    low=g.get('LOW',[])+g.get('MODERATE',[]);high=g.get('HIGH',[])+g.get('CONSUMED',[])
    if len(low)<min_n or len(high)<min_n:return {'state':'INCONCLUSIVE','low_n':len(low),'high_n':len(high),'low_mean_residual_mfe':mean(low) if low else None,'high_mean_residual_mfe':mean(high) if high else None}
    ok=mean(high)<=mean(low)*1.10;return {'state':'PASS' if ok else 'FAIL','low_n':len(low),'high_n':len(high),'low_mean_residual_mfe':mean(low),'high_mean_residual_mfe':mean(high)}

def fragility_validity(rows):
    min_n=cfg('forward_quality_policy.json')['supporting_min_group_n'];g=defaultdict(list)
    for p,o,_ in rows:
        band=o.get('neutral_band_return') or 0
        if band<=0 or o.get('mae_return') is None:continue
        g[str(p.get('fragility'))].append((o['mae_return']/band,1 if o.get('direction_outcome')=='OPPOSED' else 0))
    low=g.get('LOW',[]);high=g.get('HIGH',[])+g.get('ELEVATED',[])
    if len(low)<min_n or len(high)<min_n:return {'state':'INCONCLUSIVE','low_n':len(low),'high_n':len(high)}
    low_mae=mean(x[0] for x in low);high_mae=mean(x[0] for x in high);low_opp=mean(x[1] for x in low);high_opp=mean(x[1] for x in high);ok=high_mae>=low_mae*0.90 or high_opp>=low_opp
    return {'state':'PASS' if ok else 'FAIL','low_n':len(low),'high_n':len(high),'low_mae_multiple':low_mae,'high_mae_multiple':high_mae,'low_opposed_rate':low_opp,'high_opposed_rate':high_opp}

def r02_decision_diagnostics(rows):
    min_n=cfg('forward_quality_policy.json')['supporting_min_group_n']
    mag_order=['MINOR','MATERIAL','LARGE','EXTREME']; mg=defaultdict(list);hg=defaultdict(list);rg=defaultdict(list)
    for p,o,_ in rows:
        sc=direction_score(o.get('direction_outcome'))
        if sc is None:continue
        mg[str(p.get('dominant_root_magnitude') or 'UNKNOWN')].append(sc)
        h=p.get('dominant_root_health') or {};hg[str(h.get('state') if isinstance(h,dict) else h or 'UNKNOWN')].append(sc)
        rg[str(p.get('dominance_robustness') or 'NOT_APPLICABLE')].append(sc)
    def avgmap(g):return {k:{'n':len(v),'mean_direction_score':mean(v) if v else None} for k,v in g.items()}
    mseq=[(k,mean(mg[k])) for k in mag_order if len(mg[k])>=min_n]
    mag_state='INCONCLUSIVE' if len(mseq)<2 else ('PASS' if all(mseq[i+1][1]>=mseq[i][1]-.05 for i in range(len(mseq)-1)) else 'FAIL')
    good=hg.get('HEALTHY',[])+hg.get('PARTIAL',[]);bad=hg.get('DEGRADED',[])+hg.get('CRITICAL_GAP',[])
    health_state='INCONCLUSIVE' if len(good)<min_n or len(bad)<min_n else ('PASS' if mean(good)>=mean(bad)-.05 else 'FAIL')
    robust=rg.get('ROBUST',[])+rg.get('MOSTLY_ROBUST',[]);sens=rg.get('MODEL_SENSITIVE',[])+rg.get('UNSTABLE',[])
    robust_state='INCONCLUSIVE' if len(robust)<min_n or len(sens)<min_n else ('PASS' if mean(robust)>=mean(sens)-.05 else 'FAIL')
    return {'magnitude_ordering':{'state':mag_state,'groups':avgmap(mg),'ordered_groups':mseq},'root_health_validity':{'state':health_state,'groups':avgmap(hg)},'robustness_validity':{'state':robust_state,'groups':avgmap(rg)},'supporting_forward_diagnostic_only':True}

def all_metrics(rows):
    return {'direction':direction_quality(rows),'strength':strength_calibration(rows),'dominance':dominance_calibration(rows),'edge':edge_separation(rows),'permission':permission_quality(rows),'wait':wait_quality(rows),'path_completeness':path_completeness(rows),'consumption':consumption_validity(rows),'fragility':fragility_validity(rows),'r02_diagnostics':r02_decision_diagnostics(rows)}
