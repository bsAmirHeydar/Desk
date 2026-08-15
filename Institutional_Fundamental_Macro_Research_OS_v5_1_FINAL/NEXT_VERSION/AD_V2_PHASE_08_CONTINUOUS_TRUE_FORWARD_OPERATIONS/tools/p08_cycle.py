#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT.parent))
from AD_V2_PHASE_08_CONTINUOUS_TRUE_FORWARD_OPERATIONS.runtime.operations import run_cycle
p=argparse.ArgumentParser();p.add_argument('--data-root',required=True);p.add_argument('--now-utc');a=p.parse_args();r=run_cycle(a.data_root,ROOT,now_utc=a.now_utc);print(json.dumps(r,ensure_ascii=False,indent=2));raise SystemExit(0 if r.get('status') in {'PASS','PASS_WITH_WARNINGS','BUSY'} else 2)
