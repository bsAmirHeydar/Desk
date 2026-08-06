#!/usr/bin/env python3
"""Require unique, explicit horizon states and protect against accidental copying."""
from __future__ import annotations
import argparse, json
from _v11_common import *
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("record"); ap.add_argument("--output"); a=ap.parse_args()
    s=state(load_json(a.record)); errors=[]; hs=s.get("horizon_states",[])
    names=[h.get("horizon") for h in hs]
    if len(names)!=len(set(names)): errors.append("duplicate horizons")
    if len(hs)>1:
        sigs=[]
        for h in hs:
            x={k:v for k,v in h.items() if k not in {"horizon","next_update_trigger"}}
            sigs.append(json.dumps(x,sort_keys=True))
        if len(set(sigs))==1: errors.append("all horizon states are identical; explicit horizon justification required")
    return dump_report({"validator":"validate_horizon_separation","status":"PASS" if not errors else "FAIL","errors":errors},a.output)
if __name__=="__main__": raise SystemExit(main())
