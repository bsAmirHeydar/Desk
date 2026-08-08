#!/usr/bin/env python3
from pathlib import Path
import argparse,json,hashlib,datetime,sys

def canon(o): return json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def rh(o): return hashlib.sha256(canon(o).encode('utf-8')).hexdigest()
p=argparse.ArgumentParser();p.add_argument('--ledger',required=True);p.add_argument('--record',required=True);a=p.parse_args()
ledger=Path(a.ledger);rec=json.loads(Path(a.record).read_text(encoding='utf-8'))
if 'record_type' not in rec: raise SystemExit('record_type required')
ledger.parent.mkdir(parents=True,exist_ok=True)
prev='GENESIS'
ids=set()
if ledger.exists():
    for i,line in enumerate(ledger.read_text(encoding='utf-8').splitlines(),1):
        if not line.strip(): continue
        old=json.loads(line); ids.add(old.get('record_id')); prev=old.get('record_hash','')
        tmp=dict(old); got=tmp.pop('record_hash',None)
        if got!=rh(tmp): raise SystemExit(f'ledger hash failure at line {i}')
record_id=rec.get('record_id') or rec.get('run_id') or rec.get('outcome_id') or rec.get('counterfactual_id') or rec.get('calibration_id') or rec.get('proposal_id') or rec.get('validator_decision_id') or rec.get('alert_id')
if not record_id: raise SystemExit('stable record id required')
if record_id in ids: raise SystemExit('duplicate record id: '+record_id)
wrap={'record_type':rec['record_type'],'record_id':record_id,'created_at_utc':rec.get('created_at_utc') or datetime.datetime.now(datetime.timezone.utc).isoformat(),'previous_record_hash':prev,'payload':rec}
wrap['record_hash']=rh(wrap)
with ledger.open('a',encoding='utf-8',newline='\n') as f:f.write(json.dumps(wrap,ensure_ascii=False,sort_keys=True)+'\n')
print(json.dumps({'status':'PASS','record_id':record_id,'record_hash':wrap['record_hash']},indent=2))
