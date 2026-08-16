from __future__ import annotations
from pathlib import Path
import subprocess,json,hashlib
from .common import load_json,hobj,now_utc,dump_json

AUTHORIZED_FROZEN_DELTAS={'ROOT_V2_LAUNCHER'}


def git(repo,*args,check=True):
    q=subprocess.run(['git','-C',str(repo),*args],text=True,capture_output=True)
    if check and q.returncode: raise RuntimeError(q.stderr.strip() or q.stdout.strip())
    return q.stdout.strip()


def verify_baseline(repo, phase_root):
    repo=Path(repo).resolve();phase_root=Path(phase_root)
    cfg=load_json(phase_root/'config/baseline_binding.json');rows=[]
    for x in cfg['git_blob_dependencies']:
        rel=x['rel'];expected=x['git_blob'];actual=git(repo,'rev-parse',f'HEAD:{rel}',check=False)
        ok=actual==expected
        rows.append({'id':x['id'],'rel':rel,'status':'PASS' if ok else 'FAIL','expected_git_blob':expected,'actual_git_blob':actual or None})
    return {'status':'PASS' if all(x['status']=='PASS' for x in rows) else 'FAIL_CLOSED','rows':rows,'baseline_commit':cfg['baseline_commit']}


def verify_p12_authorized_delta(repo, phase_root):
    repo=Path(repo).resolve();v=repo/'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL';p12=v/'NEXT_VERSION/AD_V2_PHASE_12_FINAL_IMPLEMENTATION_FREEZE_ACCEPTANCE';reg=load_json(p12/'config/final_freeze_registry.json');rows=[]
    from importlib.util import spec_from_file_location,module_from_spec
    spec=spec_from_file_location('p12freeze',p12/'runtime/freeze.py');m=module_from_spec(spec);spec.loader.exec_module(m)
    for s in reg['surfaces']:
        sid=s['surface_id'];mode=s.get('verification_mode','STATIC_SHA256')
        if sid in AUTHORIZED_FROZEN_DELTAS:
            rows.append({'surface_id':sid,'status':'AUTHORIZED_P13_DELTA','rel':s['rel']});continue
        if mode=='P11_GIT_FROZEN_V1_BINDING':
            try:
                b=m.v1_binding(repo);ok=b.get('status')=='PASS';rows.append({'surface_id':sid,'status':'PASS' if ok else 'FAIL','binding':b})
            except Exception as e:rows.append({'surface_id':sid,'status':'FAIL','error':str(e)})
        else:
            path=repo/s['rel'];actual=m.sha(path) if path.is_file() else None;ok=actual==s.get('sha256');rows.append({'surface_id':sid,'status':'PASS' if ok else 'FAIL','rel':s['rel'],'expected':s.get('sha256'),'actual':actual})
    bad=[x for x in rows if x['status']=='FAIL']
    return {'status':'PASS' if not bad else 'FAIL_CLOSED','authorized_delta':'ROOT_V2_LAUNCHER_ONLY','rows':rows,'failed':len(bad)}


def write_amendment(data_root, repo, phase_root, checks):
    out=Path(data_root)/'alpha_desk_v2'/'p13_control_room'/'amendments';out.mkdir(parents=True,exist_ok=True)
    base_receipt=Path(data_root)/'alpha_desk_v2'/'p12_finalization'/'final_implementation_receipt.json';base=None
    if base_receipt.exists():
        base=load_json(base_receipt)
    rec={'schema_version':'1.0.0','phase':'AD-V2-P13','record_type':'POST_P12_PRESENTATION_AMENDMENT_RECEIPT','status':'PASS' if all(x.get('status')=='PASS' for x in checks) else 'FAIL_CLOSED','generated_at_utc':now_utc(),'canonical_output_contract':'AD-V2-P13','gold_control_room_schema':'alpha_desk_v2.gold_control_room.v1','presentation_science_authority':'NONE','v1_permission_authority':'PRESERVED','broker_authority':'NONE','science_mutation':False,'base_p12_receipt_present':bool(base),'base_p12_receipt_hash':(base or {}).get('receipt_hash'),'base_p12_status':(base or {}).get('status'),'git_head':git(repo,'rev-parse','HEAD'),'checks':checks,'authorized_frozen_delta':['AlphaDesk.ps1'],'old_p12_receipt_rewritten':False}
    rec['receipt_hash']=hobj(rec);p=out/(rec['generated_at_utc'].replace(':','').replace('-','')+'_'+rec['receipt_hash'][:12]+'.json');dump_json(p,rec);dump_json(Path(data_root)/'alpha_desk_v2'/'p13_control_room'/'latest_amendment.json',rec);return rec,p

def verify_amendment_scope(repo, phase_root):
    repo=Path(repo).resolve();phase_root=Path(phase_root);cfg=load_json(phase_root/'config/baseline_binding.json');base=cfg['baseline_commit'];prefix='Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL/NEXT_VERSION/AD_V2_PHASE_13_CANONICAL_GOLD_CONTROL_ROOM_OUTPUT/'
    anc=subprocess.run(['git','-C',str(repo),'merge-base','--is-ancestor',base,'HEAD']).returncode==0
    committed=set(x for x in git(repo,'diff','--name-only',base+'..HEAD',check=False).splitlines() if x)
    work=set(x for x in git(repo,'diff','--name-only','HEAD',check=False).splitlines() if x)
    untracked=set(x for x in git(repo,'ls-files','--others','--exclude-standard',check=False).splitlines() if x)
    changed=committed|work|untracked
    allowed=lambda x: x=='AlphaDesk.ps1' or x.startswith(prefix)
    bad=sorted(x for x in changed if not allowed(x))
    return {'status':'PASS' if anc and not bad else 'FAIL_CLOSED','baseline_commit':base,'baseline_is_ancestor':anc,'changed_paths':sorted(changed),'unauthorized_paths':bad,'allowed':['AlphaDesk.ps1',prefix+'*']}
