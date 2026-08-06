#!/usr/bin/env python3
"""Prevent ordinal scores from being represented as calibrated probabilities."""
from __future__ import annotations
import argparse, json, re
from _v11_common import *
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("record"); ap.add_argument("--output"); a=ap.parse_args()
    doc=load_json(a.record); s=state(doc); errors=[]
    m=s.get("methodology",{}); mode=m.get("scoring_mode")
    if mode=="EMPIRICALLY_CALIBRATED_MODE":
        if not m.get("estimand"): errors.append("calibrated mode requires estimand")
        if not m.get("calibration_evidence_locator"): errors.append("calibrated mode requires calibration_evidence_locator")
        if s.get("validation",{}).get("calibration_status") not in {"OUT_OF_SAMPLE_PARTIAL","OUT_OF_SAMPLE_VALIDATED"}:
            errors.append("calibrated mode requires out-of-sample calibration status")
    else:
        raw=json.dumps(doc,ensure_ascii=False).lower()
        for phrase in ["probability of profit","percent probability","win probability"]:
            if phrase in raw: errors.append(f"ordinal/hybrid record contains false probability phrase: {phrase}")
    return dump_report({"validator":"validate_no_false_probability","status":"PASS" if not errors else "FAIL","errors":errors},a.output)
if __name__=="__main__": raise SystemExit(main())
