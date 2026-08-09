#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys,subprocess
p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--output',required=True);p.add_argument('--vault-root');p.add_argument('--evidence-pack');p.add_argument('--require-evidence-pack',action='store_true');p.add_argument('--d4-ledger');a=p.parse_args();mod=Path(__file__).resolve().parent.parent;root=Path(a.vault_root).resolve() if a.vault_root else mod.parent
cmd=[sys.executable,str(mod/'tools/alphalab_semantic_integrity.py'),'--input',a.input,'--vault-root',str(root)]
if a.evidence_pack:cmd += ['--evidence-pack',a.evidence_pack]
if a.require_evidence_pack:cmd += ['--require-evidence-pack']
if a.d4_ledger:cmd += ['--d4-ledger',a.d4_ledger]
q=subprocess.run(cmd,capture_output=True,text=True)
if q.returncode:raise SystemExit('SEMANTIC_INTEGRITY_FAILED: '+q.stdout.strip())
x=json.loads(Path(a.input).read_text(encoding='utf-8'));pre=x['pre_cognitive_permission'];fund=x['fundamental_direction'];final=pre;constraints=[];state='CLEAR';app=x.get('cognitive_applicability') or {};exceptions={z.get('invariant_id') for z in x.get('propagation_exceptions') or [] if isinstance(z,dict)}
if fund not in {'BULLISH','BEARISH'} and pre in {'BUY','SELL'}:final='NO_TRADE';constraints.append('NON_DIRECTIONAL_FUNDAMENTAL_CANNOT_CARRY_PERMISSION');state='INSUFFICIENT_EVIDENCE'
tour=x['hypothesis_set'].get('tournament_state')
if tour in {'CONTESTED','FRAGMENTED','NO_CREDIBLE_DOMINANT_HYPOTHESIS','INSUFFICIENT_EVIDENCE'}:
    critical=x['hypothesis_set'].get('decision_critical_conflicts') or []
    if critical or tour in {'NO_CREDIBLE_DOMINANT_HYPOTHESIS','INSUFFICIENT_EVIDENCE'}:final='NO_TRADE';constraints.append('DECISION_CRITICAL_HYPOTHESIS_CONTEST');state='CONTESTED' if tour!='INSUFFICIENT_EVIDENCE' else 'INSUFFICIENT_EVIDENCE'
    elif state=='CLEAR':state='CONSTRAINED'
critical_dims=sorted({u.get('dimension') for u in x['uncertainty_profile'].get('dimensions') or [] if u.get('level')=='DECISION_CRITICAL'})
if critical_dims:final='NO_TRADE';constraints.append('DECISION_CRITICAL_UNCERTAINTY:'+','.join(critical_dims));state='INSUFFICIENT_EVIDENCE'
md=x['model_disagreement'];um=md.get('unmodeled_driver_risk')
if um=='DECISION_CRITICAL' or md.get('action')=='HOLD_NO_TRADE':final='NO_TRADE';constraints.append('UNMODELED_DRIVER_RISK');state='MODEL_DISAGREEMENT'
elif um=='HIGH' and final!='NO_TRADE':constraints.append('HIGH_UNMODELED_DRIVER_EARLY_REVIEW');state='CONSTRAINED'
adv=x['adversarial_review'].get('adjudication')
if adv in {'REJECTED','INSUFFICIENT_EVIDENCE'}:final='NO_TRADE';constraints.append('ADVERSARIAL_REVIEW_'+adv);state='INSUFFICIENT_EVIDENCE'
elif adv=='CONTESTED' and final!='NO_TRADE':final='NO_TRADE';constraints.append('ADVERSARIAL_CONTEST');state='CONTESTED'
elif adv=='THESIS_SURVIVES_CONSTRAINED' and state=='CLEAR':state='CONSTRAINED'
if x['premortem'].get('unmonitorable_decision_critical_risk') is True:final='NO_TRADE';constraints.append('UNMONITORABLE_DECISION_CRITICAL_RISK');state='INSUFFICIENT_EVIDENCE'
ut=x['decision_utility'].get('utility_state')
if ut=='FAVOR_NO_TRADE':final='NO_TRADE';constraints.append('UTILITY_FAVORS_NO_TRADE');state='CONSTRAINED' if state=='CLEAR' else state
elif ut=='FAVOR_DELAY' and final!='NO_TRADE':final='NO_TRADE';constraints.append('UTILITY_FAVORS_DELAY');state='DELAYED'
elif ut=='CONTESTED' and state=='CLEAR':state='CONSTRAINED'
ss=x['scenario_tree'].get('tree_state')
if ss in {'CONTESTED','FRAGMENTED','INSUFFICIENT_EVIDENCE'} and final!='NO_TRADE':constraints.append('SCENARIO_TREE_'+ss);state='MULTI_SCENARIO_CLEAR' if ss=='CONTESTED' else 'CONSTRAINED'
elif ss=='MULTIPLE_COMPETITIVE' and state=='CLEAR':state='MULTI_SCENARIO_CLEAR'
# Defense-in-depth: important upstream states cannot be silently ignored. Semantic validator allows explicit exceptions.
def constrain(code,hard=False,newstate='CONSTRAINED'):
    global final,state
    if code in exceptions:return
    constraints.append(code)
    if hard:final='NO_TRADE'
    if state=='CLEAR' or hard:state=newstate
if app.get('causal_graph',{}).get('status')=='PRESENT' and (x.get('causal_graph') or {}).get('graph_state')=='BROKEN':constrain('CAUSAL_GRAPH_BROKEN',True,'CONTESTED')
if app.get('global_reconciliation',{}).get('status')=='PRESENT' and (x.get('global_reconciliation') or {}).get('state')=='INCONSISTENT':constrain('GLOBAL_RECONCILIATION_INCONSISTENT',False,'CONSTRAINED')
if app.get('consumption_state',{}).get('status')=='PRESENT' and (x.get('consumption_state') or {}).get('remaining_asymmetry') in {'VERY_POOR','POOR'}:constrain('REMAINING_ASYMMETRY_POOR',False,'CONSTRAINED')
if app.get('driver_transition',{}).get('status')=='PRESENT' and (x.get('driver_transition') or {}).get('state') in {'TAKEOVER','FRAGMENTED'}:constrain('DRIVER_TRANSITION_MATERIAL',False,'CONSTRAINED')
if app.get('regime_state',{}).get('status')=='PRESENT':
    rg=x.get('regime_state') or {}
    if rg.get('mapping_stability')=='BROKEN' or rg.get('structural_break_risk') in {'HIGH','VERY_HIGH'}:constrain('REGIME_MAPPING_UNSTABLE',False,'CONSTRAINED')
if pre=='NO_TRADE' and final!='NO_TRADE':raise SystemExit('SAFETY_NEW_PERMISSION_CREATED')
if pre in {'BUY','SELL'} and final not in {pre,'NO_TRADE'}:raise SystemExit('SAFETY_DIRECTION_FLIP')
outside=x['meta_edge_router'].get('outside_strategy_edges') or []

def manual(trigger_id,description,materiality='MATERIAL'):
    return {'trigger_id':trigger_id,'description':description,'monitor_mode':'MANUAL_OBSERVATION','materiality':materiality,'manual_observation':description,'response':'REVIEW'}
# Preserve structured triggers to the final adapter. Pick the most decision-material available trigger; scheduler can later optimize timing.
candidates=[]
if md.get('action') in {'EARLY_REVIEW','RESEARCH_ESCALATION'}:candidates.append(manual('MODEL_DISAGREEMENT_'+md.get('action'),'Model disagreement '+md.get('action'),'DECISION_CRITICAL' if um=='DECISION_CRITICAL' else 'MATERIAL'))
for t in x['hypothesis_set'].get('resolution_observations') or []:
    if isinstance(t,dict):candidates.append(t)
if app.get('driver_transition',{}).get('status')=='PRESENT':
    t=(x.get('driver_transition') or {}).get('next_resolution_trigger')
    if isinstance(t,dict):candidates.append(t)
if app.get('policy_reaction_state',{}).get('status')=='PRESENT':
    pr=x.get('policy_reaction_state') or {}
    states=pr.get('states') if 'mode' in pr else [pr]
    for ps in states or []:
        t=ps.get('next_reassessment_trigger')
        if isinstance(t,dict):candidates.append(t)
for s in x.get('scenario_tree',{}).get('scenarios') or []:
    candidates.extend([t for t in (s.get('invalidation_triggers') or []) if isinstance(t,dict)])
for fp in x.get('premortem',{}).get('failure_paths') or []:
    t=fp.get('early_warning_trigger')
    if isinstance(t,dict) and t.get('materiality') in {'DECISION_CRITICAL','MATERIAL'}:candidates.append(t)
rank={'DECISION_CRITICAL':0,'MATERIAL':1,'SUPPORTING':2,'CONTEXTUAL':3}
candidates=sorted(candidates,key=lambda t:rank.get(t.get('materiality'),9))
next_review=candidates[0] if candidates else manual('NEXT_DECISION_MATERIAL_CAUSAL_TRIGGER','Next decision-material causal trigger')
rescue=bool(pre=='NO_TRADE' and fund in {'BULLISH','BEARISH'} and tour in {'DOMINANT','CO_DOMINANT'} and not critical_dims and um not in {'HIGH','DECISION_CRITICAL'} and adv in {'THESIS_SURVIVES','THESIS_SURVIVES_CONSTRAINED'} and ut=='FAVOR_ACTION')
out={'version':'1.2.0','instrument':x['instrument'],'analysis_cutoff_utc':x['analysis_cutoff_utc'],'active_strategy_horizon':x['active_strategy_horizon'],'fundamental_direction':fund,'final_direction':fund,'pre_cognitive_permission':pre,'cognitive_permission':final,'cognitive_state':state,'tournament_state':tour,'scenario_state':ss,'decision_critical_uncertainties':critical_dims,'unmodeled_driver_risk':um or 'UNDETERMINED','adversarial_adjudication':adv or 'INSUFFICIENT_EVIDENCE','utility_state':ut or 'UNDETERMINED','applied_cognitive_constraints':sorted(set(constraints)),'outside_strategy_edges':outside,'next_review_trigger':next_review,'cognitive_rescue_candidate':rescue,'direction_flip_forbidden':True,'positive_permission_creation_forbidden':True}
Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf-8');print(json.dumps(out,ensure_ascii=False))
