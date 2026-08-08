#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys
p=argparse.ArgumentParser();p.add_argument('--vault-root',required=True);a=p.parse_args();r=Path(a.vault_root);m=r/'100 Six-Market D2 Fact Books and Production Shadow Engine';e=[]
try:c=json.loads((m/'config/six_market_d2_coverage.json').read_text());sm=json.loads((m/'config/six_market_d2_source_map.json').read_text());sr=json.loads((m/'config/d2_source_registry.json').read_text())
except Exception as x:print(json.dumps({'status':'FAIL','errors':[str(x)]},indent=2));sys.exit(2)
markets=['XAUUSD','NASDAQ100','SP500','DJIA','EURUSD','USDJPY'];domains=['POSITIONING_OWNERSHIP','ACTUAL_FLOW','FUNDING_PLUMBING','INSTITUTIONAL_MECHANICS','MARKET_CAPACITY'];states={'FULL_PUBLIC','PARTIAL_PUBLIC','LICENSED_REQUIRED','UNAVAILABLE','UNDETERMINED'};ids={x['source_id'] for x in sr['sources']}
if c.get('production_universe')!=markets:e.append('UNIVERSE_MISMATCH')
if c.get('domains')!=domains:e.append('DOMAIN_MISMATCH')
for mk in markets:
    cells=c.get('coverage',{}).get(mk,{})
    if set(cells)!=set(domains):e.append('COVERAGE_DOMAIN_MISMATCH_'+mk)
    if set(sm.get('markets',{}).get(mk,{}))!=set(domains):e.append('SOURCE_MAP_DOMAIN_MISMATCH_'+mk)
    for d in domains:
        x=cells.get(d,{})
        if x.get('baseline_state') not in states:e.append('BAD_STATE_'+mk+'_'+d)
        if x.get('authority_mode')!='CANONICAL_SHADOW' or x.get('permission_effect_v18')!='NONE':e.append('D2_SOURCE_AUTHORITY_DRIFT_'+mk+'_'+d)
        for sid in sm.get('markets',{}).get(mk,{}).get(d,[]):
            if sid not in ids:e.append('UNKNOWN_SOURCE_'+mk+'_'+d+'_'+sid)
print(json.dumps({'status':'PASS' if not e else 'FAIL','markets':len(markets),'domains':len(domains),'cells':30,'registered_sources':len(ids),'errors':e},indent=2));sys.exit(0 if not e else 2)
