#!/usr/bin/env python3
import argparse,json
from _v12_common import load_json,daily_output_errors
ap=argparse.ArgumentParser(description='Validate V12 daily executive output completeness.')
ap.add_argument('input'); ap.add_argument('--require-all-markets',action='store_true')
a=ap.parse_args(); e=daily_output_errors(load_json(a.input),a.require_all_markets)
print(json.dumps({'status':'PASS' if not e else 'FAIL','errors':e},indent=2)); raise SystemExit(0 if not e else 1)
