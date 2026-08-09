from pathlib import Path
import json,subprocess,sys,os,importlib.util
from .selftest import run as selftest
def _r2_compat(v):
    p=str(v/'RUNTIME'/'R2 Prompt Execution OS')
    if p not in sys.path:sys.path.insert(0,p)
    from alpha_prompt_runtime.registry import PromptRegistry
    from alpha_prompt_runtime.graph import ProcessGraph
    reg=PromptRegistry(v);errs=list(reg.validate() or []);g=ProcessGraph(reg.graph);errs+=list(g.validate() or []);ids=reg.process_ids();checks=[('r2_process_count',len(ids)==25),('r2_direction_authority',[x for x in ids if 'fundamental_direction' in reg.manifest(x)['authority']['can_create']]==['W31_FUNDAMENTAL']),('r2_permission_authority',[x for x in ids if 'final_permission' in reg.manifest(x)['authority']['can_create']]==['P63_FINAL_DECISION']),('r2_prompt_pack',reg.pack.get('version')=='ALPHALAB_PROMPT_PACK_1.0.0')];return checks,errs
def run(vault_root):
    v=Path(vault_root);checks=[];errors=[]
    try:rm=json.loads((v/'RUNTIME'/'RUNTIME_MANIFEST.json').read_text(encoding='utf-8'));checks += [('runtime_r3',rm.get('runtime_version') in ('R3.0.0','R4.0.0')),('scientific_v213',rm.get('scientific_stack')=='V21.3.0'),('direction_authority_none',rm.get('authority',{}).get('direction')=='NONE'),('permission_authority_none',rm.get('authority',{}).get('permission')=='NONE'),('operational_block_only',rm.get('operational_execution',{}).get('authority')=='BLOCK_ONLY')]
    except Exception as e:errors.append('runtime_manifest:'+str(e))
    try:c,e=_r2_compat(v);checks+=c;errors+=e
    except Exception as e:checks.append(('r2_compat',False));errors.append('r2_compat:'+str(e))
    tool=v/'RUNTIME'/'R1 Foundation'/'tools'/'alpha_runtime.py';q=subprocess.run([sys.executable,str(tool),'--vault-root',str(v),'preflight'],capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'});checks.append(('r1_preflight',q.returncode==0))
    if q.returncode:errors.append('r1_preflight:'+(q.stdout+q.stderr)[-3000:])
    has_js=importlib.util.find_spec('jsonschema') is not None;checks.append(('jsonschema_runtime_available',has_js));
    if not has_js:errors.append('jsonschema is required by R2 strict output validation; the R3 installer attempts to bootstrap it before any Vault mutation.')
    # Existing R2 strict output validation requires jsonschema; keep this a visible capability check, not a hidden dependency.
    st=selftest(v);checks.append(('r3_selftest',st['status']=='PASS'));errors.extend(st.get('errors',[]));errs=errors+[n for n,ok in checks if not ok]
    return {'status':'PASS' if not errs else 'FAIL','checks':[{'name':n,'pass':ok} for n,ok in checks],'selftest':st,'errors':errs}
