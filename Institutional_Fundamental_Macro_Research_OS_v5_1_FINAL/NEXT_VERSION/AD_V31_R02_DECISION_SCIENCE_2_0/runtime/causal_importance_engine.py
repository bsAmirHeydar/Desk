from __future__ import annotations
from .common import cfg

def infer_regime(p03=None,kernel=None,explicit=None):
    pol=cfg('regime_importance_policy.json');allowed=set(pol['states'])
    for v in (explicit,(p03 or {}).get('regime_context'),(kernel or {}).get('regime_context')):
        if isinstance(v,dict):v=v.get('state') or v.get('regime')
        if v in allowed:return v
    return pol['default_state']
def importance(root_id,horizon,regime='NORMAL'):
    mat=cfg('causal_importance_matrix.json');base=(mat.get('matrix',{}).get(root_id) or {}).get(horizon,'UNKNOWN');over=(cfg('regime_importance_policy.json').get('overrides',{}).get(regime) or {}).get(root_id);state=over or base
    return {'state':state,'root_id':root_id,'horizon':horizon,'regime':regime,'base_state':base,'regime_override':over,'source':'R02_CAUSAL_IMPORTANCE_MATRIX','llm_authority':False}
