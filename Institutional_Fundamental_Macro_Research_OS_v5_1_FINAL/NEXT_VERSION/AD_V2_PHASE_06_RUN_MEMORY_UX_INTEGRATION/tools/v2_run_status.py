#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys
BASE=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(BASE.parent))
from AD_V2_PHASE_06_RUN_MEMORY_UX_INTEGRATION.runtime.v2_memory import status

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--data-root',required=True); a=ap.parse_args(); o=status(a.data_root); print(json.dumps(o,ensure_ascii=False,indent=2)); return 0 if o.get('status')=='PASS' else 2
if __name__=='__main__': raise SystemExit(main())
