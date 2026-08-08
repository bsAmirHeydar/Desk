#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys,datetime
p=argparse.ArgumentParser();p.add_argument('--registry',required=True);a=p.parse_args();r=json.loads(Path(a.registry).read_text());e=[];ids=set();valid={'REPORT_ONLY','CONFIDENCE_CAP','VALIDITY_SHORTEN','DELAY_PERMISSION','SUPPRESS_PERMISSION','CAPACITY_BLOCK','RESTORE_EXISTING_DIRECTION_PERMISSION','CREATE_PERMISSION_WITH_EXISTING_FUNDAMENTAL_DIRECTION'}
for i,x in enumerate(r.get('records',[])):
    pid=x.get('promotion_id')
    if not pid:e.append(f'record {i} missing promotion_id')
    if pid in ids:e.append('duplicate promotion_id '+str(pid))
    ids.add(pid)
    if x.get('status') not in {'ACTIVE','SUSPENDED','RETIRED'}:e.append(str(pid)+' invalid status')
    if x.get('authority_class') not in valid:e.append(str(pid)+' invalid authority_class')
    if x.get('authority_class')=='CREATE_PERMISSION_WITH_EXISTING_FUNDAMENTAL_DIRECTION' and x.get('allowed_preconditions',{}).get('requires_directional_fundamental') is not True:e.append(str(pid)+' positive create missing directional fundamental guard')
    if x.get('status')=='ACTIVE' and not x.get('validator_decision_id'):e.append(str(pid)+' active without validator decision')
print(json.dumps({'status':'PASS' if not e else 'FAIL','records':len(r.get('records',[])),'errors':e},indent=2));sys.exit(0 if not e else 2)
