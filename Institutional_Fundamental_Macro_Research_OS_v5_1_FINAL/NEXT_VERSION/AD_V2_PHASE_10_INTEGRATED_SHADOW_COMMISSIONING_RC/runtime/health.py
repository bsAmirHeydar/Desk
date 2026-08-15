from __future__ import annotations
from pathlib import Path
import sys

def integrated_health(data_root,phase_parent):
 pp=Path(phase_parent).resolve()
 if str(pp) not in sys.path:sys.path.insert(0,str(pp))
 src={}
 for n in range(0,10):
  prefix=f'AD_V2_PHASE_{n:02d}_'
  matches=list(pp.glob(prefix+'*'))
  src[f'P{n:02d}']=bool(matches and (matches[0]/'DEVELOPMENT_MANIFEST.json').is_file())
 try:
  from AD_V2_PHASE_08_CONTINUOUS_TRUE_FORWARD_OPERATIONS.runtime.operations import status as p08_status
  p08=p08_status(data_root)
 except Exception as e:p08={'status':'UNAVAILABLE','error':str(e)}
 try:
  from AD_V2_PHASE_09_SCIENTIFIC_LEARNING_EVOLUTION_GOVERNANCE.runtime.operations import status as p09_status
  p09=p09_status(data_root)
 except Exception as e:p09={'status':'UNAVAILABLE','error':str(e)}
 source_ok=all(src.values()); warnings=[]
 if p08.get('status')!='PASS':warnings.append('P08_OPERATIONAL_STATUS_'+str(p08.get('status')))
 if p09.get('status')!='PASS':warnings.append('P09_OPERATIONAL_STATUS_'+str(p09.get('status')))
 p7=(p08.get('p07') or {}) if isinstance(p08,dict) else {}
 evidence={'true_forward_commitments':p7.get('commitments',0),'mature_outcomes':p7.get('mature_outcomes',0),'p08_mature_linked':p08.get('mature_linked',0) if isinstance(p08,dict) else 0,'p09_learning_cases':p09.get('learning_cases',0) if isinstance(p09,dict) else 0}
 if not source_ok: status='FAIL_CLOSED'
 elif warnings: status='PASS_WITH_WARNINGS'
 else: status='PASS'
 return {'schema_version':'1.0.0','phase':'AD-V2-P10','status':status,'source':{'phases':src,'all_present':source_ok},'operations':{'p08':p08,'p09':p09,'warnings':warnings},'evidence':evidence,'authority':{'v1_production_authoritative':True,'trade_permission':'V1_INHERITED','mainline_override':False,'auto_promotion':False,'auto_tuning':False,'broker':'NONE'}}
