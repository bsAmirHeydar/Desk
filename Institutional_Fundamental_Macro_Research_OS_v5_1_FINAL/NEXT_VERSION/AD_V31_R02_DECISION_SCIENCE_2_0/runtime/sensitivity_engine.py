from __future__ import annotations
from .common import cfg
from .robust_dominance_engine import reconcile

def evaluate(roots):
    pol=cfg('dominance_robustness_policy.json');results=[reconcile([dict(x) for x in roots],v) for v in pol['variants']];canonical=results[0];cd=canonical['causal_direction'];dirs=[x['causal_direction'] for x in results];directional=set(x for x in dirs if x in ('BULLISH_GOLD','BEARISH_GOLD'))
    if cd not in ('BULLISH_GOLD','BEARISH_GOLD'):
        rob='NOT_APPLICABLE';sens='NOT_APPLICABLE'
    elif len(directional)>1:
        rob='UNSTABLE';sens='HIGH'
    else:
        mixed=sum(x=='MIXED' for x in dirs)
        same=sum(x==cd for x in dirs)
        if same==len(results):rob='ROBUST';sens='LOW'
        elif mixed<=2 and same>=len(results)-2:rob='MOSTLY_ROBUST';sens='ELEVATED'
        else:rob='MODEL_SENSITIVE';sens='HIGH'
    return {'canonical':canonical,'variants':[{'variant_id':v['variant_id'],'causal_direction':r['causal_direction'],'dominance_state':r['dominance_state'],'dominant_root':r['dominant_root'],'contradiction':r['contradiction']} for v,r in zip(pol['variants'],results)],'robustness':rob,'model_sensitivity':sens,'variant_count':len(results),'variant_frequency_is_not_probability':True}
