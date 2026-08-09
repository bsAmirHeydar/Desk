import json, subprocess, sys
from pathlib import Path
from .selftest import run as selftest

def run(vault_root):
    v=Path(vault_root); checks=[]; errors=[]
    st=selftest(v); checks.append({'name':'r2_selftest','pass':st['status']=='PASS','detail':st})
    # R1 preflight must pass
    tool=v/'RUNTIME'/'R1 Foundation'/'tools'/'alpha_runtime.py'
    if tool.exists():
        q=subprocess.run([sys.executable,str(tool),'--vault-root',str(v),'preflight'],capture_output=True,text=True,env={**__import__('os').environ,'PYTHONDONTWRITEBYTECODE':'1'})
        checks.append({'name':'r1_preflight','pass':q.returncode==0,'detail':(q.stdout+q.stderr)[-4000:]})
    else: checks.append({'name':'r1_preflight','pass':False,'detail':'R1 tool missing'})
    # scientific production prompt/manifest exists
    try:
        j=json.loads((v/'CURRENT_PRODUCTION_MANIFEST.json').read_text(encoding='utf-8')); ok=j.get('current_stack')=='V21.3.0' and (v/j['production_entrypoint']).exists()
    except Exception as e: ok=False; errors.append(str(e))
    checks.append({'name':'scientific_stack_and_entrypoint','pass':ok})
    if any(not x['pass'] for x in checks): errors += [x['name'] for x in checks if not x['pass']]
    return {'status':'PASS' if not errors else 'FAIL','runtime':'R2.0.0','scientific_stack':'V21.3.0','checks':checks,'errors':errors}
