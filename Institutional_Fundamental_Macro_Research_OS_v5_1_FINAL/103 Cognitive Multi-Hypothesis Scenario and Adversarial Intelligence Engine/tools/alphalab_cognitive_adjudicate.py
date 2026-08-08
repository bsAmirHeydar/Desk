#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys,subprocess
p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--output',required=True);p.add_argument('--vault-root');a=p.parse_args();mod=Path(__file__).resolve().parent.parent;root=Path(a.vault_root).resolve() if a.vault_root else mod.parent
q=subprocess.run([sys.executable,str(mod/'tools/alphalab_semantic_integrity.py'),'--input',a.input,'--vault-root',str(root)],capture_output=True,text=True)
if q.returncode:raise SystemExit('SEMANTIC_INTEGRITY_FAILED: '+q.stdout.strip())
x=json.loads(Path(a.input).read_text(encoding='utf-8'));pre=x['pre_cognitive_permission'];fund=x['fundamental_direction'];final=pre;constraints=[];state='CLEAR'
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
if pre=='NO_TRADE' and final!='NO_TRADE':raise SystemExit('SAFETY_NEW_PERMISSION_CREATED')
if pre in {'BUY','SELL'} and final not in {pre,'NO_TRADE'}:raise SystemExit('SAFETY_DIRECTION_FLIP')
outside=x['meta_edge_router'].get('outside_strategy_edges') or []
# Valid review candidates only. NONE is a state, not a trigger.
candidates=[]
if md.get('action') in {'EARLY_REVIEW','RESEARCH_ESCALATION'}:candidates.append('MODEL_DISAGREEMENT_'+md.get('action'))
for t in x['hypothesis_set'].get('resolution_observations') or []:
 if isinstance(t,dict) and t.get('description'):candidates.append(t['description'])
next_review=candidates[0] if candidates else 'NEXT_DECISION_MATERIAL_CAUSAL_TRIGGER'
rescue=bool(pre=='NO_TRADE' and fund in {'BULLISH','BEARISH'} and tour in {'DOMINANT','CO_DOMINANT'} and not critical_dims and um not in {'HIGH','DECISION_CRITICAL'} and adv in {'THESIS_SURVIVES','THESIS_SURVIVES_CONSTRAINED'} and ut=='FAVOR_ACTION')
out={'version':'1.1.0','instrument':x['instrument'],'analysis_cutoff_utc':x['analysis_cutoff_utc'],'active_strategy_horizon':x['active_strategy_horizon'],'fundamental_direction':fund,'final_direction':fund,'pre_cognitive_permission':pre,'cognitive_permission':final,'cognitive_state':state,'tournament_state':tour,'scenario_state':ss,'decision_critical_uncertainties':critical_dims,'unmodeled_driver_risk':um or 'UNDETERMINED','adversarial_adjudication':adv or 'INSUFFICIENT_EVIDENCE','utility_state':ut or 'UNDETERMINED','applied_cognitive_constraints':constraints,'outside_strategy_edges':outside,'next_review_trigger':next_review,'cognitive_rescue_candidate':rescue,'direction_flip_forbidden':True,'positive_permission_creation_forbidden':True}
Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf-8');print(json.dumps(out,ensure_ascii=False))
