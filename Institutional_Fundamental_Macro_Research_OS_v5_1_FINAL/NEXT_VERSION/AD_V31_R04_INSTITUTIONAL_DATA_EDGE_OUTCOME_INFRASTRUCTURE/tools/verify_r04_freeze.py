from __future__ import annotations
import json,sys
from pathlib import Path
HERE=Path(__file__).resolve();NEXT=HERE.parents[2]
if str(NEXT) not in sys.path:sys.path.insert(0,str(NEXT))
from AD_V31_R04_INSTITUTIONAL_DATA_EDGE_OUTCOME_INFRASTRUCTURE.runtime.data_freeze import verify_manifest
x=verify_manifest();print(json.dumps(x,indent=2));raise SystemExit(0 if x['status']=='PASS' else 1)
