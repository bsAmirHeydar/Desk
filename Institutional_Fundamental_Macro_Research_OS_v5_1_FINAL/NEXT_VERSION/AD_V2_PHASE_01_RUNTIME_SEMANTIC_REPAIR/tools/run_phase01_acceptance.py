#!/usr/bin/env python3
from pathlib import Path
import argparse, json, subprocess, sys, os

def run(cmd,cwd=None):
    env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
    p=subprocess.run(cmd,cwd=cwd,text=True,capture_output=True,env=env)
    return {'cmd':[str(x) for x in cmd],'returncode':p.returncode,'stdout':p.stdout[-16000:],'stderr':p.stderr[-16000:]}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--repo-root',required=True); ap.add_argument('--json',action='store_true'); a=ap.parse_args()
    repo=Path(a.repo_root).resolve(); vault=repo/'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL'; phase=vault/'NEXT_VERSION/AD_V2_PHASE_01_RUNTIME_SEMANTIC_REPAIR'; p00=vault/'NEXT_VERSION/AD_V2_PHASE_00_PRESSURE_PRICE_CONSTITUTION'
    steps=[]
    steps.append(run([sys.executable,str(p00/'tools/run_phase00_acceptance.py'),'--repo-root',str(repo),'--json']))
    steps.append(run([sys.executable,str(phase/'tools/legacy_v1_defect_probe.py'),'--repo-root',str(repo),'--json']))
    steps.append(run([sys.executable,str(phase/'tools/validate_phase01.py'),'--repo-root',str(repo),'--json']))
    # Validate the original V11 example through the closed V1 validator; P01 must not disturb Module 89 semantics.
    v11=vault/'89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine'
    steps.append(run([sys.executable,str(v11/'tools/validate_v11_state_schema.py'),str(v11/'examples/example_gold.json')],cwd=vault))
    # P00 acceptance already runs the V21 cognitive regression; do not duplicate that expensive step here.
    ok=all(x['returncode']==0 for x in steps)
    out={'status':'PASS' if ok else 'FAIL','phase':'AD-V2-P01','steps':steps}
    if a.json: print(json.dumps(out,indent=2))
    else:
        print('PHASE 01 ACCEPTANCE:',out['status'])
        for i,s in enumerate(steps,1): print(f"[{i}] rc={s['returncode']} {s['cmd'][1] if len(s['cmd'])>1 else s['cmd'][0]}")
    return 0 if ok else 3
if __name__=='__main__': sys.exit(main())
