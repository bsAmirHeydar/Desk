from __future__ import annotations
from .provider_registry import get

def assess(provider_id, probe=None):
    p=get(provider_id)
    if not p:return {'provider_id':provider_id,'state':'UNKNOWN','reason':'UNREGISTERED'}
    if p.get('access_class')=='PRIVATE' and not p.get('configured'):
        return {'provider_id':provider_id,'state':'UNAVAILABLE','reason':'PRIVATE_GAP'}
    if p.get('entitlement_required') and not p.get('entitled'):
        return {'provider_id':provider_id,'state':'ENTITLEMENT_MISSING','reason':'ENTITLEMENT_MISSING'}
    if not p.get('configured'):
        return {'provider_id':provider_id,'state':'UNAVAILABLE','reason':'NOT_CONFIGURED'}
    if probe is None:
        return {'provider_id':provider_id,'state':'UNKNOWN','reason':'NOT_PROBED'}
    if probe.get('rate_limited'): return {'provider_id':provider_id,'state':'RATE_LIMITED','reason':'RATE_LIMIT'}
    if probe.get('schema_ok') is False:return {'provider_id':provider_id,'state':'SCHEMA_DRIFT','reason':'SCHEMA_DRIFT'}
    if probe.get('reachable') is False:return {'provider_id':provider_id,'state':'UNAVAILABLE','reason':'UNREACHABLE'}
    if probe.get('fresh') is False:return {'provider_id':provider_id,'state':'STALE','reason':'STALE_ECONOMIC_TIME'}
    return {'provider_id':provider_id,'state':'HEALTHY','reason':'PROBE_PASS'}
