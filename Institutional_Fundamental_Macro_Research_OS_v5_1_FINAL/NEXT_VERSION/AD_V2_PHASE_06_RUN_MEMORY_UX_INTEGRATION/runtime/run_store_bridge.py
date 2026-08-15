#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import json,sys,hashlib

PHASE='AD-V2-P06'; VERSION='0.6.0'

def _canon(x): return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def _hash(x): return hashlib.sha256(_canon(x).encode()).hexdigest()

def attach(vault_root,data_root,run_id,state,extension,changes,portable_memory,report_model):
    vault=Path(vault_root).resolve(); r1=vault/'RUNTIME'/'R1 Foundation'
    if str(r1) not in sys.path: sys.path.insert(0,str(r1))
    from alpha_runtime.runtime import AlphaRuntime
    rt=AlphaRuntime(vault,data_root); m=rt.store.load_manifest(run_id)
    if m.get('run_close_seal_hash'):
        return {'status':'SKIPPED_CLOSE_SEALED','run_id':run_id,'decision_world_write':False,'broker_authority':'NONE'}
    if not m.get('decision_seal_hash'):
        return {'status':'SKIPPED_NO_DECISION_SEAL','run_id':run_id,'decision_world_write':False,'broker_authority':'NONE'}
    payloads={'v2_gold_run_state':state,'v2_run_capsule_extension':extension,'v2_change_set':changes,'v2_portable_memory':portable_memory,'v2_report_model':report_model}; results=[]
    existing={x['logical_name']:x for x in rt.catalog.list_artifacts(run_id)}
    for name,obj in payloads.items():
        if name in existing:
            old=rt.store.load_artifact_json(run_id,name)
            if _hash(old)!=_hash(obj): raise RuntimeError('existing V2 artifact differs: '+name)
            results.append({'logical_name':name,'status':'ALREADY_PRESENT_IDENTICAL'}); continue
        ref=rt.store.put_artifact(run_id,name,'OUTCOME','OUTCOME',obj,'application/json',producer_process_id='AD_V2_P06',producer_version=VERSION); results.append({'logical_name':name,'status':'ATTACHED','artifact_hash':ref['artifact_hash']})
    return {'status':'PASS','run_id':run_id,'artifacts':results,'decision_world_write':False,'broker_authority':'NONE'}
