#!/usr/bin/env python3
from pathlib import Path
import argparse, json, sys, importlib.util
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('kc',ROOT/'runtime/knowledge_compiler.py'); kc=importlib.util.module_from_spec(spec); spec.loader.exec_module(kc)
ap=argparse.ArgumentParser(); ap.add_argument('--out'); ap.add_argument('--json',action='store_true'); a=ap.parse_args()
r,p=kc.write_receipt(a.out)
if a.json: print(json.dumps(r,ensure_ascii=False,indent=2))
else:
 print('AD-V3-P01 GOLD KNOWLEDGE COMPILER:',r['status']); print('facts:',r['registry']['fact_count']); print('surfaces:',r['surface_coverage']['discovered_surface_count']); print('receipt:',p)
sys.exit(0 if r['status']=='PASS' else 2)
