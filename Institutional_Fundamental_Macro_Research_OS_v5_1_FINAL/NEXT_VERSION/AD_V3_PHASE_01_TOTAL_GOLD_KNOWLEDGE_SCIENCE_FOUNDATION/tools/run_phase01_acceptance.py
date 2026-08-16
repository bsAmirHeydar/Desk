#!/usr/bin/env python3
from pathlib import Path
import subprocess,sys,json
ROOT=Path(__file__).resolve().parents[1]
cmd=[sys.executable,str(ROOT/'tools/validate_phase01.py'),'--json']
p=subprocess.run(cmd,capture_output=True,text=True)
try: val=json.loads(p.stdout)
except Exception: val={'status':'FAIL','raw_stdout':p.stdout,'raw_stderr':p.stderr}
# compile canonical receipt only after validation invocation
q=subprocess.run([sys.executable,str(ROOT/'tools/compile_gold_knowledge.py'),'--json'],capture_output=True,text=True)
try: comp=json.loads(q.stdout)
except Exception: comp={'status':'FAIL_CLOSED','raw_stdout':q.stdout,'raw_stderr':q.stderr}
out={'phase':'AD-V3-P01','acceptance_status':'PASS' if p.returncode==0 and q.returncode==0 and comp.get('status')=='PASS' else 'FAIL','validation':val,'compiler_status':comp.get('status'),'fact_count':(comp.get('registry') or {}).get('fact_count'),'surface_count':(comp.get('surface_coverage') or {}).get('discovered_surface_count'),'v2_freeze':(comp.get('v2_freeze') or {}).get('status'),'p02_handoff':comp.get('p02_handoff')}
print(json.dumps(out,ensure_ascii=False,indent=2)); sys.exit(0 if out['acceptance_status']=='PASS' else 2)
