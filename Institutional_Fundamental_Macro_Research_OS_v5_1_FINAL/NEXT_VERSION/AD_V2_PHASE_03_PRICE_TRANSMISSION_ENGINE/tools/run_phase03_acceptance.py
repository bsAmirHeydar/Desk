#!/usr/bin/env python3
from pathlib import Path
import argparse,hashlib,json,os,subprocess,sys,tempfile

def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for c in iter(lambda:f.read(1024*1024),b''): h.update(c)
    return h.hexdigest()

def run(cmd,env):
    p=subprocess.run(cmd,text=True,capture_output=True,env=env)
    if p.stdout: sys.stdout.write(p.stdout)
    if p.stderr: sys.stderr.write(p.stderr)
    if p.returncode!=0: raise RuntimeError('command failed: '+' '.join(map(str,cmd)))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo-root',required=True);ap.add_argument('--json-out');a=ap.parse_args(); repo=Path(a.repo_root).resolve(); vault=repo/'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL'; here=Path(__file__).resolve().parents[1]; env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
    dep=json.loads((here/'baseline/P00_P01_P02_DEPENDENCY_FINGERPRINT.json').read_text(encoding='utf-8'))
    checks=[]
    for d in dep['requires']:
        p=vault/d['path']; ok=p.is_file() and sha(p)==d['sha256']; checks.append({'name':'dependency:'+d['phase'],'status':'PASS' if ok else 'FAIL'});
        if not ok: raise SystemExit('P03 dependency mismatch: '+d['path'])
    with tempfile.TemporaryDirectory(prefix='ad_v2_p03_acc_') as td:
        td=Path(td)
        run([sys.executable,str(here/'tools/validate_phase03.py'),'--repo-root',str(repo),'--json-out',str(td/'p03.json')],env)
        p03=json.loads((td/'p03.json').read_text()); checks.append({'name':'P03_VALIDATOR','status':p03['status'],'passed':p03['passed'],'failed':p03['failed']})
        # P02 regression (P02 emits JSON to stdout with --json)
        p02=vault/'NEXT_VERSION/AD_V2_PHASE_02_DIRECTIONAL_PRESSURE_ENGINE/tools/validate_phase02.py'
        q=subprocess.run([sys.executable,str(p02),'--repo-root',str(repo),'--json'],text=True,capture_output=True,env=env)
        if q.returncode!=0:
            if q.stdout: sys.stdout.write(q.stdout)
            if q.stderr: sys.stderr.write(q.stderr)
            raise RuntimeError('P02 regression failed')
        r2=json.loads(q.stdout); checks.append({'name':'P02_REGRESSION','status':r2['status'],'passed':r2['passed'],'failed':r2['tests']-r2['passed']})
    status='PASS' if all(x.get('status')=='PASS' for x in checks) else 'FAIL'
    out={'schema_version':'1.0.0','phase':'AD-V2-P03','status':status,'checks':checks,'deployment':'SHADOW_ONLY','v1_production_authority_unchanged':True,'p02_pressure_authority_unchanged':True}
    if a.json_out: Path(a.json_out).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out,ensure_ascii=False,indent=2))
    return 0 if status=='PASS' else 1
if __name__=='__main__': raise SystemExit(main())
