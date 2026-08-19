\
from __future__ import annotations
import json,sys,subprocess,tempfile,hashlib
from pathlib import Path
HERE=Path(__file__).resolve();PH=HERE.parents[1];NEXT=PH.parent;REPO=NEXT.parents[1]
if str(NEXT) not in sys.path:sys.path.insert(0,str(NEXT))
from AD_V31_R05_OPERATIONS_HUMAN_INTELLIGENCE_FINALIZATION.runtime.status import status
from AD_V31_R05_OPERATIONS_HUMAN_INTELLIGENCE_FINALIZATION.runtime.recovery import recovery_status,recover
from AD_V31_R05_OPERATIONS_HUMAN_INTELLIGENCE_FINALIZATION.runtime.common import sha_file

def ck(n,o,d=None):return {'name':n,'status':'PASS' if o else 'FAIL','detail':d}
def run(path,args=None,timeout=300):
 cp=subprocess.run([sys.executable,str(path)]+(args or []),capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=timeout)
 try:x=json.loads(cp.stdout)
 except Exception:x={'raw':cp.stdout[-1200:],'stderr':cp.stderr[-1200:]}
 return cp.returncode,x

def main():
 c=[]
 rc,g=run(PH/'tools/run_golden_operations_matrix.py');c.append(ck('Golden Operations Matrix PASS',rc==0 and g.get('status')=='PASS',g.get('case_count')))
 rc,p10=run(NEXT/'AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN/tools/run_phase10_acceptance.py',timeout=360);c.append(ck('P10 one-run operations PASS',rc==0 and p10.get('acceptance_status')=='PASS',p10.get('check_count')))
 # status read-only: hash real forward/PIT state paths before/after
 targets=[NEXT/'AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0/artifacts/state/forward_state.json',NEXT/'AD_V31_R04_INSTITUTIONAL_DATA_EDGE_OUTCOME_INFRASTRUCTURE/artifacts/state/pit.sqlite3']
 def snap():return {str(p):sha_file(p) if p.exists() else None for p in targets}
 b=snap();st=status(REPO);a=snap();c.append(ck('v31 ops status is read-only',b==a and st.get('read_only') is True,{'before':b,'after':a}))
 c.append(ck('status separates last attempt and last success','last_attempt' in st and 'last_success' in st))
 c.append(ck('status reports R04 cohort continuation',st.get('r04_cohort_continues') is True and st.get('r05_cohort_reset') is False))
 # recovery status read-only and safe target policy
 rs=recovery_status(REPO);c.append(ck('recovery status is diagnostic only',rs.get('scientific_state_mutation_allowed') is False,rs.get('state')))
 recsrc=(PH/'runtime/recovery.py').read_text(encoding='utf-8');c.append(ck('recovery code cannot touch P09/R01/PIT scientific stores',all(x not in recsrc for x in ['forward_state.json','qualification_ledger','pit.sqlite3','scientific_config'])))
 # scheduler optional/off by default
 pol=json.loads((PH/'config/operations_cadence_policy.json').read_text());c.append(ck('optional scheduler disabled by default',pol.get('enabled_by_default') is False))
 c.append(ck('scheduler preserves P09 episode authority',pol.get('scientific_episode_independence_owned_by')=='AD-V3-P09'))
 # backup script coverage and cache exclusion policy
 bp=json.loads((PH/'config/backup_policy.json').read_text());c.append(ck('backup policy covers scientific runtime state',set(['P09_STATE','R04_PIT_STATE','R01_QUALIFICATION_STATE','P12_CERTIFICATION_RECEIPTS']).issubset(set(bp.get('include',[]))),bp))
 c.append(ck('backup excludes transient caches/secrets','CACHE' in bp.get('exclude',[]) and 'SECRETS' in bp.get('exclude',[])))
 # atomic latest implementation
 am=(NEXT/'AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN/runtime/artifact_manager.py').read_text(encoding='utf-8');c.append(ck('latest pointer publishing uses temp+replace','name+\'.tmp\'' in am and 'os.replace' in am))
 # scheduler/root tooling paths are repo-relative and PS5.1-compatible subset
 scripts=list((PH/'tools').glob('*.ps1')); txt='\n'.join(x.read_text(encoding='utf-8',errors='ignore') for x in scripts);c.append(ck('operator PowerShell tools are relative-path based','C:\\Users\\' not in txt and '/mnt/' not in txt));rtxt='\n'.join(x.read_text(encoding='utf-8',errors='ignore') for x in (PH/'runtime').glob('*.py')); c.append(ck('scheduler is not auto-installed by Python/runtime','/Create' not in rtxt and 'schtasks.exe /Create' not in rtxt))
 ok=all(x['status']=='PASS' for x in c);out={'record_type':'AD_V31_R05_OPERATIONS_CERTIFICATION','status':'PASS' if ok else 'FAIL','check_count':len(c),'checks':c,'scheduler_default':'DISABLED','r04_cohort_continues':True,'r05_cohort_reset':False,'trade_execution_authority':'NONE'};print(json.dumps(out,ensure_ascii=False,indent=2));return 0 if ok else 2
if __name__=='__main__':raise SystemExit(main())
