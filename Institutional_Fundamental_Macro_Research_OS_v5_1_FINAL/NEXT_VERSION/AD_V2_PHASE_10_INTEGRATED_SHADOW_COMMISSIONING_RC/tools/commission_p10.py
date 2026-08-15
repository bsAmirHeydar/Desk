#!/usr/bin/env python3
from pathlib import Path
import argparse,json,subprocess,sys
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE))
from runtime.commissioning import commission
from runtime.common import write_json

def run(cmd):
    p=subprocess.run(cmd,text=True,capture_output=True)
    if p.stdout: sys.stdout.write(p.stdout)
    if p.stderr: sys.stderr.write(p.stderr)
    return p

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--repo-root',required=True)
    ap.add_argument('--data-root',required=True)
    ap.add_argument('--output')
    ap.add_argument('--r4-profile',choices=['CORE','FULL'],default='FULL')
    a=ap.parse_args()
    repo=Path(a.repo_root).resolve()
    vault=repo/'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL'
    acc=run([sys.executable,str(BASE/'tools/run_phase10_acceptance.py'),'--repo-root',str(repo)])
    acc_ok=acc.returncode==0
    cert=vault/'RUNTIME/R4 Scientific Certification and Reproducibility Hardening/tools/alpha_certify.py'
    core=run([sys.executable,str(cert),'--vault-root',str(vault),'certify','--profile','CORE'])
    core_ok=core.returncode==0
    full_status='NOT_RUN'
    if a.r4_profile=='FULL':
        full=run([sys.executable,str(cert),'--vault-root',str(vault),'certify','--profile','FULL'])
        full_status='PASS' if full.returncode==0 else 'FAIL'
    rec=commission(a.data_root,BASE.parent,full_stack_regression_pass=acc_ok,integrated_e2e_pass=acc_ok,r4_core_pass=core_ok,r4_full_status=full_status)
    if full_status=='FAIL': rec['status']='FAIL_CLOSED'; rec['warnings'].append('R4_FULL_FAILED')
    p=a.output or str(Path(a.data_root)/'alpha_desk_v2/p10_commissioning/latest_commissioning_receipt.json')
    write_json(p,rec)
    print(json.dumps(rec,ensure_ascii=False,indent=2))
    return 0 if rec['status']!='FAIL_CLOSED' else 1
if __name__=='__main__':raise SystemExit(main())
