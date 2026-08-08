#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys
p=argparse.ArgumentParser();p.add_argument('--vault-root',required=True);a=p.parse_args();r=Path(a.vault_root);m=json.loads((r/'102 Forward Validation Calibration Promotion and Scientific Governance Engine/config/six_market_validation_map.json').read_text());err=[]
for k,v in m['markets'].items():
    if v.get('status')!='D4_FORWARD_ACTIVE':err.append(k+' inactive')
    if not (r/v['book']).exists():err.append(k+' book missing')
print(json.dumps({'status':'PASS' if not err else 'FAIL','markets_checked':len(m['markets']),'errors':err},indent=2));sys.exit(0 if not err else 2)
