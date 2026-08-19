\
from __future__ import annotations
import json,sys,re
from pathlib import Path
HERE=Path(__file__).resolve(); PH=HERE.parents[1]; NEXT=PH.parent; REPO=NEXT.parents[1]
if str(NEXT) not in sys.path: sys.path.insert(0,str(NEXT))
from AD_V31_R05_OPERATIONS_HUMAN_INTELLIGENCE_FINALIZATION.runtime.common import load_json
from AD_V31_R05_OPERATIONS_HUMAN_INTELLIGENCE_FINALIZATION.runtime.r05_freeze import verify_science

def ck(n,o,d=None): return {'name':n,'status':'PASS' if o else 'FAIL','detail':d}
def main():
 c=[]; cfg=PH/'config'; req=['r05_operations_policy.json','run_lock_policy.json','operations_cadence_policy.json','operations_retention_policy.json','health_policy.json','human_terminology.json','human_presentation_policy.json','recovery_policy.json','backup_policy.json','r05_release_policy.json','r05_freeze_policy.json']
 c.append(ck('all R05 config present',all((cfg/x).exists() for x in req),[x for x in req if not (cfg/x).exists()]))
 rel=load_json(cfg/'r05_release_policy.json',{}); c.append(ck('R05 is operations/presentation only',rel.get('classification')=='OPERATIONS_PRESENTATION_ONLY' and rel.get('new_science') is False,rel))
 c.append(ck('R05 does not reset R04 cohort',rel.get('cohort_reset') is False and rel.get('active_qualification_cohort')=='R04_CONTINUES',rel))
 c.append(ck('next state Frozen Live Qualification and no R06',rel.get('next_state')=='FROZEN_LIVE_QUALIFICATION' and rel.get('r06_planned') is False,rel))
 sci=verify_science(); c.append(ck('pre-R05 scientific surfaces unchanged',sci.get('status')=='PASS',sci.get('drift')))
 cad=load_json(cfg/'operations_cadence_policy.json',{}); c.append(ck('scheduler disabled by default',cad.get('enabled_by_default') is False,cad)); c.append(ck('cadence cannot backdate predictions','DO_NOT_BACKDATE' in str(cad.get('missed_run_policy')),cad.get('missed_run_policy')))
 hp=load_json(cfg/'human_presentation_policy.json',{}); c.append(ck('human presentation has four cognitive levels',set((hp.get('levels') or {}).values())=={'10_SECOND','1_MINUTE','5_MINUTE','FORENSIC'},hp.get('levels')))
 c.append(ck('fake charts and small-n seduction forbidden',hp.get('fake_chart_forbidden') is True and hp.get('small_n_seduction_forbidden') is True,hp))
 health=load_json(cfg/'health_policy.json',{}); c.append(ck('health has no opaque score',health.get('opaque_score_forbidden') is True)); c.append(ck('blocked health dominates',health.get('blocked_dominates') is True))
 op=load_json(cfg/'r05_operations_policy.json',{}); c.append(ck('WAIT and UNKNOWN are not runtime failures',op.get('wait_is_runtime_failure') is False and op.get('unknown_is_runtime_failure') is False,op))
 c.append(ck('last attempt and success explicitly separated',op.get('last_attempt_separate_from_last_success') is True and op.get('failed_attempt_must_not_replace_last_success') is True))
 alpha=(NEXT/'AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN/tools/alpha_desk.py').read_text(encoding='utf-8'); c.append(ck('R05 status/recovery commands exposed','v31-ops-status' in alpha and 'v31-recovery-status' in alpha and 'v31-recover' in alpha)); c.append(ck('no R05 normal science-run command introduced','run-r05' not in alpha.lower()))
 orch=(NEXT/'AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN/runtime/gold_orchestrator.py').read_text(encoding='utf-8'); c.append(ck('P10 remains canonical one-run orchestrator','r05_preflight' in orch and 'r05_write_operations_receipt' in orch and 'STAGE_ORDER' in orch)); c.append(ck('R03 still between decision and precommit',"'DECISION_CALIBRATION','PERSPECTIVE_OVERLAY','FORWARD_PRECOMMIT'" in orch.replace(' ','')))
 pres=load_json(NEXT/'AD_V3_PHASE_11_FINAL_INSTITUTIONAL_GOLD_CONTROL_ROOM/config/presentation_policy.json',{}); c.append(ck('P11 human profile present',pres.get('profile')=='HUMAN_INSTITUTIONAL_FA' or 'HUMAN_INSTITUTIONAL_FA' in str(pres),pres))
 rend=(NEXT/'AD_V3_PHASE_11_FINAL_INSTITUTIONAL_GOLD_CONTROL_ROOM/runtime/renderer.py').read_text(encoding='utf-8'); c.append(ck('P11 has 10-second human view','نمای ۱۰ ثانیه‌ای' in rend)); c.append(ck('P11 has audit-mode disclosure','audit-only' in rend and 'نمای فنی' in rend)); c.append(ck('primary price-pressure language preserved','فشار بنیادی ≠ رفتار قیمت' in rend))
 docs=['QUICK_START_FA.md']+[f'docs/{i:02d} '+n for i,n in [(1,'Final Operator Model.md'),(2,'One Run Operations.md'),(3,'Failure Recovery.md'),(4,'Last Attempt vs Last Success.md'),(5,'Forward Cadence Operations.md'),(6,'Human Intelligence Architecture.md'),(7,'Control Room Cognitive Levels.md'),(8,'Human Terminology Dictionary.md'),(9,'Data Health for Operators.md'),(10,'Forward Qualification for Operators.md'),(11,'Backup and Disaster Recovery.md'),(12,'Frozen Live Qualification.md'),(13,'Post-R05 Change Classification.md')]]
 c.append(ck('final operator documentation complete',all((PH/x).exists() for x in docs),[x for x in docs if not (PH/x).exists()]))
 ps=list((PH/'tools').glob('*.ps1')); txt='\n'.join(x.read_text(encoding='utf-8',errors='ignore') for x in ps); c.append(ck('PowerShell tools avoid PS7-only ternary/null-coalescing syntax','??' not in txt and not re.search(r'\?\s*[^:]+:',txt),[x.name for x in ps]))
 c.append(ck('R05 artifacts gitignored','AD_V31_R05_OPERATIONS_HUMAN_INTELLIGENCE_FINALIZATION/artifacts/' in (REPO/'.gitignore').read_text(encoding='utf-8-sig')))
 ok=all(x['status']=='PASS' for x in c); out={'phase':'AD-V3.1-R05','version':'3.1.5-operations-human-intelligence','validation_status':'PASS' if ok else 'FAIL','check_count':len(c),'checks':c,'science_drift_count':len(sci.get('drift') or []),'cohort_reset':False,'next_state':'FROZEN_LIVE_QUALIFICATION','r06_planned':False}; print(json.dumps(out,ensure_ascii=False,indent=2)); return 0 if ok else 2
if __name__=='__main__': raise SystemExit(main())
