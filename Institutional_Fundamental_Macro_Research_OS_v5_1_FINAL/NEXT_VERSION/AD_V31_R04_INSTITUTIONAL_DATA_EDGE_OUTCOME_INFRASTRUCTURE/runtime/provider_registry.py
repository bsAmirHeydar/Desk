from __future__ import annotations
from .common import PHASE,load_json,env_present

def registry(): return load_json(PHASE/'config/provider_capability_registry.json',{}) or {}

def capabilities():
    out=[]
    for p in registry().get('providers',[]):
        q=dict(p); req=q.get('required_env') or []
        q['configured']=all(env_present(x) for x in req) if req else bool(q.get('configured_without_env',False))
        q['entitled']=q['configured'] if q.get('entitlement_required') else True
        if q.get('activation_state') in ('UNAVAILABLE','PRIVATE_GAP','PAID_GAP'):
            q['authorized_for_use']=False
        else:q['authorized_for_use']=bool(q['configured'] and q['entitled'])
        out.append(q)
    return out

def get(provider_id): return next((x for x in capabilities() if x['provider_id']==provider_id),None)

def access_counts():
    c={}
    for p in capabilities():c[p['access_class']]=c.get(p['access_class'],0)+1
    return c
