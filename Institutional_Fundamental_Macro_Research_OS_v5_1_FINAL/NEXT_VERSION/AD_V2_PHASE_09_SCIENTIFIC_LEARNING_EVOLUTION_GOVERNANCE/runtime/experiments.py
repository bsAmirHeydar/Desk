from datetime import datetime,timezone
import hashlib,json
class ExperimentError(ValueError):pass
def _dt(s):
 d=datetime.fromisoformat(str(s).replace('Z','+00:00'));return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
def create(challenger,policy,sealed_at_utc):
 if challenger.get('record_type')!='P09_SHADOW_CHALLENGER':raise ExperimentError('valid challenger required')
 seed=challenger['challenger_id']+'|'+sealed_at_utc;eid='P09EXP_'+hashlib.sha256(seed.encode()).hexdigest()[:24].upper()
 e={'schema_version':'1.0.0','phase':'AD-V2-P09','record_type':'P09_CHALLENGER_EXPERIMENT','experiment_id':eid,'challenger_id':challenger['challenger_id'],'challenger_hash':challenger['challenger_hash'],'sealed_at_utc':sealed_at_utc,'excluded_generation_episode_keys':challenger.get('generation_episode_keys') or [],'validation_policy':{'eligible_provenance':policy['eligible_validation_provenance'],'validation_must_be_post_experiment_seal':True,'reuse_generation_episodes_forbidden':True,'minimum_candidate_validation_episodes':policy['minimum_candidate_validation_episodes']},'status':'FROZEN_AWAITING_FUTURE_VALIDATION','authority':{'auto_promote':False,'science_write':False,'permission_change':False,'broker':'NONE'},'integrity':{'status':'PASS','hypothesis_generation_data_excluded':True,'future_validation_only':True}}
 e['experiment_hash']='sha256:'+hashlib.sha256(json.dumps(e,sort_keys=True,separators=(',',':'),default=str).encode()).hexdigest();return e

def eligible_link(experiment,link):
 if link.get('sample_provenance') not in experiment['validation_policy']['eligible_provenance']:return False
 if link.get('independent_episode_key') in set(experiment['excluded_generation_episode_keys']):return False
 seal=link.get('joined_at_utc') or link.get('matured_at_utc')
 return bool(seal and _dt(seal)>_dt(experiment['sealed_at_utc']))
