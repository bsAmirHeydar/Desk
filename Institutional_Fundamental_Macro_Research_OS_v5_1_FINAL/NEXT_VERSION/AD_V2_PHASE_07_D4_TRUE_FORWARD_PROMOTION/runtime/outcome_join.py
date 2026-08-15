#!/usr/bin/env python3
from __future__ import annotations
from datetime import datetime,timezone
import hashlib,json
PHASE='AD-V2-P07'
class OutcomeError(ValueError): pass
def _canon(x): return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,default=str)
def _hash(x): return 'sha256:'+hashlib.sha256(_canon(x).encode()).hexdigest()
def _dt(s):
    d=datetime.fromisoformat(str(s).replace('Z','+00:00')); return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
def verify_commitment(c):
    if c.get('record_type')!='V2_FORWARD_COMMITMENT': return False
    h=c.get('commitment_hash'); x=dict(c); x.pop('commitment_hash',None); return h==_hash(x)
def join(commitment:dict,outcome:dict,*,joined_at_utc=None):
    if not verify_commitment(commitment): raise OutcomeError('invalid/tampered commitment')
    if not isinstance(outcome,dict) or outcome.get('record_type') not in {'OUTCOME','V2_OUTCOME'}: raise OutcomeError('compatible outcome required')
    if outcome.get('run_id')!=commitment.get('run_id'): raise OutcomeError('outcome run_id mismatch')
    ms=outcome.get('maturity_state')
    if ms not in {'IMMATURE','MATURE','EXPIRY_WITHOUT_TRIGGER','UNSCORABLE'}: raise OutcomeError('invalid maturity_state')
    matured=outcome.get('matured_at_utc') or joined_at_utc or datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
    if _dt(matured)<_dt(commitment['sealed_at_utc']): raise OutcomeError('outcome predates forward commitment')
    metrics={k:outcome.get(k) for k in ['realized_r','mfe_r','mae_r','time_to_trigger_seconds','time_to_mfe_seconds','cost_r','exit_reason'] if k in outcome}
    oh=_hash(outcome); seed=commitment['commitment_id']+'|'+oh
    out={'schema_version':'1.0.0','phase':PHASE,'record_type':'V2_OUTCOME_LINK','outcome_link_id':'V2OL_'+hashlib.sha256(seed.encode()).hexdigest()[:24].upper(),'commitment_id':commitment['commitment_id'],'commitment_hash':commitment['commitment_hash'],'run_id':commitment['run_id'],'sample_provenance':commitment['sample_provenance'],'true_forward_eligible':commitment['true_forward_eligible'],'independent_episode_key':commitment['independent_episode_key'],'trading_day':commitment['trading_day'],'regime':commitment.get('regime'),'hypothesis_family_id':commitment.get('hypothesis_family_id'),'features':commitment['features'],'maturity_state':ms,'matured_at_utc':matured,'joined_at_utc':joined_at_utc or datetime.now(timezone.utc).isoformat().replace('+00:00','Z'),'metrics':metrics,'outcome_hash':oh,'integrity':{'status':'PASS','commitment_rewritten':False,'outcome_after_commitment':True,'true_forward_label_preserved':True}}
    out['outcome_link_hash']=_hash(out)
    return out
