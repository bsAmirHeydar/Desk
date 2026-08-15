#!/usr/bin/env python3
from pathlib import Path
import argparse, json, os, subprocess, sys
sys.dont_write_bytecode=True

def run(cmd,cwd=None,timeout=120):
    p=subprocess.run(cmd,cwd=cwd,text=True,capture_output=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},timeout=timeout)
    return {'cmd':[str(x) for x in cmd],'returncode':p.returncode,'stdout':p.stdout[-16000:],'stderr':p.stderr[-16000:]}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--repo-root',required=True); ap.add_argument('--json',action='store_true'); a=ap.parse_args()
    repo=Path(a.repo_root).resolve(); vault=repo/'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL'; phase=vault/'NEXT_VERSION/AD_V2_PHASE_02_DIRECTIONAL_PRESSURE_ENGINE'; p01=vault/'NEXT_VERSION/AD_V2_PHASE_01_RUNTIME_SEMANTIC_REPAIR'; steps=[]
    steps.append(run([sys.executable,str(p01/'tools/run_phase01_acceptance.py'),'--repo-root',str(repo),'--json']))
    steps.append(run([sys.executable,str(phase/'tools/validate_phase02.py'),'--repo-root',str(repo),'--json']))
    cli=phase/'tools/pressure_engine_cli.py'; fixture=phase/'tests/fixtures/explicit_gold_pressure.json'
    steps.append(run([sys.executable,str(cli),'--input',str(fixture)]))
    v11=vault/'89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine'
    steps.append(run([sys.executable,str(v11/'tools/validate_v11_state_schema.py'),str(v11/'examples/example_gold.json')],cwd=vault))
    ok=all(x['returncode']==0 for x in steps); out={'status':'PASS' if ok else 'FAIL','phase':'AD-V2-P02','steps':steps}
    if a.json: print(json.dumps(out,indent=2))
    else:
        print('PHASE 02 ACCEPTANCE:',out['status'])
        for i,s in enumerate(steps,1): print(f"[{i}] rc={s['returncode']} {s['cmd'][1] if len(s['cmd'])>1 else s['cmd'][0]}")
    return 0 if ok else 3
if __name__=='__main__': sys.exit(main())
