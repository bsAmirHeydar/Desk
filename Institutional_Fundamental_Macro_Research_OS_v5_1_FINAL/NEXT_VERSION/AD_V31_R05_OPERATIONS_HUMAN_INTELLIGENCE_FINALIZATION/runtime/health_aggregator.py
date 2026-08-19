from __future__ import annotations

def aggregate(subsystems):
    order={'UNKNOWN':0,'HEALTHY':1,'DEGRADED':2,'ACTION_REQUIRED':3,'BLOCKED':4}
    states=[str((v or {}).get('state','UNKNOWN')) for v in (subsystems or {}).values()]
    overall=max(states,key=lambda x:order.get(x,0)) if states else 'UNKNOWN'
    critical=[k for k,v in (subsystems or {}).items() if (v or {}).get('state')=='BLOCKED']
    action=[k for k,v in (subsystems or {}).items() if (v or {}).get('state')=='ACTION_REQUIRED']
    return {'overall_state':overall,'critical_subsystems':critical,'action_required_subsystems':action,'subsystems':subsystems or {},'opaque_score':None}
