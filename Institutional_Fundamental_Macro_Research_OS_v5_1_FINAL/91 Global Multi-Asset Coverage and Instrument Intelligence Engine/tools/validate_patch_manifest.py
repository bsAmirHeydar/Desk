#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,pathlib,hashlib,sys
def sh(p):return hashlib.sha256(p.read_bytes()).hexdigest()
a=argparse.ArgumentParser();a.add_argument("--patch-root",required=True);x=a.parse_args();pr=pathlib.Path(x.patch_root);m=json.loads((pr/"PATCH_MANIFEST.json").read_text());bad=[];seen=set()
for z in m.get("files_added",[])+m.get("files_modified",[]):
 rel=z["path"];p=pr/"payload"/rel
 if rel in seen:bad.append("duplicate "+rel)
 seen.add(rel)
 if "__pycache__" in rel or rel.endswith(".pyc"):bad.append("cache "+rel)
 if not p.is_file():bad.append("missing "+rel)
 elif sh(p)!=z["sha256_after"]:bad.append("hash "+rel)
print(json.dumps({"status":"PASS" if not bad else "FAIL","checked":len(seen),"errors":bad},indent=2));sys.exit(bool(bad))
