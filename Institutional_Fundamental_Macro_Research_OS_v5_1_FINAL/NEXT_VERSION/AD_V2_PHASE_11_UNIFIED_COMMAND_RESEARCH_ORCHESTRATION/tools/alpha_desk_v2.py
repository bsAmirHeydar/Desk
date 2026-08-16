#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys,subprocess
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE));from runtime.unified_launcher import run_gold;from runtime.cluster import compile_cluster;from runtime.common import data_root

def _tool(repo,phase,tool,args):
 v=Path(repo)/'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL';p=v/'NEXT_VERSION'/phase/'tools'/tool
 q=subprocess.run([sys.executable,str(p),*args]);return q.returncode

def main():
 ap=argparse.ArgumentParser(prog='AlphaDesk');ap.add_argument('--repo-root',required=True);sp=ap.add_subparsers(dest='cmd',required=True)
 r=sp.add_parser('run');r.add_argument('subject');r.add_argument('--input-pack');r.add_argument('--window-seconds',type=int,default=60);r.add_argument('--output-dir');r.add_argument('--no-persist',action='store_true')
 c=sp.add_parser('cluster');c.add_argument('subject',nargs='?',default='Gold')
 sp.add_parser('status');sp.add_parser('health');sp.add_parser('tf-status');sp.add_parser('learning-status');sp.add_parser('rc-status')
 a=ap.parse_args();repo=Path(a.repo_root).resolve();v=repo/'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL';dr=data_root(repo)
 if a.cmd=='run':
  if str(a.subject).upper() not in {'GOLD','XAU','XAUUSD'}:raise SystemExit('P11 V2 one-command is Gold-only')
  out=run_gold(repo,input_pack=a.input_pack,window_seconds=a.window_seconds,output_dir=a.output_dir,persist=not a.no_persist);print(json.dumps(out,ensure_ascii=False,indent=2));return 0
 if a.cmd=='cluster':print(json.dumps(compile_cluster(BASE),ensure_ascii=False,indent=2));return 0
 if a.cmd=='health':return _tool(repo,'AD_V2_PHASE_10_INTEGRATED_SHADOW_COMMISSIONING_RC','p10_health.py',['--data-root',str(dr)])
 if a.cmd=='tf-status':return _tool(repo,'AD_V2_PHASE_08_CONTINUOUS_TRUE_FORWARD_OPERATIONS','p08_status.py',['--data-root',str(dr)])
 if a.cmd=='learning-status':return _tool(repo,'AD_V2_PHASE_09_SCIENTIFIC_LEARNING_EVOLUTION_GOVERNANCE','p09_status.py',['--data-root',str(dr)])
 if a.cmd=='rc-status':return _tool(repo,'AD_V2_PHASE_10_INTEGRATED_SHADOW_COMMISSIONING_RC','p10_status.py',['--data-root',str(dr)])
 if a.cmd=='status':
  print(json.dumps({'schema_version':'1.0.0','phase':'AD-V2-P11','status':'PASS','subject':'XAUUSD','front_door':'AlphaDesk.ps1','cluster':compile_cluster(BASE),'authority':{'v1':'AUTHORITATIVE','v2':'SHADOW','permission':'V1_INHERITED','broker':'NONE'}},ensure_ascii=False,indent=2));return 0
 return 2
if __name__=='__main__':raise SystemExit(main())
