#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from _v13_common import adapters
a=argparse.ArgumentParser();a.add_argument("--vault-root",required=True);x=a.parse_args();bad=[k for k,v in adapters(x.vault_root).items() if not v.get("confidence_caps")];print(json.dumps({"status":"PASS" if not bad else "FAIL","errors":bad},indent=2));sys.exit(bool(bad))
