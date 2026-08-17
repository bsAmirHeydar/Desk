from __future__ import annotations
import json,pathlib,sys,hashlib
P=pathlib.Path(__file__).resolve().parents[1];N=P.parent;REPO=N.parents[1];sys.path.insert(0,str(N))
def load(p):return json.loads(pathlib.Path(p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def ck(n,o,d=None):return {'name':n,'status':'PASS' if o else 'FAIL','detail':d}
def main():
 checks=[]; base=load(P/'baseline/PRE_P08_AUTHORITY_HASHES.json')
 arch=load(N/'AD_V3_PHASE_05_INTEGRITY_ARCHITECTURE_CONSOLIDATION/config/architecture_surface_registry.json');surface={x.get('path'):x for x in arch.get('surfaces',[])}
 drift=[];governed=[]
 for k,v in base['hashes'].items():
  f=REPO/v['path']; actual=sha(f) if f.exists() else None
  if actual!=v['sha256']:
   own=surface.get(v['path']) or {}
   if own.get('class')=='GOVERNANCE_VERSIONED' and str(own.get('owner','')).startswith('AD-V3-P09'):governed.append({'surface':k,'path':v['path'],'classification':'DOWNSTREAM_GOVERNANCE_VERSIONED'})
   else:drift.append({'surface':k,'expected':v['sha256'],'actual':actual})
 checks.append(ck('pre-P08 scientific and authority surfaces unchanged',not drift,{'science_drift':drift,'accepted_downstream_governance':governed}))
 for f in ['decision_calibration_policy.json','causal_importance_policy.json','magnitude_policy.json','dominance_policy.json','empirical_calibration_policy.json']:
  checks.append(ck('config '+f+' present',(P/'config'/f).exists()))
 pipe=(N/'AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING/runtime/pipeline.py').read_text(encoding='utf-8-sig')
 checks.append(ck('P04 pipeline invokes P08 calibration','AD_V3_PHASE_08_DECISION_SCIENCE_CALIBRATION' in pipe and 'p08_decision_calibration.json' in pipe))
 launcher=(REPO/'AlphaDesk.ps1').read_text(encoding='utf-8-sig');checks.append(ck('v3-decision-status launcher present','AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN' in launcher))
 pol=load(P/'config/decision_calibration_policy.json');checks.append(ck('no production or trade execution authority',pol['production_promotion_forbidden'] is True and pol['trade_execution_authority']=='NONE'))
 status='PASS' if all(x['status']=='PASS' for x in checks) else 'FAIL_CLOSED';out={'phase':'AD-V3-P08','validation_status':status,'check_count':len(checks),'checks':checks,'science_drift':drift};print(json.dumps(out,indent=2,ensure_ascii=False));return 0 if status=='PASS' else 2
if __name__=='__main__':raise SystemExit(main())
