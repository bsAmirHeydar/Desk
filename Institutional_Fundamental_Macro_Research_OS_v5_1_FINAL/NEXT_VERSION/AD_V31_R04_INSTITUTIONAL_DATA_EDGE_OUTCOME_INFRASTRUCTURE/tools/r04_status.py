from __future__ import annotations
import json,sys
from pathlib import Path
HERE=Path(__file__).resolve();NEXT=HERE.parents[2]
if str(NEXT) not in sys.path:sys.path.insert(0,str(NEXT))
from AD_V31_R04_INSTITUTIONAL_DATA_EDGE_OUTCOME_INFRASTRUCTURE.runtime.data_edge_runtime import status
from AD_V31_R04_INSTITUTIONAL_DATA_EDGE_OUTCOME_INFRASTRUCTURE.runtime.cohort_boundary import load_boundary
from AD_V31_R04_INSTITUTIONAL_DATA_EDGE_OUTCOME_INFRASTRUCTURE.runtime.data_freeze import verify_manifest
x=status();x['qualification_boundary']=load_boundary();x['freeze']=verify_manifest();print(json.dumps(x,indent=2,ensure_ascii=False));raise SystemExit(0 if x['freeze'].get('status')=='PASS' else 1)
