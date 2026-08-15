from __future__ import annotations
import hashlib,json

def _num(x):
 try:return float(x) if x is not None else None
 except:return None
def _mode(fid,confidence,reason,owner):return {'failure_family':fid,'confidence':confidence,'status':'HYPOTHESIS_ONLY','owner':owner,'reason':reason}
def classify(link,policy):
 f=link.get('features') or {};m=link.get('metrics') or {};mfe=_num(m.get('mfe_r'));mae=_num(m.get('mae_r'))
 if link.get('maturity_state')!='MATURE':return []
 if mfe is None:return [_mode('EVALUATION_PROFILE_MISMATCH','LOW','Mature link has no MFE_R; scoring/profile lineage requires review.','P08')]
 weak=mfe < float(policy['weak_mfe_r_threshold']); severe=mae is not None and mae >= float(policy['severe_mae_r_threshold'])
 modes=[]
 if weak and f.get('pressure_class') in {'HIGH','VERY_HIGH','EXTREME'}:
  modes.append(_mode('PRESSURE_MODEL_MISS','LOW','Strong frozen Pressure followed by weak favorable excursion; this does not prove Pressure was wrong.','P02'))
 if weak and f.get('transmission_state') in {'ALIGNED','ALIGNED_INCOMPLETE','OVER_TRANSMISSION'}:
  modes.append(_mode('TRANSMISSION_EXPECTATION_MISS','MEDIUM','Transmission appeared aligned but subsequent excursion was weak.','P03'))
 if weak and f.get('unreleased_pressure') in {'HIGH','VERY_HIGH'}:
  modes.append(_mode('LATENT_PRESSURE_OVERSTATEMENT','MEDIUM','High Unreleased Pressure did not produce material favorable excursion.','P04'))
 if weak and f.get('opposing_move_maturity') in {'MATURE','EXHAUSTING','EXHAUSTED'}:
  modes.append(_mode('OPPOSING_MATURITY_PREMATURE','MEDIUM','Opposing move was classified mature/exhausting but outcome remained weak.','P04'))
 if weak and (f.get('release_readiness')=='HIGH_READINESS' or f.get('release_lifecycle') in {'RELEASE_CANDIDATE','RELEASE','EXPANSION'}):
  modes.append(_mode('RELEASE_FALSE_POSITIVE','HIGH' if severe else 'MEDIUM','High release state did not translate into material favorable excursion.','P04'))
 if weak and f.get('missing_driver_escalation') in {'RESEARCH_ESCALATION','DECISION_CRITICAL'}:
  modes.append(_mode('MISSING_DRIVER_UNRESOLVED','MEDIUM','Upstream already flagged a missing-driver risk and the poor outcome preserves that unresolved hypothesis.','P03/P05'))
 if weak and f.get('event_readiness_cap') is False:
  modes.append(_mode('EVENT_RESET_GUARD_MISS','LOW','Weak outcome occurred without an event-readiness cap; event-state review may be warranted.','P05'))
 if not modes:modes=[_mode('NO_CLEAR_MODEL_FAILURE','UNRESOLVED','Outcome does not isolate a specific upstream scientific failure.','P09')]
 return modes

def build_case(link,policy,created_at_utc):
 modes=classify(link,policy); seed=str(link.get('outcome_link_id'))+'|'+str(link.get('outcome_link_hash'))
 cid='P09LC_'+hashlib.sha256(seed.encode()).hexdigest()[:24].upper()
 c={'schema_version':'1.0.0','phase':'AD-V2-P09','record_type':'P09_LEARNING_CASE','learning_case_id':cid,'outcome_link_id':link.get('outcome_link_id'),'outcome_link_hash':link.get('outcome_link_hash'),'commitment_id':link.get('commitment_id'),'commitment_hash':link.get('commitment_hash'),'run_id':link.get('run_id'),'sample_provenance':link.get('sample_provenance'),'true_forward_eligible':bool(link.get('true_forward_eligible')),'independent_episode_key':link.get('independent_episode_key'),'trading_day':link.get('trading_day'),'regime':link.get('regime'),'hypothesis_family_id':link.get('hypothesis_family_id'),'frozen_features':link.get('features') or {},'outcome_metrics':link.get('metrics') or {},'suspected_failure_modes':modes,'created_at_utc':created_at_utc,'integrity':{'status':'PASS','upstream_rewritten':False,'outcome_attribution_is_hypothesis':True,'single_case_model_change_forbidden':True,'historical_not_true_forward':link.get('sample_provenance')!='TRUE_FORWARD' or bool(link.get('true_forward_eligible'))},'authority':{'science_mutation':'NONE','trade_permission':'V1_INHERITED','broker':'NONE'}}
 c['learning_case_hash']='sha256:'+hashlib.sha256(json.dumps(c,sort_keys=True,separators=(',',':'),default=str).encode()).hexdigest();return c
