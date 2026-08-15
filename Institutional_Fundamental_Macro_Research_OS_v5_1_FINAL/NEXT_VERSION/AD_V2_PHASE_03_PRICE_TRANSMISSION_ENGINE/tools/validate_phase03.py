#!/usr/bin/env python3
from pathlib import Path
import argparse,copy,hashlib,json,sys
HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE/'runtime'))
from price_transmission import build_transmission,_pressure_fingerprint

PASS=0;FAIL=0;DETAIL=[]
def chk(name,cond,detail=None):
    global PASS,FAIL
    if cond: PASS+=1; DETAIL.append({'name':name,'status':'PASS'})
    else: FAIL+=1; DETAIL.append({'name':name,'status':'FAIL','detail':detail})

def p02(sign='BUY',cls='BUY_HIGH',conf='HIGH'):
    mid=65 if sign=='BUY' else -65
    return {'status':'PASS','active_horizon':'SESSION_1_6H','as_of_utc':'2026-08-14T12:00:00Z','pressure_core':{'sign':sign,'class':cls,'signed_range':{'low':55 if sign=='BUY' else -75,'high':75 if sign=='BUY' else -55},'signed_midpoint':mid},'pressure_dynamics':{'trend':'RISING','snapshot_delta':5,'acceleration':'BUYWARD_ACCELERATION' if sign=='BUY' else 'SELLWARD_ACCELERATION'},'fundamental_driver_consumption':{'value':'PARTIAL'},'remaining_causal_pressure':{'value':'HIGH'},'persistence':{'value':'HIGH'},'contradiction_load':{'class':'LOW'},'pressure_confidence':{'class':conf},'integrity':{'status':'PASS'}}

def sig(p, *, method='EXPERT_RANGE',prov='JUDGMENTAL',decl='2026-08-14T12:05:00Z',unit='PCT_RETURN',exp=(0.30,0.70),earliest=0,latest=1800,pathways=True):
    tr={'instrument':'XAUUSD','unit':unit,'minimum_material_response':0.05,'earliest_material_response_seconds':earliest,'latest_expected_lag_seconds':latest}
    if exp is not None: tr['expected_aligned_range']={'low':exp[0],'high':exp[1]}
    s={'signature_id':'SIG-1','pressure_fingerprint':_pressure_fingerprint(p),'active_horizon':'SESSION_1_6H','declared_at_utc':decl,'method':method,'method_provenance':prov,'target_response':tr,'pathways':[]}
    if pathways:
        s['pathways']=[
          {'channel_id':'US2Y','expected_direction':'DOWN','independence_group':'POLICY_PATH'},
          {'channel_id':'REAL10Y','expected_direction':'DOWN','independence_group':'REAL_RATE'},
          {'channel_id':'DXY','expected_direction':'DOWN','independence_group':'USD'},
          {'channel_id':'GC_PROXY','expected_direction':'UP','independence_group':'TARGET_PROXY','mechanically_linked_target_proxy':True}
        ]
    return s

def act(resp, *, start='2026-08-14T12:05:00Z',end='2026-08-14T12:25:00Z',unit='PCT_RETURN',channels=None):
    return {'window_start_utc':start,'window_end_utc':end,'target':{'instrument':'XAUUSD','unit':unit,'observed_response':resp,'data_quality':'DIRECT'},'channels':channels or [
      {'channel_id':'US2Y','observed_direction':'DOWN'},{'channel_id':'REAL10Y','observed_direction':'DOWN'},{'channel_id':'DXY','observed_direction':'DOWN'},{'channel_id':'GC_PROXY','observed_direction':'UP'}]}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo-root',required=True);ap.add_argument('--json-out');a=ap.parse_args()
    repo=Path(a.repo_root).resolve(); vault=repo/'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL'
    # dependency surface exists
    for rel in ['NEXT_VERSION/AD_V2_PHASE_00_PRESSURE_PRICE_CONSTITUTION/DEVELOPMENT_MANIFEST.json','NEXT_VERSION/AD_V2_PHASE_01_RUNTIME_SEMANTIC_REPAIR/DEVELOPMENT_MANIFEST.json','NEXT_VERSION/AD_V2_PHASE_02_DIRECTIONAL_PRESSURE_ENGINE/DEVELOPMENT_MANIFEST.json']:
        chk('dependency:'+rel,(vault/rel).is_file())
    p=p02(); s=sig(p)
    # State cases
    r=build_transmission(p,s,act(0.50)); chk('aligned',r.get('transmission_state',{}).get('state')=='ALIGNED',r)
    rneg=build_transmission(p,s,act(-0.40)); chk('buy_negative_transmission',rneg.get('transmission_state',{}).get('state')=='NEGATIVE_TRANSMISSION',rneg)
    ps=p02('SELL','SELL_HIGH'); ss=sig(ps); chk('sell_aligned',build_transmission(ps,ss,act(-0.50)).get('transmission_state',{}).get('state')=='ALIGNED')
    chk('sell_negative',build_transmission(ps,ss,act(0.40)).get('transmission_state',{}).get('state')=='NEGATIVE_TRANSMISSION')
    sdel=sig(p,latest=1800); chk('delayed',build_transmission(p,sdel,act(0.01,end='2026-08-14T12:20:00Z')).get('transmission_state',{}).get('state')=='DELAYED')
    chk('compression',build_transmission(p,sdel,act(0.01,end='2026-08-14T12:45:01Z')).get('transmission_state',{}).get('state')=='COMPRESSION')
    chk('aligned_incomplete',build_transmission(p,sdel,act(0.20,end='2026-08-14T12:20:00Z')).get('transmission_state',{}).get('state')=='ALIGNED_INCOMPLETE')
    chk('under_transmission',build_transmission(p,sdel,act(0.20,end='2026-08-14T12:45:01Z')).get('transmission_state',{}).get('state')=='UNDER_TRANSMISSION')
    chk('over_transmission',build_transmission(p,s,act(1.00)).get('transmission_state',{}).get('state')=='OVER_TRANSMISSION')
    sd=sig(p,method='DIRECTION_ONLY',exp=None); chk('direction_only',build_transmission(p,sd,act(0.20)).get('transmission_state',{}).get('state')=='ALIGNED_DIRECTION_ONLY')
    searly=sig(p,earliest=1800,latest=3600); chk('not_yet_observable',build_transmission(p,searly,act(0.5,end='2026-08-14T12:20:00Z')).get('transmission_state',{}).get('state')=='NOT_YET_OBSERVABLE')
    # Point in time + identity failures
    sbad=sig(p,decl='2026-08-14T12:10:00Z'); chk('posthoc_signature_fail',build_transmission(p,sbad,act(0.5,start='2026-08-14T12:05:00Z')).get('status')=='FAIL_CLOSED')
    sfp=sig(p); sfp['pressure_fingerprint']='bad'; chk('pressure_fingerprint_fail',build_transmission(p,sfp,act(0.5)).get('status')=='FAIL_CLOSED')
    sh=sig(p); sh['active_horizon']='MULTI_DAY_2_10D'; chk('horizon_mismatch_fail',build_transmission(p,sh,act(0.5)).get('status')=='FAIL_CLOSED')
    chk('unit_mismatch_fail',build_transmission(p,s,act(0.5,unit='LOG_RETURN')).get('status')=='FAIL_CLOSED')
    sp=sig(p,method='POST_HOC_PRICE_FIT'); chk('posthoc_method_fail',build_transmission(p,sp,act(0.5)).get('status')=='FAIL_CLOSED')
    semp=sig(p,method='EVENT_CONDITIONED_RANGE',prov='EMPIRICAL'); chk('empirical_without_validation_fail',build_transmission(p,semp,act(0.5)).get('status')=='FAIL_CLOSED')
    semp['validation_ref']='D4-VALID-001'; chk('empirical_with_validation_pass',build_transmission(p,semp,act(0.5)).get('status')=='PASS')
    # Residual/efficiency
    rr=build_transmission(p,s,act(-0.4)); chk('residual_below_expectation',rr.get('counterfactual_residual',{}).get('state')=='BELOW_EXPECTATION')
    chk('efficiency_negative',rr.get('transmission_efficiency',{}).get('class')=='NEGATIVE')
    ra=build_transmission(p,s,act(0.5)); chk('efficiency_expected',ra.get('transmission_efficiency',{}).get('class')=='EXPECTED')
    # Pathways + independence
    rp=build_transmission(p,s,act(0.5)); chk('pathway_coherent',rp.get('pathway_diagnostics',{}).get('state')=='COHERENT',rp.get('pathway_diagnostics'))
    # mechanically linked GC does not add independent group
    chk('target_proxy_not_independent',rp.get('pathway_diagnostics',{}).get('independent_group_count')==3,rp.get('pathway_diagnostics'))
    fragch=[{'channel_id':'US2Y','observed_direction':'UP'},{'channel_id':'REAL10Y','observed_direction':'UP'},{'channel_id':'DXY','observed_direction':'DOWN'},{'channel_id':'GC_PROXY','observed_direction':'UP'}]
    rf=build_transmission(p,s,act(0.5,channels=fragch)); chk('pathway_fragmented',rf.get('pathway_diagnostics',{}).get('state')=='FRAGMENTED',rf.get('pathway_diagnostics'))
    unkch=[{'channel_id':'DXY','observed_direction':'DOWN'}]; ru=build_transmission(p,s,act(0.5,channels=unkch)); chk('pathway_unknown_reduces_coverage',ru.get('pathway_diagnostics',{}).get('coverage')<1 and ru.get('status')=='PASS',ru.get('pathway_diagnostics'))
    # Pressure immutability attack: multiple price paths, identical upstream pressure reference/fingerprint
    r_up=build_transmission(p,s,act(0.6)); r_dn=build_transmission(p,s,act(-0.6));
    chk('pressure_fingerprint_same_across_price_attack',r_up.get('upstream_pressure_reference',{}).get('fingerprint')==r_dn.get('upstream_pressure_reference',{}).get('fingerprint'))
    chk('pressure_class_same_across_price_attack',r_up.get('upstream_pressure_reference',{}).get('class')==r_dn.get('upstream_pressure_reference',{}).get('class')=='BUY_HIGH')
    chk('price_attack_changes_transmission_not_pressure',r_up.get('transmission_state',{}).get('state')!=r_dn.get('transmission_state',{}).get('state'))
    chk('pressure_mutation_false',not r_dn.get('integrity',{}).get('pressure_mutation_detected'))
    # anti-storytelling/future fields
    blob=json.dumps(r_dn,sort_keys=True).lower()
    chk('no_absorption_confirmation','absorption_confirmed' not in blob)
    chk('no_liquidity_grab_confirmation','liquidity_grab_confirmed' not in blob)
    chk('no_unreleased_pressure','unreleased_pressure' not in r_dn)
    chk('no_opposing_move_maturity','opposing_move_maturity' not in r_dn)
    chk('no_release_readiness','release_readiness' not in r_dn)
    chk('no_release_state','release_state' not in r_dn)
    chk('no_trade_permission','trade_permission' not in r_dn)
    # missing driver escalation
    cand=[{'candidate_id':'FUNDING_STRESS','label':'Funding stress'},{'candidate_id':'OPTIONS_MECHANICS','label':'Options/dealer mechanics'}]
    re1=build_transmission(p,s,act(-0.4),divergence_history_count=1,missing_driver_candidates=cand)
    chk('negative_research_escalation',re1.get('missing_driver_escalation',{}).get('level')=='RESEARCH_ESCALATION',re1.get('missing_driver_escalation'))
    chk('candidate_unconfirmed',all(x.get('status')=='UNCONFIRMED' for x in re1.get('missing_driver_escalation',{}).get('candidate_missing_drivers',[])))
    re2=build_transmission(p,s,act(-0.4),divergence_history_count=2,missing_driver_candidates=cand)
    chk('persistent_high_conf_decision_critical',re2.get('missing_driver_escalation',{}).get('level')=='DECISION_CRITICAL',re2.get('missing_driver_escalation'))
    plow=p02(conf='LOW'); slow=sig(plow); relow=build_transmission(plow,slow,act(-0.4),divergence_history_count=3)
    chk('low_pressure_conf_not_decision_critical',relow.get('missing_driver_escalation',{}).get('level')!='DECISION_CRITICAL')
    # qualitative signature residual/efficiency unavailable
    rd=build_transmission(p,sd,act(0.2)); chk('direction_only_no_numeric_residual',rd.get('counterfactual_residual',{}).get('state')=='UNAVAILABLE')
    chk('direction_only_efficiency_unavailable',rd.get('transmission_efficiency',{}).get('class')=='UNAVAILABLE')
    # invalid ranges/timing
    sinv=sig(p); sinv['target_response']['expected_aligned_range']={'low':0.8,'high':0.2}; chk('invalid_range_fail',build_transmission(p,sinv,act(0.5)).get('status')=='FAIL_CLOSED')
    stime=sig(p); stime['target_response']['earliest_material_response_seconds']=2000; stime['target_response']['latest_expected_lag_seconds']=1000; chk('invalid_timing_fail',build_transmission(p,stime,act(0.5)).get('status')=='FAIL_CLOSED')
    # invalid P02
    pb=copy.deepcopy(p); pb['integrity']['status']='FAIL_CLOSED'; chk('bad_p02_fail',build_transmission(pb,s,act(0.5)).get('status')=='FAIL_CLOSED')
    report={'phase':'AD-V2-P03','status':'PASS' if FAIL==0 else 'FAIL','passed':PASS,'failed':FAIL,'checks':DETAIL}
    if a.json_out: Path(a.json_out).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'phase':report['phase'],'status':report['status'],'passed':PASS,'failed':FAIL},indent=2))
    return 0 if FAIL==0 else 1
if __name__=='__main__': raise SystemExit(main())
