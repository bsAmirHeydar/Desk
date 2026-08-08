#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys
p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--output',required=True);a=p.parse_args()
x=json.loads(Path(a.input).read_text(encoding='utf-8'))
req=['version','instrument','analysis_cutoff_utc','active_strategy_horizon','fundamental_direction','pre_cognitive_permission','hypothesis_set','horizon_tensor','uncertainty_profile','scenario_tree','model_disagreement','adversarial_review','premortem','decision_utility','meta_edge_router']
miss=[k for k in req if k not in x]
if miss:raise SystemExit('MISSING_REQUIRED: '+','.join(miss))
if x.get('version')!='1.0.0':raise SystemExit('BAD_VERSION')
pre=x['pre_cognitive_permission'];fund=x['fundamental_direction'];final=pre;constraints=[];state='CLEAR'
# Direction can never be changed here.
if fund not in {'BULLISH','BEARISH'} and pre in {'BUY','SELL'}:
    final='NO_TRADE';constraints.append('NON_DIRECTIONAL_FUNDAMENTAL_CANNOT_CARRY_PERMISSION');state='INSUFFICIENT_EVIDENCE'
# Competing-hypothesis gate.
tour=(x.get('hypothesis_set') or {}).get('tournament_state')
if tour in {'CONTESTED','FRAGMENTED','NO_CREDIBLE_DOMINANT_HYPOTHESIS','INSUFFICIENT_EVIDENCE'}:
    # Material contest is a hold; contextual contest may be represented outside the load-bearing tournament.
    critical=(x.get('hypothesis_set') or {}).get('decision_critical_conflicts') or []
    if critical or tour in {'NO_CREDIBLE_DOMINANT_HYPOTHESIS','INSUFFICIENT_EVIDENCE'}:
        final='NO_TRADE';constraints.append('DECISION_CRITICAL_HYPOTHESIS_CONTEST');state='CONTESTED' if tour!='INSUFFICIENT_EVIDENCE' else 'INSUFFICIENT_EVIDENCE'
    elif state=='CLEAR':state='CONSTRAINED'
# Typed uncertainty gate.
critical_dims=[]
for u in (x.get('uncertainty_profile') or {}).get('dimensions') or []:
    if u.get('level')=='DECISION_CRITICAL':critical_dims.append(u.get('dimension'))
if critical_dims:
    final='NO_TRADE';constraints.append('DECISION_CRITICAL_UNCERTAINTY:'+','.join(sorted(set(critical_dims))));state='INSUFFICIENT_EVIDENCE'
# Unmodeled-driver / market disagreement is diagnostic and can only constrain or block, never reverse.
md=x.get('model_disagreement') or {}; um=md.get('unmodeled_driver_risk')
if um=='DECISION_CRITICAL' or md.get('action')=='HOLD_NO_TRADE':
    final='NO_TRADE';constraints.append('UNMODELED_DRIVER_RISK');state='MODEL_DISAGREEMENT'
elif um=='HIGH' and final!='NO_TRADE':
    constraints.append('HIGH_UNMODELED_DRIVER_EARLY_REVIEW');state='CONSTRAINED'
# Adversarial review.
adv=(x.get('adversarial_review') or {}).get('adjudication')
if adv in {'REJECTED','INSUFFICIENT_EVIDENCE'}:
    final='NO_TRADE';constraints.append('ADVERSARIAL_REVIEW_'+adv);state='INSUFFICIENT_EVIDENCE'
elif adv=='CONTESTED' and final!='NO_TRADE':
    final='NO_TRADE';constraints.append('ADVERSARIAL_CONTEST');state='CONTESTED'
elif adv=='THESIS_SURVIVES_CONSTRAINED' and state=='CLEAR':state='CONSTRAINED'
# Pre-mortem.
pm=x.get('premortem') or {}
if pm.get('unmonitorable_decision_critical_risk') is True:
    final='NO_TRADE';constraints.append('UNMONITORABLE_DECISION_CRITICAL_RISK');state='INSUFFICIENT_EVIDENCE'
# Utility is non-directional: it may delay/no-trade, never create/flip.
ut=(x.get('decision_utility') or {}).get('utility_state')
if ut=='FAVOR_NO_TRADE':
    final='NO_TRADE';constraints.append('UTILITY_FAVORS_NO_TRADE');state='CONSTRAINED' if state=='CLEAR' else state
elif ut=='FAVOR_DELAY' and final!='NO_TRADE':
    final='NO_TRADE';constraints.append('UTILITY_FAVORS_DELAY');state='DELAYED'
elif ut=='CONTESTED' and state=='CLEAR':state='CONSTRAINED'
# Scenario state can constrain but does not vote direction.
ss=(x.get('scenario_tree') or {}).get('tree_state')
if ss in {'CONTESTED','FRAGMENTED','INSUFFICIENT_EVIDENCE'} and final!='NO_TRADE':
    constraints.append('SCENARIO_TREE_'+ss);state='MULTI_SCENARIO_CLEAR' if ss=='CONTESTED' else 'CONSTRAINED'
elif ss=='MULTIPLE_COMPETITIVE' and state=='CLEAR':state='MULTI_SCENARIO_CLEAR'
# Safety: never create permission from NO_TRADE and never flip.
if pre=='NO_TRADE' and final!='NO_TRADE':raise SystemExit('SAFETY_NEW_PERMISSION_CREATED')
if pre in {'BUY','SELL'} and final not in {pre,'NO_TRADE'}:raise SystemExit('SAFETY_DIRECTION_FLIP')
# Outside-strategy edge is report-only.
outside=(x.get('meta_edge_router') or {}).get('outside_strategy_edges') or []
next_review=''
# Pull the most concrete condition from model disagreement or hypothesis resolution first.
for candidate in [md.get('action'), *(((x.get('hypothesis_set') or {}).get('resolution_observations') or []))]:
    if candidate:
        next_review=str(candidate);break
out={'version':'1.0.0','instrument':x['instrument'],'analysis_cutoff_utc':x['analysis_cutoff_utc'],'active_strategy_horizon':x['active_strategy_horizon'],'fundamental_direction':fund,'final_direction':fund,'pre_cognitive_permission':pre,'cognitive_permission':final,'cognitive_state':state,'tournament_state':tour,'scenario_state':ss,'decision_critical_uncertainties':sorted(set(critical_dims)),'unmodeled_driver_risk':um or 'UNDETERMINED','adversarial_adjudication':adv or 'INSUFFICIENT_EVIDENCE','utility_state':ut or 'UNDETERMINED','applied_cognitive_constraints':constraints,'outside_strategy_edges':outside,'next_review_trigger':next_review or 'NEXT_DECISION_MATERIAL_CAUSAL_TRIGGER','direction_flip_forbidden':True,'positive_permission_creation_forbidden':True}
Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf-8');print(json.dumps(out,ensure_ascii=False))
