#!/usr/bin/env python3
from pathlib import Path
import argparse,json
p=argparse.ArgumentParser();p.add_argument('--vault-root',required=True);p.add_argument('--instrument',required=True);p.add_argument('--horizon',required=True);p.add_argument('--material-topic',default='');a=p.parse_args()
r=Path(a.vault_root); reg=json.loads((r/'100 Six-Market D2 Fact Books and Production Shadow Engine/config/fact_observability_registry.json').read_text()); mp=json.loads((r/'100 Six-Market D2 Fact Books and Production Shadow Engine/config/six_market_observability_map.json').read_text()); sr=json.loads((r/'100 Six-Market D2 Fact Books and Production Shadow Engine/config/d2_source_registry.json').read_text())
sources={s['source_id']:s for s in sr['sources']}; fams={f['family_id']:f for f in reg['families']}; out=[]
for fid,c in mp['markets'].get(a.instrument,{}).items():
    if c['materiality']=='NOT_MATERIAL' or a.horizon not in c.get('active_horizons',[]): continue
    f=fams[fid]; priority=[]
    for kind in ['direct_or_primary_source_ids','proxy_or_context_source_ids','licensed_or_private_source_ids']:
        for sid in f.get(kind,[]):
            if sid in sources: priority.append({'source_id':sid,'route':kind,'access_class':sources[sid].get('access_class'),'freshness_class':sources[sid].get('freshness_class'),'current_state_eligible':a.horizon in sources[sid].get('current_state_horizons',[])})
    out.append({'family_id':fid,'baseline_materiality':c['materiality'],'runtime_materiality':'TO_BE_ADJUDICATED','required_when':c['required_when'],'known_private_gap':c['known_private_gap'],'sources':priority})
print(json.dumps({'version':'1.0.0','instrument':a.instrument,'horizon':a.horizon,'material_topic':a.material_topic,'families':out,'principle':'SMALLEST_SUFFICIENT_MATERIAL_FACT_SET_NO_SILENT_GAPS'},indent=2))
