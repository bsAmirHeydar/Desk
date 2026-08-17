#!/usr/bin/env python3
import argparse,json,pathlib,sys
P=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(P.parent))
from AD_V3_PHASE_12_FINAL_CERTIFICATION_PRODUCTION_FREEZE.runtime.promotion import perform_promotion
ap=argparse.ArgumentParser();ap.add_argument('--approve',action='store_true');a=ap.parse_args()
try:r=perform_promotion(a.approve);print(json.dumps(r,ensure_ascii=False,indent=2));raise SystemExit(0)
except Exception as e:print(json.dumps({'status':'DENIED','error':str(e),'promotion_performed':False},ensure_ascii=False,indent=2));raise SystemExit(2)
