#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, pathlib, sys
from _v12_common import load_json, independence_errors

def main():
    ap=argparse.ArgumentParser(description='Validate typed cross-asset edges and independence.')
    ap.add_argument('input')
    args=ap.parse_args()
    doc=load_json(args.input)
    errors=independence_errors(doc)
    out={{'status':'PASS' if not errors else 'FAIL','validator':'validate_cross_asset_independence','errors':errors}}
    print(json.dumps(out,indent=2))
    return 0 if not errors else 1
if __name__=='__main__': raise SystemExit(main())
