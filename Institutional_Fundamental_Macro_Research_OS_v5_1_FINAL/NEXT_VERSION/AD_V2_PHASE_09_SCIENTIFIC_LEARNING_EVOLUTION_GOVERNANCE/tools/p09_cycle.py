#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys
HERE=Path(__file__).resolve().parent;PH=HERE.parent;PP=PH.parent
for p in (str(PH),str(PP)):
 if p not in sys.path:sys.path.insert(0,p)
from runtime.operations import run_cycle
ap=argparse.ArgumentParser();ap.add_argument('--data-root',required=True);ap.add_argument('--now-utc');a=ap.parse_args();print(json.dumps(run_cycle(a.data_root,PH,a.now_utc),ensure_ascii=False,indent=2))
