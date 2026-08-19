from __future__ import annotations
from .common import PHASE,load_json

def groups():return load_json(PHASE/'config/scientific_equivalence_groups.json',{}) or {}
def equivalent(a,b):
    for g in groups().get('groups',[]):
        ids=g.get('provider_ids',[])
        if a in ids and b in ids:return True
    return False

def choose(primary,candidates,health):
    ph=health.get(primary,{}).get('state')
    if ph=='HEALTHY':return {'provider_id':primary,'primary_failed':False,'fallback_used':False,'reason':'PRIMARY_HEALTHY'}
    for c in candidates:
        if equivalent(primary,c) and health.get(c,{}).get('state')=='HEALTHY':
            return {'provider_id':c,'primary_failed':True,'fallback_used':True,'fallback_provider':c,'reason':ph or 'PRIMARY_UNHEALTHY'}
    return {'provider_id':None,'primary_failed':True,'fallback_used':False,'reason':'NO_SCIENTIFICALLY_EQUIVALENT_HEALTHY_PROVIDER'}
