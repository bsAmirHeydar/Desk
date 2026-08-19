#!/usr/bin/env python3
from pathlib import Path
import argparse,json,datetime
P=Path(__file__).resolve().parents[1];ap=argparse.ArgumentParser();ap.add_argument('--commit',required=True);a=ap.parse_args();p=P/'artifacts/state/LOCAL_R03_BASELINE.json';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps({'baseline_commit':a.commit,'recorded_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00','Z'),'local_deployment_artifact':True},indent=2)+'\n');print(p)
