from pathlib import Path
import json,sys,uuid,copy
from .common import now,hobj,load
class HostBridgeError(RuntimeError):pass

def _paths(vault):
 for p in [vault/'RUNTIME'/'R3 Operational Execution and Learning OS']:
  if str(p) not in sys.path:sys.path.insert(0,str(p))

def _host(vault,data_root):
 _paths(vault)
 from alpha_operational_runtime.host import make_host
 hp=load(vault/'RUNTIME/R3 Operational Execution and Learning OS/config/host_policy.json');b=hp['bindings']['PRODUCTION_COMMAND']
 caps=set((b.get('required_capabilities') or [])+(b.get('optional_capabilities') or []))
 if 'MODEL_PROCESS' not in caps:raise HostBridgeError('MODEL_PROCESS host capability required')
 return make_host(b,data_root,production=True),caps,b

def _invoke_artifact(vault,data_root,*,run_id,process_id,prompt_path,artifact_name,schema_path,context):
 host,caps,b=_host(vault,data_root);prompt_path=Path(prompt_path);schema=load(schema_path);prompt=prompt_path.read_text(encoding='utf-8')
 inv={'schema_version':'1.0.0','operation':'MODEL_PROCESS','invocation_id':'P11INV_'+uuid.uuid4().hex[:16].upper(),'run_id':run_id,'process_id':process_id,'job_hash':hobj({'run_id':run_id,'process_id':process_id,'context':context,'prompt':prompt}),'model_profile':'REASONING_MAX','prompt':{'path':str(prompt_path),'sha256':'sha256:'+__import__('hashlib').sha256(prompt.encode()).hexdigest(),'text':prompt,'absolute_path':None},'context':{'analysis_cutoff_utc':context.get('analysis_cutoff_utc'),'prompt_pack_version':'AD_V2_P11_GOLD_MASTER_CLUSTER_1.0.0','bundle_hash':'sha256:'+hobj(context),'input_artifacts':context.get('input_artifacts') or [],'canonical_context':context.get('canonical_context') or [],'runtime_evidence_snapshots':context.get('runtime_evidence_snapshots') or [],'runtime_evidence_hash':'sha256:'+hobj(context.get('runtime_evidence_snapshots') or []),'forbidden_context_check':{'status':'PASS','free_conversation_memory':False}},'output_contract':{'process_version':'1.0.0','expected_outputs':[{'logical_name':artifact_name,'schema_ref':str(schema_path)}],'schemas':[{'logical_name':artifact_name,'schema_ref':str(schema_path),'schema':schema}],'envelope_schema':load(vault/'RUNTIME/R2 Prompt Execution OS/schemas/AlphaLab_R2_Process_Output_Envelope.schema.json')},'host_hints':{'stateless':True,'no_free_conversation_memory':True,'strict_point_in_time':True,'proxy_never_promoted_to_fact':True}}
 inv['invocation_hash']='sha256:'+hobj({k:v for k,v in inv.items() if k not in {'invocation_id','invocation_hash'}})
 out,rec=host.invoke(inv,1)
 if out.get('status')!='OK':raise HostBridgeError('host model process failed: '+str(out.get('error') or out.get('status')))
 env=out.get('process_output')
 if not isinstance(env,dict) or env.get('status')!='PRESENT':raise HostBridgeError('host missing PRESENT process_output')
 arts=env.get('artifacts') or {};val=arts.get(artifact_name)
 if not isinstance(val,dict):raise HostBridgeError('host missing '+artifact_name)
 return val,rec

def precommit(vault,data_root,phase_root,run_id,artifacts,canonical_context):
 ctx={'analysis_cutoff_utc':artifacts.get('analysis_cutoff_utc'),'input_artifacts':[{'logical_name':k,'json':v} for k,v in artifacts.items() if k!='analysis_cutoff_utc'],'canonical_context':canonical_context,'runtime_evidence_snapshots':[]}
 return _invoke_artifact(vault,data_root,run_id=run_id,process_id='V2_GOLD_MASTER_PRECOMMIT',prompt_path=Path(phase_root)/'prompts/gold_precommit_master.md',artifact_name='v2_precommit',schema_path=Path(phase_root)/'schemas/AlphaDesk_V2_P11_GoldPrecommit.schema.json',context=ctx)

def retrieve_window(vault,data_root,phase_root,*,cutoff_utc,label):
 host,caps,b=_host(vault,data_root)
 if 'EVIDENCE_RETRIEVAL' not in caps:raise HostBridgeError('EVIDENCE_RETRIEVAL capability required for automatic live one-command run')
 cfg=load(Path(phase_root)/'config/live_observation_requirements.json');sn=[]
 for req in cfg['requirements']:
  rq={'schema_version':'1.0.0','operation':'EVIDENCE_RETRIEVAL','analysis_cutoff_utc':cutoff_utc,'capture_mode':'P11_POST_SIGNATURE_RESPONSE','run_mode':'SHADOW_LIVE','instrument':'XAUUSD','requirements':[req],'source_contracts':[{'source_id':x,'role':'P11_LIVE_OBSERVATION'} for x in req.get('source_ids',[])],'strict_point_in_time':True,'p11_window_label':label}
  rows=host.retrieve(rq) or []
  for x in rows:
   y=copy.deepcopy(x);y['p11_requirement_id']=req['requirement_id'];y['p11_window_label']=label;sn.append(y)
 return sn

def response(vault,data_root,phase_root,run_id,sealed_signature,t0,t1,gold_context):
 ctx={'analysis_cutoff_utc':sealed_signature.get('declared_at_utc'),'input_artifacts':[{'logical_name':'sealed_expected_signature','json':sealed_signature},{'logical_name':'gold_context','json':gold_context}],'canonical_context':[],'runtime_evidence_snapshots':[{'window':'T0','snapshots':t0},{'window':'T1','snapshots':t1}]}
 return _invoke_artifact(vault,data_root,run_id=run_id,process_id='V2_GOLD_RESPONSE_OBSERVATION',prompt_path=Path(phase_root)/'prompts/gold_response_observation.md',artifact_name='v2_response_observation',schema_path=Path(phase_root)/'schemas/AlphaDesk_V2_P11_GoldResponseObservation.schema.json',context=ctx)
