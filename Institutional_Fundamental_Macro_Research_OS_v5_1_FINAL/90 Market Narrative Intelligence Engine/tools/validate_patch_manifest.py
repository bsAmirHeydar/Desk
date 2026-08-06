#!/usr/bin/env python3
import argparse,hashlib,json,pathlib

def h(p):
 x=hashlib.sha256();
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''): x.update(b)
 return x.hexdigest()
ap=argparse.ArgumentParser(description='Validate V12 patch manifest and payload hashes.')
ap.add_argument('--patch-root',required=True); a=ap.parse_args(); r=pathlib.Path(a.patch_root); e=[]
m=json.loads((r/'PATCH_MANIFEST.json').read_text()); seen=set()
for item in m.get('files_added',[])+m.get('files_modified',[]):
 rel=item['path']
 if rel in seen: e.append(f'duplicate path {rel}')
 seen.add(rel)
 pp=pathlib.PurePosixPath(rel)
 if pp.is_absolute() or '..' in pp.parts: e.append(f'unsafe path {rel}')
 p=r/'payload'/rel
 if not p.is_file(): e.append(f'missing payload {rel}')
 elif h(p)!=item['sha256_after']: e.append(f'hash mismatch {rel}')
print(json.dumps({'status':'PASS' if not e else 'FAIL','errors':e,'checked':len(seen)},indent=2)); raise SystemExit(0 if not e else 1)
