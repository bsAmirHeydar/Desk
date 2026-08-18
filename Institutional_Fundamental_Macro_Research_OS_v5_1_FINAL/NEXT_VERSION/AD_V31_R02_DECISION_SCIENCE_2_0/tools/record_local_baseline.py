#!/usr/bin/env python3
from pathlib import Path
import argparse,json
P=Path(__file__).resolve().parents[1];ap=argparse.ArgumentParser();ap.add_argument('--commit',required=True);a=ap.parse_args();p=P/'baseline/LOCAL_R02_BASELINE.json';p.write_text(json.dumps({'baseline_commit':a.commit,'provenance':'operator local git','phase':'AD-V3.1-R02'},indent=2)+'\n');print(json.dumps({'status':'PASS','baseline_commit':a.commit}))
