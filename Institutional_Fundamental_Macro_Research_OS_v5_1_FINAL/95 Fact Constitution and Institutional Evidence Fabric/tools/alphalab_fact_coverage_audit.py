#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys
p=argparse.ArgumentParser(); p.add_argument('--vault-root',required=True); a=p.parse_args(); r=Path(a.vault_root); m=r/'95 Fact Constitution and Institutional Evidence Fabric'
errors=[]
try:
    c=json.loads((m/'config/six_market_fact_coverage.json').read_text(encoding='utf-8')); reg=json.loads((m/'config/fact_family_registry.json').read_text(encoding='utf-8'))
except Exception as e: print(json.dumps({'status':'FAIL','errors':[str(e)]},indent=2)); sys.exit(2)
markets=['XAUUSD','NASDAQ100','SP500','DJIA','EURUSD','USDJPY']; fams=[x['id'] for x in reg['families']]
if c.get('production_universe')!=markets: errors.append('PRODUCTION_UNIVERSE_MISMATCH')
if len(fams)!=10 or len(set(fams))!=10: errors.append('FACT_FAMILY_COUNT_NOT_10')
for market in markets:
    cells=c.get('coverage',{}).get(market,{})
    if set(cells)!=set(fams): errors.append('COVERAGE_CELL_MISMATCH_'+market)
    for f,x in cells.items():
        if x.get('state')=='REGISTERED_D2_PENDING' and x.get('new_decision_authority') is not False: errors.append('D2_PENDING_PROMOTED_'+market+'_'+f)
print(json.dumps({'status':'PASS' if not errors else 'FAIL','markets':len(markets),'families':len(fams),'cells':len(markets)*len(fams),'errors':errors},indent=2)); sys.exit(0 if not errors else 2)
