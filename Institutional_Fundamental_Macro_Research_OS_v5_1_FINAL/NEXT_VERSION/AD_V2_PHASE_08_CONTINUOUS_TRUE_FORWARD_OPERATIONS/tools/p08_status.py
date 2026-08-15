#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT.parent))
from AD_V2_PHASE_08_CONTINUOUS_TRUE_FORWARD_OPERATIONS.runtime.operations import status
p=argparse.ArgumentParser();p.add_argument('--data-root',required=True);a=p.parse_args();r=status(a.data_root);print(json.dumps(r,ensure_ascii=False,indent=2));raise SystemExit(0 if r.get('status')=='PASS' else 2)
