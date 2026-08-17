from __future__ import annotations
from pathlib import Path
import json, subprocess, sys
from .common import load_json, write_json, iso

MACHINE_GATE_ORDER=('P01_FROZEN','P02_3_2_6_FROZEN','P03_3_3_6_FROZEN','P04_ACCEPTANCE_PASS','P09_FORWARD_EVIDENCE_PROVISIONAL','ZERO_INTEGRITY_FAILURES','EXPLICIT_OPERATOR_APPROVAL')

def state_path(phase_root): return Path(phase_root)/'artifacts'/'state'/'promotion_state.json'
def default_state(): return {'record_type':'AD_V3_P04_PROMOTION_STATE','state':'SHADOW_COMMISSIONING','updated_at_utc':iso(),'production_direction_authority':False,'production_trade_permission_authority':False,'v2_baseline_retained':True,'automatic_promotion_forbidden':True}
def load_state(phase_root):
    p=state_path(phase_root); return load_json(p,default_state()) if p.exists() else default_state()
def save_state(phase_root,s): write_json(state_path(phase_root),s); return s

def _next_root(phase_root): return Path(phase_root).parent
def _run_acceptance(script):
    try:
        p=subprocess.run([sys.executable,str(script)],capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=180)
        try: payload=json.loads(p.stdout)
        except Exception: payload={'raw_stdout':p.stdout[-2000:],'raw_stderr':p.stderr[-2000:]}
        return {'pass':p.returncode==0 and payload.get('acceptance_status',payload.get('status'))=='PASS','returncode':p.returncode,'payload':payload}
    except Exception as e:
        return {'pass':False,'error':type(e).__name__+': '+str(e)}

def machine_enforced_gate_ids(phase_root):
    policy=load_json(Path(phase_root)/'config'/'promotion_policy.json',{})
    declared=tuple(policy.get('promotion_requires') or ())
    return declared if declared==MACHINE_GATE_ORDER else MACHINE_GATE_ORDER

def collect_machine_gate_results(phase_root,commissioning_state,approve=False):
    phase_root=Path(phase_root); n=_next_root(phase_root)
    p1=n/'AD_V3_PHASE_01_TOTAL_GOLD_KNOWLEDGE_SCIENCE_FOUNDATION'; p2=n/'AD_V3_PHASE_02_TOTAL_LIVE_DATA_OBSERVABILITY_FABRIC'; p3=n/'AD_V3_PHASE_03_CAUSAL_GOLD_BRAIN_DECISION_ENGINE'
    r1=_run_acceptance(p1/'tools'/'run_phase01_acceptance.py'); r2=_run_acceptance(p2/'tools'/'run_phase02_acceptance.py'); r3=_run_acceptance(p3/'tools'/'run_phase03_acceptance.py'); r4=_run_acceptance(phase_root/'tools'/'run_phase04_acceptance.py')
    p1_payload=r1.get('payload') or {}; p2_manifest=load_json(p2/'DEVELOPMENT_MANIFEST.json',{}); p3_manifest=load_json(p3/'DEVELOPMENT_MANIFEST.json',{})
    p09=n/'AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0'
    p09_state='UNAVAILABLE'; p09_integrity=0
    if p09.exists():
        try:
            from AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0.runtime.forward_runtime import status as p09_status
            ps=p09_status(p09); p09_state=((ps.get('statistics') or {}).get('forward_evidence_state') or 'UNAVAILABLE'); p09_integrity=int(((ps.get('state') or {}).get('integrity_failures',0)) if isinstance(ps.get('state'),dict) else 0)
        except Exception:
            p09_state='UNAVAILABLE'; p09_integrity=1
    return {
      'P01_FROZEN':bool(r1.get('pass') and p1_payload.get('v2_freeze')=='PASS'),
      'P02_3_2_6_FROZEN':bool(r2.get('pass') and p2_manifest.get('revision')=='3.2.6'),
      'P03_3_3_6_FROZEN':bool(r3.get('pass') and p3_manifest.get('revision')=='3.3.6'),
      'P04_ACCEPTANCE_PASS':bool(r4.get('pass')),
      'P09_FORWARD_EVIDENCE_PROVISIONAL':p09_state in ('PROVISIONAL','MATURE'),
      'ZERO_INTEGRITY_FAILURES':commissioning_state.get('integrity_failures',0)==0 and p09_integrity==0,
      'EXPLICIT_OPERATOR_APPROVAL':approve is True,
      '_evidence':{'P01':r1,'P02':r2,'P03':r3,'P04':r4,'P09_forward_evidence_state':p09_state,'legacy_P04_sample_state':commissioning_state.get('sample_state')}
    }

def enforce_declared_gates(policy,gate_results):
    if policy.get('automatic_promotion_forbidden') is not True: raise ValueError('AUTOMATIC_PROMOTION_POLICY_NOT_FAIL_CLOSED')
    declared=policy.get('promotion_requires') or []
    machine=list(MACHINE_GATE_ORDER)
    if declared!=machine: raise ValueError('PROMOTION_POLICY_IMPLEMENTATION_GATE_DRIFT')
    missing=[g for g in declared if g not in gate_results]
    if missing: raise ValueError('PROMOTION_GATES_UNAVAILABLE:'+','.join(missing))
    failed=[g for g in declared if gate_results.get(g) is not True]
    if failed: raise ValueError('PROMOTION_GATES_FAILED:'+','.join(failed))
    return True

def promote(phase_root,commissioning_state,approve=False):
    phase_root=Path(phase_root); policy=load_json(phase_root/'config'/'promotion_policy.json',{})
    gates=collect_machine_gate_results(phase_root,commissioning_state,approve)
    enforce_declared_gates(policy,gates)
    s=default_state(); s.update(state='PRODUCTION_V3',updated_at_utc=iso(),promoted_at_utc=iso(),production_direction_authority=True,production_trade_permission_authority=True,manual_operator_approval=True,promotion_gate_receipt={k:v for k,v in gates.items() if not k.startswith('_')})
    return save_state(phase_root,s)
def rollback(phase_root):
    s=default_state(); s.update(updated_at_utc=iso(),rollback_reason='OPERATOR_ROLLBACK_TO_SHADOW')
    return save_state(phase_root,s)
