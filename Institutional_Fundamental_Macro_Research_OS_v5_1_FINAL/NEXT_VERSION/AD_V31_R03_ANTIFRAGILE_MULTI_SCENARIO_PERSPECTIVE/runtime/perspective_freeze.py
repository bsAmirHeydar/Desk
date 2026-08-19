from __future__ import annotations
from pathlib import Path
from .common import PH,sha_file,sha_obj,load
SURF=['config/*.json','runtime/*.py','schemas/*.json']
def current():
    files=[]
    for pat in SURF:
        for p in sorted(PH.glob(pat)):
            if p.name=='perspective_freeze.py':pass
            files.append({'path':str(p.relative_to(PH.parent.parent.parent.parent)) if False else str(p.relative_to(PH)),'sha256':sha_file(p)})
    fp='R03SCI_'+sha_obj(files).upper()
    return {'files':files,'perspective_science_fingerprint':fp}
def verify_manifest():
    man=load(PH/'qualification/R03_PERSPECTIVE_FREEZE_MANIFEST.json',{}) or {};cur=current();ok=bool(man) and man.get('perspective_science_fingerprint')==cur['perspective_science_fingerprint'] and man.get('files')==cur['files'];return {'status':'PASS' if ok else 'FAIL_CLOSED','perspective_science_fingerprint':cur['perspective_science_fingerprint'],'expected_fingerprint':man.get('perspective_science_fingerprint'),'file_count':len(cur['files'])}
