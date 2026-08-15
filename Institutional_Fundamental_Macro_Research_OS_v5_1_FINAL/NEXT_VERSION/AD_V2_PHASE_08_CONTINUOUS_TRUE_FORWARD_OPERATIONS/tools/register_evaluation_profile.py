#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT.parent))
from AD_V2_PHASE_08_CONTINUOUS_TRUE_FORWARD_OPERATIONS.runtime.profiles import register
p=argparse.ArgumentParser();p.add_argument('--data-root',required=True);p.add_argument('--profile',required=True);a=p.parse_args();r=register(a.data_root,json.loads(Path(a.profile).read_text(encoding='utf-8')));print(json.dumps(r,indent=2))
