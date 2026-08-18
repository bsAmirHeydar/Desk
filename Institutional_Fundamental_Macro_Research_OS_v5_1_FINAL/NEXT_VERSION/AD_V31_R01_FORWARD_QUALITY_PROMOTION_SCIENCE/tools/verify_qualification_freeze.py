#!/usr/bin/env python3
import json,pathlib,sys
P=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(P.parent))
from AD_V31_R01_FORWARD_QUALITY_PROMOTION_SCIENCE.runtime.qualification_freeze import verify_manifest
r=verify_manifest();print(json.dumps(r,indent=2));raise SystemExit(0 if r['status']=='PASS' else 2)
