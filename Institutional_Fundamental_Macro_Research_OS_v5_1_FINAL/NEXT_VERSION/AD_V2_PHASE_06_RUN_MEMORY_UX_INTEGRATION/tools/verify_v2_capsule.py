#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys
BASE=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(BASE.parent))
from AD_V2_PHASE_06_RUN_MEMORY_UX_INTEGRATION.runtime.v2_memory import verify

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--path',required=True); a=ap.parse_args(); o=verify(a.path); print(json.dumps(o,indent=2)); return 0 if o.get('status')=='PASS' else 2
if __name__=='__main__': raise SystemExit(main())
