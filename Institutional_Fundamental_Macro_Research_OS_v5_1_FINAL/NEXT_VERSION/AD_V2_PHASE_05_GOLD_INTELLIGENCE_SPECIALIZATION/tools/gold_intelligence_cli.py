#!/usr/bin/env python3
from pathlib import Path
import argparse,json,importlib.util,sys
ROOT=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('g',ROOT/'runtime/gold_intelligence.py'); g=importlib.util.module_from_spec(s); s.loader.exec_module(g)
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('input'); ap.add_argument('--as-of',required=True); ap.add_argument('--horizon',required=True); a=ap.parse_args(); obs=json.loads(Path(a.input).read_text()); out=g.build_gold_intelligence(obs,as_of_utc=a.as_of,active_horizon=a.horizon); print(json.dumps(out,ensure_ascii=False,indent=2)); return 0 if out.get('status')=='PASS' else 2
if __name__=='__main__': raise SystemExit(main())
