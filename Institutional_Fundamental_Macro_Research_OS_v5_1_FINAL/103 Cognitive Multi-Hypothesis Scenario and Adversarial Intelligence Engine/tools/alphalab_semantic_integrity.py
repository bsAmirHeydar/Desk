#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys
H={"MICRO_0_15M","SHORT_15_60M","SESSION_1_6H","DAILY_OPEN_TO_CLOSE","MULTI_DAY_2_10D","SWING_2_8W","CYCLICAL","STRUCTURAL"}
DIRMAP={'BULLISH':{'BULLISH','STRONGLY_BULLISH'},'BEARISH':{'BEARISH','STRONGLY_BEARISH'},'NEUTRAL':{'NEUTRAL'},'UNRESOLVED':{'MIXED','UNDETERMINED'}}
OPTIONAL=['surprise_state','policy_reaction_state','regime_state','causal_graph','reflexivity_state','consumption_state','driver_transition','global_reconciliation']
def fail(errors,msg):errors.append(msg)
def trig_ok(t):
    if not isinstance(t,dict):return False
    mode=t.get('monitor_mode')
    if mode=='MACHINE_PREDICATE':return bool(t.get('metric') and t.get('operator'))
    if mode=='SCHEDULED_TIME':return bool(t.get('time_utc'))
    if mode=='EVENT_RELEASE':return bool(t.get('description'))
    if mode=='MANUAL_OBSERVATION':return bool(t.get('manual_observation'))
    return False
def validate(x,root=None):
    e=[];inst=x.get('instrument');cut=x.get('analysis_cutoff_utc');hor=x.get('active_strategy_horizon');fund=x.get('fundamental_direction');pre=x.get('pre_cognitive_permission')
    app=x.get('cognitive_applicability') or {}
    for k in OPTIONAL:
        ent=app.get(k)
        if not ent:fail(e,'APPLICABILITY_MISSING:'+k);continue
        st=ent.get('status')
        if st=='PRESENT' and k not in x:fail(e,'STATE_MARKED_PRESENT_BUT_MISSING:'+k)
        if st!='PRESENT' and k in x:fail(e,'STATE_PRESENT_BUT_APPLICABILITY_'+str(st)+':'+k)
    hs=x.get('hypothesis_set') or {}
    for name,val in [('instrument',inst),('analysis_cutoff_utc',cut),('active_horizon',hor)]:
        if hs.get(name)!=val:fail(e,'HYPOTHESIS_SET_'+name.upper()+'_MISMATCH')
    hyps=hs.get('hypotheses') or [];ids=[h.get('hypothesis_id') for h in hyps];idset=set(ids)
    if len(ids)!=len(idset):fail(e,'DUPLICATE_HYPOTHESIS_ID')
    dom=hs.get('dominant_hypothesis_ids') or [];chal=hs.get('strongest_challenger_ids') or [];tour=hs.get('tournament_state')
    for z in dom+chal:
        if z not in idset:fail(e,'UNKNOWN_TOURNAMENT_HYPOTHESIS_ID:'+str(z))
    if set(dom)&set(chal):fail(e,'DOMINANT_AND_CHALLENGER_OVERLAP')
    if tour=='DOMINANT' and len(dom)!=1:fail(e,'DOMINANT_STATE_REQUIRES_EXACTLY_ONE_DOMINANT')
    if tour=='CO_DOMINANT' and len(dom)<2:fail(e,'CO_DOMINANT_REQUIRES_AT_LEAST_TWO_DOMINANT')
    if tour in {'NO_CREDIBLE_DOMINANT_HYPOTHESIS','INSUFFICIENT_EVIDENCE'} and dom:fail(e,'NO_DOMINANT_STATE_CANNOT_HAVE_DOMINANT_IDS')
    # evidence traceability and trigger monitorability
    for h in hyps:
        for fld,role in [('supporting_evidence','SUPPORT'),('contradicting_evidence','CONTRADICT'),('missing_evidence','MISSING')]:
            for ev in h.get(fld) or []:
                if ev.get('role')!=role:fail(e,f'EVIDENCE_ROLE_MISMATCH:{h.get("hypothesis_id")}:{fld}')
                if ev.get('materiality') in {'DECISION_CRITICAL','MATERIAL'} and ev.get('lineage_status') not in {'TRACEABLE','PARTIAL'}:fail(e,'LOAD_BEARING_EVIDENCE_UNTRACEABLE:'+str(ev.get('evidence_id')))
                if ev.get('horizon') not in H:fail(e,'BAD_EVIDENCE_HORIZON:'+str(ev.get('evidence_id')))
        for fld in ['confirmation_triggers','invalidation_triggers']:
            for t in h.get(fld) or []:
                if t.get('materiality') in {'DECISION_CRITICAL','MATERIAL'} and not trig_ok(t):fail(e,'UNMONITORABLE_HYPOTHESIS_TRIGGER:'+str(t.get('trigger_id')))
    # active horizon tensor must agree with Fundamental top direction
    ht=x.get('horizon_tensor') or {}
    if ht.get('active_strategy_horizon')!=hor:fail(e,'HORIZON_TENSOR_ACTIVE_HORIZON_MISMATCH')
    ast=[s for s in ht.get('states') or [] if s.get('horizon')==hor]
    if len(ast)!=1:fail(e,'ACTIVE_HORIZON_REQUIRES_EXACTLY_ONE_STATE')
    elif fund in DIRMAP and ast[0].get('fundamental_direction') not in DIRMAP[fund]:fail(e,'FUNDAMENTAL_DIRECTION_ACTIVE_HORIZON_MISMATCH')
    # unique uncertainty dimensions + explicit critical list sync
    up=x.get('uncertainty_profile') or {}; dims=[u.get('dimension') for u in up.get('dimensions') or []]
    if len(dims)!=len(set(dims)):fail(e,'DUPLICATE_UNCERTAINTY_DIMENSION')
    crit=sorted({u.get('dimension') for u in up.get('dimensions') or [] if u.get('level')=='DECISION_CRITICAL'})
    if sorted(up.get('decision_critical_dimensions') or [])!=crit:fail(e,'DECISION_CRITICAL_UNCERTAINTY_LIST_MISMATCH')
    # scenario integrity
    st=x.get('scenario_tree') or {}
    if st.get('active_horizon')!=hor:fail(e,'SCENARIO_ACTIVE_HORIZON_MISMATCH')
    if st.get('as_of_utc')!=cut:fail(e,'SCENARIO_CUTOFF_MISMATCH')
    scenarios=st.get('scenarios') or [];sids=[s.get('scenario_id') for s in scenarios]
    if len(sids)!=len(set(sids)):fail(e,'DUPLICATE_SCENARIO_ID')
    if len(scenarios)==1 and not st.get('single_scenario_justification'):fail(e,'SINGLE_SCENARIO_REQUIRES_JUSTIFICATION')
    prim=[s for s in scenarios if s.get('plausibility_band')=='PRIMARY']
    if st.get('tree_state')=='PRIMARY_SCENARIO_IDENTIFIED' and len(prim)!=1:fail(e,'PRIMARY_TREE_REQUIRES_EXACTLY_ONE_PRIMARY')
    pmode=st.get('probability_mode')
    probs=[]
    for s in scenarios:
        if s.get('horizon')!=hor:fail(e,'SCENARIO_HORIZON_MISMATCH:'+str(s.get('scenario_id')))
        for hid in s.get('source_hypothesis_ids') or []:
            if hid not in idset:fail(e,'SCENARIO_UNKNOWN_HYPOTHESIS:'+str(hid))
        for fld in ['confirmation_triggers','invalidation_triggers']:
            for t in s.get(fld) or []:
                if t.get('materiality') in {'DECISION_CRITICAL','MATERIAL'} and not trig_ok(t):fail(e,'UNMONITORABLE_SCENARIO_TRIGGER:'+str(t.get('trigger_id')))
        for tr in s.get('transition_paths') or []:
            if tr.get('to_scenario_id') not in set(sids):fail(e,'SCENARIO_TRANSITION_UNKNOWN_TARGET:'+str(tr.get('to_scenario_id')))
            if not trig_ok(tr.get('trigger') or {}):fail(e,'UNMONITORABLE_SCENARIO_TRANSITION:'+str(s.get('scenario_id')))
        p=s.get('calibrated_probability')
        if p is not None:probs.append(float(p))
        imp=s.get('permission_implication');sd=s.get('direction')
        if pre=='BUY' and imp=='SUPPORT_EXISTING' and sd not in {'BULLISH','STRONGLY_BULLISH'}:fail(e,'SCENARIO_PERMISSION_DIRECTION_INCONSISTENT:'+str(s.get('scenario_id')))
        if pre=='SELL' and imp=='SUPPORT_EXISTING' and sd not in {'BEARISH','STRONGLY_BEARISH'}:fail(e,'SCENARIO_PERMISSION_DIRECTION_INCONSISTENT:'+str(s.get('scenario_id')))
        if pre=='NO_TRADE' and imp=='SUPPORT_EXISTING':fail(e,'NO_TRADE_SCENARIO_CANNOT_SUPPORT_EXISTING_PERMISSION:'+str(s.get('scenario_id')))
    if pmode=='QUALITATIVE' and probs:fail(e,'QUALITATIVE_SCENARIOS_CANNOT_HAVE_NUMERIC_PROBABILITIES')
    if pmode=='CALIBRATED':
        if not st.get('calibration_record_id'):fail(e,'CALIBRATED_SCENARIOS_REQUIRE_CALIBRATION_RECORD')
        if len(probs)!=len(scenarios):fail(e,'CALIBRATED_SCENARIOS_REQUIRE_ALL_PROBABILITIES')
        elif abs(sum(probs)-1.0)>0.01:fail(e,'CALIBRATED_SCENARIO_PROBABILITIES_MUST_SUM_TO_ONE')
    # Regime dimension vocabulary
    if app.get('regime_state',{}).get('status')=='PRESENT':
        rp={}
        if root:
            q=Path(root)/'103 Cognitive Multi-Hypothesis Scenario and Adversarial Intelligence Engine/config/regime_policy.json'
            if q.exists():rp=json.loads(q.read_text()).get('dimension_state_map') or {}
        for d in (x.get('regime_state') or {}).get('dimensions') or []:
            allowed=rp.get(d.get('dimension'))
            if allowed and d.get('state') not in allowed:fail(e,'REGIME_STATE_INVALID_FOR_DIMENSION:'+str(d.get('dimension'))+':'+str(d.get('state')))
    # Causal graph refs and semantic edges
    if app.get('causal_graph',{}).get('status')=='PRESENT':
        g=x.get('causal_graph') or {}
        if g.get('horizon')!=hor:fail(e,'CAUSAL_GRAPH_HORIZON_MISMATCH')
        if g.get('as_of_utc')!=cut:fail(e,'CAUSAL_GRAPH_CUTOFF_MISMATCH')
        nids={n.get('node_id') for n in g.get('nodes') or []}
        for ed in g.get('edges') or []:
            if ed.get('from_node') not in nids or ed.get('to_node') not in nids:fail(e,'CAUSAL_EDGE_UNKNOWN_NODE:'+str(ed.get('edge_id')))
    # policy cutoff
    if app.get('policy_reaction_state',{}).get('status')=='PRESENT' and (x.get('policy_reaction_state') or {}).get('as_of_utc')!=cut:fail(e,'POLICY_REACTION_CUTOFF_MISMATCH')
    # premortem monitorability assertion must be backed by trigger
    pm=x.get('premortem') or {}
    for fp in pm.get('failure_paths') or []:
        if fp.get('monitorable') and not trig_ok(fp.get('early_warning_trigger') or {}):fail(e,'PREMORTEM_MONITORABLE_WITHOUT_VALID_TRIGGER:'+str(fp.get('failure_id')))
    return e

def main():
    p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--vault-root');a=p.parse_args();x=json.loads(Path(a.input).read_text(encoding='utf-8'));e=validate(x,a.vault_root);print(json.dumps({'status':'PASS' if not e else 'FAIL','errors':e},indent=2,ensure_ascii=False));return 0 if not e else 2
if __name__=='__main__':raise SystemExit(main())
