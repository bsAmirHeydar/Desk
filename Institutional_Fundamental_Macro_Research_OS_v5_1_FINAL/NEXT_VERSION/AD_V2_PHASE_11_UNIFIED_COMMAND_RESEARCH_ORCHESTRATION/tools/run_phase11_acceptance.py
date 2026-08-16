#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys,tempfile,copy

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo-root',required=True);a=ap.parse_args();repo=Path(a.repo_root).resolve();v=repo/'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL';phase=v/'NEXT_VERSION/AD_V2_PHASE_11_UNIFIED_COMMAND_RESEARCH_ORCHESTRATION';parent=phase.parent
 if str(parent) not in sys.path:sys.path.insert(0,str(parent))
 if str(phase) not in sys.path:sys.path.insert(0,str(phase))
 from runtime.cluster import compile_cluster
 import runtime.unified_launcher as u
 checks=[]
 def ck(n,o,d=None):checks.append({'name':n,'status':'PASS' if o else 'FAIL','detail':d})
 c1=compile_cluster(phase);c2=compile_cluster(phase);ck('cluster_deterministic',c1['prompt_sha256']==c2['prompt_sha256']);ck('cluster_10',c1['cluster_count']==10)
 # Explicit P10 input replay through the P11 front door (no persistence, no host dependency).
 fixture=v/'NEXT_VERSION/AD_V2_PHASE_10_INTEGRATED_SHADOW_COMMISSIONING_RC/tests/fixtures/integrated_gold_shadow_input.json'
 with tempfile.TemporaryDirectory() as td:
  try:r=u.run_gold(repo,input_pack=fixture,window_seconds=1,output_dir=td,persist=False);ck('explicit_pack_run',r.get('status')=='PASS' and r.get('mode')=='EXPLICIT_INPUT_PACK')
  except Exception as e:ck('explicit_pack_run',False,str(e))
 # Deterministic fixture one-command orchestration; monkeypatch external V1/host/P10 boundaries only.
 events=[]
 rawpre={'pressure_input':json.loads(fixture.read_text())['pressure_input'],'expected_signature_template':json.loads(fixture.read_text())['expected_signature'],'missing_driver_candidates':[],'integrity':{'status':'PASS','target_price_used_for_pressure':False}}
 rawpre['expected_signature_template'].pop('declared_at_utc',None);rawpre['expected_signature_template'].pop('pressure_fingerprint',None)
 arts={'run_capsule':json.loads(fixture.read_text())['base_capsule'],'analysis_cutoff_utc':'2026-08-15T10:00:00Z'}
 orig={k:getattr(u,k) for k in ['run_shadow','load_artifacts','precommit','retrieve_window','response','run_with_pack','now']}
 clock=iter(['2026-08-15T10:01:00Z','2026-08-15T10:01:01Z','2026-08-15T10:02:01Z'])
 try:
  u.run_shadow=lambda v,d:(events.append('V1') or ({'status':'PASS'},'P11-FIXTURE-RUN'))
  u.load_artifacts=lambda v,d,r:(events.append('ARTIFACTS') or arts)
  u.precommit=lambda *args,**kwargs:(events.append('PRECOMMIT') or (copy.deepcopy(rawpre),{'request_hash':'pre'}))
  def ret(*args,**kwargs):events.append('T0' if kwargs.get('label')=='T0' else 'T1');return [{'snapshot_id':kwargs.get('label'),'source_id':'FIXTURE','retrieved_at':'2026-08-15T10:02:00Z'}]
  u.retrieve_window=ret
  def resp(*args,**kwargs):events.append('RESPONSE');sig=args[4] if len(args)>4 else kwargs.get('sealed_signature');return ({'actual_response':json.loads(fixture.read_text())['actual_response'],'gold_observations':json.loads(fixture.read_text())['gold_observations'],'integrity':{'status':'PASS','pressure_mutated':False}},{'request_hash':'resp'})
  u.response=resp
  u.run_with_pack=lambda *args,**kwargs:(events.append('P10') or {'status':'PASS','run_id':'P11-FIXTURE-RUN'})
  u.now=lambda:next(clock,'2026-08-15T10:02:02Z')
  with tempfile.TemporaryDirectory() as td:
   # isolate data root through env
   import os;old=os.environ.get('ALPHALAB_DATA_ROOT');os.environ['ALPHALAB_DATA_ROOT']=td
   try:r=u.run_gold(repo,window_seconds=1,output_dir=td,persist=False,sleep_fn=lambda x:events.append('SLEEP'))
   finally:
    if old is None:os.environ.pop('ALPHALAB_DATA_ROOT',None)
    else:os.environ['ALPHALAB_DATA_ROOT']=old
  ck('one_command_fixture',r.get('status')=='PASS' and r.get('mode')=='ONE_COMMAND_LIVE_SHADOW')
  ck('precommit_before_t0',events.index('PRECOMMIT')<events.index('T0'))
  ck('t0_before_t1',events.index('T0')<events.index('T1'))
  ck('response_after_t1',events.index('T1')<events.index('RESPONSE'))
  ck('p10_last',events.index('RESPONSE')<events.index('P10'))
 except Exception as e:ck('one_command_fixture',False,str(e))
 finally:
  for k,val in orig.items():setattr(u,k,val)
 # root CLI cluster smoke
 q=__import__('subprocess').run([sys.executable,str(phase/'tools/alpha_desk_v2.py'),'--repo-root',str(repo),'cluster','Gold'],capture_output=True,text=True);ck('cli_cluster',q.returncode==0 and 'GOLD_MASTER_CLUSTER_V2_1' in q.stdout,q.stderr[-500:])
 fail=[x for x in checks if x['status']!='PASS'];out={'schema_version':'1.0.0','phase':'AD-V2-P11','status':'PASS' if not fail else 'FAIL','checks':checks};print(json.dumps(out,ensure_ascii=False,indent=2));return 0 if not fail else 2
if __name__=='__main__':raise SystemExit(main())
