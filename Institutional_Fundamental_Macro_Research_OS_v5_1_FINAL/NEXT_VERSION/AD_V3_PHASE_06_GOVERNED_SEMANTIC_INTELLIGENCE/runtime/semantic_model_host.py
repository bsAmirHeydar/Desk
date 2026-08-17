from __future__ import annotations
from pathlib import Path
import json, os, sys, uuid, time
from .common import load_json, sha256_obj, sha256_file

class SemanticHostError(RuntimeError): pass

def _vault(repo_root): return Path(repo_root)/'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL'
def _phase(repo_root): return _vault(repo_root)/'NEXT_VERSION'/'AD_V3_PHASE_06_GOVERNED_SEMANTIC_INTELLIGENCE'

def _binding_info(repo_root):
    v=_vault(repo_root); cfg=load_json(v/'RUNTIME/R3 Operational Execution and Learning OS/config/host_policy.json'); b=cfg['bindings']['PRODUCTION_COMMAND']; return v,b

def _model_name(vault,profile='GOVERNANCE'):
    p=vault/'RUNTIME/Production Commissioning/config/model_bindings.json'
    if not p.exists(): return None
    c=load_json(p); return (c.get('profiles',{}).get(profile) or {}).get('model') or c.get('default_model')

def host_status(repo_root):
    v,b=_binding_info(repo_root); env_name=b.get('command_env','ALPHALAB_HOST_COMMAND'); direct=bool(os.environ.get(env_name)); local=v/'RUNTIME/Production Commissioning/tools/openai_host.py'; key=bool(os.environ.get('OPENAI_API_KEY')); configured=direct or (key and local.exists())
    return {'configured':configured,'binding':'PRODUCTION_COMMAND','adapter':b.get('adapter'),'command_env':env_name,'command_env_set':direct,'auto_local_commissioned_host':bool((not direct) and key and local.exists()),'openai_key_present':key,'model_profile':'GOVERNANCE','model':_model_name(v,'GOVERNANCE'),'outside_evidence_authority':False,'web_search_authority':False}

def _ensure_host_env(vault,binding):
    env_name=binding.get('command_env','ALPHALAB_HOST_COMMAND'); old_cmd=os.environ.get(env_name); old_vault=os.environ.get('ALPHALAB_VAULT_ROOT'); changed=False
    if not old_cmd:
        local=vault/'RUNTIME/Production Commissioning/tools/openai_host.py'
        if os.environ.get('OPENAI_API_KEY') and local.exists():
            os.environ[env_name]=json.dumps([sys.executable,str(local)],ensure_ascii=False); changed=True
        else: raise SemanticHostError('MODEL_HOST_UNAVAILABLE')
    os.environ['ALPHALAB_VAULT_ROOT']=str(vault)
    return env_name,old_cmd,old_vault,changed

def _restore_env(env_name,old_cmd,old_vault,changed):
    if changed:
        if old_cmd is None: os.environ.pop(env_name,None)
        else: os.environ[env_name]=old_cmd
    if old_vault is None: os.environ.pop('ALPHALAB_VAULT_ROOT',None)
    else: os.environ['ALPHALAB_VAULT_ROOT']=old_vault

def invoke(repo_root,request_packet):
    repo_root=Path(repo_root); phase=_phase(repo_root); vault,binding=_binding_info(repo_root)
    st=host_status(repo_root)
    if not st['configured']: raise SemanticHostError('MODEL_HOST_UNAVAILABLE')
    r3=vault/'RUNTIME/R3 Operational Execution and Learning OS'
    if str(r3) not in sys.path: sys.path.insert(0,str(r3))
    from alpha_operational_runtime.host import make_host
    prompt_path=phase/'prompts/governed_semantic_system.md'; schema_path=phase/'schemas/semantic_model_response.schema.json'; prompt=prompt_path.read_text(encoding='utf-8'); schema=load_json(schema_path)
    inv={'schema_version':'1.0.0','operation':'MODEL_PROCESS','invocation_id':'P06INV_'+uuid.uuid4().hex[:16].upper(),'run_id':request_packet.get('source_semantic_packet_id') or request_packet.get('packet_id'),'process_id':'AD_V3_P06_GOVERNED_SEMANTIC_ADJUDICATION','job_hash':sha256_obj({'request_packet':request_packet,'prompt_sha256':sha256_file(prompt_path)}),'model_profile':'GOVERNANCE',
      'prompt':{'path':str(prompt_path.relative_to(vault)),'absolute_path':str(prompt_path),'sha256':'sha256:'+sha256_file(prompt_path),'text':prompt},
      'context':{'analysis_cutoff_utc':None,'prompt_pack_version':'P06_SEMANTIC_PROMPT_1.0.0','bundle_hash':'sha256:'+sha256_obj(request_packet),'input_artifacts':[{'logical_name':'semantic_request_packet','json':request_packet}],'canonical_context':[],'runtime_evidence_snapshots':[],'forbidden_context_check':{'status':'PASS','free_conversation_memory':False,'outside_evidence':False,'web_search':False}},
      'output_contract':{'process_version':'1.0.0','expected_outputs':[{'logical_name':'semantic_model_response','schema_ref':str(schema_path)}],'schemas':[{'logical_name':'semantic_model_response','schema_ref':str(schema_path),'schema':schema}]},
      'host_hints':{'stateless':True,'no_free_conversation_memory':True,'strict_point_in_time':True,'no_web_search':True,'outside_evidence_forbidden':True}}
    inv['invocation_hash']='sha256:'+sha256_obj({k:v for k,v in inv.items() if k not in {'invocation_id','invocation_hash'}})
    env_name=old_cmd=old_vault=None; changed=False
    t0=time.monotonic()
    try:
        env_name,old_cmd,old_vault,changed=_ensure_host_env(vault,binding)
        host=make_host(binding,phase/'artifacts'/'host_runtime',production=True)
        out,rec=host.invoke(inv,1)
    except Exception as e:
        raise SemanticHostError(str(e)) from e
    finally:
        if env_name: _restore_env(env_name,old_cmd,old_vault,changed)
    if out.get('status')!='OK': raise SemanticHostError('MODEL_PROCESS_FAILED:'+str(out.get('error') or out.get('status')))
    env=out.get('process_output') or {}
    if env.get('status')!='PRESENT': raise SemanticHostError('MODEL_PROCESS_NOT_PRESENT:'+str(env.get('status')))
    val=(env.get('artifacts') or {}).get('semantic_model_response')
    if not isinstance(val,dict): raise SemanticHostError('SEMANTIC_MODEL_RESPONSE_MISSING')
    meta={'provider':rec.get('provider'),'model':rec.get('model'),'model_version':rec.get('model_version'),'request_id':rec.get('request_id'),'latency_ms':rec.get('latency_ms'),'input_tokens':rec.get('input_tokens'),'output_tokens':rec.get('output_tokens'),'model_profile':'GOVERNANCE','host_adapter':rec.get('adapter'),'model_latency_ms':round((time.monotonic()-t0)*1000,3)}
    return val,meta,rec
