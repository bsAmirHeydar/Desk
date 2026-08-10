from pathlib import Path
import json,sys,subprocess,os
from .util import now,uid,add_runtime_paths,case,run_tool
from .fingerprint import verify as verify_fingerprint
from .attacks import run as attacks
from .environment import inspect as inspect_environment

def run(vault_root,profile='CORE'):
    v=Path(vault_root).resolve();profile=profile.upper();add_runtime_paths(v);cases=[]
    # inherited preflights
    tools=[('R4-001','R1',v/'RUNTIME'/'R1 Foundation'/'tools'/'alpha_runtime.py',['--vault-root',str(v),'preflight']),('R4-002','R2',v/'RUNTIME'/'R2 Prompt Execution OS'/'tools'/'alpha_prompt_runtime.py',['preflight','--vault-root',str(v)]),('R4-003','R3',v/'RUNTIME'/'R3 Operational Execution and Learning OS'/'tools'/'alpha.py',['--vault-root',str(v),'preflight']),('R4-004','M1_METHOD',v/'RUNTIME'/'Core Research Method Kernel'/'tools'/'alpha_method.py',['--vault-root',str(v),'preflight'])]
    for cid,name,t,args in tools:
        q=run_tool([sys.executable,str(t),*args]);cases.append(case(cid,'INHERITED','PASS' if q.returncode==0 else 'FAIL',{'component':name,'tail':(q.stdout+q.stderr)[-5000:]}))
    fp=verify_fingerprint(v);cases.append(case('R4-033','DRIFT','PASS' if fp['pass'] else 'FAIL',fp))
    cases.extend(attacks(v,profile))
    # de-duplicate by case id, keeping the last (attack result overrides catalog placeholders)
    d={x['case_id']:x for x in cases};cases=list(d.values());cases.sort(key=lambda x:x['case_id'])
    hard_fail=[x for x in cases if x['hard'] and x['status']=='FAIL']
    env=None
    if profile=='ENVIRONMENT':
        env=inspect_environment(v);status='PENDING' if not hard_fail else 'FAIL';classification='ENVIRONMENT_ATTESTATION_PENDING' if not hard_fail else 'NOT_CERTIFIED'
    elif hard_fail:status='FAIL';classification='NOT_CERTIFIED'
    elif profile=='FULL':status='PASS';classification='FULL_OFFLINE_CERTIFIED'
    else:status='PASS';classification='CORE_CERTIFIED'
    return {'schema_version':'1.0.0','certification_id':uid('CERT'),'profile':profile,'status':status,'classification':classification,'scientific_stack':'V21.3.0','runtime':'R4.0.0','surface_fingerprint':fp.get('actual_surface_hash'),'cases':cases,'environment':env,'created_at_utc':now(),'non_claims':['NO_PROFITABILITY_CERTIFICATION','NO_FORECAST_CORRECTNESS_GUARANTEE','NO_PRIVATE_SOURCE_AVAILABILITY_CLAIM','NO_PROVIDER_DETERMINISM_CLAIM_WITHOUT_ENVIRONMENT_ATTESTATION']}
