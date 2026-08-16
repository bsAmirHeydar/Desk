from __future__ import annotations
import argparse, json, pathlib, sys
HERE=pathlib.Path(__file__).resolve(); PHASE=HERE.parents[1]; sys.path.insert(0,str(PHASE))
from runtime.executor import execute

def main():
 p=argparse.ArgumentParser(description='AD-V3-P02 mandatory Gold live acquisition fabric')
 p.add_argument('--horizon',default='ALL'); p.add_argument('--as-of',default=None); p.add_argument('--data-root',default=str(PHASE/'artifacts'/'live_store'))
 p.add_argument('--fixture-dir',default=None); p.add_argument('--no-network',action='store_true'); p.add_argument('--json',action='store_true')
 a=p.parse_args(); r=execute(PHASE,a.horizon,a.as_of,a.data_root,a.fixture_dir,a.no_network); rec=r['coverage_receipt']
 if a.json: print(json.dumps(rec,indent=2,ensure_ascii=False))
 else:
  print('AD-V3-P02 GOLD ACQUISITION:',rec['analysis_admission']); print(json.dumps(rec['fact_counts'],indent=2)); print(json.dumps(rec['source_counts'],indent=2))
 return 3 if rec['analysis_admission']=='BLOCKED' else (2 if rec['analysis_admission']=='DEGRADED' else 0)
if __name__=='__main__': raise SystemExit(main())
