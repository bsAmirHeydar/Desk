from __future__ import annotations
from datetime import datetime,timezone
from pathlib import Path
import json,sys
from .common import hsh
from .health import integrated_health

def _maturity(h):
 e=h.get('evidence') or {}; n=int(e.get('mature_outcomes') or e.get('p08_mature_linked') or 0)
 if n<=0:return 'NO_FORWARD_DATA'
 if n<30:return 'EARLY_FORWARD_DATA'
 return 'RESEARCH_VALIDATION_ELIGIBLE_OR_HIGHER_CHECK_P07'

def commission(data_root,phase_parent,*,full_stack_regression_pass=True,integrated_e2e_pass=True,r4_core_pass=True,r4_full_status='NOT_RUN'):
 h=integrated_health(data_root,phase_parent); warnings=[]
 if h['status']=='PASS_WITH_WARNINGS':warnings.extend((h.get('operations') or {}).get('warnings') or [])
 if not full_stack_regression_pass:warnings.append('FULL_STACK_REGRESSION_FAILED')
 if not integrated_e2e_pass:warnings.append('INTEGRATED_E2E_FAILED')
 if not r4_core_pass:warnings.append('R4_CORE_FAILED')
 hard=not (full_stack_regression_pass and integrated_e2e_pass and r4_core_pass and (h.get('source') or {}).get('all_present'))
 status='FAIL_CLOSED' if hard else ('PASS_WITH_WARNINGS' if warnings else 'PASS')
 rec={'schema_version':'1.0.0','phase':'AD-V2-P10','record_type':'P10_RC_COMMISSIONING_RECEIPT','rc_id':'ALPHA_DESK_V2_RC1_SHADOW','status':status,'created_at_utc':datetime.now(timezone.utc).isoformat().replace('+00:00','Z'),'engineering':{'full_stack_regression':'PASS' if full_stack_regression_pass else 'FAIL','integrated_gold_e2e':'PASS' if integrated_e2e_pass else 'FAIL','r4_core':'PASS' if r4_core_pass else 'FAIL','r4_full':r4_full_status,'health_status':h['status']},'evidence_maturity':{'state':_maturity(h),'true_forward_commitments':h['evidence'].get('true_forward_commitments'),'mature_outcomes':h['evidence'].get('mature_outcomes'),'learning_cases':h['evidence'].get('p09_learning_cases'),'engineering_pass_does_not_imply_empirical_validation':True},'warnings':warnings,'authority':{'v1_production_authoritative':True,'trade_permission':'V1_INHERITED','mainline_override':False,'auto_promotion':False,'auto_tuning':False,'broker':'NONE','deployment':'V2_RC_SHADOW_ONLY'}}
 rec['receipt_hash']=hsh(rec);return rec
