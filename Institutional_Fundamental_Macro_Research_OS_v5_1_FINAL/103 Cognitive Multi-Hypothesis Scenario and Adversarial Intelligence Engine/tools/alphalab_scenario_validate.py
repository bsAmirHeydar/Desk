#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys
p=argparse.ArgumentParser();p.add_argument('--input',required=True);a=p.parse_args();x=json.loads(Path(a.input).read_text(encoding='utf-8'));e=[]
sc=x.get('scenarios') or []
if not 2<=len(sc)<=6:e.append('Scenario count must be 2..6.')
ids=[s.get('scenario_id') for s in sc]
if len(ids)!=len(set(ids)):e.append('Duplicate scenario_id.')
if x.get('numeric_probabilities_used') is not False:e.append('Numeric probabilities not authorized.')
for s in sc:
    for k in ['required_conditions','early_indicators','confirmation_triggers','invalidation_triggers','expected_leaders','expected_market_signature','transition_paths']:
        if k not in s:e.append(f"{s.get('scenario_id')}: missing {k}")
    if not s.get('confirmation_triggers') and not s.get('invalidation_triggers'):e.append(f"{s.get('scenario_id')}: no observable trigger")
    for t in s.get('transition_paths') or []:
        if t.get('to_scenario_id') not in ids:e.append(f"{s.get('scenario_id')}: transition target missing {t.get('to_scenario_id')}")
print(json.dumps({'status':'PASS' if not e else 'FAIL','scenario_count':len(sc),'errors':e},indent=2));sys.exit(0 if not e else 2)
