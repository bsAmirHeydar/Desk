#!/usr/bin/env python3
from pathlib import Path
import sys,json
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P.parent));from AD_V31_R03_ANTIFRAGILE_MULTI_SCENARIO_PERSPECTIVE.runtime.perspective_freeze import verify_manifest
r=verify_manifest();print(json.dumps(r,indent=2,ensure_ascii=False));raise SystemExit(0 if r['status']=='PASS' else 2)
