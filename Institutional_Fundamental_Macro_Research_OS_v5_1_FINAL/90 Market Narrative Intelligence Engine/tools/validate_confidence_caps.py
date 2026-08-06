#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, pathlib, sys
from _v12_common import load_json, confidence_cap_errors

def main():
    ap=argparse.ArgumentParser(description='Validate public/proxy data confidence caps.')
    ap.add_argument('input')
    args=ap.parse_args()
    doc=load_json(args.input)
    errors=confidence_cap_errors(doc)
    out={{'status':'PASS' if not errors else 'FAIL','validator':'validate_confidence_caps','errors':errors}}
    print(json.dumps(out,indent=2))
    return 0 if not errors else 1
if __name__=='__main__': raise SystemExit(main())
