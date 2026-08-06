#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, pathlib, sys
from _v12_common import load_json, structural_errors

def main():
    ap=argparse.ArgumentParser(description='Validate the V12 structural state contract.')
    ap.add_argument('input')
    args=ap.parse_args()
    doc=load_json(args.input)
    errors=structural_errors(doc)
    out={{'status':'PASS' if not errors else 'FAIL','validator':'validate_v12_narrative_state_schema','errors':errors}}
    print(json.dumps(out,indent=2))
    return 0 if not errors else 1
if __name__=='__main__': raise SystemExit(main())
