#!/usr/bin/env python3
from pathlib import Path
import argparse,hashlib,json,os,subprocess,sys,tempfile

def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for c in iter(lambda:f.read(1024*1024),b''): h.update(c)
 return h.hexdigest()

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--repo-root',required=True); ap.add_argument('--json-out'); a=ap.parse_args(); repo=Path(a.repo_root).resolve(); vault=repo/'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL'; phase=vault/'NEXT_VERSION/AD_V2_PHASE_05_GOLD_INTELLIGENCE_SPECIALIZATION'; env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}; checks=[]
 deps=json.loads((phase/'baseline/P00_P01_P02_P03_P04_DEPENDENCY_FINGERPRINT.json').read_text())
 for d in deps['requires']:
  p=vault/d['path']; ok=p.is_file() and sha(p)==d['sha256']; checks.append({'name':'dependency:'+d['phase'],'status':'PASS' if ok else 'FAIL'})
 p=subprocess.run([sys.executable,str(phase/'tools/validate_phase05.py'),'--json'],text=True,capture_output=True,env=env)
 if p.returncode!=0: sys.stdout.write(p.stdout); sys.stderr.write(p.stderr); return 2
 r=json.loads(p.stdout); checks.append({'name':'P05_VALIDATOR','status':r['status'],'passed':r['passed'],'failed':r['failed']})
 # P04 regression
 p04=vault/'NEXT_VERSION/AD_V2_PHASE_04_LATENT_RELEASE_ENGINE/tools/run_phase04_acceptance.py'
 with tempfile.TemporaryDirectory(prefix='ad_v2_p05_p04reg_') as td:
  jout=Path(td)/'p04.json'; p=subprocess.run([sys.executable,str(p04),'--repo-root',str(repo)],text=True,capture_output=True,env=env)
  if p.returncode!=0: sys.stdout.write(p.stdout); sys.stderr.write(p.stderr); return 2
  # P04 acceptance prints JSON to stdout
  try: r4=json.loads(p.stdout)
  except Exception: r4={'status':'FAIL'}
  checks.append({'name':'P04_REGRESSION','status':r4.get('status','FAIL')})
 status='PASS' if all(x['status']=='PASS' for x in checks) else 'FAIL'; out={'schema_version':'1.0.0','phase':'AD-V2-P05','status':status,'checks':checks,'deployment':'SHADOW_ONLY','v1_production_authority_unchanged':True,'p02_pressure_authority_unchanged':True,'p03_transmission_authority_unchanged':True,'p04_release_authority_unchanged':True}
 txt=json.dumps(out,ensure_ascii=False,indent=2); print(txt)
 if a.json_out: Path(a.json_out).write_text(txt+'\n',encoding='utf-8')
 return 0 if status=='PASS' else 2
if __name__=='__main__': raise SystemExit(main())
