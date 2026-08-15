#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];VAULT=ROOT.parents[1]
def sha(p):
 h=hashlib.sha256();
 with open(p,'rb') as f:
  for c in iter(lambda:f.read(1024*1024),b''):h.update(c)
 return h.hexdigest()
def main():
 checks=[];base=json.loads((ROOT/'baseline/P00_P01_P02_P03_P04_P05_P06_D4_DEPENDENCY_FINGERPRINT.json').read_text())
 for d in base['dependencies']:
  p=VAULT.parent/d['path'];ok=p.is_file() and sha(p)==d['sha256'];checks.append({'name':'dependency:'+d['phase'],'status':'PASS' if ok else 'FAIL'})
 p=subprocess.run([sys.executable,str(ROOT/'tools/validate_phase07.py')],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True);ok=p.returncode==0;checks.append({'name':'P07_VALIDATOR','status':'PASS' if ok else 'FAIL','stdout':p.stdout[-500:] if not ok else None,'stderr':p.stderr[-500:] if not ok else None})
 # P06 regression acceptance
 p06=VAULT/'NEXT_VERSION/AD_V2_PHASE_06_RUN_MEMORY_UX_INTEGRATION/tools/run_phase06_acceptance.py';q=subprocess.run([sys.executable,str(p06),'--repo-root',str(VAULT.parent)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True);checks.append({'name':'P06_REGRESSION','status':'PASS' if q.returncode==0 else 'FAIL','stderr':q.stderr[-500:] if q.returncode else None})
 failed=[x for x in checks if x['status']!='PASS'];out={'schema_version':'1.0.0','phase':'AD-V2-P07','status':'PASS' if not failed else 'FAIL','checks':checks,'deployment':'SHADOW_ONLY','true_forward_status':'TRUE_FORWARD_EVIDENCE_INSUFFICIENT_AT_INSTALL','commissioning':'NOT_COMMISSIONED','v1_production_authority_unchanged':True,'trade_permission':'V1_INHERITED','broker':'NONE'};print(json.dumps(out,indent=2));return 0 if not failed else 2
if __name__=='__main__':raise SystemExit(main())
