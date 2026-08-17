from __future__ import annotations
import argparse,json,pathlib,sys
HERE=pathlib.Path(__file__).resolve(); PH=HERE.parents[1]; REPO=PH.parents[2]; sys.path.insert(0,str(PH.parent))
from AD_V3_PHASE_07_LIVE_INTRADAY_GOLD_DATA_KERNEL.runtime.kernel_runtime import run_kernel

def main():
 p=argparse.ArgumentParser(description='AD-V3-P07 governed Gold acquisition kernel'); p.add_argument('--horizon',default='SESSION_1_6H'); p.add_argument('--mode',default='NORMAL',choices=['NORMAL','FULL_REFRESH','CACHE_ONLY']); p.add_argument('--as-of'); p.add_argument('--data-root'); p.add_argument('--output-root'); p.add_argument('--fixture-network-dir'); p.add_argument('--json',action='store_true'); a=p.parse_args()
 r=run_kernel(REPO,a.horizon,a.mode,a.as_of,a.data_root,a.output_root,a.fixture_network_dir)
 print(json.dumps(r,indent=2,ensure_ascii=False))
 return 3 if r.get('analysis_admission')=='BLOCKED' else (2 if r.get('analysis_admission')=='DEGRADED' else 0)
if __name__=='__main__': raise SystemExit(main())
