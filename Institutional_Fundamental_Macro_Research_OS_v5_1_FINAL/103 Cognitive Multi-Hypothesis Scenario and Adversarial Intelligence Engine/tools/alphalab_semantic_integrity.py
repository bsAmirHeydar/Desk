#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys,datetime
H={"MICRO_0_15M","SHORT_15_60M","SESSION_1_6H","DAILY_OPEN_TO_CLOSE","MULTI_DAY_2_10D","SWING_2_8W","CYCLICAL","STRUCTURAL"}
DIRMAP={'BULLISH':{'BULLISH','STRONGLY_BULLISH'},'BEARISH':{'BEARISH','STRONGLY_BEARISH'},'NEUTRAL':{'NEUTRAL'},'UNRESOLVED':{'MIXED','UNDETERMINED'}}
OPTIONAL=['surprise_state','policy_reaction_state','regime_state','causal_graph','reflexivity_state','consumption_state','driver_transition','global_reconciliation']
LEVEL={'UNKNOWN':0,'LOW':1,'MODERATE':2,'HIGH':3,'DECISION_CRITICAL':4}
def fail(e,msg): e.append(msg)
def parse_dt(s):
 try:return datetime.datetime.fromisoformat((s or '').replace('Z','+00:00')) if s else None
 except:return None
def trig_ok(t):
 if not isinstance(t,dict):return False
 mode=t.get('monitor_mode');op=t.get('operator')
 if mode=='MACHINE_PREDICATE':
  if not (t.get('metric') and op):return False
  if op in {'GT','GTE','LT','LTE','EQ','NEQ'}:return t.get('value') is not None or bool(t.get('reference'))
  if op in {'CROSSES_ABOVE','CROSSES_BELOW'}:return bool(t.get('reference'))
  if op=='CHANGES_STATE':return t.get('value') is not None
  if op=='OBSERVED':return t.get('value') is not None or bool(t.get('reference')) or bool(t.get('event_id'))
  return False
 if mode=='SCHEDULED_TIME':return parse_dt(t.get('time_utc')) is not None
 if mode=='EVENT_RELEASE':return bool(t.get('event_id'))
 if mode=='MANUAL_OBSERVATION':return bool(t.get('manual_observation'))
 return False
def has_uncertainty(x,dims,minlevel='HIGH'):
 want=set(dims);thr=LEVEL[minlevel]
 return any(u.get('dimension') in want and LEVEL.get(u.get('level'),0)>=thr for u in (x.get('uncertainty_profile') or {}).get('dimensions') or [])
def load_ledger_ids(path):
 ids=set();cal=set()
 if not path:return ids,cal
 p=Path(path)
 if not p.exists():return ids,cal
 for line in p.read_text(encoding='utf-8').splitlines():
  if not line.strip():continue
  try:o=json.loads(line)
  except:continue
  ids.add(o.get('record_id'))
  pay=o.get('payload') or {}
  if o.get('record_type')=='CALIBRATION_REPORT' or pay.get('record_type')=='CALIBRATION_REPORT':
   if pay.get('calibration_id'):cal.add(pay.get('calibration_id'))
   if o.get('record_id'):cal.add(o.get('record_id'))
 return ids,cal
def load_evidence_pack(path):
 if not path:return None,{},{},[]
 p=Path(path)
 if not p.exists():return None,{},{},['EVIDENCE_PACK_NOT_FOUND']
 try:pack=json.loads(p.read_text(encoding='utf-8'))
 except Exception as ex:return None,{},{},['EVIDENCE_PACK_PARSE:'+str(ex)]
 facts={f.get('fact_id'):f for f in pack.get('fact_records') or [] if f.get('fact_id')}
 roots={}
 for f in facts.values():
  if f.get('root_cause_id'):roots.setdefault(f['root_cause_id'],[]).append(f['fact_id'])
 return pack,facts,roots,[]
def validate(x,root=None,evidence_pack=None,require_evidence_pack=False,d4_ledger=None):
 e=[];inst=x.get('instrument');cut=x.get('analysis_cutoff_utc');hor=x.get('active_strategy_horizon');fund=x.get('fundamental_direction');pre=x.get('pre_cognitive_permission')
 app=x.get('cognitive_applicability') or {};exceptions={z.get('invariant_id') for z in x.get('propagation_exceptions') or [] if isinstance(z,dict)}
 for k in OPTIONAL:
  ent=app.get(k)
  if not ent:fail(e,'APPLICABILITY_MISSING:'+k);continue
  st=ent.get('status')
  if st=='PRESENT' and k not in x:fail(e,'STATE_MARKED_PRESENT_BUT_MISSING:'+k)
  if st!='PRESENT' and k in x:fail(e,'STATE_PRESENT_BUT_APPLICABILITY_'+str(st)+':'+k)
 # Context-sensitive applicability: flexible, but directional/actionable runs cannot bypass key cognition.
 directional=fund in {'BULLISH','BEARISH'}; actionable=pre in {'BUY','SELL'}
 if directional:
  for k in ['regime_state','causal_graph']:
   if app.get(k,{}).get('status')=='NOT_APPLICABLE':fail(e,'DIRECTIONAL_RUN_CANNOT_MARK_NOT_APPLICABLE:'+k)
 if actionable and app.get('consumption_state',{}).get('status')=='NOT_APPLICABLE':fail(e,'ACTIONABLE_PERMISSION_REQUIRES_CONSUMPTION_STATE_OR_UNAVAILABLE')
 hs=x.get('hypothesis_set') or {}
 for name,val in [('instrument',inst),('analysis_cutoff_utc',cut),('active_horizon',hor)]:
  if hs.get(name)!=val:fail(e,'HYPOTHESIS_SET_'+name.upper()+'_MISMATCH')
 hyps=hs.get('hypotheses') or [];ids=[h.get('hypothesis_id') for h in hyps];idset=set(ids)
 if len(ids)!=len(idset):fail(e,'DUPLICATE_HYPOTHESIS_ID')
 policy_related=any(h.get('family') in {'POLICY_REACTION','FX_RELATIVE_POLICY'} for h in hyps)
 if policy_related and app.get('policy_reaction_state',{}).get('status')=='NOT_APPLICABLE':fail(e,'POLICY_RELATED_HYPOTHESIS_REQUIRES_POLICY_REACTION_STATE_OR_UNAVAILABLE')
 if any(h.get('reflexive_loops') for h in hyps) and app.get('reflexivity_state',{}).get('status')=='NOT_APPLICABLE':fail(e,'REFLEXIVE_HYPOTHESIS_REQUIRES_REFLEXIVITY_STATE_OR_UNAVAILABLE')
 dom=hs.get('dominant_hypothesis_ids') or [];chal=hs.get('strongest_challenger_ids') or [];tour=hs.get('tournament_state')
 for z in dom+chal:
  if z not in idset:fail(e,'UNKNOWN_TOURNAMENT_HYPOTHESIS_ID:'+str(z))
 if set(dom)&set(chal):fail(e,'DOMINANT_AND_CHALLENGER_OVERLAP')
 if tour=='DOMINANT' and len(dom)!=1:fail(e,'DOMINANT_STATE_REQUIRES_EXACTLY_ONE_DOMINANT')
 if tour=='CO_DOMINANT' and len(dom)<2:fail(e,'CO_DOMINANT_REQUIRES_AT_LEAST_TWO_DOMINANT')
 if tour in {'NO_CREDIBLE_DOMINANT_HYPOTHESIS','INSUFFICIENT_EVIDENCE'} and dom:fail(e,'NO_DOMINANT_STATE_CANNOT_HAVE_DOMINANT_IDS')
 # Optional evidence pack provides actual D1 referential integrity.
 pack,facts,roots,pe=load_evidence_pack(evidence_pack);e.extend(pe)
 if pack:
  if pack.get('symbol')!=inst:fail(e,'EVIDENCE_PACK_SYMBOL_MISMATCH')
  if pack.get('analysis_cutoff_utc')!=cut:fail(e,'EVIDENCE_PACK_CUTOFF_MISMATCH')
 load_refs=[];derived_roots=set();dc_contra=set();partial_material=False
 for h in hyps:
  for fld,role in [('supporting_evidence','SUPPORT'),('contradicting_evidence','CONTRADICT'),('missing_evidence','MISSING')]:
   for ev in h.get(fld) or []:
    if ev.get('role')!=role:fail(e,f'EVIDENCE_ROLE_MISMATCH:{h.get("hypothesis_id")}:{fld}')
    mat=ev.get('materiality');lin=ev.get('lineage_status');et=ev.get('evidence_type')
    if mat=='DECISION_CRITICAL' and lin!='TRACEABLE' and et!='MISSING_EVIDENCE':fail(e,'DECISION_CRITICAL_EVIDENCE_MUST_BE_TRACEABLE:'+str(ev.get('evidence_id')))
    if mat=='MATERIAL' and lin not in {'TRACEABLE','PARTIAL'} and et!='MISSING_EVIDENCE':fail(e,'MATERIAL_EVIDENCE_UNTRACEABLE:'+str(ev.get('evidence_id')))
    if mat=='MATERIAL' and lin=='PARTIAL':partial_material=True
    if ev.get('horizon') not in H:fail(e,'BAD_EVIDENCE_HORIZON:'+str(ev.get('evidence_id')))
    if mat in {'DECISION_CRITICAL','MATERIAL'} and ev.get('root_id'):derived_roots.add(ev.get('root_id'))
    if fld=='contradicting_evidence' and mat=='DECISION_CRITICAL':dc_contra.add(ev.get('evidence_id'))
    if et=='FACT_REF' and mat in {'DECISION_CRITICAL','MATERIAL'}:load_refs.append(ev)
    if pack and et=='FACT_REF':
     fid=ev.get('fact_id');fact=facts.get(fid)
     if not fact:fail(e,'FACT_REF_NOT_FOUND_IN_EVIDENCE_PACK:'+str(fid));continue
     if ev.get('root_id') and fact.get('root_cause_id') and ev.get('root_id')!=fact.get('root_cause_id'):fail(e,'FACT_REF_ROOT_MISMATCH:'+str(fid))
     if ev.get('source_grade') and (fact.get('source') or {}).get('tier') and ev.get('source_grade')!=(fact.get('source') or {}).get('tier'):fail(e,'FACT_REF_SOURCE_GRADE_MISMATCH:'+str(fid))
     t=fact.get('time') or {};fs=parse_dt(t.get('first_seen_time') or t.get('publication_time'));co=parse_dt(cut)
     if fs and co and fs>co:fail(e,'FACT_REF_VISIBLE_AFTER_CUTOFF:'+str(fid))
  for fld in ['confirmation_triggers','invalidation_triggers']:
   for t in h.get(fld) or []:
    if t.get('materiality') in {'DECISION_CRITICAL','MATERIAL'} and not trig_ok(t):fail(e,'UNMONITORABLE_HYPOTHESIS_TRIGGER:'+str(t.get('trigger_id')))
 if require_evidence_pack and load_refs and not pack:fail(e,'LOAD_BEARING_FACT_REFS_REQUIRE_D1_EVIDENCE_PACK')
 if partial_material and not has_uncertainty(x,{'DATA','MEASUREMENT','SOURCE'},'MODERATE') and 'MATERIAL_PARTIAL_LINEAGE' not in exceptions:fail(e,'MATERIAL_PARTIAL_LINEAGE_REQUIRES_UNCERTAINTY_OR_EXCEPTION')
 # Tournament counts are derived where evidence roots exist, never trusted blindly.
 tb=hs.get('tournament_basis') or {};mode=tb.get('root_count_mode')
 if derived_roots:
  if mode=='DERIVED_COMPLETE':
   if tb.get('independent_root_count')!=len(derived_roots):fail(e,'INDEPENDENT_ROOT_COUNT_NOT_DERIVED')
   if sorted(tb.get('derived_root_ids') or [])!=sorted(derived_roots):fail(e,'DERIVED_ROOT_IDS_MISMATCH')
   if tb.get('critical_contradiction_count')!=len(dc_contra) or tb.get('derived_critical_contradiction_count')!=len(dc_contra):fail(e,'CRITICAL_CONTRADICTION_COUNT_NOT_DERIVED')
  elif mode not in {'DERIVED_PARTIAL','MANUAL_WITH_DISCLOSURE'}:fail(e,'ROOT_COUNT_MODE_REQUIRED_WHEN_LOAD_BEARING_ROOTS_EXIST')
 if len(hyps)>1 and tour in {'DOMINANT','CO_DOMINANT'}:
  matrix=hs.get('evidence_matrix') or [];mids={m.get('hypothesis_id') for m in matrix}
  if not set(ids).issubset(mids):fail(e,'DOMINANT_TOURNAMENT_REQUIRES_NON_ADDITIVE_EVIDENCE_MATRIX')
 # active horizon tensor must agree with Fundamental top direction
 ht=x.get('horizon_tensor') or {}
 if ht.get('active_strategy_horizon')!=hor:fail(e,'HORIZON_TENSOR_ACTIVE_HORIZON_MISMATCH')
 ast=[s for s in ht.get('states') or [] if s.get('horizon')==hor]
 if len(ast)!=1:fail(e,'ACTIVE_HORIZON_REQUIRES_EXACTLY_ONE_STATE')
 elif fund in DIRMAP and ast[0].get('fundamental_direction') not in DIRMAP[fund]:fail(e,'FUNDAMENTAL_DIRECTION_ACTIVE_HORIZON_MISMATCH')
 # uncertainty
 up=x.get('uncertainty_profile') or {};dims=[u.get('dimension') for u in up.get('dimensions') or []]
 if len(dims)!=len(set(dims)):fail(e,'DUPLICATE_UNCERTAINTY_DIMENSION')
 crit=sorted({u.get('dimension') for u in up.get('dimensions') or [] if u.get('level')=='DECISION_CRITICAL'})
 if sorted(up.get('decision_critical_dimensions') or [])!=crit:fail(e,'DECISION_CRITICAL_UNCERTAINTY_LIST_MISMATCH')
 # scenarios
 st=x.get('scenario_tree') or {}
 if st.get('active_horizon')!=hor:fail(e,'SCENARIO_ACTIVE_HORIZON_MISMATCH')
 if st.get('as_of_utc')!=cut:fail(e,'SCENARIO_CUTOFF_MISMATCH')
 scenarios=st.get('scenarios') or [];sids=[s.get('scenario_id') for s in scenarios]
 if len(sids)!=len(set(sids)):fail(e,'DUPLICATE_SCENARIO_ID')
 if len(scenarios)==1 and not st.get('single_scenario_justification'):fail(e,'SINGLE_SCENARIO_REQUIRES_JUSTIFICATION')
 prim=[s for s in scenarios if s.get('plausibility_band')=='PRIMARY']
 if st.get('tree_state')=='PRIMARY_SCENARIO_IDENTIFIED' and len(prim)!=1:fail(e,'PRIMARY_TREE_REQUIRES_EXACTLY_ONE_PRIMARY')
 probs=[]
 for s in scenarios:
  if s.get('horizon')!=hor:fail(e,'SCENARIO_HORIZON_MISMATCH:'+str(s.get('scenario_id')))
  for hid in s.get('source_hypothesis_ids') or []:
   if hid not in idset:fail(e,'SCENARIO_UNKNOWN_HYPOTHESIS:'+str(hid))
  for fld in ['confirmation_triggers','invalidation_triggers']:
   for t in s.get(fld) or []:
    if t.get('materiality') in {'DECISION_CRITICAL','MATERIAL'} and not trig_ok(t):fail(e,'UNMONITORABLE_SCENARIO_TRIGGER:'+str(t.get('trigger_id')))
  for trn in s.get('transition_paths') or []:
   if trn.get('to_scenario_id') not in set(sids):fail(e,'SCENARIO_TRANSITION_UNKNOWN_TARGET:'+str(trn.get('to_scenario_id')))
   if not trig_ok(trn.get('trigger') or {}):fail(e,'UNMONITORABLE_SCENARIO_TRANSITION:'+str(s.get('scenario_id')))
  p=s.get('calibrated_probability')
  if p is not None:probs.append(float(p))
  imp=s.get('permission_implication');sd=s.get('direction')
  if pre=='BUY' and imp=='SUPPORT_EXISTING' and sd not in {'BULLISH','STRONGLY_BULLISH'}:fail(e,'SCENARIO_PERMISSION_DIRECTION_INCONSISTENT:'+str(s.get('scenario_id')))
  if pre=='SELL' and imp=='SUPPORT_EXISTING' and sd not in {'BEARISH','STRONGLY_BEARISH'}:fail(e,'SCENARIO_PERMISSION_DIRECTION_INCONSISTENT:'+str(s.get('scenario_id')))
  if pre=='NO_TRADE' and imp=='SUPPORT_EXISTING':fail(e,'NO_TRADE_SCENARIO_CANNOT_SUPPORT_EXISTING_PERMISSION:'+str(s.get('scenario_id')))
 pmode=st.get('probability_mode')
 if pmode=='QUALITATIVE' and probs:fail(e,'QUALITATIVE_SCENARIOS_CANNOT_HAVE_NUMERIC_PROBABILITIES')
 if pmode=='CALIBRATED':
  cid=st.get('calibration_record_id')
  if not cid:fail(e,'CALIBRATED_SCENARIOS_REQUIRE_CALIBRATION_RECORD')
  if not st.get('calibration_reference_class_id'):fail(e,'CALIBRATED_SCENARIOS_REQUIRE_REFERENCE_CLASS_ID')
  if len(probs)!=len(scenarios):fail(e,'CALIBRATED_SCENARIOS_REQUIRE_ALL_PROBABILITIES')
  elif abs(sum(probs)-1.0)>0.01:fail(e,'CALIBRATED_SCENARIO_PROBABILITIES_MUST_SUM_TO_ONE')
  _,calids=load_ledger_ids(d4_ledger)
  if not d4_ledger:fail(e,'CALIBRATED_SCENARIOS_REQUIRE_D4_LEDGER_FOR_REFERENTIAL_VALIDATION')
  elif cid not in calids:fail(e,'CALIBRATION_RECORD_NOT_FOUND_IN_D4_LEDGER:'+str(cid))
 # Regime vocabulary/horizon
 if app.get('regime_state',{}).get('status')=='PRESENT':
  rg=x.get('regime_state') or {}
  if rg.get('primary_horizon')!=hor:fail(e,'REGIME_PRIMARY_HORIZON_MISMATCH')
  rp={}
  if root:
   q=Path(root)/'103 Cognitive Multi-Hypothesis Scenario and Adversarial Intelligence Engine/config/regime_policy.json'
   if q.exists():rp=json.loads(q.read_text()).get('dimension_state_map') or {}
  for d in rg.get('dimensions') or []:
   allowed=rp.get(d.get('dimension'))
   if allowed and d.get('state') not in allowed:fail(e,'REGIME_STATE_INVALID_FOR_DIMENSION:'+str(d.get('dimension'))+':'+str(d.get('state')))
   ah=d.get('applicable_horizons') or []
   if ah and hor not in ah:fail(e,'REGIME_DIMENSION_DOES_NOT_APPLY_TO_ACTIVE_HORIZON:'+str(d.get('dimension')))
 # Causal graph
 if app.get('causal_graph',{}).get('status')=='PRESENT':
  g=x.get('causal_graph') or {}
  if g.get('horizon')!=hor:fail(e,'CAUSAL_GRAPH_HORIZON_MISMATCH')
  if g.get('as_of_utc')!=cut:fail(e,'CAUSAL_GRAPH_CUTOFF_MISMATCH')
  nids={n.get('node_id') for n in g.get('nodes') or []}
  for ed in g.get('edges') or []:
   if ed.get('from_node') not in nids or ed.get('to_node') not in nids:fail(e,'CAUSAL_EDGE_UNKNOWN_NODE:'+str(ed.get('edge_id')))
   for t in ed.get('activation_predicates') or []:
    if not trig_ok(t):fail(e,'BAD_CAUSAL_ACTIVATION_PREDICATE:'+str(ed.get('edge_id')))
 # policy reaction supports single/non-FX and bilateral FX
 if app.get('policy_reaction_state',{}).get('status')=='PRESENT':
  pr=x.get('policy_reaction_state') or {}
  if 'mode' in pr:
   if pr.get('as_of_utc')!=cut:fail(e,'POLICY_REACTION_BUNDLE_CUTOFF_MISMATCH')
   for ps in pr.get('states') or []:
    if ps.get('as_of_utc')!=cut:fail(e,'POLICY_REACTION_STATE_CUTOFF_MISMATCH')
   if inst in {'EURUSD','USDJPY'} and policy_related and pr.get('mode')!='BILATERAL':fail(e,'FX_POLICY_REACTION_MUST_BE_BILATERAL_WHEN_POLICY_IS_MATERIAL')
  else:
   if pr.get('as_of_utc')!=cut:fail(e,'POLICY_REACTION_CUTOFF_MISMATCH')
   if inst in {'EURUSD','USDJPY'} and policy_related:fail(e,'FX_POLICY_REACTION_MUST_USE_BILATERAL_BUNDLE')
 # premortem monitorability
 pm=x.get('premortem') or {}
 for fp in pm.get('failure_paths') or []:
  mode=fp.get('monitorability_mode');ok=trig_ok(fp.get('early_warning_trigger') or {})
  if fp.get('monitorable') and not ok:fail(e,'PREMORTEM_MONITORABLE_WITHOUT_VALID_TRIGGER:'+str(fp.get('failure_id')))
  if mode=='AUTOMATIC' and (fp.get('early_warning_trigger') or {}).get('monitor_mode')=='MANUAL_OBSERVATION':fail(e,'PREMORTEM_AUTOMATIC_CANNOT_USE_MANUAL_TRIGGER:'+str(fp.get('failure_id')))
  if mode=='UNMONITORABLE' and fp.get('monitorable') is True:fail(e,'PREMORTEM_MONITORABILITY_CONTRADICTION:'+str(fp.get('failure_id')))
 # Upstream→downstream propagation with explicit auditable exceptions.
 adv=(x.get('adversarial_review') or {}).get('adjudication');ut=(x.get('decision_utility') or {}).get('utility_state')
 def reflected_or_exception(inv,condition):
  if condition or inv in exceptions:return
  fail(e,'UPSTREAM_STATE_NOT_PROPAGATED:'+inv)
 if app.get('causal_graph',{}).get('status')=='PRESENT' and (x.get('causal_graph') or {}).get('graph_state')=='BROKEN':
  reflected_or_exception('BROKEN_CAUSAL_GRAPH_PROPAGATES',has_uncertainty(x,{'TRANSMISSION','CAUSAL'},'HIGH') or adv not in {'THESIS_SURVIVES'} or ut!='FAVOR_ACTION')
 if app.get('global_reconciliation',{}).get('status')=='PRESENT' and (x.get('global_reconciliation') or {}).get('state')=='INCONSISTENT':
  reflected_or_exception('INCONSISTENT_GLOBAL_STATE_PROPAGATES',has_uncertainty(x,{'MODEL','CAUSAL','TRANSMISSION'},'HIGH') or adv not in {'THESIS_SURVIVES'} or ut!='FAVOR_ACTION')
 if app.get('consumption_state',{}).get('status')=='PRESENT' and (x.get('consumption_state') or {}).get('remaining_asymmetry') in {'VERY_POOR','POOR'}:
  reflected_or_exception('POOR_REMAINING_ASYMMETRY_PROPAGATES',ut!='FAVOR_ACTION' or adv in {'THESIS_SURVIVES_CONSTRAINED','CONTESTED','REJECTED','INSUFFICIENT_EVIDENCE'})
 if app.get('driver_transition',{}).get('status')=='PRESENT' and (x.get('driver_transition') or {}).get('state') in {'TAKEOVER','FRAGMENTED'}:
  reflected_or_exception('DRIVER_TAKEOVER_PROPAGATES',has_uncertainty(x,{'CAUSAL','TIMING'},'HIGH') or adv not in {'THESIS_SURVIVES'})
 if app.get('regime_state',{}).get('status')=='PRESENT':
  rg=x.get('regime_state') or {}
  if rg.get('mapping_stability')=='BROKEN' or rg.get('structural_break_risk') in {'HIGH','VERY_HIGH'}:
   reflected_or_exception('REGIME_BREAK_RISK_PROPAGATES',has_uncertainty(x,{'REGIME'},'HIGH') or adv not in {'THESIS_SURVIVES'})
 return e

def main():
 p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--vault-root');p.add_argument('--evidence-pack');p.add_argument('--require-evidence-pack',action='store_true');p.add_argument('--d4-ledger');a=p.parse_args()
 x=json.loads(Path(a.input).read_text(encoding='utf-8'));e=validate(x,a.vault_root,a.evidence_pack,a.require_evidence_pack,a.d4_ledger);print(json.dumps({'status':'PASS' if not e else 'FAIL','errors':e},indent=2,ensure_ascii=False));return 0 if not e else 2
if __name__=='__main__':raise SystemExit(main())
