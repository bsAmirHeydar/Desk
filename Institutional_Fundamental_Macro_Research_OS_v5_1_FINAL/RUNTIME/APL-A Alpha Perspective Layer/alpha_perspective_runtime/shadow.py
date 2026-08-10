from pathlib import Path
import json,time,base64
from .util import load_json,chash,shaobj,uid,now,add_paths
from .registry import APLRegistry
class APLShadowError(RuntimeError):pass
CORE_ALLOWED={'decision_evidence_pack','evidence_integrity_receipt','market_state_reconciliation','hypothesis_set','causal_graph','root_channel_map','scenario_tree','d2_shadow_pack','run_request','scope_state','visibility_receipt','retrieval_plan'}
CORE_FORBIDDEN={'final_permission','d3_edge','utility_state','d4_governance','thesis_destroyer','model_disagreement','premortem','global_reconciliation','outcome','future_price_path','realized_r','counterfactual_outcome'}
def _artifact(rt,run_id,name):
 rows=[r for r in rt.catalog.list_artifacts(run_id) if r['logical_name']==name]
 if not rows:raise APLShadowError('missing required APL input '+name)
 r=rows[0];b=rt.store.objects.get_bytes(r['artifact_hash'])
 try:j=json.loads(b.decode('utf-8'));return {'logical_name':name,'artifact_hash':r['artifact_hash'],'media_type':r.get('media_type') or 'application/json','json':j}
 except:return {'logical_name':name,'artifact_hash':r['artifact_hash'],'media_type':'application/octet-stream','content_base64':base64.b64encode(b).decode()}
def _build(vault,rt,reg,run_id,pid,memory):
 m=reg.manifest(pid);inputs=[]
 for name in m['required_inputs']:
  if name in memory:inputs.append(memory[name]);continue
  if name not in CORE_ALLOWED:raise APLShadowError('non-authorized core input '+name)
  inputs.append(_artifact(rt,run_id,name))
 for i in inputs:
  if i['logical_name'] in CORE_FORBIDDEN:raise APLShadowError('forbidden input leaked '+i['logical_name'])
 canon=[]
 for rel in m['canonical_dependencies']:
  p=(Path(vault)/rel).resolve()
  if Path(vault).resolve() not in p.parents:raise APLShadowError('canon path escape')
  canon.append({'path':rel,'sha256':chash(p),'absolute_path':str(p),'byte_length':p.stat().st_size})
 outs=[]
 for o in m['outputs']:outs.append({'logical_name':o['logical_name'],'schema_ref':o['schema_ref'],'schema':load_json(Path(vault)/o['schema_ref'])})
 prompt=Path(vault)/m['prompt_path']; pb=prompt.read_bytes();runm=rt.store.load_manifest(run_id)
 inv={'schema_version':'1.0.0','operation':'MODEL_PROCESS','invocation_id':uid('APL_INV'),'run_id':run_id,'process_id':pid,'job_hash':shaobj([run_id,pid,chash(prompt),[(x['logical_name'],x['artifact_hash']) for x in inputs]]),'model_profile':m['model_profile'],'prompt':{'path':m['prompt_path'],'sha256':chash(prompt),'absolute_path':str(prompt),'text':None},'context':{'analysis_cutoff_utc':runm['analysis_cutoff_utc'],'prompt_pack_version':reg.pack['version'],'bundle_hash':shaobj([(x['logical_name'],x['artifact_hash']) for x in inputs]),'input_artifacts':inputs,'canonical_context':canon,'runtime_evidence_snapshots':[],'runtime_evidence_hash':shaobj([]),'forbidden_context_check':'APL_A_PREDECISION_FROZEN_CONTEXT_ONLY'},'output_contract':{'process_version':m['version'],'expected_outputs':[o['logical_name'] for o in m['outputs']],'schemas':outs,'envelope_schema':{}},'host_hints':{'stateless':True,'no_web':True,'shadow_only':True,'no_free_conversation_memory':True,'strict_point_in_time':True}}
 inv['invocation_hash']=shaobj({k:v for k,v in inv.items() if k not in ('invocation_id','invocation_hash')});return inv
def run_shadow(vault,rt,host_factory,run_id,production=True,fixture_host=None):
 add_paths(vault)
 existing={r['logical_name']:r for r in rt.catalog.list_artifacts(run_id,'LEARNING')}
 if 'apl_a_shadow_bundle' in existing and 'apl_a_forward_telemetry' in existing:
  return {'status':'PASS','mode':'ALREADY_COMPLETE','decision_world_unchanged':True,'bundle_artifact_hash':existing['apl_a_shadow_bundle']['artifact_hash'],'telemetry':rt.store.load_artifact_json(run_id,'apl_a_forward_telemetry')}
 reg=APLRegistry(vault);errs=reg.validate()
 if errs:raise APLShadowError('; '.join(errs))
 m=rt.store.load_manifest(run_id)
 if not m.get('decision_seal_hash'):raise APLShadowError('APL-A shadow requires decision seal')
 before={r['logical_name']:r['artifact_hash'] for r in rt.catalog.list_artifacts(run_id,'DECISION')}
 memory={};t0=time.monotonic();findings=[]
 host=fixture_host if fixture_host is not None else host_factory(production)
 for pid in reg.ids():
  inv=_build(vault,rt,reg,run_id,pid,memory);out,receipt=host.invoke(inv,1)
  if out.get('status')!='OK':raise APLShadowError(pid+' host failure '+str(out.get('error')))
  env=out.get('process_output') or {};arts=env.get('artifacts') or {};pm=reg.manifest(pid)
  expected={x['logical_name']:x for x in pm['outputs']}
  if set(arts)!=set(expected):raise APLShadowError(pid+' output set mismatch')
  from alpha_prompt_runtime.validation import validate_json_schema
  for name,payload in arts.items():
   validate_json_schema(vault,expected[name]['schema_ref'],payload)
   ref=rt.store.put_artifact(run_id,name,'LEARNING','LEARNING',payload,'application/json',producer_process_id=pid,producer_version='1.0.0')
   memory[name]={'logical_name':name,'artifact_hash':ref['artifact_hash'],'media_type':'application/json','json':payload};findings.append(name)
  rt.store.put_artifact(run_id,'apl_a_host_receipt_'+pid.lower(),'LEARNING','LEARNING',receipt,'application/json',producer_process_id='APL_A_HOST',producer_version='1.0.0')
 after={r['logical_name']:r['artifact_hash'] for r in rt.catalog.list_artifacts(run_id,'DECISION')}
 if before!=after:raise APLShadowError('DATA_PARITY_FAILURE decision world changed')
 bundle={'schema_version':'1.0.0','run_id':run_id,'mode':'SHADOW_ONLY','decision_seal_hash':m['decision_seal_hash'],'artifacts':{k:v['artifact_hash'] for k,v in memory.items()},'authority':{'direction':'NONE','permission':'NONE','fact':'NONE','broker_write':'NONE'}}
 bref=rt.store.put_artifact(run_id,'apl_a_shadow_bundle','LEARNING','LEARNING',bundle,'application/json',producer_process_id='APL_A',producer_version='1.0.0')
 active=[]
 try:
  x=memory['apl_lens_activation_receipt']['json'];active=[z.get('lens_id') for z in x.get('lenses',[]) if z.get('state') in ('ACTIVE','CONDITIONAL','CONTESTED')]
 except:pass
 research=[]
 try:research=memory['apl_research_requests']['json'].get('requests',[])
 except:pass
 telemetry={'schema_version':'1.0.0','run_id':run_id,'active_lenses':active,'material_findings':findings,'would_request':['DEEPEN_RESEARCH' if research else 'NO_CHANGE'],'complexity':{'processes_executed':len(reg.ids()),'latency_ms':round((time.monotonic()-t0)*1000,3)},'authority':{'production_permission_mutation':False,'direction_mutation':False}}
 rt.store.put_artifact(run_id,'apl_a_forward_telemetry','LEARNING','LEARNING',telemetry,'application/json',producer_process_id='APL_A',producer_version='1.0.0')
 for req in research:
  rt.lifecycle.event(run_id,'APL_RESEARCH_REQUEST_PENDING',{'request_id':req.get('request_id'),'route':'P11_EVIDENCE_PLAN_NEXT_GOVERNED_RUN','direct_retrieval':False})
 rt.lifecycle.event(run_id,'APL_A_SHADOW_COMPLETE',{'process_count':len(reg.ids()),'decision_world_unchanged':True,'bundle_hash':bref['artifact_hash']})
 return {'status':'PASS','decision_world_unchanged':True,'bundle_artifact_hash':bref['artifact_hash'],'telemetry':telemetry}
