#!/usr/bin/env python3
from pathlib import Path
import argparse,json,hashlib,sys

def canon(o):return json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def rh(o):return hashlib.sha256(canon(o).encode()).hexdigest()
p=argparse.ArgumentParser();p.add_argument('--ledger',required=True);a=p.parse_args();q=Path(a.ledger);prev='GENESIS';n=0;ids=set();err=[]
if not q.exists(): raise SystemExit('ledger not found')
for i,line in enumerate(q.read_text(encoding='utf-8').splitlines(),1):
    if not line.strip():continue
    n+=1
    try:o=json.loads(line)
    except Exception as e:err.append(f'line {i} json {e}');continue
    if o.get('previous_record_hash')!=prev:err.append(f'line {i} previous hash mismatch')
    t=dict(o);got=t.pop('record_hash',None);calc=rh(t)
    if got!=calc:err.append(f'line {i} record hash mismatch')
    if o.get('record_id') in ids:err.append(f'line {i} duplicate id')
    ids.add(o.get('record_id'));prev=got
print(json.dumps({'status':'PASS' if not err else 'FAIL','records':n,'last_hash':prev,'errors':err},indent=2));sys.exit(0 if not err else 2)
