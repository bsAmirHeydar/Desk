#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE));from runtime.health import integrated_health

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--data-root',required=True);a=ap.parse_args();o=integrated_health(a.data_root,BASE.parent);print(json.dumps(o,ensure_ascii=False,indent=2));return 0 if o['status']!='FAIL_CLOSED' else 1
if __name__=='__main__':raise SystemExit(main())
