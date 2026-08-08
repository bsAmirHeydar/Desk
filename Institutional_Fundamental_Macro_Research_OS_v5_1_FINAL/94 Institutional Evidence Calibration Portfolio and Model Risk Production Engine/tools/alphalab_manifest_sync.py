#!/usr/bin/env python3
import argparse,json,hashlib,sys
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('--vault-root',required=True); p.add_argument('--write',action='store_true'); p.add_argument('--check',action='store_true'); a=p.parse_args(); r=Path(a.vault_root)
j=r/'CURRENT_PRODUCTION_MANIFEST.json'; y=r/'CURRENT_PRODUCTION_MANIFEST.yaml'; meta=r/'MANIFEST_MIRROR_HASHES.json'
obj=json.loads(j.read_text(encoding='utf-8')); expected='# GENERATED MIRROR — machine authority is CURRENT_PRODUCTION_MANIFEST.json\n'+json.dumps(obj,indent=2,ensure_ascii=False)+'\n'
def h(b): return hashlib.sha256(b).hexdigest()
if a.write:
    y.write_text(expected,encoding='utf-8',newline='\n'); m={'version':obj['version'],'json_sha256':h(j.read_bytes()),'yaml_sha256':h(y.read_bytes())}; meta.write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8'); print(json.dumps(m)); sys.exit(0)
errors=[]
if not y.exists() or y.read_text(encoding='utf-8')!=expected: errors.append('manifest YAML mirror drift')
if not meta.exists(): errors.append('manifest mirror hash metadata missing')
else:
    m=json.loads(meta.read_text(encoding='utf-8'))
    if m.get('json_sha256')!=h(j.read_bytes()): errors.append('manifest JSON hash drift')
    if y.exists() and m.get('yaml_sha256')!=h(y.read_bytes()): errors.append('manifest YAML hash drift')
print(json.dumps({'status':'PASS' if not errors else 'FAIL','errors':errors},indent=2)); sys.exit(0 if not errors else 2)
