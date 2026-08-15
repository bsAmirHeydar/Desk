#!/usr/bin/env python3
from pathlib import Path
import argparse,hashlib,json,os,subprocess,sys

def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for c in iter(lambda:f.read(1024*1024),b''): h.update(c)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--repo-root',required=True); a=ap.parse_args(); repo=Path(a.repo_root).resolve(); vault=repo/'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL'; phase=vault/'NEXT_VERSION/AD_V2_PHASE_04_LATENT_RELEASE_ENGINE'; env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
    checks=[]
    deps=json.loads((phase/'baseline/P00_P01_P02_P03_DEPENDENCY_FINGERPRINT.json').read_text(encoding='utf-8'))
    for d in deps['requires']:
        p=vault/d['path']; ok=p.is_file() and sha(p)==d['sha256']; checks.append({'name':'dependency:'+d['phase'],'status':'PASS' if ok else 'FAIL'})
    p=subprocess.run([sys.executable,str(phase/'tools/validate_phase04.py'),'--json'],text=True,capture_output=True,env=env)
    if p.returncode!=0:
        sys.stdout.write(p.stdout); sys.stderr.write(p.stderr); return 2
    r=json.loads(p.stdout); checks.append({'name':'P04_VALIDATOR','status':r['status'],'passed':r['passed'],'failed':r['failed']})
    p03=vault/'NEXT_VERSION/AD_V2_PHASE_03_PRICE_TRANSMISSION_ENGINE/tools/run_phase03_acceptance.py'
    import tempfile
    with tempfile.TemporaryDirectory(prefix='ad_v2_p04_p03reg_') as td:
        jout=Path(td)/'p03.json'
        p=subprocess.run([sys.executable,str(p03),'--repo-root',str(repo),'--json-out',str(jout)],text=True,capture_output=True,env=env)
        if p.returncode!=0:
            sys.stdout.write(p.stdout); sys.stderr.write(p.stderr); return 2
        r3=json.loads(jout.read_text(encoding='utf-8')); checks.append({'name':'P03_REGRESSION','status':r3['status'],'passed':sum(int(x.get('passed',0)) for x in r3.get('checks',[]) if isinstance(x.get('passed'),int)),'failed':sum(int(x.get('failed',0)) for x in r3.get('checks',[]) if isinstance(x.get('failed'),int))})
    status='PASS' if all(c['status']=='PASS' for c in checks) else 'FAIL'
    out={'schema_version':'1.0.0','phase':'AD-V2-P04','status':status,'checks':checks,'deployment':'SHADOW_ONLY','v1_production_authority_unchanged':True,'p02_pressure_authority_unchanged':True,'p03_transmission_authority_unchanged':True}
    print(json.dumps(out,ensure_ascii=False,indent=2)); return 0 if status=='PASS' else 2
if __name__=='__main__': raise SystemExit(main())
