from __future__ import annotations
import datetime
from .common import config,stable_id
FORBIDDEN={'future_price_reversal','future_outcome_used_for_boundary','future_price','future_return'}
def _dt(x): return datetime.datetime.fromisoformat(str(x).replace('Z','+00:00'))
def build_episodes(decisions):
    pol=config('empirical_calibration_policy.json'); fields=pol['episode_signature_fields']; maxgap=datetime.timedelta(hours=pol['max_unchanged_episode_gap_hours'])
    rows=sorted(decisions,key=lambda x:x.get('generated_at_utc') or '')
    for r in rows:
        if FORBIDDEN.intersection(r): raise ValueError('LOOKAHEAD_BOUNDARY_FIELD_FORBIDDEN')
    eps=[]; cur=None
    for r in rows:
        sig=tuple(r.get(k) for k in fields); t=_dt(r['generated_at_utc'])
        new=cur is None or sig!=cur['_sig'] or t-cur['_last_t']>maxgap
        if new:
            if cur:
                cur.pop('_sig');cur.pop('_last_t');eps.append(cur)
            cur={'episode_id':stable_id('P08EP',{'start':r['generated_at_utc'],'sig':sig}),'start_utc':r['generated_at_utc'],'end_utc':r['generated_at_utc'],'horizon':r.get('horizon','SESSION_1_6H'),'causal_direction':r.get('causal_direction'),'dominant_root':r.get('dominant_root'),'pressure_strength':r.get('pressure_strength'),'dominance_state':r.get('dominance_state'),'run_count':1,'run_ids':[r.get('run_id')],'outcome_alignment':r.get('outcome_alignment'),'_sig':sig,'_last_t':t}
        else:
            cur['end_utc']=r['generated_at_utc'];cur['run_count']+=1;cur['run_ids'].append(r.get('run_id'));cur['_last_t']=t
            # Outcome is evaluation metadata, never boundary authority.
            if r.get('outcome_alignment') in ('ALIGNED','OPPOSED'): cur['outcome_alignment']=r.get('outcome_alignment')
    if cur:
        cur.pop('_sig');cur.pop('_last_t');eps.append(cur)
    return eps
