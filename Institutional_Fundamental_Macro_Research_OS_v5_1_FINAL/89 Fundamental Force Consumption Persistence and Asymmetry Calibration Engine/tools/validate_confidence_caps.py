#!/usr/bin/env python3
"""Enforce declared confidence caps and public-data flow ceilings."""
from __future__ import annotations
import argparse
from _v11_common import *
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("record"); ap.add_argument("--output"); a=ap.parse_args()
    s=state(load_json(a.record)); errors=[]
    caps=s.get("provenance",{}).get("confidence_caps",[])
    for c in caps:
        target=get_path(s,c.get("field",""))
        if isinstance(target,dict): actual=target.get("confidence")
        else: actual=target
        if isinstance(actual,(int,float)) and actual>c.get("cap",100):
            errors.append(f"{c['field']} confidence {actual} exceeds cap {c['cap']}")
    unavailable={x.get("input") for x in s.get("provenance",{}).get("unavailable_inputs",[])}
    flow=s.get("consumption_v2",{}).get("mechanical_flow_exhaustion",{})
    if "proprietary_flow_data" in unavailable and isinstance(flow,dict) and (flow.get("confidence") or 0)>65:
        errors.append("mechanical flow exhaustion confidence exceeds 65 without proprietary flow data")
    return dump_report({"validator":"validate_confidence_caps","status":"PASS" if not errors else "FAIL","errors":errors},a.output)
if __name__=="__main__": raise SystemExit(main())
