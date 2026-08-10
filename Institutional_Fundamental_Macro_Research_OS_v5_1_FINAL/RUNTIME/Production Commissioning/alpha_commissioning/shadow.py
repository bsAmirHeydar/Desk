from pathlib import Path
import os, sys, json, subprocess
from .util import load_json,dump_json,now,data_root,host_command_json,add_runtime_paths,current_certification_surface

def _read_json_stdout(s):
    t=s.strip();start=t.find('{');end=t.rfind('}')
    if start<0 or end<start:raise RuntimeError('no JSON object in launcher stdout')
    return json.loads(t[start:end+1])

def certify(vault_root,runs_per_instrument=None):
    v=Path(vault_root).resolve();dr=data_root(v);pol=load_json(v/'RUNTIME'/'Production Commissioning'/'config'/'commissioning_policy.json');envp=dr/'commissioning'/'environment_receipt.json'
    if not envp.is_file():return {'schema_version':'1.0.0','status':'FAIL','classification':'NOT_CERTIFIED','runs':[],'errors':['environment certification receipt missing'],'created_at_utc':now()}
    envr=load_json(envp)
    if envr.get('classification')!='ENVIRONMENT_CERTIFIED' or envr.get('status')!='PASS':return {'schema_version':'1.0.0','status':'FAIL','classification':'NOT_CERTIFIED','runs':[],'errors':['environment is not certified'],'created_at_utc':now()}
    surface=current_certification_surface(v)
    if envr.get('certification_surface_fingerprint')!=surface:return {'schema_version':'1.0.0','status':'FAIL','classification':'NOT_CERTIFIED','runs':[],'errors':['environment certification is stale relative to current R4/C1 surface'],'created_at_utc':now()}
    n=int(runs_per_instrument or pol['shadow_profile']['runs_per_instrument']);tool=v/'RUNTIME'/'R3 Operational Execution and Learning OS'/'tools'/'alpha.py';host_json=host_command_json(v);results=[];errors=[]
    env={**os.environ,'ALPHALAB_HOST_COMMAND':host_json,'ALPHALAB_VAULT_ROOT':str(v),'PYTHONDONTWRITEBYTECODE':'1'}
    for inst in pol['shadow_instruments']:
        for rep in range(n):
            cmd=[sys.executable,str(tool),'--vault-root',str(v),'--data-root',str(dr),'run',inst,'--mode','SHADOW_LIVE','--coverage','STRICT_FULL','--depth','DEEP','--output-depth','FULL','--execution-profile','SHADOW_ONLY_V1','--host-binding','PRODUCTION_COMMAND','--decision-only']
            q=subprocess.run(cmd,capture_output=True,text=True,env=env)
            item={'instrument':inst,'replicate':rep+1,'returncode':q.returncode}
            if q.returncode:
                item['status']='FAIL';item['error']=(q.stdout+q.stderr)[-8000:];errors.append(inst+': runtime failure');results.append(item);continue
            try:
                out=_read_json_stdout(q.stdout);rid=out['run_id'];add_runtime_paths(v);from alpha_runtime.runtime import AlphaRuntime;rt=AlphaRuntime(v,dr);m=rt.store.load_manifest(rid);ret=rt.store.load_artifact_json(rid,'r3_retrieval_receipt');fp=rt.store.load_artifact_json(rid,'final_permission');
                names={a['logical_name'] for a in rt.catalog.list_artifacts(rid)}
                method_ok='method_plan' in names and 'method_predecision_validation_receipt' in names
                apl_ok='apl_a_shadow_bundle' in names or 'apl_a_forward_telemetry' in names
                from .true_forward import seal_run,verify_commitment
                fc=seal_run(v,rid,'TRUE_FORWARD');fv=verify_commitment(v,fc['commitment_id'])
                item.update({'status':'PASS','run_id':rid,'analysis_cutoff_utc':m.get('analysis_cutoff_utc'),'decision_seal_hash':m.get('decision_seal_hash'),'permission':fp.get('permission'),'decision_critical_gap_count':ret.get('decision_critical_gap_count',0),'material_gap_count':ret.get('material_gap_count',0),'retrieval_skew_seconds':ret.get('retrieval_skew_seconds'),'m1_observed':method_ok,'apl_a_shadow_observed':apl_ok,'forward_commitment_id':fc['commitment_id'],'forward_seal_valid':fv['status']=='PASS'})
                if not m.get('decision_seal_hash'):item['status']='FAIL';errors.append(inst+': decision seal missing')
                if not method_ok:item['status']='FAIL';errors.append(inst+': M1 method artifacts missing')
                if not apl_ok:item['status']='FAIL';errors.append(inst+': APL-A shadow artifact missing')
                if fv['status']!='PASS':item['status']='FAIL';errors.append(inst+': forward seal invalid')
            except Exception as e:item.update({'status':'FAIL','error':str(e)});errors.append(inst+': receipt inspection failed')
            results.append(item)
    runtime_ok=all(x.get('status')=='PASS' for x in results) and len(results)==len(pol['shadow_instruments'])*n;dc=sum(int(x.get('decision_critical_gap_count') or 0) for x in results);mat=sum(int(x.get('material_gap_count') or 0) for x in results);status='PASS' if runtime_ok else 'FAIL'
    out={'schema_version':'1.0.0','status':status,'classification':'SHADOW_PRODUCTION_CERTIFIED' if status=='PASS' else 'NOT_CERTIFIED','runs':results,'instrument_count':len(pol['shadow_instruments']),'runs_per_instrument':n,'decision_critical_gap_total':dc,'material_gap_total':mat,'source_sufficiency':'FULL' if dc==0 else 'PARTIAL_OR_INSUFFICIENT','profitability_claim':'NONE','broker_write':False,'certification_surface_fingerprint':surface,'created_at_utc':now(),'errors':errors};dump_json(dr/'commissioning'/'shadow_receipt.json',out);return out
