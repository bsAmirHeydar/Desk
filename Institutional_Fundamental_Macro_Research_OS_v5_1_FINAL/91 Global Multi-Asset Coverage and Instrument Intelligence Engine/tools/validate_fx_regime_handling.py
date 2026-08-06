#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from _v13_common import ex,load
a=argparse.ArgumentParser();a.add_argument("--vault-root",required=True);x=a.parse_args();ok=False
for p in ex(x.vault_root,"example_fx_"):
 s=load(p).get("fx_state",{})
 if s.get("regime")=="PEG" and s.get("intervention")=="REQUIRED_COMPONENT":ok=True
print(json.dumps({"status":"PASS" if ok else "FAIL"},indent=2));sys.exit(0 if ok else 1)
