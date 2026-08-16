#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE));from runtime.commissioning import run
p=argparse.ArgumentParser();p.add_argument('--repo-root',required=True);p.add_argument('--data-root',required=True);p.add_argument('--r4-profile',default='FULL');a=p.parse_args();o=run(a.repo_root,a.data_root,BASE,a.r4_profile);print(json.dumps(o,ensure_ascii=False,indent=2));raise SystemExit(0 if o.get('status')=='PASS' else 2)
