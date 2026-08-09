from pathlib import Path
import json
from .certification import run as certify

def run(vault_root):
    v=Path(vault_root);errs=[]
    try:
        rm=json.loads((v/'RUNTIME'/'RUNTIME_MANIFEST.json').read_text(encoding='utf-8'));ok=rm.get('runtime_version')=='R4.0.0' and rm.get('scientific_stack')=='V21.3.0' and rm.get('authority',{}).get('direction')=='NONE' and rm.get('authority',{}).get('permission')=='NONE'
    except Exception as e:ok=False;errs.append(str(e))
    core=certify(v,'CORE');full=certify(v,'FULL')
    if not ok:errs.append('R4 runtime manifest/authority invariant failed')
    if core['status']!='PASS':errs.append('R4 core certification failed')
    if full['status']!='PASS':errs.append('R4 full offline certification failed')
    return {'status':'PASS' if not errs else 'FAIL','runtime':'R4.0.0','scientific_stack':'V21.3.0','core_certification':core,'full_offline_certification':full,'errors':errs}
