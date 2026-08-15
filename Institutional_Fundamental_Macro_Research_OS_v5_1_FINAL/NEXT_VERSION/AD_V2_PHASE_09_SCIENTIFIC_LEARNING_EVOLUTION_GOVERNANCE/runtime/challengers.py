import hashlib,json
class ChallengerError(ValueError):pass

def validate_spec(family,spec,policy):
 if family not in policy['allowed_families']:raise ChallengerError('challenger family not allowed')
 raw=json.dumps(spec,sort_keys=True).lower()
 for t in policy['forbidden_tokens']:
  if t.lower() in raw:raise ChallengerError('forbidden challenger content: '+t)
 if spec.get('auto_apply') or spec.get('upstream_write') or spec.get('permission_change') or spec.get('broker_write'):raise ChallengerError('challenger may not gain authority')
 return True

def create(hypothesis,spec,policy,sealed_at_utc):
 family=hypothesis['candidate_family'];validate_spec(family,spec,policy);seed=hypothesis['hypothesis_id']+'|'+json.dumps(spec,sort_keys=True);cid='P09CH_'+hashlib.sha256(seed.encode()).hexdigest()[:24].upper()
 c={'schema_version':'1.0.0','phase':'AD-V2-P09','record_type':'P09_SHADOW_CHALLENGER','challenger_id':cid,'source_hypothesis_id':hypothesis['hypothesis_id'],'source_hypothesis_hash':hypothesis['hypothesis_hash'],'family':family,'sealed_at_utc':sealed_at_utc,'spec':spec,'status':'SHADOW_PROPOSAL_ONLY','generation_episode_keys':hypothesis.get('generation_episode_keys') or [],'authority':{'auto_apply':False,'upstream_write':False,'permission_change':False,'broker':'NONE'},'integrity':{'status':'PASS','constitutional_invariants_preserved':True,'future_validation_required':True}}
 c['challenger_hash']='sha256:'+hashlib.sha256(json.dumps(c,sort_keys=True,separators=(',',':'),default=str).encode()).hexdigest();return c
