from __future__ import annotations
from pathlib import Path
from .common import sha256_file, stable_id, iso, write_json

def build(run_id,run_dir,precommit,production_authority=False):
    rd=Path(run_dir); hashes={}
    for p in sorted(rd.iterdir()):
        if p.is_file() and p.name!='capsule.json': hashes[p.name]=sha256_file(p)
    c={'record_type':'AD_V3_P04_RUN_CAPSULE','run_id':run_id,'created_at_utc':iso(),'precommit_id':precommit['precommit_id'],'artifact_hashes':hashes,'artifact_count':len(hashes),'point_in_time_immutable':True,'production_authority':bool(production_authority)}
    c['capsule_id']=stable_id('P04CAP',c); write_json(rd/'capsule.json',c); return c


def build_final_seal(run_id,run_dir,capsule,receipt):
    rd=Path(run_dir)
    targets={}
    for name in ('capsule.json','pipeline_receipt.json'):
        p=rd/name
        if p.exists(): targets[name]=sha256_file(p)
    seal={'record_type':'AD_V3_P04_FINAL_RUN_SEAL','run_id':run_id,'created_at_utc':iso(),'capsule_id':capsule.get('capsule_id'),'pipeline_status':receipt.get('status'),'sealed_hashes':targets,'sealed_artifact_count':len(targets),'final_run_seal':True}
    seal['seal_id']=stable_id('P04SEAL',seal)
    write_json(rd/'run_seal.json',seal)
    return seal
