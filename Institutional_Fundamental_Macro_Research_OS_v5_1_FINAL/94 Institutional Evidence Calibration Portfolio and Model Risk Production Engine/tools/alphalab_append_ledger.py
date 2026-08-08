#!/usr/bin/env python3
import argparse,json,hashlib,datetime,os
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('--ledger',required=True); p.add_argument('--record',required=True); a=p.parse_args()
rec=json.loads(Path(a.record).read_text(encoding='utf-8')); raw=json.dumps(rec,sort_keys=True,separators=(',',':')).encode(); rec['_record_sha256']=hashlib.sha256(raw).hexdigest()
l=Path(a.ledger); l.parent.mkdir(parents=True,exist_ok=True)
with l.open('a',encoding='utf-8',newline='\n') as f: f.write(json.dumps(rec,separators=(',',':'))+'\n')
print(rec['_record_sha256'])
