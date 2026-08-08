#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--input',required=True);a=p.parse_args();x=json.loads(Path(a.input).read_text());e=[]
for k in ['version','instrument','fundamental_direction','final_direction','pre_d3_permission','final_permission','d3_edge_quality','reversal_hazard','asymmetry_state','validity_action','applied_rules','deduplicated_root_ids','direction_flip_forbidden','new_permission_creation_forbidden_v19']:
    if k not in x:e.append('MISSING_'+k)
if x.get('version')!='1.0.0':e.append('VERSION')
if x.get('final_direction')!=x.get('fundamental_direction'):e.append('DIRECTION_FLIP')
pre=x.get('pre_d3_permission');fin=x.get('final_permission')
if pre=='NO_TRADE' and fin!='NO_TRADE':e.append('NEW_PERMISSION_FROM_NO_TRADE')
if pre in {'BUY','SELL'} and fin not in {pre,'NO_TRADE'}:e.append('PERMISSION_INVERSION')
if x.get('direction_flip_forbidden') is not True:e.append('DIRECTION_GUARD_FALSE')
if x.get('new_permission_creation_forbidden_v19') is not True:e.append('PROMOTION_GUARD_FALSE')
print(json.dumps({'status':'PASS' if not e else 'FAIL','errors':e},indent=2));sys.exit(0 if not e else 2)
