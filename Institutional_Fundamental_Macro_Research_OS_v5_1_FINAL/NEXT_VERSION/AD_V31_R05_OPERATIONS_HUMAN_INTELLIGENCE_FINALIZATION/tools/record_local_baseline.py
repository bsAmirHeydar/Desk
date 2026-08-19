#!/usr/bin/env python3
import argparse,json,pathlib,datetime
P=pathlib.Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser();ap.add_argument('--commit',required=True);a=ap.parse_args();out=P/'artifacts/state/LOCAL_R05_BASELINE.json';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps({'baseline_commit':a.commit,'recorded_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00','Z'),'cohort_reset':False},indent=2)+'\n',encoding='utf-8');print(out)
