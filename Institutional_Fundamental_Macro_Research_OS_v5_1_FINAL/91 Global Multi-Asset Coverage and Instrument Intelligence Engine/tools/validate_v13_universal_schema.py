#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from _v13_common import ex,load,errors
a=argparse.ArgumentParser();a.add_argument("--vault-root",required=True);x=a.parse_args();bad=[]
for p in ex(x.vault_root):
 d=load(p)
 if "states" in d or "report_mode" in d:continue
 z=errors(d)
 if z:bad.append({"file":p.name,"errors":z})
print(json.dumps({"status":"PASS" if not bad else "FAIL","errors":bad},indent=2));sys.exit(bool(bad))
