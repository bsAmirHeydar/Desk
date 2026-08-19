from __future__ import annotations
from pathlib import Path
import os,platform,subprocess
from .common import PHASE,NEXT,load_json,iso
from .health_aggregator import aggregate
from .operations_runtime import semantic_host_state
from .recovery import recovery_status

def scheduler_state():
    pol=load_json(PHASE/'config/operations_cadence_policy.json',{}) or {}
    if os.name!='nt':return {'state':'NOT_APPLICABLE_PLATFORM','enabled_by_default':pol.get('enabled_by_default',False),'frequency_minutes':pol.get('frequency_minutes')}
    try:
        cp=subprocess.run(['schtasks.exe','/Query','/TN','AlphaDesk_Gold_Commission'],capture_output=True,text=True,timeout=5)
        state='INSTALLED' if cp.returncode==0 else 'NOT_INSTALLED'
    except Exception:state='UNKNOWN'
    return {'state':state,'enabled_by_default':pol.get('enabled_by_default',False),'frequency_minutes':pol.get('frequency_minutes')}

def status(repo):
    from AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN.runtime.runtime_status import status as p10_status
    from AD_V31_R04_INSTITUTIONAL_DATA_EDGE_OUTCOME_INFRASTRUCTURE.runtime.data_edge_runtime import status as r04_status
    from AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0.runtime.forward_runtime import status as p09_status
    from AD_V31_R01_FORWARD_QUALITY_PROMOTION_SCIENCE.runtime.qualification_engine import qualify
    from AD_V3_PHASE_12_FINAL_CERTIFICATION_PRODUCTION_FREEZE.runtime.freeze import verify_manifest
    repo=Path(repo);p10=p10_status(repo);r04=r04_status();p09p=NEXT/'AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0';p09=p09_status(p09p);q=qualify();fr=verify_manifest(repo);sched=scheduler_state();rec=recovery_status(repo)
    sem=semantic_host_state();sub={
      'RUNTIME':{'state':'ACTION_REQUIRED' if rec.get('state')=='RECOVERY_REQUIRED' else 'HEALTHY','detail':p10.get('runtime_lock')},
      'DATA':{'state':'DEGRADED' if (r04.get('critical_provider_gaps') or []) else 'HEALTHY','detail':r04.get('critical_provider_gaps')},
      'PROVIDERS':{'state':'DEGRADED' if r04.get('configured_provider_count',0)<r04.get('provider_count',0) else 'HEALTHY','detail':{'configured':r04.get('configured_provider_count'),'total':r04.get('provider_count')}},
      'SEMANTIC':{'state':'DEGRADED' if sem!='CONFIGURED' else 'HEALTHY','detail':sem},
      'PIT_STORE':{'state':'HEALTHY' if (r04.get('pit_store') or {}).get('status')=='PASS' else 'BLOCKED','detail':r04.get('pit_store')},
      'OUTCOME_RECOVERY':{'state':'HEALTHY','detail':{'historically_recovered':(p09.get('statistics') or {}).get('historically_recovered_count',0)}},
      'FORWARD_LEDGER':{'state':'BLOCKED' if int(p09.get('integrity_failures',0)) else 'HEALTHY','detail':(p09.get('statistics') or {}).get('forward_evidence_state')},
      'QUALIFICATION':{'state':'HEALTHY' if q.get('production_qualification_state')=='QUALIFIED' else 'DEGRADED','detail':q.get('production_qualification_state')},
      'REPORT':{'state':'HEALTHY' if p10.get('last_success') else 'DEGRADED','detail':(p10.get('last_success') or {}).get('html')},
      'FREEZE':{'state':'HEALTHY' if fr.get('status')=='PASS' else 'BLOCKED','detail':fr.get('status')},
      'SCHEDULER':{'state':'HEALTHY' if sched.get('state') in ('INSTALLED','NOT_INSTALLED','NOT_APPLICABLE_PLATFORM') else 'DEGRADED','detail':sched},
      'BACKUP':{'state':'DEGRADED','detail':'OPTIONAL_BACKUP_NOT_VERIFIED_THIS_STATUS_RUN'}
    };h=aggregate(sub)
    action=None
    if h['overall_state']=='BLOCKED':action='اجرای Desk متوقف است؛ ابتدا وضعیت Freeze/PIT/Forward Ledger را بررسی کنید.'
    elif rec.get('state')=='RECOVERY_REQUIRED':action='یک وضعیت عملیاتی قابل بازیابی وجود دارد؛ v31-recovery-status را بررسی کنید.'
    elif sem!='CONFIGURED':action='تفسیر معنایی محافظه‌کارانه فعال است؛ در صورت نیاز credential/host را پیکربندی کنید.'
    return {'record_type':'AD_V31_R05_OPS_STATUS','version':'3.1.5-operations-human-intelligence','release':'ALPHA_DESK_V3_1_R05_GOLD','mode':p10.get('promotion_state'),'last_attempt':p10.get('last_attempt'),'last_success':p10.get('last_success'),'current_lock':p10.get('runtime_lock'),'runtime_health':h,'data_health':sub['DATA'],'provider_health':sub['PROVIDERS'],'semantic_status':sem,'pit_health':sub['PIT_STORE'],'forward_status':p09.get('statistics'),'qualification_state':q,'scheduler_state':sched,'report_path':(p10.get('last_success') or {}).get('html'),'operator_action_required':action,'r04_cohort_continues':True,'r05_cohort_reset':False,'trade_execution_authority':'NONE','read_only':True,'as_of_utc':iso()}
