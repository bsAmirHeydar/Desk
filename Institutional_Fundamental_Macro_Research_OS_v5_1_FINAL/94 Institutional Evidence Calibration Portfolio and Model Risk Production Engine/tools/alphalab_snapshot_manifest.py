#!/usr/bin/env python3
import argparse,hashlib,json,datetime
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('files',nargs='+'); p.add_argument('--output',required=True); a=p.parse_args()
out={'generated_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'snapshots':[]}
for x in a.files:
 f=Path(x); b=f.read_bytes(); out['snapshots'].append({'path':str(f),'sha256':hashlib.sha256(b).hexdigest(),'size_bytes':len(b)})
Path(a.output).write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(a.output)
