from __future__ import annotations
import argparse,sys
from pathlib import Path
HERE=Path(__file__).resolve();NEXT=HERE.parents[2]
if str(NEXT) not in sys.path:sys.path.insert(0,str(NEXT))
from AD_V31_R04_INSTITUTIONAL_DATA_EDGE_OUTCOME_INFRASTRUCTURE.runtime.common import PHASE,save_json,iso
ap=argparse.ArgumentParser();ap.add_argument('--commit',required=True);a=ap.parse_args();save_json(PHASE/'artifacts/state/LOCAL_R04_BASELINE.json',{'baseline_commit':a.commit,'recorded_at':iso(),'local_only':True});print(a.commit)
