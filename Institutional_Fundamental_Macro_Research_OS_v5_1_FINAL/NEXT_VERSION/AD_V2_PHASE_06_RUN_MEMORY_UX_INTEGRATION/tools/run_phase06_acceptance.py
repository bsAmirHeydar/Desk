#!/usr/bin/env python3
from pathlib import Path
import argparse,hashlib,json,os,subprocess,sys

def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for c in iter(lambda:f.read(1024*1024),b''): h.update(c)
 return h.hexdigest()
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--repo-root',required=True); a=ap.parse_args(); repo=Path(a.repo_root).resolve(); phase=repo/'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL/NEXT_VERSION/AD_V2_PHASE_06_RUN_MEMORY_UX_INTEGRATION'; fp=json.loads((phase/'baseline/P00_P01_P02_P03_P04_P05_DEPENDENCY_FINGERPRINT.json').read_text()); checks=[]
 for d in fp['dependencies']:
  p=repo/d['path']; ok=p.is_file() and sha(p)==d['sha256']; checks.append({'name':'dependency:'+d['phase'],'status':'PASS' if ok else 'FAIL'})
 env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}; q=subprocess.run([sys.executable,str(phase/'tools/validate_phase06.py')],capture_output=True,text=True,env=env);
 try: v=json.loads(q.stdout)
 except Exception: v={'status':'FAIL','raw':q.stdout,'stderr':q.stderr}
 checks.append({'name':'P06_VALIDATOR','status':'PASS' if q.returncode==0 and v.get('status')=='PASS' else 'FAIL','passed':v.get('passed'),'failed':v.get('failed')})
 # P05 regression
 p05=repo/'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL/NEXT_VERSION/AD_V2_PHASE_05_GOLD_INTELLIGENCE_SPECIALIZATION/tools/run_phase05_acceptance.py'; r=subprocess.run([sys.executable,str(p05),'--repo-root',str(repo)],capture_output=True,text=True,env=env); checks.append({'name':'P05_REGRESSION','status':'PASS' if r.returncode==0 else 'FAIL'})
 out={'schema_version':'1.0.0','phase':'AD-V2-P06','status':'PASS' if all(x['status']=='PASS' for x in checks) else 'FAIL','checks':checks,'deployment':'SHADOW_ONLY','v1_production_authority_unchanged':True,'p02_pressure_authority_unchanged':True,'p03_transmission_authority_unchanged':True,'p04_release_authority_unchanged':True,'p05_gold_authority_unchanged':True,'trade_permission':'V1_INHERITED','broker':'NONE'}; print(json.dumps(out,ensure_ascii=False,indent=2)); return 0 if out['status']=='PASS' else 2
if __name__=='__main__': raise SystemExit(main())
