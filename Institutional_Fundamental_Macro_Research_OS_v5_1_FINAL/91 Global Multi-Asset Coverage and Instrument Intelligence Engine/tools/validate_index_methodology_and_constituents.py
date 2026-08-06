#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from _v13_common import ex,load
a=argparse.ArgumentParser();a.add_argument("--vault-root",required=True);x=a.parse_args();bad=[];n=0
for p in ex(x.vault_root,"example_index_"):
 n+=1;s=load(p).get("index_state",{})
 if "methodology" not in s or "constituents" not in s:bad.append(p.name)
print(json.dumps({"status":"PASS" if n>=3 and not bad else "FAIL","count":n,"errors":bad},indent=2));sys.exit(0 if n>=3 and not bad else 1)
