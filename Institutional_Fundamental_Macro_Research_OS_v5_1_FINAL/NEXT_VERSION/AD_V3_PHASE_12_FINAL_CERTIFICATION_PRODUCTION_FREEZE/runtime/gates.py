from __future__ import annotations
from pathlib import Path
import json,subprocess,sys
from .common import PHASE,NEXT,REPO,load
from .freeze import verify_manifest
GATE_IDS=tuple(x['gate_id'] for x in load(PHASE/'config/final_promotion_gate_registry.json',{}).get('gates',[]))
def _acc(phase):
 p=list(NEXT.glob('AD_V3_PHASE_'+phase+'_*'))[0]/'tools'/('run_phase'+phase+'_acceptance.py');cp=subprocess.run([sys.executable,str(p)],capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=300)
 try:o=json.loads(cp.stdout)
 except Exception:o={}
 return cp.returncode==0 and o.get('acceptance_status')=='PASS'
def real_p09():
 from AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0.runtime.forward_runtime import status
 return status(NEXT/'AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0')
def real_r01():
 from AD_V31_R01_FORWARD_QUALITY_PROMOTION_SCIENCE.runtime.qualification_engine import qualify
 return qualify()
def _static_cert():return load(PHASE/'certification/FINAL_CERTIFICATION_RECEIPT.json',{}) or {}
def collect(approve=False,deep=False,repo=REPO):
 fr=verify_manifest(repo);p09=real_p09();q=real_r01();p11=load(NEXT/'AD_V3_PHASE_11_FINAL_INSTITUTIONAL_GOLD_CONTROL_ROOM/PHASE_11_HANDOFF.json',{}) or {};cert=_static_cert();gold=load(PHASE/'certification/GOLDEN_CERTIFICATION_RECEIPT.json',{}) or {};rb=load(PHASE/'certification/ROLLBACK_CERTIFICATION_RECEIPT.json',{}) or {};rt=load(PHASE/'certification/ROUTING_CERTIFICATION_RECEIPT.json',{}) or {}
 if deep: phase={f'P{i:02d}_PASS':_acc(f'{i:02d}') for i in range(1,12)}
 else: phase={f'P{i:02d}_PASS':cert.get('phase_status',{}).get(f'P{i:02d}')=='PASS' for i in range(1,12)}
 g={**phase,
 'P09_IMPLEMENTATION_PASS':phase.get('P09_PASS',False),
 'R01_IMPLEMENTATION_PASS':cert.get('phase_status',{}).get('R01')=='PASS',
 'R02_IMPLEMENTATION_PASS':cert.get('phase_status',{}).get('R02')=='PASS',
 'R03_IMPLEMENTATION_PASS':cert.get('phase_status',{}).get('R03')=='PASS',
 'R04_IMPLEMENTATION_PASS':cert.get('phase_status',{}).get('R04')=='PASS',
 'P12_CERTIFICATION_PASS':cert.get('implementation_status')=='PASS' and fr.get('classes',{}).get('CERTIFICATION_IMMUTABLE',{}).get('status')=='PASS',
 'SCIENCE_FREEZE_VALID':fr.get('classes',{}).get('SCIENTIFIC_IMMUTABLE',{}).get('status')=='PASS','RUNTIME_FREEZE_VALID':fr.get('classes',{}).get('RUNTIME_IMMUTABLE',{}).get('status')=='PASS','REPORT_FREEZE_VALID':fr.get('classes',{}).get('REPORT_CONTRACT_IMMUTABLE',{}).get('status')=='PASS',
 'ZERO_SCIENCE_DRIFT':fr.get('classes',{}).get('SCIENTIFIC_IMMUTABLE',{}).get('status')=='PASS','ZERO_CRITICAL_INTEGRITY_FAILURES':int(p09.get('integrity_failures',0))==0 and phase.get('P05_PASS',False),
 'P09_SAMPLE_MATURITY_GATE':q.get('sample_gate') is True,'R01_FORWARD_QUALITY_GATE':q.get('quality_gate') is True,'R01_COVERAGE_GATE':q.get('coverage_gate') is True,'R01_CRITICAL_SUBGROUP_GATE':q.get('critical_subgroup_gate') is True,
 'GOLDEN_CERTIFICATION_PASS':gold.get('status')=='PASS','ROLLBACK_CERTIFIED':rb.get('status')=='PASS','PRODUCTION_ROUTING_CERTIFIED':rt.get('status')=='PASS','V2_ROLLBACK_AVAILABLE':rb.get('v2_p11')=='PASS' and rb.get('v2_p13')=='PASS','P11_VISUAL_ACCEPTANCE_PASS':str(p11.get('visual_acceptance','')).startswith('PASS'),'P11_SECURITY_ACCEPTANCE_PASS':p11.get('security_acceptance')=='PASS','EXPLICIT_OPERATOR_APPROVAL':approve is True}
 result={k:g.get(k,False) for k in GATE_IDS};return result,{'P09':p09,'R01':q,'freeze':fr,'forward_state':q.get('sample_maturity'),'forward_quality_state':q.get('forward_quality_state'),'coverage_state':q.get('coverage_state'),'critical_subgroup_state':q.get('critical_subgroup_state')}
def enforce(gates):
 missing=[g for g in GATE_IDS if g not in gates];failed=[g for g in GATE_IDS if gates.get(g) is not True]
 if missing:raise ValueError('FINAL_PROMOTION_GATES_UNAVAILABLE:'+','.join(missing))
 if failed:raise ValueError('FINAL_PROMOTION_GATES_FAILED:'+','.join(failed))
 return True
def certification_state(repo=REPO):
 from AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING.runtime.promotion import load_state
 state=(load_state(NEXT/'AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING') or {}).get('state','SHADOW_COMMISSIONING');cert=_static_cert();fr=verify_manifest(repo);q=real_r01()
 if state=='PRODUCTION_V3':return 'PRODUCTION_V3'
 if cert.get('implementation_status')!='PASS' or fr.get('status')!='PASS':return 'NOT_CERTIFIED'
 if not q.get('sample_gate'):return 'CERTIFIED_PENDING_FORWARD_SAMPLE'
 if q.get('forward_quality_state')=='FAIL':return 'FORWARD_QUALITY_FAILED'
 if not q.get('quality_gate'):return 'CERTIFIED_PENDING_FORWARD_QUALITY'
 if not q.get('coverage_gate'):return 'CERTIFIED_PENDING_COVERAGE'
 if not q.get('critical_subgroup_gate'):return 'FORWARD_QUALITY_FAILED'
 g,_=collect(False,False,repo);others=all(v for k,v in g.items() if k!='EXPLICIT_OPERATOR_APPROVAL')
 return 'PRODUCTION_ELIGIBLE' if others else 'ENGINEERING_CERTIFIED'
