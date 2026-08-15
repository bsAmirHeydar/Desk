import hashlib,json

def build(pattern,taxonomy,sealed_at_utc):
 if not pattern.get('proposal_eligible'):return None
 mp={x['id']:x for x in taxonomy['families']};fam=pattern['failure_family'];row=mp.get(fam)
 if not row:return None
 seed=pattern['pattern_id']+'|'+row['candidate_family'];hid='P09HYP_'+hashlib.sha256(seed.encode()).hexdigest()[:24].upper()
 q={
  'PRESSURE_MODEL_MISS':'Does the causal-root or magnitude model systematically overstate Gold Pressure in this recurring cohort?',
  'TRANSMISSION_EXPECTATION_MISS':'Is the expected Gold response signature or lag window systematically too optimistic?',
  'LATENT_PRESSURE_OVERSTATEMENT':'Are Unreleased Pressure rules systematically overstating latent reserve?',
  'OPPOSING_MATURITY_PREMATURE':'Is opposing-move maturity being assigned before non-price sponsorship has truly decayed?',
  'RELEASE_FALSE_POSITIVE':'Are Release Readiness/Release gates admitting too many weak expansions?',
  'MISSING_DRIVER_UNRESOLVED':'Which recurring missing driver or observability gap explains these residuals?',
  'EVENT_RESET_GUARD_MISS':'Should event-reset gating be tightened for this recurring cohort?',
  'DATA_QUALITY_OR_COVERAGE':'Which data-integrity guard is missing or too permissive?',
  'EVALUATION_PROFILE_MISMATCH':'Does the evaluation profile misrepresent the risk unit or maturity horizon?'}
 h={'schema_version':'1.0.0','phase':'AD-V2-P09','record_type':'P09_RESEARCH_HYPOTHESIS','hypothesis_id':hid,'source_pattern_id':pattern['pattern_id'],'failure_family':fam,'scientific_owner':row['owner'],'candidate_family':row['candidate_family'],'research_question':q.get(fam,'Review the recurring scientific failure hypothesis.'),'sealed_at_utc':sealed_at_utc,'status':'RESEARCH_PROPOSAL','source_counts':pattern['counts'],'generation_episode_keys':pattern['episode_keys'],'validation_episode_reuse_forbidden':True,'required_next_step':'OPERATOR_REVIEW_THEN_SHADOW_CHALLENGER_EXPERIMENT','authority':{'auto_apply':False,'upstream_write':False,'permission_change':False,'broker':'NONE'},'integrity':{'status':'PASS','true_forward_recurrence_gate_passed':True,'single_case_not_sufficient':True,'hypothesis_not_conclusion':True}}
 h['hypothesis_hash']='sha256:'+hashlib.sha256(json.dumps(h,sort_keys=True,separators=(',',':'),default=str).encode()).hexdigest();return h
