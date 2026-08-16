#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys,subprocess,tempfile,shutil
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE));from runtime.freeze import verify
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo-root',required=True);a=ap.parse_args();repo=Path(a.repo_root).resolve();v=repo/'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL';checks=[]
 def ck(n,o,d=None):checks.append({'name':n,'status':'PASS' if o else 'FAIL','detail':d})
 ck('freeze_pass',verify(repo,BASE)['status']=='PASS')
 p11=v/'NEXT_VERSION/AD_V2_PHASE_11_UNIFIED_COMMAND_RESEARCH_ORCHESTRATION';q=subprocess.run([sys.executable,str(p11/'tools/run_phase11_acceptance.py'),'--repo-root',str(repo)],capture_output=True,text=True,env={**__import__('os').environ,'PYTHONDONTWRITEBYTECODE':'1'});ck('p11_acceptance',q.returncode==0,q.stderr[-500:])
 q=subprocess.run([sys.executable,str(p11/'tools/alpha_desk_v2.py'),'--repo-root',str(repo),'cluster','Gold'],capture_output=True,text=True,env={**__import__('os').environ,'PYTHONDONTWRITEBYTECODE':'1'});ck('cluster_command',q.returncode==0 and 'GOLD_MASTER_CLUSTER_V2_1' in q.stdout)
 q=subprocess.run([sys.executable,str(p11/'tools/alpha_desk_v2.py'),'--repo-root',str(repo),'status'],capture_output=True,text=True,env={**__import__('os').environ,'PYTHONDONTWRITEBYTECODE':'1'});ck('status_command',q.returncode==0 and 'AlphaDesk.ps1' in q.stdout)
 # tamper simulation on copy of frozen launcher
 with tempfile.TemporaryDirectory() as td:
  td=Path(td);shutil.copytree(repo,td/'r',dirs_exist_ok=True);t=td/'r'/'AlphaDesk.ps1';t.write_text(t.read_text(encoding='utf-8')+'\n# tamper\n',encoding='utf-8');ck('tamper_detected',verify(td/'r',BASE)['status']=='FAIL_CLOSED')
 with tempfile.TemporaryDirectory() as td:
  td=Path(td);shutil.copytree(repo,td/'r',dirs_exist_ok=True);t=td/'r'/'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL/RUNTIME/Unified Research Interface/alpha_interface_runtime/executor.py';t.write_text(t.read_text(encoding='utf-8')+'\n# authority-surface tamper\n',encoding='utf-8');ck('v1_authority_surface_tamper_detected',verify(td/'r',BASE)['status']=='FAIL_CLOSED')
 fail=[x for x in checks if x['status']!='PASS'];print(json.dumps({'schema_version':'1.0.0','phase':'AD-V2-P12','status':'PASS' if not fail else 'FAIL','checks':checks},ensure_ascii=False,indent=2));return 0 if not fail else 2
if __name__=='__main__':raise SystemExit(main())
