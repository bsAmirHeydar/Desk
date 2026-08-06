#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,pathlib,sys
a=argparse.ArgumentParser();a.add_argument("--vault-root",required=True);x=a.parse_args();r=pathlib.Path(x.vault_root);req=["89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/00 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine MOC.md","89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/v11_fundamental_state.schema.json","90 Market Narrative Intelligence Engine/00 Market Narrative Intelligence Engine MOC.md","90 Market Narrative Intelligence Engine/v12_market_intelligence_state.schema.json","90 Market Narrative Intelligence Engine/41 Alpha Lab V12 Daily Fundamental and Narrative Analysis Prompt.md"];bad=[z for z in req if not (r/z).is_file()];txt=" ".join((r/z).read_text(encoding="utf-8",errors="replace") for z in req if (r/z).is_file());
for z in ["remaining pressure","narrative validity","narrative dominance","point-in-time"]:
 if z not in txt.lower():bad.append(z)
print(json.dumps({"status":"PASS" if not bad else "FAIL","errors":bad},indent=2));sys.exit(bool(bad))
