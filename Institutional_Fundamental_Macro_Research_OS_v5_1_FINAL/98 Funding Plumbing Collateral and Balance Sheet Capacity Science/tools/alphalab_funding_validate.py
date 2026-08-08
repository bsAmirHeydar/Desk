#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys
p=argparse.ArgumentParser();p.add_argument('--state',required=True);a=p.parse_args();x=json.loads(Path(a.state).read_text());e=[]
for k in ['instrument','as_of_utc','authority_mode','coverage_state','stress_state','evidence_ids','permission_effect_v18']:
    if k not in x:e.append('MISSING_'+k)
if x.get('authority_mode')!='CANONICAL_SHADOW':e.append('AUTHORITY_NOT_SHADOW')
if x.get('permission_effect_v18')!='NONE':e.append('PREMATURE_PERMISSION_EFFECT')
print(json.dumps({'status':'PASS' if not e else 'FAIL','errors':e},indent=2));sys.exit(0 if not e else 2)
