#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from _v13_common import registry
a=argparse.ArgumentParser();a.add_argument("--vault-root",required=True);x=a.parse_args();r=[z for z in registry(x.vault_root) if z["asset_family"]=="COMMODITY"];bad=[z["canonical_id"] for z in r if not z["implementation_type"] or not z["venue_or_provider"] or not z["benchmark"]]
print(json.dumps({"status":"PASS" if len(r)>=35 and not bad else "FAIL","count":len(r),"errors":bad},indent=2));sys.exit(0 if len(r)>=35 and not bad else 1)
