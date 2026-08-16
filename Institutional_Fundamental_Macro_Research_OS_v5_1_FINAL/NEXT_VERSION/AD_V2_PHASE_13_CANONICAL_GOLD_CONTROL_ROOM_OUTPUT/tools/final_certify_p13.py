#!/usr/bin/env python3
from pathlib import Path
import argparse,sys,json,subprocess,os
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE))
from runtime.common import data_root
from runtime.governance import verify_p12_authorized_delta,verify_amendment_scope,write_amendment

def call(name,cmd):
 q=subprocess.run(cmd,text=True,capture_output=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'});return {'name':name,'status':'PASS' if q.returncode==0 else 'FAIL','stdout_tail':q.stdout[-1200:],'stderr_tail':q.stderr[-800:]}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo-root',required=True);ap.add_argument('--data-root');ap.add_argument('--r4-profile',default='CORE',choices=['CORE','FULL']);a=ap.parse_args();repo=Path(a.repo_root).resolve();dr=Path(a.data_root).resolve() if a.data_root else data_root(repo);v=repo/'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL';checks=[]
 scope=verify_amendment_scope(repo,BASE);checks.append({'name':'P13_AMENDMENT_SCOPE','status':scope['status'],'detail':scope.get('unauthorized_paths')});gov=verify_p12_authorized_delta(repo,BASE);checks.append({'name':'P12_GOVERNANCE_WITH_AUTHORIZED_P13_DELTA','status':gov['status'],'detail':gov.get('failed')})
 checks.append(call('P13_VALIDATOR',[sys.executable,str(BASE/'tools/validate_phase13.py'),'--repo-root',str(repo)]))
 checks.append(call('P13_ACCEPTANCE',[sys.executable,str(BASE/'tools/run_phase13_acceptance.py'),'--repo-root',str(repo)]));checks.append(call('P13_VISUAL_ACCEPTANCE',[sys.executable,str(BASE/'tools/run_visual_acceptance.py'),'--repo-root',str(repo)]))
 p11=v/'NEXT_VERSION/AD_V2_PHASE_11_UNIFIED_COMMAND_RESEARCH_ORCHESTRATION';p10=v/'NEXT_VERSION/AD_V2_PHASE_10_INTEGRATED_SHADOW_COMMISSIONING_RC';p09=v/'NEXT_VERSION/AD_V2_PHASE_09_SCIENTIFIC_LEARNING_EVOLUTION_GOVERNANCE';p08=v/'NEXT_VERSION/AD_V2_PHASE_08_CONTINUOUS_TRUE_FORWARD_OPERATIONS'
 checks.append(call('P11_ACCEPTANCE',[sys.executable,str(p11/'tools/run_phase11_acceptance.py'),'--repo-root',str(repo)]));checks.append(call('P10_ACCEPTANCE',[sys.executable,str(p10/'tools/run_phase10_acceptance.py'),'--repo-root',str(repo)]));checks.append(call('P09_VALIDATOR',[sys.executable,str(p09/'tools/validate_phase09.py'),'--repo-root',str(repo)]));checks.append(call('P08_VALIDATOR',[sys.executable,str(p08/'tools/validate_phase08.py'),'--repo-root',str(repo)]))
 cert=v/'RUNTIME/R4 Scientific Certification and Reproducibility Hardening/tools/alpha_certify.py';checks.append(call('R4_'+a.r4_profile,[sys.executable,str(cert),'--vault-root',str(v),'certify','--profile',a.r4_profile]))
 normalized=[{'name':x['name'],'status':'PASS' if x['status']=='PASS' else 'FAIL'} for x in checks];rec,path=write_amendment(dr,repo,BASE,normalized);out={'schema_version':'1.0.0','phase':'AD-V2-P13','status':'PASS' if rec['status']=='PASS' else 'FAIL_CLOSED','checks':checks,'amendment_receipt':str(path),'receipt_hash':rec['receipt_hash']};print(json.dumps(out,ensure_ascii=False,indent=2));return 0 if out['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
