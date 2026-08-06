#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from _v13_common import registry
a=argparse.ArgumentParser();a.add_argument("--vault-root",required=True);x=a.parse_args();bad=[r["canonical_id"] for r in registry(x.vault_root) if not r["metadata_valid_from"]]
print(json.dumps({"status":"PASS" if not bad else "FAIL","errors":bad},indent=2));sys.exit(bool(bad))
