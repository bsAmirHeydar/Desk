from pathlib import Path
from .util import load_json,chash,sha256_obj

def verify(vault_root):
    v=Path(vault_root); cfg=load_json(v/'RUNTIME'/'R4 Scientific Certification and Reproducibility Hardening'/'config'/'certification_surface_baseline.json');bad=[]
    volatile=[rel for rel in cfg.get('files',{}) if '__pycache__' in Path(rel).parts or rel.endswith('.pyc')]
    for rel in volatile: bad.append({'path':rel,'reason':'VOLATILE_SURFACE_ENTRY'})
    for rel,h in cfg['files'].items():
        p=v/rel
        if not p.is_file(): bad.append({'path':rel,'reason':'MISSING'})
        else:
            a=chash(p)
            if a!=h: bad.append({'path':rel,'reason':'HASH_MISMATCH','expected':h,'actual':a})
    actual=sha256_obj(sorted((k,chash(v/k) if (v/k).is_file() else None) for k in cfg['files']))
    return {'pass':not bad,'expected_surface_hash':cfg['surface_hash'],'actual_surface_hash':actual,'bad':bad,'file_count':len(cfg['files'])}
