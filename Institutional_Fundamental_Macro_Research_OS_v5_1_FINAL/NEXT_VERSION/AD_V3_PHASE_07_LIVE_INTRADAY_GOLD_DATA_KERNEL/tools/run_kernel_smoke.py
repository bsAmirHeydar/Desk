from __future__ import annotations
import argparse,json,pathlib,sys,urllib.request
HERE=pathlib.Path(__file__).resolve(); PH=HERE.parents[1]; REPO=PH.parents[2]; sys.path.insert(0,str(PH.parent))
from AD_V3_PHASE_07_LIVE_INTRADAY_GOLD_DATA_KERNEL.runtime.kernel_runtime import run_kernel

def main():
 p=argparse.ArgumentParser(); p.add_argument('--horizon',default='SESSION_1_6H'); p.add_argument('--mode',default='NORMAL',choices=['NORMAL','FULL_REFRESH','CACHE_ONLY']); p.add_argument('--fixture-network-dir'); p.add_argument('--json',action='store_true'); a=p.parse_args()
 if not a.fixture_network_dir and a.mode!='CACHE_ONLY':
  try:
   urllib.request.urlopen('https://www.federalreserve.gov/',timeout=5).read(32)
  except Exception as e:
   out={'phase':'AD-V3-P07','live_kernel_smoke':'NOT_RUN_NETWORK_UNAVAILABLE','reason':type(e).__name__+':'+str(e)}; print(json.dumps(out,indent=2)); return 0
 try: r=run_kernel(REPO,a.horizon,a.mode,fixture_network_dir=a.fixture_network_dir)
 except Exception as e:
  print(json.dumps({'phase':'AD-V3-P07','live_kernel_smoke':'FAIL','error':type(e).__name__+':'+str(e)},indent=2)); return 2
 out={'phase':'AD-V3-P07','live_kernel_smoke':'PASS','run_id':r['run_id'],'horizon':r['horizon'],'mode':r['mode'],'live_kernel_total':r['kernel_health']['live_kernel_total'],'live_kernel_fresh':r['kernel_health']['live_kernel_fresh'],'context_reused':r['performance']['context_reused'],'context_refreshed':r['performance']['context_refreshed'],'network_requests':r['performance']['network_requests'],'duration_ms':r['performance']['total_p07_ms'],'admission':r['analysis_admission']}
 print(json.dumps(out,indent=2,ensure_ascii=False)); return 0 if r['analysis_admission']!='BLOCKED' else 3
if __name__=='__main__': raise SystemExit(main())
