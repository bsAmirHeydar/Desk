from __future__ import annotations
import argparse,json,pathlib,sys
HERE=pathlib.Path(__file__).resolve(); PH=HERE.parents[1]; sys.path.insert(0,str(PH.parent))
from AD_V3_PHASE_07_LIVE_INTRADAY_GOLD_DATA_KERNEL.runtime.acquisition_planner import build_plan

def main():
 p=argparse.ArgumentParser(); p.add_argument('--horizon',default='SESSION_1_6H'); p.add_argument('--mode',default='NORMAL',choices=['NORMAL','FULL_REFRESH','CACHE_ONLY']); p.add_argument('--as-of'); p.add_argument('--json',action='store_true'); a=p.parse_args()
 r=build_plan(a.horizon,a.mode,a.as_of)
 if a.json: print(json.dumps(r,indent=2,ensure_ascii=False))
 else:
  print(f"P07 PLAN {r['plan_id']} | {r['horizon']} | {r['mode']}")
  print(json.dumps(r['counts'],indent=2,ensure_ascii=False))
  for x in r['sources']: print(f"{x['action']:<18} {x['source_id']:<36} {x['cadence']:<18} {x['reason']}")
 return 0
if __name__=='__main__': raise SystemExit(main())
