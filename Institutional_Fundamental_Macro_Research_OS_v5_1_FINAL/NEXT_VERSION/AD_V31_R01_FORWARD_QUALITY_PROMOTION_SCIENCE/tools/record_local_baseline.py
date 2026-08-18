#!/usr/bin/env python3
import argparse,json,pathlib
P=pathlib.Path(__file__).resolve().parents[1];ap=argparse.ArgumentParser();ap.add_argument('--commit',required=True);a=ap.parse_args();o={'record_type':'AD_V31_R01_LOCAL_BASELINE_RECEIPT','baseline_commit':a.commit};d=P/'artifacts/state';d.mkdir(parents=True,exist_ok=True);(d/'local_baseline_receipt.json').write_text(json.dumps(o,indent=2)+'\n');print(json.dumps(o,indent=2))
