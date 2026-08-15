#!/usr/bin/env python3
from pathlib import Path
import argparse, json, subprocess, sys

def locate_vault(repo):
    p=repo/'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL'
    return p if p.is_dir() else repo

def run(cmd, cwd=None):
    p=subprocess.run(cmd,cwd=cwd,text=True,capture_output=True)
    return {"cmd":cmd,"returncode":p.returncode,"stdout":p.stdout[-12000:],"stderr":p.stderr[-12000:]}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--repo-root',required=True); ap.add_argument('--json',action='store_true'); a=ap.parse_args()
    repo=Path(a.repo_root).resolve(); vault=locate_vault(repo)
    phase=vault/'NEXT_VERSION/AD_V2_PHASE_00_PRESSURE_PRICE_CONSTITUTION'
    steps=[]
    steps.append(run([sys.executable,str(phase/'tools/validate_phase00.py'),'--repo-root',str(repo),'--json']))
    # V1 cognitive self-test is a regression check; P00 is additive-only and must not break it.
    cognitive=vault/'103 Cognitive Multi-Hypothesis Scenario and Adversarial Intelligence Engine/tools/alphalab_cognitive_selftest.py'
    if cognitive.is_file(): steps.append(run([sys.executable,str(cognitive)],cwd=vault))
    ok=all(x['returncode']==0 for x in steps)
    out={"status":"PASS" if ok else "FAIL","phase":"AD-V2-P00","steps":steps}
    if a.json: print(json.dumps(out,indent=2))
    else:
        print('PHASE 00 ACCEPTANCE:',out['status'])
        for i,s in enumerate(steps,1): print(f"[{i}] rc={s['returncode']} {s['cmd'][1] if len(s['cmd'])>1 else s['cmd'][0]}")
    return 0 if ok else 3
if __name__=='__main__': sys.exit(main())
