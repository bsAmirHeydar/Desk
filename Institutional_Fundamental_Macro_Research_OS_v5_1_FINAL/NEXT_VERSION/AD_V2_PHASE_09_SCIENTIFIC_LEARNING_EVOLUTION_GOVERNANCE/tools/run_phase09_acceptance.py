#!/usr/bin/env python3
from pathlib import Path
import json,subprocess,sys,tempfile
PH=Path(__file__).resolve().parent.parent;PP=PH.parent

def run(cmd):return subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
def main():
 checks=[]
 v=run([sys.executable,str(PH/'tools/validate_phase09.py')]);
 try:vj=json.loads(v.stdout)
 except:vj={}
 checks.append({'name':'P09_VALIDATOR','status':'PASS' if v.returncode==0 and vj.get('status')=='PASS' else 'FAIL','passed':vj.get('passed'),'failed':vj.get('failed')})
 # P08 regression
 p8=PP/'AD_V2_PHASE_08_CONTINUOUS_TRUE_FORWARD_OPERATIONS/tools/run_phase08_acceptance.py';r=run([sys.executable,str(p8)]);checks.append({'name':'P08_REGRESSION','status':'PASS' if r.returncode==0 else 'FAIL'})
 # manifests unchanged/readable
 for n in range(0,9):
  ds=list(PP.glob(f'AD_V2_PHASE_{n:02d}_*/DEVELOPMENT_MANIFEST.json'))
  checks.append({'name':f'P{n:02d}_MANIFEST_PRESENT','status':'PASS' if len(ds)==1 else 'FAIL'})
 fail=[x for x in checks if x['status']!='PASS'];out={'schema_version':'1.0.0','phase':'AD-V2-P09','status':'PASS' if not fail else 'FAIL','checks':checks,'deployment':'SHADOW_LEARNING_ONLY','authority':{'auto_mutation':False,'trade_permission':'V1_INHERITED','broker':'NONE'}};print(json.dumps(out,ensure_ascii=False,indent=2));return 0 if not fail else 1
if __name__=='__main__':raise SystemExit(main())
