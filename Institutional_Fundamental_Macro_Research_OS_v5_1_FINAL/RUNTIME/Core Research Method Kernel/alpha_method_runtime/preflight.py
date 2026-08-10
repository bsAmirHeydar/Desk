from pathlib import Path
import json, subprocess, sys
from .registry import MethodRegistry
from .selftest import run as selftest
from .parity import run as parity

def run(vault_root):
    v=Path(vault_root).resolve(); reg=MethodRegistry(v); checks=[]; errors=[]
    errs=reg.validate(); checks.append({'name':'registry_and_manifest','pass':not errs,'detail':errs})
    # No actual APL-B runtime may exist. Mentions in docs/specs do not count as installation.
    aplb=list((v/'RUNTIME').glob('APL-B*'))+list((v/'RUNTIME').glob('**/APL_B_MANIFEST.json'))
    checks.append({'name':'no_apl_b_runtime','pass':not aplb,'detail':[str(x.relative_to(v)) for x in aplb]})
    try:
        a=json.loads((v/'RUNTIME'/'APL-A Alpha Perspective Layer'/'APL_A_MANIFEST.json').read_text(encoding='utf-8')); ok=a.get('mode')=='SHADOW_ONLY' and all(a.get('authority',{}).get(k)=='NONE' for k in ('fact','direction','permission','broker_write'))
    except Exception as e: ok=False; errors.append(str(e))
    checks.append({'name':'apl_a_authority_unchanged','pass':ok})
    st=selftest(v); checks.append({'name':'method_selftest','pass':st['status']=='PASS','detail':{'passed':st.get('passed'),'total':st.get('total'),'errors':st.get('errors')}})
    pa=parity(v); checks.append({'name':'decision_parity','pass':pa['status']=='PASS','detail':pa})
    # inherited scientific baseline quick checks
    tools=[v/'RUNTIME'/'R1 Foundation'/'tools'/'alpha_runtime.py',v/'RUNTIME'/'R2 Prompt Execution OS'/'tools'/'alpha_prompt_runtime.py']
    if not all(x.is_file() for x in tools): errors.append('inherited runtime tool missing')
    bad=[x for x in checks if not x['pass']]; errors += [x['name'] for x in bad]
    return {'status':'PASS' if not errors else 'FAIL','method_version':'M1.0.0','scientific_stack':'V21.3.0','runtime':'R4.0.0','checks':checks,'errors':errors}
