from __future__ import annotations
from pathlib import Path
from collections import defaultdict
from .common import config,load,iso

def sample_state(n):
    if n<=0:return 'UNAVAILABLE'
    if n<20:return 'INSUFFICIENT'
    if n<50:return 'EARLY'
    if n<100:return 'USABLE'
    return 'MATURE'

def load_registry(path=None):
    if path and Path(path).exists(): return load(path)
    return {'record_type':'AD_V3_P08_EMPIRICAL_CALIBRATION_REGISTRY','method_version':config('empirical_calibration_policy.json')['method_version'],'generated_at_utc':None,'overall_sample_state':'UNAVAILABLE','episode_count':0,'entries':[],'historical_calibration_is_not_forward_validation':True}

def authority_for(registry,root_id,horizon):
    row=next((x for x in registry.get('entries') or [] if x.get('root_id')==root_id and x.get('horizon')==horizon),None)
    if not row:return {'state':'UNAVAILABLE','sample_state':'UNAVAILABLE','sample_count':0}
    return {'state':row.get('empirical_authority','NEUTRAL'),'sample_state':row.get('sample_state','UNAVAILABLE'),'sample_count':row.get('sample_count',0),'shrunken_alignment':row.get('shrunken_alignment')}

def split_calibration_holdout(episodes):
    rows=sorted(episodes,key=lambda x:x.get('start_utc') or '')
    if len(rows)<100: return rows,[], 'INSUFFICIENT_FOR_HOLDOUT'
    cut=max(1,int(len(rows)*0.7)); return rows[:cut],rows[cut:],'TIME_ORDERED_70_30'

def calibrate_from_episodes(episodes,horizon='SESSION_1_6H'):
    pol=config('empirical_calibration_policy.json'); calibration,holdout,split_state=split_calibration_holdout(episodes); by=defaultdict(list)
    for e in calibration:
        rid=e.get('dominant_root'); out=e.get('outcome_alignment')
        if rid and out in ('ALIGNED','OPPOSED'): by[(rid,e.get('horizon') or horizon)].append(out)
    entries=[]
    for (rid,h),outs in sorted(by.items()):
        n=len(outs); aligned=sum(x=='ALIGNED' for x in outs); prior=pol['shrinkage_prior_samples']; shr=(aligned+prior*pol['neutral_alignment_prior'])/(n+prior); ss=sample_state(n)
        auth='NEUTRAL'
        if n>=pol['minimum_active_empirical_samples']:
            auth='SUPPORTIVE' if shr>=pol['supportive_threshold'] else 'CAUTION' if shr<=pol['caution_threshold'] else 'NEUTRAL'
        entries.append({'root_id':rid,'horizon':h,'sample_count':n,'sample_state':ss,'aligned_count':aligned,'opposed_count':n-aligned,'shrunken_alignment':round(shr,6),'empirical_authority':auth})
    total=sum(x['sample_count'] for x in entries); return {'record_type':'AD_V3_P08_EMPIRICAL_CALIBRATION_REGISTRY','method_version':pol['method_version'],'generated_at_utc':iso(),'overall_sample_state':sample_state(total),'episode_count':len(episodes),'calibration_episode_count':len(calibration),'holdout_episode_count':len(holdout),'holdout_state':split_state,'evaluated_episode_count':total,'entries':entries,'historical_calibration_is_not_forward_validation':True}
