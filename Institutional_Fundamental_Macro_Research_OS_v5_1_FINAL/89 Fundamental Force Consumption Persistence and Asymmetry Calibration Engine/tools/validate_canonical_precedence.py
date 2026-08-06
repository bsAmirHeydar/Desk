#!/usr/bin/env python3
"""Validate the V11 canonical authority map contains mandatory concepts and paths."""
from __future__ import annotations
import argparse, pathlib, re
from _v11_common import *
MANDATORY=["force","consumption","remaining_pressure","persistence","reversal_risk","fundamental_asymmetry","confidence_caps","calibration"]
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--vault-root",required=True); ap.add_argument("--output"); a=ap.parse_args()
    p=pathlib.Path(a.vault_root)/"V11_CANONICAL_AUTHORITY_MAP.yaml"; errors=[]
    if not p.exists(): errors.append("authority map missing")
    else:
        t=p.read_text(encoding="utf-8")
        for x in MANDATORY:
            if re.search(rf"(?m)^\s*{re.escape(x)}\s*:",t) is None: errors.append(f"authority concept missing: {x}")
        for match in re.findall(r'primary:\s*"([^"]+)"',t):
            if not (pathlib.Path(a.vault_root)/match).exists(): errors.append(f"primary path missing: {match}")
    return dump_report({"validator":"validate_canonical_precedence","status":"PASS" if not errors else "FAIL","errors":errors},a.output)
if __name__=="__main__": raise SystemExit(main())
