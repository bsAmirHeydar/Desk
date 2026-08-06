#!/usr/bin/env python3
"""Check V10.4 semantic entry points and V11 preservation markers."""
from __future__ import annotations
import argparse, pathlib
from _v11_common import *
REQUIRED_PATHS=[
"00 HOME.md","01 COVERAGE MATRIX.md",
"75 ChatGPT Institutional Market Analysis Prompts/00 ChatGPT Institutional Market Analysis Prompts MOC.md",
"81 Scientific QA and Certification Framework/00 Scientific QA and Certification Framework MOC.md",
"84 Canonical Retrieval Evidence and Version Control/00 Canonical Retrieval Evidence and Version Control MOC.md",
"87 Alpha Lab Asset-Specific Persian PDF Analysis Prompts/00 Alpha Lab Asset-Specific Persian PDF Analysis Prompts MOC.md",
"88 Hybrid Daily Session Event Fundamental State Engine/00 Hybrid Daily Session Event Fundamental State Engine MOC.md",
"88 Hybrid Daily Session Event Fundamental State Engine/14 Hybrid Fundamental State Schema.md",
"89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/00 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine MOC.md"]
MARKERS={
"88 Hybrid Daily Session Event Fundamental State Engine/14 Hybrid Fundamental State Schema.md":["direction","intensity","confidence","consumption","remaining_pressure"],
"89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/13 Remaining Fundamental Pressure Decomposition.md":["not","100","consumption"],
"89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/16 Fundamental Path Asymmetry and Edge Availability.md":["fundamental","execution"]
}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--vault-root",required=True); ap.add_argument("--output"); a=ap.parse_args()
    root=pathlib.Path(a.vault_root); errors=[]
    for rel in REQUIRED_PATHS:
        if not (root/rel).is_file(): errors.append(f"missing required path: {rel}")
    for rel,marks in MARKERS.items():
        p=root/rel
        if p.exists():
            t=p.read_text(encoding="utf-8",errors="replace").lower()
            for m in marks:
                if m.lower() not in t: errors.append(f"semantic marker {m!r} missing in {rel}")
    # The current schema explicitly enumerates 25 record types.
    schema=(root/"88 Hybrid Daily Session Event Fundamental State Engine/14 Hybrid Fundamental State Schema.md")
    if schema.exists():
        t=schema.read_text(encoding="utf-8",errors="replace")
        if not ("25" in t and "record" in t.lower()): errors.append("25 V10.4 record-type preservation not evidenced")
    return dump_report({"validator":"validate_v10_regression_preservation","status":"PASS" if not errors else "FAIL","errors":errors},a.output)
if __name__=="__main__": raise SystemExit(main())
