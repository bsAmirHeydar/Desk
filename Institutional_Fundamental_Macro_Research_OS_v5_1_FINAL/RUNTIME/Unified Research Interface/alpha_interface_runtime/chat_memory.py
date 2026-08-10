import json
from pathlib import Path
from .memory import verify_capsule

def discover(paths):
    rows=[]
    for x in paths or []:
        p=Path(x)
        if p.is_file() and p.suffix.lower()=='.json':
            v=verify_capsule(p)
            if v.get('status')=='PASS':
                try:o=json.loads(p.read_text(encoding='utf-8'));rows.append({'path':str(p),'run_id':o.get('run_id'),'subject':o.get('subject'),'capsule_hash':o.get('capsule_hash')})
                except Exception:pass
    return {'status':'PASS','capsules':rows,'conflicts':[]}
