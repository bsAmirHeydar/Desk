from pathlib import Path
import json,hashlib,importlib.util
class FreezeError(RuntimeError):pass
TEXT_EXTENSIONS={'.ps1','.psm1','.psd1','.py','.json','.md','.txt','.yaml','.yml','.toml','.ini','.cfg','.csv','.html','.htm','.js','.ts','.tsx','.jsx','.css','.xml'}
def sha(p):
 p=Path(p);b=p.read_bytes()
 if p.suffix.lower() in TEXT_EXTENSIONS:b=b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
 return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def _load_guard(repo):
 p=Path(repo)/'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL/NEXT_VERSION/AD_V2_PHASE_11_UNIFIED_COMMAND_RESEARCH_ORCHESTRATION';g=p/'runtime/v1_launcher_guard.py';spec=importlib.util.spec_from_file_location('p11_v1_guard_freeze',g);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m,p
def v1_binding(repo):
 m,p=_load_guard(repo);return m.verify_v1_root_launcher(repo,m.load_policy(p))
def verify(repo,phase_root):
 repo=Path(repo).resolve();reg=load(Path(phase_root)/'config/final_freeze_registry.json');rows=[]
 for s in reg['surfaces']:
  mode=s.get('verification_mode','STATIC_SHA256');p=repo/s['rel']
  if mode=='P11_GIT_FROZEN_V1_BINDING':
   try:
    b=v1_binding(repo);ok=b.get('status')=='PASS';rows.append({'surface_id':s['surface_id'],'status':'PASS' if ok else 'FAIL','rel':s['rel'],'verification_mode':mode,'binding':b})
   except Exception as e:rows.append({'surface_id':s['surface_id'],'status':'FAIL','rel':s['rel'],'verification_mode':mode,'error':str(e)})
  else:
   actual=sha(p) if p.is_file() else None;exp=s.get('sha256');ok=p.is_file() and actual==exp;rows.append({'surface_id':s['surface_id'],'status':'PASS' if ok else 'FAIL','rel':s['rel'],'verification_mode':mode,'expected_sha256':exp,'actual_sha256':actual})
 bad=[x for x in rows if x['status']!='PASS'];return {'schema_version':'1.0.0','phase':'AD-V2-P12','status':'PASS' if not bad else 'FAIL_CLOSED','implementation_version':reg['implementation_version'],'surfaces':rows,'failed_count':len(bad),'empirical_promotion_separate':True}
