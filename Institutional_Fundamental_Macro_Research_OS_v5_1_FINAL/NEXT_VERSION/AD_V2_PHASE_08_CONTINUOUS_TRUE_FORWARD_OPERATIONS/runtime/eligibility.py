#!/usr/bin/env python3
from __future__ import annotations
from datetime import datetime,timezone
from pathlib import Path
import json,hashlib
from .store import root,atomic_create,append,event,hsh,read_jsonl
from .profiles import active_for
class EligibilityError(ValueError):pass

def dt(s):
    d=datetime.fromisoformat(str(s).replace('Z','+00:00'));return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
def _load_p06_modules(phase_parent):
    import sys
    if str(phase_parent) not in sys.path:sys.path.insert(0,str(phase_parent))
    from AD_V2_PHASE_06_RUN_MEMORY_UX_INTEGRATION.runtime.v2_memory import read_index,verify
    from AD_V2_PHASE_07_D4_TRUE_FORWARD_PROMOTION.runtime.feature_freeze import freeze
    from AD_V2_PHASE_07_D4_TRUE_FORWARD_PROMOTION.runtime.true_forward import persist_commitment,read_jsonl as p07_read
    return read_index,verify,freeze,persist_commitment,p07_read

def _disposition_path(data_root,run_id):return root(data_root)/'run_dispositions'/str(run_id)/'disposition.json'
def _binding_path(data_root,cid):return root(data_root)/'bindings'/cid/'binding.json'

def freeze_new(data_root,phase_parent,policy,now_utc=None,activation_cutoff_utc=None):
    now=dt(now_utc) if now_utc else datetime.now(timezone.utc);read_index,verify,freeze,persist_commitment,p07_read=_load_p06_modules(phase_parent)
    p07root=Path(data_root)/'alpha_desk_v2/p07_validation';committed={x.get('run_id') for x in p07_read(p07root/'commitments/index.jsonl') if x.get('run_id')}
    rows=read_index(data_root);new=[];late=[];skipped=[];invalid=[];baseline_ignored=[]
    # oldest first, bounded
    rows=sorted(rows,key=lambda x:dt(x.get('as_of')))
    for row in rows:
        if len(new)>=policy['max_new_commitments_per_cycle']:break
        run_id=row.get('run_id');
        if not run_id or run_id in committed:skipped.append({'run_id':run_id,'reason':'ALREADY_COMMITTED'});continue
        dp=_disposition_path(data_root,run_id)
        if dp.exists():skipped.append({'run_id':run_id,'reason':'DISPOSITION_EXISTS'});continue
        p=Path(row.get('path',''))
        if not p.is_file():invalid.append({'run_id':run_id,'reason':'P06_CAPSULE_MISSING'});continue
        # Pre-P08 history is a baseline, not a late true-forward failure.
        if activation_cutoff_utc and row.get('created_at_utc'):
            try:
                if dt(row.get('created_at_utc')) < dt(activation_cutoff_utc):
                    baseline_ignored.append({'run_id':run_id,'reason':'PRE_P08_BASELINE'});continue
            except Exception:
                pass
        v=verify(p)
        if v.get('status')!='PASS':invalid.append({'run_id':run_id,'reason':'P06_CAPSULE_VERIFY_FAIL'});continue
        ext=json.loads(p.read_text(encoding='utf-8'));state=ext.get('canonical_v2_state') or {}
        if state.get('subject')!='XAUUSD' or state.get('status')!='PASS' or ((state.get('integrity') or {}).get('status'))!='PASS':invalid.append({'run_id':run_id,'reason':'P06_STATE_NOT_ELIGIBLE'});continue
        if state.get('deployment') not in set(policy['allowed_p06_deployments']):invalid.append({'run_id':run_id,'reason':'P06_DEPLOYMENT_NOT_ALLOWED'});continue
        created=ext.get('created_at_utc');analysis=state.get('as_of')
        if not created or not analysis:invalid.append({'run_id':run_id,'reason':'TIMESTAMP_MISSING'});continue
        a_to_p06=(dt(created)-dt(analysis)).total_seconds();p06_to_now=(now-dt(created)).total_seconds()
        reason=None
        if a_to_p06<0 or a_to_p06>policy['max_analysis_to_p06_seal_seconds']:reason='ANALYSIS_TO_P06_SEAL_SLA_FAIL'
        elif p06_to_now<0 or p06_to_now>policy['max_p06_to_commitment_freeze_seconds']:reason='P06_TO_P08_FREEZE_SLA_FAIL'
        if reason:
            disp={'schema_version':'1.0.0','phase':'AD-V2-P08','record_type':'P08_RUN_DISPOSITION','run_id':run_id,'status':'LATE_TRUE_FORWARD_REJECTED','reason':reason,'analysis_to_p06_seal_seconds':a_to_p06,'p06_to_freeze_seconds':p06_to_now,'recorded_at_utc':now.isoformat().replace('+00:00','Z'),'true_forward_eligible':False,'authority':{'trade_permission':'V1_INHERITED','broker':'NONE'}};disp['disposition_hash']=hsh(disp);atomic_create(dp,disp);append(root(data_root)/'run_dispositions/index.jsonl',{'run_id':run_id,'status':disp['status'],'reason':reason,'path':str(dp),'disposition_hash':disp['disposition_hash']});late.append(disp);continue
        seal=now.isoformat().replace('+00:00','Z')
        c=freeze(state,sample_provenance='TRUE_FORWARD',sealed_at_utc=seal,regime=policy.get('default_regime','UNKNOWN'))
        pr=active_for(data_root,state.get('horizon'),seal)
        bind={'schema_version':'1.0.0','phase':'AD-V2-P08','record_type':'P08_OPERATING_BINDING','run_id':run_id,'p06_capsule_path':str(p),'p06_capsule_extension_hash':ext.get('capsule_extension_hash'),'p06_state_hash':state.get('canonical_v2_state_hash'),'commitment_id':c['commitment_id'],'commitment_hash':c['commitment_hash'],'sealed_at_utc':seal,'analysis_to_p06_seal_seconds':a_to_p06,'p06_to_commitment_freeze_seconds':p06_to_now,'evaluation_profile_id':pr.get('profile_id') if pr else None,'evaluation_profile_hash':pr.get('profile_hash') if pr else None,'automatic_r_scoring_enabled':bool(pr),'freeze_before_observation_read':True,'authority':{'trade_permission':'V1_INHERITED','broker':'NONE'}};bind['binding_hash']=hsh(bind)
        # persist P07 first, then immutable P08 binding; both occur before observation scan
        persist_commitment(data_root,c);atomic_create(_binding_path(data_root,c['commitment_id']),bind);append(root(data_root)/'bindings/index.jsonl',{'commitment_id':c['commitment_id'],'run_id':run_id,'profile_id':bind['evaluation_profile_id'],'automatic_r_scoring_enabled':bind['automatic_r_scoring_enabled'],'path':str(_binding_path(data_root,c['commitment_id'])),'binding_hash':bind['binding_hash']});committed.add(run_id);new.append({'commitment':c,'binding':bind})
    return {'status':'PASS','new_commitments':new,'late_rejections':late,'baseline_ignored':baseline_ignored,'skipped':skipped,'invalid':invalid,'observation_store_read':False}
