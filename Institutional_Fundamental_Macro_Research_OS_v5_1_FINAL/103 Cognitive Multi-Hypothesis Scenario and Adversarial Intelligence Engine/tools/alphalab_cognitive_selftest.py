#!/usr/bin/env python3
from pathlib import Path
import json, subprocess, sys, tempfile
R=Path(__file__).resolve().parents[2]
M=R/'103 Cognitive Multi-Hypothesis Scenario and Adversarial Intelligence Engine'
T=M/'tools'
checks=[]
def ck(name,cond,detail=None): checks.append({'name':name,'pass':bool(cond),'detail':detail})
def run(args):
    q=subprocess.run([sys.executable,*map(str,args)],capture_output=True,text=True)
    return q.returncode,q.stdout,q.stderr
m=json.loads((R/'CURRENT_PRODUCTION_MANIFEST.json').read_text(encoding='utf-8'))
ch=m.get('cognitive_hardening') or {}
ck('stack_v21',m.get('current_stack')=='V21.0.0',m.get('current_stack'))
ck('direction_fundamental_only',m.get('decision_authority',{}).get('direction')=='FUNDAMENTAL_ONLY',m.get('decision_authority'))
ck('cognitive_enforced',ch.get('authority_mode')=='ENFORCED_COGNITIVE_HARDENING',ch)
ck('no_cognitive_direction_flip',ch.get('direction_flip_allowed') is False,ch)
ck('no_cognitive_positive_permission',ch.get('positive_permission_creation') is False,ch)
ck('market_price_diagnostic_only',ch.get('market_price_direction_authority') is False and ch.get('market_price_model_diagnostic') is True,ch)
ck('qualitative_scenarios',ch.get('scenario_probability_mode')=='QUALITATIVE_UNLESS_D4_CALIBRATED',ch)

def h(hid,title,fam='POLICY_REACTION',pl='DOMINANT'):
    return {'hypothesis_id':hid,'title':title,'family':fam,'mechanism':'observed fact changes policy/transmission path','root_ids':[hid+'_ROOT'],'target_horizons':['SESSION_1_6H'],'direction_by_horizon':{'SESSION_1_6H':'BULLISH' if hid=='H1' else 'BEARISH'},'supporting_evidence':['F1'],'contradicting_evidence':[],'missing_evidence':['WATCH1'],'expected_leaders':['US2Y'],'expected_market_signatures':['rates lead'],'confirmation_triggers':['US2Y confirms'],'invalidation_triggers':['US2Y reverses'],'regime_dependencies':['NORMAL'],'reflexive_loops':[],'plausibility_band':pl,'evidence_quality':'HIGH','causal_coherence':'HIGH','materiality':'MATERIAL','outside_fundamental_strategy':False}

def sc(sid,role,hid,direction,pl):
    other='S2' if sid=='S1' else 'S1'
    return {'scenario_id':sid,'role':role,'source_hypothesis_ids':[hid],'plausibility_band':pl,'horizon':'SESSION_1_6H','direction':direction,'required_conditions':['condition holds'],'early_indicators':['leader confirms'],'confirmation_triggers':['confirm observable'],'invalidation_triggers':['invalidate observable'],'expected_leaders':['US2Y'],'expected_market_signature':['cross asset confirms'],'permission_implication':'SUPPORT_EXISTING' if direction=='BULLISH' else 'CONSTRAIN_EXISTING','transition_paths':[{'to_scenario_id':other,'trigger':'opposite leader trigger'}]}

def base_input(pre='BUY',fund='BULLISH'):
    return {
      'version':'1.0.0','instrument':'NASDAQ100','analysis_cutoff_utc':'2026-08-08T12:00:00Z','active_strategy_horizon':'SESSION_1_6H','fundamental_direction':fund,'pre_cognitive_permission':pre,
      'hypothesis_set':{'version':'1.0.0','instrument':'NASDAQ100','analysis_cutoff_utc':'2026-08-08T12:00:00Z','active_horizon':'SESSION_1_6H','hypotheses':[h('H1','Dovish transmission'),h('H2','Growth scare','GROWTH','COMPETITIVE')],'tournament_state':'DOMINANT','dominant_hypothesis_ids':['H1'],'strongest_challenger_ids':['H2'],'single_hypothesis_justification':None,'decision_critical_conflicts':[],'resolution_observations':['US2Y path']},
      'horizon_tensor':{'version':'1.0.0','active_strategy_horizon':'SESSION_1_6H','states':[{'horizon':'SESSION_1_6H','fundamental_direction':'BULLISH','force_band':'HIGH','persistence_class':'SESSION','consumption_band':'MODERATE','remaining_asymmetry':'FAVORABLE','reversal_hazard':'MODERATE','causal_leader':'US2Y','next_update_trigger':'US2Y reversal'}],'cross_horizon_conflict_state':'ALIGNED','direction_authority':'MODULE_89_FUNDAMENTAL_HORIZON_STATE_ONLY'},
      'uncertainty_profile':{'dimensions':[{'dimension':'CAUSAL','level':'MODERATE','reason':'challenger exists','resolution_condition':'leader divergence resolves'}],'decision_critical_dimensions':[],'single_confidence_score_used':False},
      'scenario_tree':{'version':'1.0.0','as_of_utc':'2026-08-08T12:00:00Z','active_horizon':'SESSION_1_6H','tree_state':'PRIMARY_SCENARIO_IDENTIFIED','scenarios':[sc('S1','BASE','H1','BULLISH','PRIMARY'),sc('S2','ADVERSE','H2','BEARISH','COMPETITIVE')],'numeric_probabilities_used':False},
      'model_disagreement':{'disagreement_level':'LOW','unmodeled_driver_risk':'LOW','expected_signatures':['rates lead'],'observed_contradictions':[],'candidate_missing_drivers':[],'price_used_as_direction_authority':False,'action':'NONE'},
      'adversarial_review':{'builder_thesis':'dovish transmission leads','destroyer_findings':['growth scare challenger'],'strongest_rival_hypothesis_id':'H2','strongest_contradictory_fact':None,'same_root_double_count_risks':[],'missing_driver_candidates':[],'market_signature_contradictions':[],'post_hoc_rationalization_risk':'LOW','falsification_conditions':['US2Y reverses'],'adjudication':'THESIS_SURVIVES'},
      'premortem':{'assumed_action':pre if pre!='NO_TRADE' else 'NO_TRADE','failure_paths':[{'failure_id':'F1','mechanism':'rates reversal','early_warning':'US2Y rises','monitorable':True,'response':'block'},{'failure_id':'F2','mechanism':'flow reversal','early_warning':'identified selling','monitorable':True,'response':'block'},{'failure_id':'F3','mechanism':'driver transition','early_warning':'growth channel dominates','monitorable':True,'response':'review'}],'unmonitorable_decision_critical_risk':False,'unmonitorable_risk_notes':[]},
      'decision_utility':{'dimensions':[{'dimension':'UPSIDE_POTENTIAL','band':'HIGH','reason':'remaining asymmetry'}],'utility_state':'FAVOR_ACTION','numeric_expected_utility_used':False},
      'meta_edge_router':{'primary_edge_class':'FUNDAMENTAL_EDGE','detected_edges':['FUNDAMENTAL_EDGE'],'fundamental_strategy_edge_class':'FUNDAMENTAL_EDGE','outside_strategy_edges':[],'outside_strategy_permission_effect':'NONE','research_routes':[]},
      'complexity_class':'PROPORTIONATE','load_bearing_root_ids':['H1_ROOT'],'non_load_bearing_context':['H2_ROOT']}

with tempfile.TemporaryDirectory() as td0:
    td=Path(td0); ip=td/'input.json'; op=td/'out.json'
    x=base_input(); ip.write_text(json.dumps(x),encoding='utf-8')
    rc,so,se=run([T/'alphalab_cognitive_validate.py','--input',ip]); ck('valid_multihypothesis_input',rc==0,so+se)
    rc,so,se=run([T/'alphalab_cognitive_adjudicate.py','--input',ip,'--output',op]); z=json.loads(op.read_text()); ck('clear_case_preserves_buy',rc==0 and z['cognitive_permission']=='BUY' and z['final_direction']=='BULLISH',z)
    # Scenario validator
    sp=td/'scenario.json';sp.write_text(json.dumps(x['scenario_tree']),encoding='utf-8');rc,so,se=run([T/'alphalab_scenario_validate.py','--input',sp]);ck('scenario_tree_valid',rc==0,so+se)
    # Critical hypothesis contest fail-closed.
    x=base_input();x['hypothesis_set']['tournament_state']='CONTESTED';x['hypothesis_set']['decision_critical_conflicts']=['policy vs growth materially unresolved'];ip.write_text(json.dumps(x),encoding='utf-8');run([T/'alphalab_cognitive_adjudicate.py','--input',ip,'--output',op]);z=json.loads(op.read_text());ck('critical_contest_no_trade',z['cognitive_permission']=='NO_TRADE' and z['cognitive_state']=='CONTESTED',z)
    # Critical model disagreement fail-closed but direction stays fundamental.
    x=base_input();x['model_disagreement']['unmodeled_driver_risk']='DECISION_CRITICAL';x['model_disagreement']['action']='HOLD_NO_TRADE';ip.write_text(json.dumps(x),encoding='utf-8');run([T/'alphalab_cognitive_adjudicate.py','--input',ip,'--output',op]);z=json.loads(op.read_text());ck('unmodeled_driver_no_trade_no_flip',z['cognitive_permission']=='NO_TRADE' and z['final_direction']=='BULLISH',z)
    # Outside-strategy forced flow can be detected but cannot create a trade.
    x=base_input(pre='NO_TRADE',fund='NEUTRAL');x['meta_edge_router']={'primary_edge_class':'FORCED_FLOW_EDGE','detected_edges':['FORCED_FLOW_EDGE'],'fundamental_strategy_edge_class':'NO_EDGE','outside_strategy_edges':['FORCED_FLOW_EDGE'],'outside_strategy_permission_effect':'NONE','research_routes':['SEPARATE_FLOW_STRATEGY_RESEARCH']};ip.write_text(json.dumps(x),encoding='utf-8');run([T/'alphalab_cognitive_adjudicate.py','--input',ip,'--output',op]);z=json.loads(op.read_text());ck('outside_strategy_edge_report_only',z['cognitive_permission']=='NO_TRADE' and 'FORCED_FLOW_EDGE' in z['outside_strategy_edges'],z)
    # Unmonitorable critical pre-mortem risk blocks.
    x=base_input();x['premortem']['unmonitorable_decision_critical_risk']=True;x['premortem']['unmonitorable_risk_notes']=['unknown geopolitical source'];ip.write_text(json.dumps(x),encoding='utf-8');run([T/'alphalab_cognitive_adjudicate.py','--input',ip,'--output',op]);z=json.loads(op.read_text());ck('premortem_unmonitorable_blocks',z['cognitive_permission']=='NO_TRADE',z)
    # Numeric scenario probabilities are refused.
    x=base_input();x['scenario_tree']['numeric_probabilities_used']=True;ip.write_text(json.dumps(x),encoding='utf-8');rc,so,se=run([T/'alphalab_cognitive_validate.py','--input',ip]);ck('fake_probability_rejected',rc!=0,so+se)
    # Global reconciler detects explicit same-root incompatible claims without changing directions.
    gp=td/'global.json';gout=td/'global_out.json';gp.write_text(json.dumps({'market_intents':[{'instrument':'NASDAQ100','direction':'BULLISH','implied_root_ids':['FED'],'root_direction_claims':[{'root_id':'FED','root_state':'DOVISH'}]},{'instrument':'SP500','direction':'BULLISH','implied_root_ids':['FED'],'root_direction_claims':[{'root_id':'FED','root_state':'HAWKISH'}]}]}),encoding='utf-8');rc,so,se=run([T/'alphalab_global_reconcile.py','--input',gp,'--output',gout]);gz=json.loads(gout.read_text());ck('global_reconcile_detects_inconsistency',rc==0 and gz['state']=='INCONSISTENT' and gz['direction_override_applied'] is False,gz)
    # Causal recheck scheduler selects earliest decision-material trigger.
    rp=td/'review.json';rout=td/'review_out.json';rp.write_text(json.dumps({'candidate_triggers':[{'trigger_type':'EVENT','condition':'CPI','time_utc':'2026-08-08T13:30:00Z','materiality':'DECISION_CRITICAL'},{'trigger_type':'FIXING','condition':'fix','time_utc':'2026-08-08T14:00:00Z','materiality':'MATERIAL'}]}),encoding='utf-8');rc,so,se=run([T/'alphalab_recheck_schedule.py','--input',rp,'--output',rout]);rz=json.loads(rout.read_text());ck('causal_recheck_scheduler',rc==0 and rz['next_review_trigger']['condition']=='CPI',rz)

# Acceptance inventory itself must remain broad.
acc=json.loads((M/'validation/V21_Cognitive_Acceptance_Cases.json').read_text(encoding='utf-8'))
ck('acceptance_case_count',len(acc.get('cases',[]))>=14,len(acc.get('cases',[])))
required_topics={'COMPETING_HYPOTHESES','CROSS_HORIZON','SURPRISE','SAME_ROOT_MULTI_CHANNEL','MODEL_DISAGREEMENT','OUTSIDE_STRATEGY','CRITICAL_UNCERTAINTY','SCENARIO_TREE','ADVERSARIAL','PREMORTEM','GLOBAL_RECONCILIATION','EVENT_DRIVER_TRANSITION'}
topics={c.get('topic') for c in acc.get('cases',[])}
ck('acceptance_topic_breadth',required_topics.issubset(topics),sorted(topics))
failed=[c for c in checks if not c['pass']]
print(json.dumps({'status':'PASS' if not failed else 'FAIL','tests':len(checks),'passed':len(checks)-len(failed),'checks':checks},indent=2,ensure_ascii=False))
sys.exit(0 if not failed else 2)
