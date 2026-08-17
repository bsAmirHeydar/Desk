from __future__ import annotations
from datetime import timedelta
from .common import cfg,parse_dt,stable_id,iso

def _same_primary(a,p):
    return a.get('causal_direction')==p.get('causal_direction') and a.get('dominant_root')==p.get('dominant_root') and a.get('permission_candidate')==p.get('permission_candidate')
def _material(a,p):
    keys=('dominance_state','pressure_strength','contradiction')
    return any(a.get(k)!=p.get(k) for k in keys)
def assign_episode(state,pred,now=None):
    if any(k in pred for k in ('future_price','terminal_return','outcome','future_path')): raise ValueError('LOOKAHEAD_EPISODE_INPUT_REJECTED')
    pol=cfg('episode_policy.json'); nowdt=parse_dt(now or pred['precommit_time']); open_eps=[e for e in state['episodes'] if e.get('state')=='OPEN' and e.get('cohort_id')==pred['cohort_id'] and e.get('horizon')==pred['horizon']]
    ep=open_eps[-1] if open_eps else None
    if ep:
        start=parse_dt(ep['start_time']); maxh=(pol.get('max_episode_wall_hours_by_horizon') or {}).get(pred['horizon'],24)
        expired=bool(start and nowdt and nowdt-start>timedelta(hours=float(maxh)))
        anchor=ep['anchor_state']
        if expired or not _same_primary(anchor,pred):
            ep['state']='CLOSED';ep['closed_at_utc']=iso(nowdt);ep['close_reason']='MAX_DURATION_EXCEEDED' if expired else 'MATERIAL_PRIMARY_STATE_CHANGE';ep=None
    if not ep:
        core={k:pred.get(k) for k in ['causal_direction','dominance_state','dominant_root','pressure_strength','permission_candidate','contradiction']}
        ep={'record_type':'AD_V3_P09_FORWARD_EPISODE','episode_id':stable_id('P09EP',{'cohort':pred['cohort_id'],'horizon':pred['horizon'],'start':pred['precommit_time'],'core':core}),'cohort_id':pred['cohort_id'],'horizon':pred['horizon'],'state':'OPEN','start_time':pred['precommit_time'],'anchor_state':core,'prediction_ids':[],'primary_prediction_id':pred['prediction_id'],'material_update_prediction_ids':[],'independent_sample_count':1,'membership_future_price_used':False}
        state['episodes'].append(ep);role='PRIMARY_EPISODE_SAMPLE'
    else:
        role='MATERIAL_UPDATE' if _material(ep['anchor_state'],pred) else 'DUPLICATE_EPISODE_SNAPSHOT'
        if role=='MATERIAL_UPDATE':ep['material_update_prediction_ids'].append(pred['prediction_id'])
    ep['prediction_ids'].append(pred['prediction_id'])
    pred['episode_id']=ep['episode_id'];pred['sample_role']=role
    if role!='PRIMARY_EPISODE_SAMPLE' and pred.get('eligibility')=='VALIDATION_ELIGIBLE':pred['eligibility']='DUPLICATE_EPISODE_SNAPSHOT'
    return state,pred,ep
