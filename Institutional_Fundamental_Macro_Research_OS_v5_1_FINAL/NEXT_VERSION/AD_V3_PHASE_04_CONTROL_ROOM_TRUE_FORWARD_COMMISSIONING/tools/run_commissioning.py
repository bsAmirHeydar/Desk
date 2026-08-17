from __future__ import annotations
import argparse, json, pathlib, sys
HERE=pathlib.Path(__file__).resolve(); PH=HERE.parents[1]; REPO=PH.parents[2]; sys.path.insert(0,str(PH.parent))
from AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING.runtime.pipeline import run

def main():
    p=argparse.ArgumentParser(); p.add_argument('--repo',default=str(REPO)); p.add_argument('--horizon',default='SESSION_1_6H'); p.add_argument('--skip-p02',action='store_true'); p.add_argument('--semantic-bundle'); a=p.parse_args(); print(json.dumps(run(a.repo,a.horizon,a.skip_p02,a.semantic_bundle),indent=2,ensure_ascii=False)); return 0
if __name__=='__main__': raise SystemExit(main())
