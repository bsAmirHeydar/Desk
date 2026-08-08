#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys
try:
 import jsonschema
except Exception as e:
 print(json.dumps({'status':'FAIL','errors':['jsonschema unavailable: '+str(e)]},indent=2));sys.exit(2)
p=argparse.ArgumentParser();p.add_argument('--vault-root',required=True);a=p.parse_args();r=Path(a.vault_root);m=r/'103 Cognitive Multi-Hypothesis Scenario and Adversarial Intelligence Engine';errs=[];count=0
for f in sorted((m/'schemas').glob('*.schema.json')):
 try:
  s=json.loads(f.read_text(encoding='utf-8'));jsonschema.validators.validator_for(s).check_schema(s);count+=1
 except Exception as e:errs.append(f'{f.name}: {e}')
print(json.dumps({'status':'PASS' if not errs else 'FAIL','schemas_checked':count,'errors':errs},indent=2));sys.exit(0 if not errs else 2)
