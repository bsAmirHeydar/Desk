#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys,os
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE));from runtime.final_status import status
p=argparse.ArgumentParser();p.add_argument('--repo-root',required=True);p.add_argument('--data-root',required=True);a=p.parse_args();print(json.dumps(status(a.repo_root,a.data_root,BASE),ensure_ascii=False,indent=2))
