#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys
p=argparse.ArgumentParser();p.add_argument('--vault-root',required=True);a=p.parse_args();r=Path(a.vault_root);m=r/'103 Cognitive Multi-Hypothesis Scenario and Adversarial Intelligence Engine';e=[]
markets=['XAUUSD','NASDAQ100','SP500','DJIA','EURUSD','USDJPY']
mapf=m/'config/six_market_cognitive_map.json'
try:o=json.loads(mapf.read_text(encoding='utf-8'))
except Exception as x:o={};e.append('MAP_PARSE '+str(x))
for s in markets:
    if s not in (o.get('markets') or {}):e.append('MISSING_MAP_'+s)
books={'XAUUSD':'40 XAUUSD Cognitive Book.md','NASDAQ100':'41 NASDAQ100 Cognitive Book.md','SP500':'42 SP500 Cognitive Book.md','DJIA':'43 DJIA Cognitive Book.md','EURUSD':'44 EURUSD Cognitive Book.md','USDJPY':'45 USDJPY Cognitive Book.md'}
for s,f in books.items():
    if not (m/f).exists():e.append('MISSING_BOOK_'+s)
print(json.dumps({'status':'PASS' if not e else 'FAIL','markets':len(markets),'books':sum((m/f).exists() for f in books.values()),'errors':e},indent=2));sys.exit(0 if not e else 2)
