from __future__ import annotations
import json,sys
from pathlib import Path
HERE=Path(__file__).resolve(); PH=HERE.parents[1]; NEXT=PH.parent
if str(NEXT) not in sys.path: sys.path.insert(0,str(NEXT))
from AD_V31_R05_OPERATIONS_HUMAN_INTELLIGENCE_FINALIZATION.runtime.r05_freeze import verify,verify_science
r=verify(); s=verify_science(); out={'record_type':'AD_V31_R05_FREEZE_VERIFICATION','status':'PASS' if r['status']=='PASS' and s['status']=='PASS' else 'FAIL','implementation':r,'science':s,'r04_cohort_reset':False}; print(json.dumps(out,ensure_ascii=False,indent=2)); raise SystemExit(0 if out['status']=='PASS' else 2)
