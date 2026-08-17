from __future__ import annotations
import argparse,json,pathlib
PH=pathlib.Path(__file__).resolve().parents[1];p=argparse.ArgumentParser();p.add_argument('--run-id',required=True);a=p.parse_args();rd=PH/'artifacts/runs'/a.run_id
if not rd.exists():raise SystemExit('RUN_NOT_FOUND')
print((rd/'run_result.json').read_text(encoding='utf-8') if (rd/'run_result.json').exists() else json.dumps({'files':[x.name for x in rd.iterdir()]},indent=2))
