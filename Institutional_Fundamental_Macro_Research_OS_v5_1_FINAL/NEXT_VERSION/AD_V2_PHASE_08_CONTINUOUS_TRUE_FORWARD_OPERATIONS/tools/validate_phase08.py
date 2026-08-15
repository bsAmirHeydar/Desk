#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime,timezone,timedelta
import copy,json,sys,tempfile,hashlib,os
ROOT=Path(__file__).resolve().parents[1];PARENT=ROOT.parent;sys.path.insert(0,str(PARENT))
from AD_V2_PHASE_08_CONTINUOUS_TRUE_FORWARD_OPERATIONS.runtime.observations import validate as valobs,ingest,ObservationError
from AD_V2_PHASE_08_CONTINUOUS_TRUE_FORWARD_OPERATIONS.runtime.profiles import validate as valprof,register,active_for,ProfileError
from AD_V2_PHASE_08_CONTINUOUS_TRUE_FORWARD_OPERATIONS.runtime.eligibility import freeze_new
from AD_V2_PHASE_08_CONTINUOUS_TRUE_FORWARD_OPERATIONS.runtime.outcomes import mature_pending
from AD_V2_PHASE_08_CONTINUOUS_TRUE_FORWARD_OPERATIONS.runtime.operations import run_cycle,status
from AD_V2_PHASE_06_RUN_MEMORY_UX_INTEGRATION.runtime.v2_memory import build_extension,persist
from AD_V2_PHASE_08_CONTINUOUS_TRUE_FORWARD_OPERATIONS.runtime.store import root,hsh

def main():
 checks=[]
 def ck(n,c):checks.append({'name':n,'status':'PASS' if c else 'FAIL'})
 op=json.loads((ROOT/'config/observation_policy.json').read_text());cf=json.loads((ROOT/'config/continuous_forward_policy.json').read_text());prof=json.loads((ROOT/'tests/fixtures/evaluation_profile.json').read_text());obs=json.loads((ROOT/'tests/fixtures/gold_observations.json').read_text());template=json.loads((ROOT/'tests/fixtures/p06_gold_run_state_template.json').read_text())
 # observation semantics
 v=valobs(obs[0],op,now_utc='2026-08-15T11:02:00Z');ck('obs_valid',v['price']==4350.0 and bool(v['observation_hash']))
 try:
  bad=copy.deepcopy(obs[0]);bad['observed_at_utc']='2026-08-15T12:00:00Z';valobs(bad,op,now_utc='2026-08-15T11:00:00Z');ck('future_obs_blocked',False)
 except ObservationError:ck('future_obs_blocked',True)
 try:
  bad=copy.deepcopy(obs[0]);bad.pop('provenance_ref');valobs(bad,op,now_utc='2026-08-15T11:02:00Z');ck('obs_provenance_required',False)
 except ObservationError:ck('obs_provenance_required',True)
 # profile semantics
 vp=valprof(prof);ck('profile_valid',vp['one_r_price_distance']==10.0 and bool(vp['profile_hash']))
 try:
  bad=copy.deepcopy(prof);bad['one_r_price_distance']=0;valprof(bad);ck('risk_positive',False)
 except ProfileError:ck('risk_positive',True)
 with tempfile.TemporaryDirectory() as td:
  data=Path(td)/'data';state=copy.deepcopy(template);state['as_of']='2026-08-15T09:58:00Z';state['run_id']='RUN_P08_VALID';state['request_id']='REQ_P08_VALID';state['canonical_v2_state_hash']='sha256:'+hashlib.sha256(b'P08_VALID_STATE').hexdigest();state['base_run']['run_id']=state['run_id']
  ext=build_extension(state);ext['created_at_utc']='2026-08-15T10:00:00Z';x=dict(ext);x.pop('capsule_extension_hash',None);ext['capsule_extension_hash']='sha256:'+hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest();persist(data,ext)
  # profile sealed before commitment
  register(data,prof);ck('profile_registered',active_for(data,'SESSION_1_6H','2026-08-15T10:01:00Z')['profile_id']==prof['profile_id'])
  fr=freeze_new(data,PARENT,cf,now_utc='2026-08-15T10:01:00Z');ck('freeze_new_1',len(fr['new_commitments'])==1);ck('freeze_no_observation_read',fr['observation_store_read'] is False);b=fr['new_commitments'][0]['binding'];ck('profile_bound_before_outcome',b['evaluation_profile_id']==prof['profile_id']);ck('binding_scoring_enabled',b['automatic_r_scoring_enabled'] is True)
  fr2=freeze_new(data,PARENT,cf,now_utc='2026-08-15T10:02:00Z');ck('duplicate_run_not_refrozen',len(fr2['new_commitments'])==0)
  # identical dup + conflict
  r=ingest(data,[obs[0]],op,now_utc='2026-08-15T11:02:00Z');r2=ingest(data,[obs[0]],op,now_utc='2026-08-15T11:02:00Z');ck('identical_obs_idempotent',r['added']==1 and r2['identical_duplicates']==1)
  try:
   bad=copy.deepcopy(obs[0]);bad['price']=4351;ingest(data,[bad],op,now_utc='2026-08-15T11:02:00Z');ck('conflict_obs_blocked',False)
  except ObservationError:ck('conflict_obs_blocked',True)
  ingest(data,obs[1:],op,now_utc='2026-08-15T11:02:00Z')
  m=mature_pending(data,PARENT,now_utc='2026-08-15T11:02:00Z');ck('mature_linked_1',len(m['new_outcome_links'])==1);rec=m['new_outcome_links'][0];ck('mfe_4r',abs(rec['evaluation']['mfe_r']-4.0)<1e-9);ck('mae_half_r',abs(rec['evaluation']['mae_r']-0.5)<1e-9);ck('counterfactual_label',rec['evaluation']['counterfactual'] is True);ck('no_realized_r_fabricated','realized_r' not in rec['evaluation'])
  # status
  st=status(data);ck('status_pass',st['status']=='PASS');ck('mature_count_1',st['mature_linked']==1);ck('p07_mature_1',st['p07']['mature_true_forward']==1)
 # late rejection test isolated
 with tempfile.TemporaryDirectory() as td:
  data=Path(td)/'data';state=copy.deepcopy(template);state['as_of']='2026-08-15T09:00:00Z';state['run_id']='RUN_P08_LATE';state['request_id']='REQ_P08_LATE';state['canonical_v2_state_hash']='sha256:'+hashlib.sha256(b'late').hexdigest();state['base_run']['run_id']=state['run_id'];ext=build_extension(state);ext['created_at_utc']='2026-08-15T09:01:00Z';x=dict(ext);x.pop('capsule_extension_hash',None);ext['capsule_extension_hash']='sha256:'+hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest();persist(data,ext);fr=freeze_new(data,PARENT,cf,now_utc='2026-08-15T09:20:00Z');ck('late_run_rejected',len(fr['late_rejections'])==1 and len(fr['new_commitments'])==0)
 # no profile means no invented R
 with tempfile.TemporaryDirectory() as td:
  data=Path(td)/'data';state=copy.deepcopy(template);state['as_of']='2026-08-15T09:58:00Z';state['run_id']='RUN_P08_NOPROFILE';state['request_id']='REQ_P08_NOPROFILE';state['canonical_v2_state_hash']='sha256:'+hashlib.sha256(b'noprof').hexdigest();state['base_run']['run_id']=state['run_id'];ext=build_extension(state);ext['created_at_utc']='2026-08-15T10:00:00Z';x=dict(ext);x.pop('capsule_extension_hash',None);ext['capsule_extension_hash']='sha256:'+hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest();persist(data,ext);fr=freeze_new(data,PARENT,cf,now_utc='2026-08-15T10:01:00Z');ck('no_profile_commitment_still_frozen',len(fr['new_commitments'])==1);ck('no_profile_scoring_disabled',fr['new_commitments'][0]['binding']['automatic_r_scoring_enabled'] is False);m=mature_pending(data,PARENT,now_utc='2026-08-15T12:00:00Z');ck('no_profile_no_outcome',len(m['new_outcome_links'])==0 and any(x['status']=='PROFILE_REQUIRED' for x in m['results']))
 # cycle acceptance with no P06 runs; must preserve order and no promotion
 with tempfile.TemporaryDirectory() as td:
  data=Path(td)/'data';cy=run_cycle(data,ROOT,now_utc='2026-08-15T12:00:00Z');ck('cycle_pass',cy['status'] in {'PASS','PASS_WITH_WARNINGS'});ck('activation_receipt_present',cy.get('activation',{}).get('record_type')=='P08_ACTIVATION_RECEIPT');ck('cycle_order_integrity',cy['integrity']['freeze_before_observation_read'] is True);ck('cycle_no_auto_promotion',cy['promotion_observation']['independent_validator_approved'] is False and cy['promotion_observation']['auto_promoted'] is False);ck('cycle_permission_v1',cy['authority']['trade_permission']=='V1_INHERITED');ck('cycle_broker_none',cy['authority']['broker']=='NONE')
 # configs hard invariants
 ck('policy_freeze_before_obs',cf['freeze_before_observation_read'] is True);ck('pre_activation_baseline_ignore',cf['pre_activation_runs_action']=='IGNORE_AS_PRE_P08_BASELINE');ck('policy_auto_tf',cf['auto_sample_provenance']=='TRUE_FORWARD');ck('policy_no_auto_promotion',cf['auto_promotion'] is False);ck('obs_no_network',op['network_fetch_by_p08'] is False);ep=json.loads((ROOT/'config/evaluation_profile_policy.json').read_text());ck('no_default_r_profile',ep['default_profile'] is None and ep['synthetic_r_default_forbidden'] is True);sp=json.loads((ROOT/'config/scheduler_policy.json').read_text());ck('scheduler_not_auto_source_apply',sp['auto_install_during_source_apply'] is False);ck('scheduler_interval_5',sp['default_interval_minutes']==5)
 attacks=json.loads((ROOT/'tests/p08_attack_cases.json').read_text());ck('attack_cases_40',len(attacks['cases'])>=40)
 # source does not contain obvious credential values / network imports in runtime
 runtime='\n'.join(p.read_text(encoding='utf-8') for p in (ROOT/'runtime').glob('*.py'));ck('runtime_no_requests_import','import requests' not in runtime and 'urllib.request' not in runtime);ck('runtime_no_broker','broker_order' not in runtime.lower())
 failed=[x for x in checks if x['status']!='PASS'];out={'schema_version':'1.0.0','phase':'AD-V2-P08','status':'PASS' if not failed else 'FAIL','passed':len(checks)-len(failed),'failed':len(failed),'checks':checks,'deployment':'CONTINUOUS_TRUE_FORWARD_SHADOW','authority':{'v1_production':'UNCHANGED','trade_permission':'V1_INHERITED','broker':'NONE','auto_promotion':False}};print(json.dumps(out,indent=2));return 0 if not failed else 2
if __name__=='__main__':raise SystemExit(main())
