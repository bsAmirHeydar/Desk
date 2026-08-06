#!/usr/bin/env python3
"""Require field-level provenance for load-bearing summary fields."""
from __future__ import annotations
import argparse
from _v11_common import *
REQUIRED={"force.aggregate_value","consumption_v2.summary_state","remaining_pressure_v2.aggregate_class","asymmetry_v2.path_asymmetry_class"}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("record"); ap.add_argument("--output"); a=ap.parse_args()
    s=state(load_json(a.record)); rows=s.get("provenance",{}).get("field_level_ledger",[])
    present={r.get("field") for r in rows}
    errors=[f"missing field-level provenance: {x}" for x in sorted(REQUIRED-present)]
    for i,r in enumerate(rows):
        for k in ["field","provenance","methodology_version","confidence","rationale","next_update_condition"]:
            if k not in r: errors.append(f"ledger[{i}] missing {k}")
        if r.get("provenance") not in PROVENANCE: errors.append(f"ledger[{i}] invalid provenance")
    return dump_report({"validator":"validate_score_provenance","status":"PASS" if not errors else "FAIL","errors":errors},a.output)
if __name__=="__main__": raise SystemExit(main())
