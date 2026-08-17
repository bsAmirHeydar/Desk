#!/usr/bin/env python3
import argparse,json,pathlib,sys
P=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(P.parent))
from AD_V3_PHASE_12_FINAL_CERTIFICATION_PRODUCTION_FREEZE.runtime.promotion import perform_rollback
ap=argparse.ArgumentParser();ap.add_argument('--reason',default='OPERATOR_ROLLBACK_TO_V2');a=ap.parse_args()
try:r=perform_rollback(a.reason);print(json.dumps(r,ensure_ascii=False,indent=2));raise SystemExit(0)
except Exception as e:print(json.dumps({'status':'DENIED','error':str(e)},ensure_ascii=False,indent=2));raise SystemExit(2)
