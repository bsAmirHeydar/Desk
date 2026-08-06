#!/usr/bin/env python3
"""Validate the mandatory V11 state structure and core enums."""
from __future__ import annotations
import argparse, pathlib
from _v11_common import *

def validate(doc):
    errors=[]
    try: s=state(doc)
    except Exception as e: return [str(e)]
    required=["record_id","asset","cutoff_utc","methodology","force","consumption_v2","remaining_pressure_v2","persistence_v2","asymmetry_v2","horizon_states","provenance","validation"]
    for k in required:
        if k not in s: errors.append(f"missing: {k}")
    if s.get("asset") not in {"NASDAQ_100","SP500","GOLD","EURUSD"}: errors.append("invalid asset")
    m=s.get("methodology",{})
    if m.get("vault_release")!="11.0.0" or m.get("state_schema_version")!="11.0.0": errors.append("release/schema must equal 11.0.0")
    if m.get("scoring_mode") not in {"ANALYTICAL_ORDINAL_MODE","EMPIRICALLY_CALIBRATED_MODE","HYBRID_PROVENANCE_MODE"}: errors.append("invalid scoring_mode")
    hs=s.get("horizon_states",[])
    if not hs: errors.append("at least one horizon state required")
    for i,h in enumerate(hs):
        if h.get("horizon") not in HORIZONS: errors.append(f"horizon_states[{i}] invalid horizon")
        for k in ["direction","confidence","consumption_state","persistence_class","reversal_risk","path_asymmetry_class","edge_availability","next_update_trigger"]:
            if k not in h: errors.append(f"horizon_states[{i}] missing {k}")
    prov=s.get("provenance",{})
    for k in ["field_level_ledger","unavailable_inputs","confidence_caps"]:
        if k not in prov: errors.append(f"provenance missing {k}")
    for i,x in enumerate(prov.get("field_level_ledger",[])):
        if x.get("provenance") not in PROVENANCE: errors.append(f"field provenance[{i}] invalid")
    return errors

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("record"); ap.add_argument("--output"); a=ap.parse_args()
    errors=validate(load_json(a.record))
    return dump_report({"validator":"validate_v11_state_schema","status":"PASS" if not errors else "FAIL","record":str(a.record),"errors":errors},a.output)
if __name__=="__main__": raise SystemExit(main())
