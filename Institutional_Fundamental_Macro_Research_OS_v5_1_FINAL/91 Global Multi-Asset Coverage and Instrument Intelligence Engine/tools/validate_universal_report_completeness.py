#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,pathlib,sys
a=argparse.ArgumentParser();a.add_argument("--vault-root",required=True);x=a.parse_args();m=pathlib.Path(x.vault_root)/"91 Global Multi-Asset Coverage and Instrument Intelligence Engine";req=["63 Universal Full Analysis Production Prompt.md","65 FX Launcher.md","66 Commodity Launcher.md","67 Global Index Launcher.md","68 Custom Watchlist Launcher.md","69 Cross-Sectional Ranking Launcher.md","70 Relative-Value Pair Trade Research Launcher.md"];bad=[z for z in req if not (m/z).is_file()];t=(m/req[0]).read_text(encoding="utf-8")
for z in ["Phase A","Phase B","Phase C","Phase D","Phase E","Phase F","Instrument-resolution and coverage ledger","Machine-readable V13 state"]:
 if z not in t:bad.append(z)
print(json.dumps({"status":"PASS" if not bad else "FAIL","errors":bad},indent=2));sys.exit(bool(bad))
