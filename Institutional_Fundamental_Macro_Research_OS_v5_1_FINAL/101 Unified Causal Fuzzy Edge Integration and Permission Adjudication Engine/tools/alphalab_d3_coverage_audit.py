#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--vault-root',required=True);a=p.parse_args();r=Path(a.vault_root);e=[]
q=r/'101 Unified Causal Fuzzy Edge Integration and Permission Adjudication Engine/config/six_market_translation.json'
try:x=json.loads(q.read_text())
except Exception as z:print(json.dumps({'status':'FAIL','errors':[str(z)]},indent=2));sys.exit(2)
mk=['XAUUSD','NASDAQ100','SP500','DJIA','EURUSD','USDJPY']
if x.get('production_universe')!=mk:e.append('UNIVERSE_MISMATCH')
if not x.get('generic_sign_mapping_forbidden'):e.append('GENERIC_SIGN_MAPPING_NOT_FORBIDDEN')
for m in mk:
    z=x.get('markets',{}).get(m)
    if not z:e.append('MISSING_'+m);continue
    if not z.get('channels'):e.append('NO_CHANNELS_'+m)
    if not z.get('forbidden'):e.append('NO_FORBIDDEN_SHORTCUTS_'+m)
print(json.dumps({'status':'PASS' if not e else 'FAIL','markets':len(mk),'integration_books':len([m for m in mk if (r/f"101 Unified Causal Fuzzy Edge Integration and Permission Adjudication Engine/{21+mk.index(m):02d} {m} D3 Integration Book.md").exists()]),'errors':e},indent=2));sys.exit(0 if not e else 2)
