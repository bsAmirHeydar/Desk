#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys
PH=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(PH))
from runtime.operations import status
ap=argparse.ArgumentParser();ap.add_argument('--data-root',required=True);a=ap.parse_args();print(json.dumps(status(a.data_root),ensure_ascii=False,indent=2))
