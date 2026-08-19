#!/usr/bin/env python3
from pathlib import Path
import sys,json,argparse
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P.parent))
from AD_V31_R03_ANTIFRAGILE_MULTI_SCENARIO_PERSPECTIVE.runtime.cohort_boundary import initialize
ap=argparse.ArgumentParser();ap.add_argument('--baseline-commit');a=ap.parse_args();print(json.dumps(initialize(a.baseline_commit),indent=2,ensure_ascii=False))
