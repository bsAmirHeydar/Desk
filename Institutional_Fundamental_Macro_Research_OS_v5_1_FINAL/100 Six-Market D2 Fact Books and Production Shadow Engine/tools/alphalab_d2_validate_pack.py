#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys
p=argparse.ArgumentParser();p.add_argument('--pack',required=True);a=p.parse_args();x=json.loads(Path(a.pack).read_text());e=[]
for k in ['version','authority_mode','instrument','analysis_cutoff_utc','positioning','actual_flow','funding_plumbing','institutional_mechanics','market_capacity','cross_science_independent_roots','d2_permission_effect','d3_promotion_state']:
    if k not in x:e.append('MISSING_'+k)
if x.get('version')!='1.0.0':e.append('VERSION')
if x.get('authority_mode')!='CANONICAL_SHADOW':e.append('AUTHORITY_NOT_SHADOW')
if x.get('d2_permission_effect')!='NONE':e.append('PREMATURE_D2_PERMISSION')
if x.get('d3_promotion_state') not in {'NOT_PROMOTED','PROMOTED_VIA_MODULE_101_ONLY'}:e.append('BAD_D3_PROMOTION_STATE')
print(json.dumps({'status':'PASS' if not e else 'FAIL','errors':e},indent=2));sys.exit(0 if not e else 2)
