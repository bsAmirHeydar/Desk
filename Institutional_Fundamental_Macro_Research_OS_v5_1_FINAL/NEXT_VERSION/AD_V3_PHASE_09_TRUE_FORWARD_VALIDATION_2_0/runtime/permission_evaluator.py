from __future__ import annotations
from .common import cfg

def evaluate(pred,metrics):
    pol=cfg('permission_evaluation_policy.json'); perm=pred.get('permission_candidate','WAIT'); q=metrics.get('path_quality','UNAVAILABLE'); d=metrics.get('direction_outcome','UNRESOLVED'); band=metrics.get('neutral_band_return') or 0; mfe=metrics.get('mfe_return'); mae=metrics.get('mae_return')
    if perm in ('BUY_CANDIDATE','SELL_CANDIDATE'):
        if q in ('CLEAN','ACCEPTABLE'):return {'permission_outcome':'SUPPORTED','wait_outcome':None}
        if q=='ADVERSE':return {'permission_outcome':'OPPOSED','wait_outcome':None}
        if q=='CHOPPY':return {'permission_outcome':'MIXED','wait_outcome':None}
        if q=='NO_MEANINGFUL_EDGE':return {'permission_outcome':'NEUTRAL','wait_outcome':None}
        return {'permission_outcome':'UNRESOLVED','wait_outcome':None}
    blockers=set(pred.get('permission_blockers') or [])
    if blockers.intersection(pol['wait_strong_uncertainty_blockers']):return {'permission_outcome':'NEUTRAL','wait_outcome':'WAIT_APPROPRIATE_UNCERTAINTY'}
    if q=='UNAVAILABLE':return {'permission_outcome':'NEUTRAL','wait_outcome':'WAIT_UNRESOLVED'}
    if d=='OPPOSED':return {'permission_outcome':'NEUTRAL','wait_outcome':'WAIT_PROTECTED'}
    if 'HIGH_CONSUMPTION' in blockers:
        if mfe is not None and mfe>=band*pol['wait_missed_opportunity_band_multiple'] and (mae or 0)<=band: return {'permission_outcome':'NEUTRAL','wait_outcome':'WAIT_MISSED_OPPORTUNITY'}
        return {'permission_outcome':'NEUTRAL','wait_outcome':'WAIT_PROTECTED'}
    if d=='ALIGNED' and q in ('CLEAN','ACCEPTABLE'):return {'permission_outcome':'NEUTRAL','wait_outcome':'WAIT_MISSED_OPPORTUNITY'}
    return {'permission_outcome':'NEUTRAL','wait_outcome':'WAIT_APPROPRIATE_UNCERTAINTY'}
