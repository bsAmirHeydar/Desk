#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];VAULT=ROOT.parents[1]
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for c in iter(lambda:f.read(1024*1024),b''):h.update(c)
 return h.hexdigest()
def main():
 checks=[];base=json.loads((ROOT/'baseline/P00_P01_P02_P03_P04_P05_P06_P07_DEPENDENCY_FINGERPRINT.json').read_text())
 for d in base['dependencies']:
  p=VAULT.parent/d['path'];ok=p.is_file() and sha(p)==d['sha256'];checks.append({'name':'dependency:'+d['phase'],'status':'PASS' if ok else 'FAIL'})
 p=subprocess.run([sys.executable,str(ROOT/'tools/validate_phase08.py')],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True);checks.append({'name':'P08_VALIDATOR','status':'PASS' if p.returncode==0 else 'FAIL','stdout':p.stdout[-800:] if p.returncode else None,'stderr':p.stderr[-800:] if p.returncode else None})
 p07=VAULT/'NEXT_VERSION/AD_V2_PHASE_07_D4_TRUE_FORWARD_PROMOTION/tools/run_phase07_acceptance.py';q=subprocess.run([sys.executable,str(p07)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True);checks.append({'name':'P07_REGRESSION','status':'PASS' if q.returncode==0 else 'FAIL','stderr':q.stderr[-600:] if q.returncode else None})
 failed=[x for x in checks if x['status']!='PASS'];out={'schema_version':'1.0.0','phase':'AD-V2-P08','status':'PASS' if not failed else 'FAIL','checks':checks,'deployment':'CONTINUOUS_TRUE_FORWARD_SHADOW','scheduler_activation':'OPERATOR_INSTALL_AFTER_SOURCE_COMMIT','true_forward_collection':'READY','automatic_outcome_scoring':'ONLY_WITH_PREDECLARED_PROFILE_AND_OBSERVATIONS','auto_promotion':False,'v1_production_authority_unchanged':True,'trade_permission':'V1_INHERITED','broker':'NONE'};print(json.dumps(out,indent=2));return 0 if not failed else 2
if __name__=='__main__':raise SystemExit(main())
