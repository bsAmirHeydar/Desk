from __future__ import annotations
import argparse,sys,json
from pathlib import Path
HERE=Path(__file__).resolve();NEXT=HERE.parents[2]
if str(NEXT) not in sys.path:sys.path.insert(0,str(NEXT))
from AD_V31_R04_INSTITUTIONAL_DATA_EDGE_OUTCOME_INFRASTRUCTURE.runtime.cohort_boundary import initialize
ap=argparse.ArgumentParser();ap.add_argument('--baseline-commit');a=ap.parse_args();print(json.dumps(initialize(a.baseline_commit),indent=2))
