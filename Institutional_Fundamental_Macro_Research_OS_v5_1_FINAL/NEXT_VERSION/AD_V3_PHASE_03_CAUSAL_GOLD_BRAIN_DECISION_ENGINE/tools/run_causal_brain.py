from __future__ import annotations
import argparse, json, pathlib, sys
HERE=pathlib.Path(__file__).resolve(); PHASE=HERE.parents[1]; sys.path.insert(0,str(PHASE.parent))
from AD_V3_PHASE_03_CAUSAL_GOLD_BRAIN_DECISION_ENGINE.runtime.engine import execute

def main():
    p=argparse.ArgumentParser(); p.add_argument('--p02-data-root',default=str(PHASE.parent/'AD_V3_PHASE_02_TOTAL_LIVE_DATA_OBSERVABILITY_FABRIC'/'artifacts'/'live_store')); p.add_argument('--coverage'); p.add_argument('--adjudication'); p.add_argument('--horizon',default='SESSION_1_6H'); p.add_argument('--json',action='store_true'); a=p.parse_args()
    r=execute(PHASE,a.p02_data_root,a.coverage,a.adjudication,a.horizon)
    print(json.dumps(r,indent=2,ensure_ascii=False)); return 3 if r.get('analysis_admission')=='BLOCKED' else 0
if __name__=='__main__': raise SystemExit(main())
