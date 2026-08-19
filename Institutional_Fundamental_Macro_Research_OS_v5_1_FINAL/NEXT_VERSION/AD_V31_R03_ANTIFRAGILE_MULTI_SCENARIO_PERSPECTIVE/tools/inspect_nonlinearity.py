#!/usr/bin/env python3
from pathlib import Path
import sys,json
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P.parent));from AD_V31_R03_ANTIFRAGILE_MULTI_SCENARIO_PERSPECTIVE.runtime.common import load
x=load(P/'artifacts/latest/r03_perspective_state.json',{}) or {};print(json.dumps((x.get('nonlinearity') or {}),indent=2,ensure_ascii=False))
