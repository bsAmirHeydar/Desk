#!/usr/bin/env python3
from pathlib import Path
import argparse,json
p=argparse.ArgumentParser();p.add_argument('--state-bundle',required=True);p.add_argument('--output',required=True);a=p.parse_args();x=json.loads(Path(a.state_bundle).read_text(encoding='utf-8'))
hs=x.get('hypothesis_set') or {};sc=x.get('scenario_tree') or {};up=x.get('uncertainty_profile') or {};md=x.get('model_disagreement') or {};ad=x.get('adversarial_review') or {};du=x.get('decision_utility') or {};ca=x.get('cognitive_adjudication') or {};rg=x.get('regime_state') or {};su=x.get('surprise_state') or {};rf=x.get('reflexivity_state') or {};co=x.get('consumption_state') or {};dr=x.get('driver_transition') or {};gr=x.get('global_reconciliation') or {};cg=x.get('causal_graph') or {}
source_grades=set();interaction_ids=set(x.get('interaction_hypothesis_ids') or [])
for h in hs.get('hypotheses') or []:
 for fld in ['supporting_evidence','contradicting_evidence','missing_evidence']:
  for ev in h.get(fld) or []:
   if ev.get('source_grade'):source_grades.add(ev.get('source_grade'))
 # Interaction hypotheses are retained by explicit ID or mechanism/family tag, never inferred from outcome.
 if h.get('family')=='POSITIONING_FLOW' and ('+' in (h.get('title') or '') or 'interaction' in (h.get('mechanism') or '').lower()):interaction_ids.add(h.get('hypothesis_id'))
out={
 'hypothesis_tournament_state':hs.get('tournament_state','UNDETERMINED'),'dominant_hypothesis_ids':hs.get('dominant_hypothesis_ids') or [],'strongest_challenger_ids':hs.get('strongest_challenger_ids') or [],
 'scenario_tree_state':sc.get('tree_state','UNDETERMINED'),'active_horizon':x.get('active_strategy_horizon'),'scenario_count':len(sc.get('scenarios') or []),
 'uncertainty_dimensions':[u.get('dimension') for u in up.get('dimensions') or []],'decision_critical_uncertainties':up.get('decision_critical_dimensions') or [],
 'unmodeled_driver_risk':md.get('unmodeled_driver_risk','UNDETERMINED'),'adversarial_adjudication':ad.get('adjudication','UNDETERMINED'),'utility_state':du.get('utility_state','UNDETERMINED'),
 'complexity_class':x.get('complexity_class','UNDETERMINED'),'load_bearing_root_count':len(set(x.get('load_bearing_root_ids') or [])),
 'abstention_reason_codes':ca.get('applied_cognitive_constraints') or [],'cognitive_rescue_candidate':bool(ca.get('cognitive_rescue_candidate',False)),
 'source_value_tags':sorted(source_grades),'source_grade_tags':sorted(source_grades),'interaction_hypothesis_ids':sorted(i for i in interaction_ids if i),
 'causal_graph_state':cg.get('graph_state','NOT_APPLICABLE' if not cg else 'UNDETERMINED'),'regime_overall_state':rg.get('overall_state','NOT_APPLICABLE' if not rg else 'UNDETERMINED'),'regime_mapping_stability':rg.get('mapping_stability','NOT_APPLICABLE' if not rg else 'UNDETERMINED'),
 'surprise_market_state':su.get('market_surprise','NOT_APPLICABLE' if not su else 'UNDETERMINED'),'surprise_policy_implication':su.get('policy_implication','NOT_APPLICABLE' if not su else 'UNDETERMINED'),'surprise_asset_implication':su.get('asset_implication','NOT_APPLICABLE' if not su else 'UNDETERMINED'),
 'reflexivity_phase':rf.get('aggregate_phase','NOT_APPLICABLE' if not rf else 'UNDETERMINED'),'remaining_asymmetry':co.get('remaining_asymmetry','NOT_APPLICABLE' if not co else 'UNDETERMINED'),'driver_transition_state':dr.get('state','NOT_APPLICABLE' if not dr else 'UNDETERMINED'),'global_reconciliation_state':gr.get('state','NOT_APPLICABLE' if not gr else 'UNDETERMINED'),
 'propagation_exception_ids':sorted(z.get('invariant_id') for z in x.get('propagation_exceptions') or [] if isinstance(z,dict) and z.get('invariant_id'))
}
Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf-8');print(json.dumps(out,ensure_ascii=False))
