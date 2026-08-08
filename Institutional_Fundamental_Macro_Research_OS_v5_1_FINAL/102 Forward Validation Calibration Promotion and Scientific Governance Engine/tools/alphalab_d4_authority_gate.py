#!/usr/bin/env python3
import argparse,json,hashlib,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--registry',required=True);a=p.parse_args();inp=json.loads(Path(a.input).read_text());regp=Path(a.registry);reg=json.loads(regp.read_text());fund=inp.get('fundamental_direction');base=inp.get('v19_d3_permission');final=base;applied=[];shadow=[];reasons=[]
for c in inp.get('promotion_candidates',[]):
    mid=c.get('modifier_id');matches=[x for x in reg.get('records',[]) if x.get('modifier_id')==mid and x.get('status')=='ACTIVE']
    if not matches:shadow.append(mid);continue
    x=matches[0];scope=x.get('scope',{})
    if scope.get('instruments') and inp.get('instrument') not in scope['instruments']:shadow.append(mid);continue
    cls=x.get('authority_class');proposed=c.get('proposed_permission')
    if cls in {'RESTORE_EXISTING_DIRECTION_PERMISSION','CREATE_PERMISSION_WITH_EXISTING_FUNDAMENTAL_DIRECTION'}:
        if fund not in {'BULLISH','BEARISH'}:reasons.append(mid+': fundamental direction guard');continue
        expected='BUY' if fund=='BULLISH' else 'SELL'
        if proposed!=expected:reasons.append(mid+': proposed permission conflicts with fundamental');continue
        final=proposed;applied.append(x['promotion_id'])
    elif cls in {'SUPPRESS_PERMISSION','CAPACITY_BLOCK','DELAY_PERMISSION'} and c.get('proposed_permission')=='NO_TRADE':final='NO_TRADE';applied.append(x['promotion_id'])
    else:applied.append(x['promotion_id'])
receipt={'registry_version':reg.get('version'),'registry_sha256':hashlib.sha256(regp.read_bytes()).hexdigest(),'fundamental_direction':fund,'v19_d3_permission':base,'final_v20_permission':final,'applied_promotion_ids':applied,'shadow_candidate_ids':shadow,'fail_closed_reasons':reasons}
print(json.dumps(receipt,indent=2))
