#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from _v13_common import registry
a=argparse.ArgumentParser();a.add_argument("--vault-root",required=True);x=a.parse_args();rows=registry(x.vault_root);ids=set();bad=[]
for r in rows:
 if r["canonical_id"] in ids:bad.append("duplicate "+r["canonical_id"])
 ids.add(r["canonical_id"])
 if not r["adapter_id"] or not r["metadata_valid_from"]:bad.append("incomplete "+r["canonical_id"])
print(json.dumps({"status":"PASS" if not bad and len(rows)>=150 else "FAIL","count":len(rows),"errors":bad},indent=2));sys.exit(0 if not bad and len(rows)>=150 else 1)
