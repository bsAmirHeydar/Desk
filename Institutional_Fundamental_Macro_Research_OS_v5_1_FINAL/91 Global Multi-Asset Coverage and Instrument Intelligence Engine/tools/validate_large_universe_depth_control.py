#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,pathlib,sys
a=argparse.ArgumentParser();a.add_argument("--vault-root",required=True);x=a.parse_args();t=(pathlib.Path(x.vault_root)/"91 Global Multi-Asset Coverage and Instrument Intelligence Engine/11 Universal Daily Reporting Workflow.md").read_text(encoding="utf-8").lower();bad=[z for z in ["tier 1","tier 2","tier 3","selection"] if z not in t];print(json.dumps({"status":"PASS" if not bad else "FAIL","errors":bad},indent=2));sys.exit(bool(bad))
