#!/usr/bin/env python3
from pathlib import Path
import tempfile,json,subprocess,sys,datetime
HERE=Path(__file__).resolve().parent; V=HERE.parents[1]
def run(args):
 r=subprocess.run([sys.executable,*map(str,args)],capture_output=True,text=True); return r.returncode,r.stdout+r.stderr
checks=[]
rc,o=run([HERE/'alphalab_preflight.py','--vault-root',V]); checks.append(['preflight',rc==0,o])
with tempfile.TemporaryDirectory() as td:
 td=Path(td); g={'analysis_id':'T','nodes':[{'evidence_id':'A','root_cause_id':'R'},{'evidence_id':'B','root_cause_id':'R'}],'edges':[{'from':'A','to':'B','relation':'CAUSAL_DESCENDANT'}]}; gp=td/'g.json'; gp.write_text(json.dumps(g)); rc,o=run([HERE/'alphalab_validate_evidence_graph.py',gp]); checks.append(['evidence_graph',rc==0,o])
 st={'symbol_mapping_valid':True,'market_state_known':True,'permission_valid_until_utc':(datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(minutes=30)).isoformat(),'clock_drift_seconds':0,'hard_incidents':[]}; sp=td/'s.json'; sp.write_text(json.dumps(st)); op=td/'o.json'; rc,o=run([HERE/'alphalab_operational_gate.py','--state',sp,'--policy',V/'94 Institutional Evidence Calibration Portfolio and Model Risk Production Engine/config/operational_gate_policy.json','--output',op]); checks.append(['operational_gate',rc==0 and json.loads(op.read_text())['status']=='CLEAR',o])
print(json.dumps({'status':'PASS' if all(x[1] for x in checks) else 'FAIL','checks':[{'name':n,'pass':ok,'output':o[:500]} for n,ok,o in checks]},indent=2)); sys.exit(0 if all(x[1] for x in checks) else 2)
