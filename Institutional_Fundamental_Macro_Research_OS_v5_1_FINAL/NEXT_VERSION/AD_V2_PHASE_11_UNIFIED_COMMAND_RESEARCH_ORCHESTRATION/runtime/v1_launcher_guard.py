from pathlib import Path
import hashlib,json,subprocess,argparse

TEXT_EXTENSIONS={'.ps1','.psm1','.psd1','.py','.json','.md','.txt','.yaml','.yml','.toml','.ini','.cfg','.csv','.html','.htm','.js','.ts','.tsx','.jsx','.css','.xml'}
class V1LauncherGuardError(RuntimeError):pass

def _run(repo,args,text=False):
    return subprocess.run(['git','-C',str(repo),*args],capture_output=True,text=text)

def _norm_bytes(b):
    return b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')

def _sha_bytes(b):return hashlib.sha256(b).hexdigest()

def _aggregate(rows):
    raw=json.dumps(rows,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
    return hashlib.sha256(raw).hexdigest()

def load_policy(phase_root):
    p=Path(phase_root)/'baseline/P00_P10_AND_PROMPT_SURFACE_FINGERPRINT.json'
    return json.loads(p.read_text(encoding='utf-8'))['v1_root_launcher_binding_policy']

def _p00_commit(repo,policy):
    anchor=policy['p00_anchor_rel']
    q=_run(repo,['log','--reverse','--format=%H','--diff-filter=A','--',anchor],text=True)
    rows=[x.strip() for x in q.stdout.splitlines() if x.strip()] if q.returncode==0 else []
    if not rows:raise V1LauncherGuardError('Cannot resolve P00 introduction commit for V1 authority freeze boundary')
    return rows[0]

def _verify_tracked_pre_p00(repo,rel,p00_commit,required_markers=None):
    p=repo/rel
    if not p.is_file():raise V1LauncherGuardError('Required V1 authority surface missing: '+rel)
    q=_run(repo,['ls-files','--error-unmatch','--',rel],text=True)
    if q.returncode!=0:raise V1LauncherGuardError('Required V1 authority surface is not tracked by Git HEAD: '+rel)
    q=_run(repo,['diff','--quiet','HEAD','--',rel])
    if q.returncode!=0:raise V1LauncherGuardError('Required V1 authority surface differs from current Git HEAD: '+rel)
    q=_run(repo,['diff','--cached','--quiet','HEAD','--',rel])
    if q.returncode!=0:raise V1LauncherGuardError('Required V1 authority surface has staged mutation: '+rel)
    q=_run(repo,['show','HEAD:'+rel])
    if q.returncode!=0:raise V1LauncherGuardError('Cannot read required V1 authority surface from HEAD: '+rel)
    head_bytes=q.stdout;work_bytes=p.read_bytes()
    if _sha_bytes(_norm_bytes(work_bytes))!=_sha_bytes(_norm_bytes(head_bytes)):
        raise V1LauncherGuardError('Required V1 authority surface canonical content differs from HEAD: '+rel)
    q=_run(repo,['log','-1','--format=%H','--',rel],text=True)
    last=q.stdout.strip() if q.returncode==0 else ''
    if not last:raise V1LauncherGuardError('Cannot resolve last commit for V1 authority surface: '+rel)
    q=_run(repo,['merge-base','--is-ancestor',last,p00_commit])
    if q.returncode!=0:raise V1LauncherGuardError('V1 authority surface was modified after P00 freeze boundary: '+rel)
    try:txt=_norm_bytes(head_bytes).decode('utf-8-sig')
    except UnicodeDecodeError:raise V1LauncherGuardError('V1 authority surface is not UTF-8 compatible: '+rel)
    missing=[x for x in (required_markers or []) if x.lower() not in txt.lower()]
    if missing:raise V1LauncherGuardError('V1 authority surface semantic contract missing markers in '+rel+': '+','.join(missing))
    q=_run(repo,['rev-parse','HEAD:'+rel],text=True);blob=q.stdout.strip() if q.returncode==0 else None
    return {'rel':rel,'canonical_sha256':_sha_bytes(_norm_bytes(head_bytes)),'git_blob':blob,'last_commit':last,'semantic_contract':'PASS'}

def verify_v1_root_launcher(repo,policy):
    # Compatibility function name retained for P11/P12 callers. The actual hard boundary is
    # the direct V1 authority/runtime surface used by P11. AlphaLab.ps1 is only a legacy thin wrapper.
    repo=Path(repo).resolve();p00_commit=_p00_commit(repo,policy);surfaces=[]
    reqs=policy.get('required_runtime_paths') or []
    if not reqs:raise V1LauncherGuardError('V1 authority binding policy has no required runtime paths')
    for item in reqs:
        surfaces.append(_verify_tracked_pre_p00(repo,item['rel'],p00_commit,item.get('required_markers')))

    rel=policy.get('rel','AlphaLab.ps1');launcher=repo/rel;launcher_binding=None
    if launcher.is_file():
        launcher_binding=_verify_tracked_pre_p00(repo,rel,p00_commit,policy.get('required_markers'))
        txt=_norm_bytes(launcher.read_bytes()).decode('utf-8-sig').lower()
        forbidden=[x for x in policy.get('forbidden_markers',[]) if x.lower() in txt]
        if forbidden:raise V1LauncherGuardError('Legacy V1 root launcher violates V1/V2 boundary: '+','.join(forbidden))
        launcher_presence='PRESENT_VERIFIED'
    else:
        if not policy.get('launcher_optional_when_direct_bridge',False):
            raise V1LauncherGuardError('V1 root launcher missing and policy does not permit direct-runtime binding: '+rel)
        launcher_presence='ABSENT_ALLOWED_DIRECT_RUNTIME_BRIDGE'

    aggregate_rows=[{'rel':x['rel'],'sha256':x['canonical_sha256'],'git_blob':x['git_blob']} for x in surfaces]
    if launcher_binding:
        aggregate_rows.append({'rel':launcher_binding['rel'],'sha256':launcher_binding['canonical_sha256'],'git_blob':launcher_binding['git_blob']})
    aggregate_sha=_aggregate(aggregate_rows)
    aggregate_blob='aggregate:'+_aggregate([{'rel':x['rel'],'git_blob':x['git_blob']} for x in aggregate_rows])
    return {
      'status':'PASS','rel':rel,'verification_mode':policy['verification_mode'],
      'launcher_presence':launcher_presence,'launcher_binding':launcher_binding,
      'surface_count':len(surfaces),'surfaces':surfaces,
      'canonical_sha256':aggregate_sha,'git_blob':aggregate_blob,
      'p00_commit':p00_commit,'semantic_contract':'PASS','tracked_head_binding':'PASS','pre_p00_freeze':'PASS',
      'bridge_mode':'DIRECT_V1_RUNTIME_SURFACE'
    }

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo-root',required=True);ap.add_argument('--phase-root',default=str(Path(__file__).resolve().parents[1]));a=ap.parse_args()
    try:o=verify_v1_root_launcher(a.repo_root,load_policy(a.phase_root));print(json.dumps(o,indent=2));return 0
    except Exception as e:print(json.dumps({'status':'FAIL_CLOSED','error':str(e)},indent=2));return 2
if __name__=='__main__':raise SystemExit(main())
