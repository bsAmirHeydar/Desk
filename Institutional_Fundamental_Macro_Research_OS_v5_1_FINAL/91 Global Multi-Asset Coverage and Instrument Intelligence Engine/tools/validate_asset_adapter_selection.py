#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from _v13_common import registry,adapters
a=argparse.ArgumentParser();a.add_argument("--vault-root",required=True);x=a.parse_args();ad=adapters(x.vault_root);bad=[]
for r in registry(x.vault_root):
 if r["adapter_id"] not in ad:bad.append("unknown "+r["canonical_id"])
 elif ad[r["adapter_id"]]["family"]!=r["asset_family"]:bad.append("family "+r["canonical_id"])
print(json.dumps({"status":"PASS" if not bad else "FAIL","adapters":len(ad),"errors":bad},indent=2));sys.exit(bool(bad))
