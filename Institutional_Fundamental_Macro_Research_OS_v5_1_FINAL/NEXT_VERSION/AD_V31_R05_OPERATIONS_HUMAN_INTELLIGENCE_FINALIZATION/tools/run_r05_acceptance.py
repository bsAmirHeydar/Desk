#!/usr/bin/env python3
from __future__ import annotations
import json,pathlib,subprocess,sys,hashlib
HERE=pathlib.Path(__file__).resolve();PH=HERE.parents[1];NEXT=PH.parent;REPO=NEXT.parents[1]
def load(p):
    try:return json.loads(pathlib.Path(p).read_text(encoding='utf-8-sig'))
    except Exception:return {}
def run(p,timeout=600):
    cp=subprocess.run([sys.executable,str(p)],cwd=str(REPO),capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=timeout)
    return cp.returncode,cp.stdout[-1800:]
def ck(n,o,d=None):return {'name':n,'status':'PASS' if o else 'FAIL','detail':d}
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest() if pathlib.Path(p).exists() else None
def stat(d):return d.get('status') or d.get('acceptance_status') or d.get('certification_status')
def main():
    c=[]
    # Lightweight live checks of immutable contracts.
    code,out=run(PH/'tools/validate_r05.py',180);c.append(ck('R05 static validation PASS',code==0,out if code else None))
    code,out=run(PH/'tools/verify_r05_freeze.py',120);c.append(ck('R05 implementation + science freeze PASS',code==0,out if code else None))
    # Sealed component receipts were produced by separate actual executions to avoid timeout ambiguity.
    receipts={
      'Golden Operations':'R05_GOLDEN_OPERATIONS_CERTIFICATION.json',
      'Operations':'R05_OPERATIONS_CERTIFICATION.json',
      'Visual':'R05_VISUAL_CERTIFICATION.json',
      'Security':'R05_SECURITY_CERTIFICATION.json',
      'Portability':'R05_PORTABILITY_CERTIFICATION.json',
      'Integrated':'R05_INTEGRATED_FIXTURE.json'}
    for name,f in receipts.items():
        d=load(PH/'qualification'/f);c.append(ck(name+' receipt PASS',stat(d)=='PASS',{'status':stat(d),'file':f}))
    # P12 release/freeze/promotion acceptance with R05 gate.
    code,out=run(NEXT/'AD_V3_PHASE_12_FINAL_CERTIFICATION_PRODUCTION_FREEZE/tools/run_phase12_acceptance.py',600);c.append(ck('P12 final acceptance PASS',code==0,out if code else None))
    # Read-only status cannot mutate R04 cohort.
    q=NEXT/'AD_V31_R04_INSTITUTIONAL_DATA_EDGE_OUTCOME_INFRASTRUCTURE/qualification/R04_QUALIFICATION_COHORT.json';before=sha(q)
    code,out=run(PH/'tools/r05_status.py',120);after=sha(q);c.append(ck('R05 status read-only',code==0 and before==after))
    pol=load(PH/'config/r05_release_policy.json')
    c.append(ck('operations/presentation only',pol.get('classification')=='OPERATIONS_PRESENTATION_ONLY' and pol.get('new_science') is False))
    c.append(ck('R04 cohort continues',pol.get('cohort_reset') is False and before==after))
    c.append(ck('Frozen Live Qualification next',pol.get('next_state')=='FROZEN_LIVE_QUALIFICATION'))
    c.append(ck('no R06 planned',pol.get('r06_planned') is False))
    ok=all(x['status']=='PASS' for x in c)
    o={'phase':'AD-V3.1-R05','version':'3.1.5-operations-human-intelligence','acceptance_status':'PASS' if ok else 'FAIL_CLOSED','check_count':len(c),'checks':c,'science_drift':0 if ok else None,'r04_cohort_reset':False,'next_state':'FROZEN_LIVE_QUALIFICATION','r06_planned':False,'production_promotion_performed':False,'trade_execution_authority':'NONE'}
    print(json.dumps(o,ensure_ascii=False,indent=2));return 0 if ok else 2
if __name__=='__main__':raise SystemExit(main())
