#!/usr/bin/env python3
from pathlib import Path
import argparse,json,os,subprocess,sys,tempfile

def run(cmd,env):
 p=subprocess.run(cmd,text=True,capture_output=True,env=env)
 if p.stdout:sys.stdout.write(p.stdout)
 if p.stderr:sys.stderr.write(p.stderr)
 if p.returncode!=0:raise RuntimeError('command failed: '+' '.join(map(str,cmd)))
 return p

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo-root',required=True);ap.add_argument('--json-out');a=ap.parse_args();repo=Path(a.repo_root).resolve();vault=repo/'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL';here=Path(__file__).resolve().parents[1];env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'};checks=[]
 with tempfile.TemporaryDirectory(prefix='p10_acc_') as td:
  td=Path(td);run([sys.executable,str(here/'tools/validate_phase10.py'),'--repo-root',str(repo),'--json-out',str(td/'p10.json')],env);v=json.loads((td/'p10.json').read_text());checks.append({'name':'P10_VALIDATOR','status':v['status'],'passed':v['passed'],'failed':v['failed']})
  # P09 regression is sufficient because P09 acceptance itself verifies exact P00-P08 dependencies and P08 regression.
  p09=vault/'NEXT_VERSION/AD_V2_PHASE_09_SCIENTIFIC_LEARNING_EVOLUTION_GOVERNANCE/tools/run_phase09_acceptance.py';r=run([sys.executable,str(p09),'--repo-root',str(repo)],env);checks.append({'name':'P09_REGRESSION','status':'PASS'})
 status='PASS' if all(x['status']=='PASS' for x in checks) else 'FAIL';out={'schema_version':'1.0.0','phase':'AD-V2-P10','status':status,'checks':checks,'authority':{'mainline_override':False,'trade_permission':'V1_INHERITED','broker':'NONE'},'deployment':'V2_RC_SHADOW_ONLY'}
 if a.json_out:Path(a.json_out).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(out,ensure_ascii=False,indent=2));return 0 if status=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
