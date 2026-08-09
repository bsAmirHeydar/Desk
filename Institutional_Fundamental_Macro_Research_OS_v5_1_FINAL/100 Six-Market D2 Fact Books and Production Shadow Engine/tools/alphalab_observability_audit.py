#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys
p=argparse.ArgumentParser();p.add_argument('--vault-root',required=True);a=p.parse_args();r=Path(a.vault_root);e=[]
base=r/'100 Six-Market D2 Fact Books and Production Shadow Engine/config'
reg=json.loads((base/'fact_observability_registry.json').read_text());mp=json.loads((base/'six_market_observability_map.json').read_text());sr=json.loads((base/'d2_source_registry.json').read_text())
fids=[f['family_id'] for f in reg['families']]; sids=[s['source_id'] for s in sr['sources']]
if len(fids)!=16:e.append('EXPECTED_16_OBSERVABILITY_FAMILIES')
if len(fids)!=len(set(fids)):e.append('DUPLICATE_FAMILY_ID')
if len(sids)!=len(set(sids)):e.append('DUPLICATE_SOURCE_ID')
markets=['XAUUSD','NASDAQ100','SP500','DJIA','EURUSD','USDJPY']
for m in markets:
 cells=mp.get('markets',{}).get(m,{})
 if set(cells)!=set(fids):e.append('MARKET_FAMILY_SET_MISMATCH_'+m)
 for fid,c in cells.items():
  if c.get('materiality') not in {'DECISION_CRITICAL','MATERIAL','SUPPORTING','CONTEXTUAL','NOT_MATERIAL'}:e.append('BAD_MATERIALITY_'+m+'_'+fid)
for f in reg['families']:
 for k in ['direct_or_primary_source_ids','proxy_or_context_source_ids','licensed_or_private_source_ids']:
  for sid in f.get(k,[]):
   if sid not in sids: e.append('UNKNOWN_SOURCE_'+fid+'_'+sid)
required_meta=['access_class','freshness_class','fact_semantics','current_state_horizons','context_horizons','prohibited_inferences']
for s in sr['sources']:
 for k in required_meta:
  if k not in s:e.append('SOURCE_MISSING_'+k+'_'+s['source_id'])
print(json.dumps({'status':'PASS' if not e else 'FAIL','families':len(fids),'markets':len(markets),'cells':sum(len(mp['markets'][m]) for m in markets),'sources':len(sids),'errors':e},indent=2));sys.exit(0 if not e else 2)
