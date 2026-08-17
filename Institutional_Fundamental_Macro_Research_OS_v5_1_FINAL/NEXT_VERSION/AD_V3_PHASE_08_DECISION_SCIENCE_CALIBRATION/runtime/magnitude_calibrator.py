from __future__ import annotations
from .common import config

def magnitude_from_root(root, rows):
    p=config('magnitude_policy.json'); best=None; source='P03_ROOT_STRENGTH_PROXY'
    # Use standardized numeric fields only when already present in governed row details.
    for r in rows:
        d=r.get('details') or {}
        for k in p.get('recognized_standardized_fields') or []:
            v=d.get(k)
            if isinstance(v,(int,float)):
                a=abs(float(v)); st='EXTREME' if a>=p['z_abs_thresholds']['EXTREME'] else 'LARGE' if a>=p['z_abs_thresholds']['LARGE'] else 'MATERIAL' if a>=p['z_abs_thresholds']['MATERIAL'] else 'MINOR'
                if best is None or p['rank'][st]>p['rank'][best]: best=st; source='STANDARDIZED_NUMERIC_FIELD:'+k
    if best is None: best=p['p03_strength_mapping'].get(root.get('strength','UNKNOWN'),'UNKNOWN')
    return {'state':best,'source':source,'direction_inferred':False}
