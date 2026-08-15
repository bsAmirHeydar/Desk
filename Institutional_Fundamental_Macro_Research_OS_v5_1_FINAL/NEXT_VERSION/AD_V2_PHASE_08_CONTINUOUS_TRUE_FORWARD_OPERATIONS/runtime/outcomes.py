#!/usr/bin/env python3
from __future__ import annotations
from datetime import datetime,timezone,timedelta
from pathlib import Path
import json
from .store import root,atomic_create,append,read_jsonl,hsh
from .observations import load as load_observations,dt
class OutcomeBuildError(ValueError):pass

def _load_p07(phase_parent):
    import sys
    if str(phase_parent) not in sys.path:sys.path.insert(0,str(phase_parent))
    from AD_V2_PHASE_07_D4_TRUE_FORWARD_PROMOTION.runtime.true_forward import read_jsonl as p07_read,persist_outcome_link
    from AD_V2_PHASE_07_D4_TRUE_FORWARD_PROMOTION.runtime.outcome_join import join
    return p07_read,persist_outcome_link,join

def _profile_from_binding(data_root,b):
    pid=b.get('evaluation_profile_id');ph=b.get('evaluation_profile_hash')
    if not pid:return None
    p=root(data_root)/'profiles'/pid/'profile.json'
    if not p.is_file():return None
    o=json.loads(p.read_text(encoding='utf-8'))
    if o.get('profile_hash')!=ph:return None
    return o

def _commitment_path(data_root,cid):return Path(data_root)/'alpha_desk_v2/p07_validation/commitments'/cid/'commitment.json'
def _receipt_path(data_root,cid):return root(data_root)/'maturity'/cid/'maturity_receipt.json'

def _coverage(obs,start,end,max_gap):
    rows=[x for x in obs if dt(x['observed_at_utc'])>=start and dt(x['observed_at_utc'])<=end]
    if not rows:return False,'NO_OBSERVATIONS',rows
    rows=sorted(rows,key=lambda x:dt(x['observed_at_utc']))
    if dt(rows[-1]['observed_at_utc'])<end:return False,'WINDOW_NOT_COMPLETE',rows
    times=[start]+[dt(x['observed_at_utc']) for x in rows]+[end]
    gaps=[(b-a).total_seconds() for a,b in zip(times,times[1:])]
    if gaps and max(gaps)>max_gap:return False,'OBSERVATION_GAP_TOO_LARGE',rows
    return True,'PASS',rows

def mature_pending(data_root,phase_parent,now_utc=None):
    now=dt(now_utc) if now_utc else datetime.now(timezone.utc);p07_read,persist_outcome_link,join=_load_p07(phase_parent);rt=root(data_root)
    bindings=read_jsonl(rt/'bindings/index.jsonl');out_index=p07_read(Path(data_root)/'alpha_desk_v2/p07_validation/outcomes/index.jsonl');linked={x.get('commitment_id') for x in out_index if x.get('commitment_id')};results=[];linked_new=[]
    # observation read happens here, after freeze phase
    obs=load_observations(data_root)
    for br in bindings:
        cid=br.get('commitment_id')
        if not cid or cid in linked:results.append({'commitment_id':cid,'status':'ALREADY_LINKED'});continue
        rp=_receipt_path(data_root,cid)
        if rp.exists():
            old=json.loads(rp.read_text(encoding='utf-8'));results.append({'commitment_id':cid,'status':old.get('status')});continue
        bp=Path(br.get('path',''))
        if not bp.is_file():results.append({'commitment_id':cid,'status':'BINDING_MISSING'});continue
        b=json.loads(bp.read_text(encoding='utf-8'));cp=_commitment_path(data_root,cid)
        if not cp.is_file():results.append({'commitment_id':cid,'status':'COMMITMENT_MISSING'});continue
        c=json.loads(cp.read_text(encoding='utf-8'));profile=_profile_from_binding(data_root,b)
        if not profile:
            results.append({'commitment_id':cid,'status':'PROFILE_REQUIRED'});continue
        start=dt(c['sealed_at_utc']);end=start+timedelta(seconds=int(profile['maturity_seconds']))
        if now<end:results.append({'commitment_id':cid,'status':'PENDING_MATURITY','matures_at_utc':end.isoformat().replace('+00:00','Z')});continue
        cap=start+timedelta(seconds=int(profile['reference_capture_seconds']))
        candidates=[x for x in obs if dt(x['observed_at_utc'])>=start and dt(x['observed_at_utc'])<=cap]
        if not candidates:results.append({'commitment_id':cid,'status':'PENDING_REFERENCE_OBSERVATION'});continue
        ref=sorted(candidates,key=lambda x:dt(x['observed_at_utc']))[0];ok,reason,rows=_coverage(obs,dt(ref['observed_at_utc']),end,int(profile['max_observation_gap_seconds']))
        if not ok:results.append({'commitment_id':cid,'status':'COVERAGE_INSUFFICIENT','reason':reason});continue
        direction=(c.get('features') or {}).get('pressure_sign');refp=float(ref['price']);prices=[float(x['price']) for x in rows]
        if direction=='BUY':fav=max(prices)-refp;adv=refp-min(prices);mfe_price=max(prices)
        elif direction=='SELL':fav=refp-min(prices);adv=max(prices)-refp;mfe_price=min(prices)
        else:results.append({'commitment_id':cid,'status':'UNSCORABLE','reason':'PRESSURE_SIGN_UNRESOLVED'});continue
        one=float(profile['one_r_price_distance']);mfe=max(0.0,fav)/one;mae=max(0.0,adv)/one
        mfe_row=min(rows,key=lambda x:abs(float(x['price'])-mfe_price));tmfe=max(0.0,(dt(mfe_row['observed_at_utc'])-dt(ref['observed_at_utc'])).total_seconds())
        raw={'schema_version':'1.0.0','phase':'AD-V2-P08','record_type':'P08_MATURITY_EVALUATION','commitment_id':cid,'run_id':c['run_id'],'profile_id':profile['profile_id'],'profile_hash':profile['profile_hash'],'counterfactual':profile.get('profile_kind')=='COUNTERFACTUAL_RESEARCH','reference_observation_id':ref['observation_id'],'reference_price':refp,'reference_at_utc':ref['observed_at_utc'],'maturity_end_utc':end.isoformat().replace('+00:00','Z'),'pressure_sign':direction,'mfe_r':mfe,'mae_r':mae,'time_to_mfe_seconds':tmfe,'observation_count':len(rows),'source_ids':sorted(set(x.get('source_id') for x in rows if x.get('source_id'))),'coverage_status':'PASS','evaluated_at_utc':now.isoformat().replace('+00:00','Z')};raw['evaluation_hash']=hsh(raw)
        outcome={'record_type':'OUTCOME','run_id':c['run_id'],'maturity_state':'MATURE','matured_at_utc':end.isoformat().replace('+00:00','Z'),'mfe_r':mfe,'mae_r':mae,'time_to_mfe_seconds':tmfe,'cost_r':0.0,'exit_reason':'COUNTERFACTUAL_MATURITY_WINDOW' if raw['counterfactual'] else 'PREDECLARED_EVALUATION_PROFILE'}
        ol=join(c,outcome,joined_at_utc=now.isoformat().replace('+00:00','Z'));persist_outcome_link(data_root,ol);linked.add(cid)
        rec={'schema_version':'1.0.0','phase':'AD-V2-P08','record_type':'P08_MATURITY_RECEIPT','commitment_id':cid,'status':'MATURE_LINKED','evaluation':raw,'p07_outcome_link_id':ol['outcome_link_id'],'p07_outcome_link_hash':ol['outcome_link_hash'],'authority':{'trade_permission':'V1_INHERITED','broker':'NONE'}};rec['receipt_hash']=hsh(rec);atomic_create(rp,rec);append(rt/'maturity/index.jsonl',{'commitment_id':cid,'status':'MATURE_LINKED','path':str(rp),'p07_outcome_link_id':ol['outcome_link_id'],'receipt_hash':rec['receipt_hash']});linked_new.append(rec);results.append({'commitment_id':cid,'status':'MATURE_LINKED'})
    return {'status':'PASS','observation_store_read':True,'results':results,'new_outcome_links':linked_new}
