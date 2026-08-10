from pathlib import Path
import os,sys,json,subprocess
from .util import data_root,host_command_json,add_runtime_paths,now,load_json,current_certification_surface,repo_git_state



def _require_certification(v,dr,mode):
    surface=current_certification_surface(v)
    if mode=='LIVE':
        p=dr/'commissioning'/'readiness_receipt.json'
        if not p.is_file():raise RuntimeError('LIVE is blocked: production readiness receipt is missing. Run AlphaLab_Commission.ps1 readiness --signoff after environment and shadow certification.')
        r=load_json(p);gs=repo_git_state(v)
        if r.get('status')!='PASS' or r.get('classification')!='PRODUCTION_READY_PERMISSION_ONLY':raise RuntimeError('LIVE is blocked: production readiness is not signed off.')
        if r.get('certification_surface_fingerprint')!=surface:raise RuntimeError('LIVE is blocked: readiness receipt is stale relative to current certified surface.')
        if r.get('git_commit')!=gs.get('head') or not gs.get('tracked_clean'):raise RuntimeError('LIVE is blocked: Git commit/working tree differs from the signed-off production state.')
    else:
        p=dr/'commissioning'/'environment_receipt.json'
        if not p.is_file():raise RuntimeError(mode+' is blocked: environment certification receipt is missing.')
        r=load_json(p)
        if r.get('status')!='PASS' or r.get('classification')!='ENVIRONMENT_CERTIFIED':raise RuntimeError(mode+' is blocked: environment is not certified.')
        if r.get('certification_surface_fingerprint')!=surface:raise RuntimeError(mode+' is blocked: environment certification is stale relative to current certified surface.')
    return surface

def _parse_stdout(s):
    t=s.strip();a=t.find('{');b=t.rfind('}')
    if a<0 or b<a:raise RuntimeError('Alpha runtime did not emit JSON')
    return json.loads(t[a:b+1])

def _report(v,dr,rid):
    add_runtime_paths(v)
    from alpha_runtime.runtime import AlphaRuntime
    from alpha_operational_runtime.report import Reporter
    rt=AlphaRuntime(v,dr);Reporter(v,rt).render(rid,'FULL')
    raw=rt.store.objects.get_bytes(next(x['artifact_hash'] for x in rt.catalog.list_artifacts(rid) if x['logical_name']=='r3_human_report'))
    out=dr/'reports';out.mkdir(parents=True,exist_ok=True);p=out/(rid+'.md');p.write_bytes(raw)
    fp=rt.store.load_artifact_json(rid,'final_permission');ri=rt.store.load_artifact_json(rid,'research_intent');ret=rt.store.load_artifact_json(rid,'r3_retrieval_receipt');m=rt.store.load_manifest(rid)
    return {'run_id':rid,'instrument':m['subject'],'mode':m['run_mode'],'analysis_cutoff_utc':m['analysis_cutoff_utc'],'permission':fp.get('permission'),'fundamental_direction':ri.get('fundamental_direction'),'edge_state':ri.get('edge_state'),'decision_critical_gap_count':ret.get('decision_critical_gap_count'),'material_gap_count':ret.get('material_gap_count'),'decision_seal_hash':m.get('decision_seal_hash'),'report_path':str(p)}

def main(vault_root,args,seal_truth_state=None):
    v=Path(vault_root).resolve();dr=data_root(v);tool=v/'RUNTIME'/'R3 Operational Execution and Learning OS'/'tools'/'alpha.py';env={**os.environ,'ALPHALAB_HOST_COMMAND':host_command_json(v),'ALPHALAB_VAULT_ROOT':str(v),'PYTHONDONTWRITEBYTECODE':'1'}
    if not args:raise RuntimeError('usage: AlphaLab.ps1 <INSTRUMENT|DAILY6> <LIVE|SHADOW|HISTORICAL> [timestamp]')
    subject=args[0].upper();mode=(args[1].upper() if len(args)>1 else 'LIVE');at=args[2] if len(args)>2 else None
    if mode=='SHADOW':rmode='SHADOW_LIVE';profile='SHADOW_ONLY_V1';decision_only=True
    elif mode=='LIVE':rmode='LIVE';profile='PERMISSION_ONLY_V1';decision_only=False
    elif mode=='HISTORICAL':
        if not at:raise RuntimeError('HISTORICAL requires an explicit timezone-aware timestamp')
        rmode='HISTORICAL_REPLAY';profile='PERMISSION_ONLY_V1';decision_only=True
    else:raise RuntimeError('mode must be LIVE, SHADOW, or HISTORICAL')
    _require_certification(v,dr,mode)
    cmd=[sys.executable,str(tool),'--vault-root',str(v),'--data-root',str(dr)]
    if subject=='DAILY6':
        cmd += ['daily-six-run','--mode',rmode,'--horizon','DAILY_OPEN_TO_CLOSE','--host-binding','PRODUCTION_COMMAND']
        if at:cmd += ['--at',at]
        if decision_only:cmd += ['--decision-only']
    else:
        cmd += ['run',subject,'--mode',rmode,'--horizon','DAILY_OPEN_TO_CLOSE','--coverage','STRICT_FULL','--depth','DEEP','--output-depth','FULL','--execution-profile',profile,'--host-binding','PRODUCTION_COMMAND']
        if at:cmd += ['--at',at]
        if decision_only:cmd += ['--decision-only']
    q=subprocess.run(cmd,capture_output=True,text=True,env=env)
    if q.returncode:raise RuntimeError((q.stdout+q.stderr)[-12000:])
    out=_parse_stdout(q.stdout);rids=[]
    if subject=='DAILY6':rids=[x['run_id'] for x in out['results']]
    else:rids=[out['run_id']]
    reports=[_report(v,dr,r) for r in rids]
    commitments=[]
    if mode=='SHADOW':
        from .true_forward import seal_run
        truth=seal_truth_state or 'SHADOW_LIVE'
        for r in rids: commitments.append(seal_run(v,r,truth))
    return {'schema_version':'1.0.0','status':'PASS','commissioning':'C1.0.0','true_forward_extension':'TF1.0.0','generated_at_utc':now(),'results':reports,'forward_commitments':commitments,'meta_reconciliation':out.get('meta_reconciliation')}
