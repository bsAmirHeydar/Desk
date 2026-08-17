from __future__ import annotations
from pathlib import Path
from .common import load

def phase(repo): return Path(repo)/'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL'/'NEXT_VERSION'/'AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN'
def p04(repo): return Path(repo)/'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL'/'NEXT_VERSION'/'AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING'
def normalize_subject(subject):
    s=str(subject or 'Gold').strip().lower()
    if s in {'gold','xauusd','xau'}: return 'Gold'
    raise ValueError('SUBJECT_NOT_ACTIVE_IN_ALPHA_DESK_V3: '+str(subject))
def promotion_state(repo,override=None):
    if override: return override
    from AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING.runtime.promotion import load_state
    return (load_state(p04(repo)) or {}).get('state','SHADOW_COMMISSIONING')
def resolve(repo,subject='Gold',intent='PRODUCTION',promotion_override=None):
    subject=normalize_subject(subject);intent=str(intent).upper();state=promotion_state(repo,promotion_override)
    cfg=load(phase(repo)/'config/route_policy.json',{})
    routes=cfg.get('routes',{});row=routes.get(state) or routes.get('SHADOW_COMMISSIONING') or {}
    runtime=row.get(intent)
    if runtime not in {'V2','V3'}: raise RuntimeError(f'ROUTE_UNRESOLVED state={state} intent={intent}')
    return {'record_type':'AD_V3_P10_ROUTING_RECEIPT','subject':subject,'intent':intent,'promotion_state':state,'selected_runtime':runtime,'reason':f'{state}:{intent}->{runtime}','production_authority':runtime=='V3' and intent=='PRODUCTION'}
