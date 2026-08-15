#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT.parent));from AD_V2_PHASE_07_D4_TRUE_FORWARD_PROMOTION.runtime.true_forward import status
p=argparse.ArgumentParser();p.add_argument('--data-root',required=True);a=p.parse_args();print(json.dumps(status(a.data_root),indent=2))
