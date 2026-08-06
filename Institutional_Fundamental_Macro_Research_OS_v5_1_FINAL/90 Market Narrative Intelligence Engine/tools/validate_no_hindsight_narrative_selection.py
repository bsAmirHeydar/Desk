#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, pathlib, sys
from _v12_common import load_json, no_hindsight_errors

def main():
    ap=argparse.ArgumentParser(description='Reject evidence after the analysis cutoff.')
    ap.add_argument('input')
    args=ap.parse_args()
    doc=load_json(args.input)
    errors=no_hindsight_errors(doc)
    out={{'status':'PASS' if not errors else 'FAIL','validator':'validate_no_hindsight_narrative_selection','errors':errors}}
    print(json.dumps(out,indent=2))
    return 0 if not errors else 1
if __name__=='__main__': raise SystemExit(main())
