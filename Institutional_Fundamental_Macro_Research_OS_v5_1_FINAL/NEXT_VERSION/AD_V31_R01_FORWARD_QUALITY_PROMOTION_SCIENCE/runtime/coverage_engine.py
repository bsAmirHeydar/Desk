from __future__ import annotations
from collections import Counter
from .common import cfg

def vol_regime(v):
    if not isinstance(v,(int,float)) or v<=0:return 'UNOBSERVED'
    for r in cfg('coverage_policy.json')['volatility_regime_policy']['bands']:
        if r['max'] is None or v<=r['max']:return r['state']
    return 'STRESS'
def compute(rows):
    pol=cfg('coverage_policy.json');req=pol['hard_requirements'];dirs=Counter(p.get('causal_direction') for p,o,e in rows);perms=Counter(p.get('permission_candidate') for p,o,e in rows);events=Counter(o.get('event_exposure') for p,o,e in rows);vols=Counter(vol_regime(p.get('volatility_reference')) for p,o,e in rows);roots=Counter(p.get('dominant_root') or 'UNKNOWN' for p,o,e in rows);n=len(rows);maxroot=max(roots.values())/n if n and roots else None;goodvol=[k for k,v in vols.items() if k!='UNOBSERVED' and v>=req['min_episodes_per_volatility_regime']]
    checks={
      'evaluated_primary':n>=req['min_evaluated_primary_episodes'],
      'bullish':dirs['BULLISH_GOLD']>=req['min_bullish_episodes'],
      'bearish':dirs['BEARISH_GOLD']>=req['min_bearish_episodes'],
      'actionable_permission':(perms['BUY_CANDIDATE']+perms['SELL_CANDIDATE'])>=req['min_actionable_permission_episodes'],
      'wait':perms['WAIT']>=req['min_wait_episodes'],
      'event_exposed':events['EVENT_EXPOSED']>=req['min_event_exposed_episodes'],
      'event_free':events['EVENT_FREE']>=req['min_event_free_episodes'],
      'volatility_regimes':len(goodvol)>=req['min_volatility_regimes'],
      'root_concentration':bool(maxroot is not None and maxroot<=req['max_dominant_root_share'])
    }
    return {'record_type':'AD_V31_R01_COVERAGE_MATRIX','state':'PASS' if all(checks.values()) else 'INSUFFICIENT','counts':{'evaluated_primary':n,'direction':dict(dirs),'permission':dict(perms),'event':dict(events),'volatility_regime':dict(vols),'dominant_root':dict(roots),'max_dominant_root_share':maxroot},'requirements':req,'checks':checks,'covered_volatility_regimes':goodvol}
