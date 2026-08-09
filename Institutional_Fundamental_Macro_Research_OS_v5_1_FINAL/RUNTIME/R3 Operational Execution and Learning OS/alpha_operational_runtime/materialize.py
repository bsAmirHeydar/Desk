from pathlib import Path
import json,base64
from .util import load_json,sha256_bytes,sha256_obj,uid
class MaterializeError(RuntimeError): pass
class InvocationMaterializer:
    def __init__(self,vault,rt,r2):self.vault=Path(vault);self.rt=rt;self.r2=r2
    def _artifact_payload(self,run_id,ref):
        b=self.rt.store.objects.get_bytes(ref['artifact_hash'])
        try:return {'logical_name':ref['logical_name'],'artifact_hash':ref['artifact_hash'],'media_type':ref.get('media_type') or 'application/json','json':json.loads(b.decode('utf-8'))}
        except Exception:return {'logical_name':ref['logical_name'],'artifact_hash':ref['artifact_hash'],'media_type':ref.get('media_type') or 'application/octet-stream','content_base64':base64.b64encode(b).decode()}
    def _runtime_evidence(self,run_id,pid):
        if pid not in ('W21_SNAPSHOT_AUDIT','W22_FACT_CONSTRUCTOR'):return []
        hashes=[]
        for logical in ('visibility_receipt','snapshot_manifest'):
            try:x=self.rt.store.load_artifact_json(run_id,logical)
            except Exception:continue
            if logical=='visibility_receipt':
                for r in x.get('requirements',[]):
                    for c in r.get('candidate_evaluations',[]):
                        if c.get('artifact_hash'):hashes.append((c.get('snapshot_id'),c['artifact_hash']))
            else:
                for s in x.get('snapshots',[]):
                    if s.get('artifact_hash'):hashes.append((s.get('snapshot_id'),s['artifact_hash']))
        # R3 proxy/supporting context is explicit supplemental typed evidence; it never changes the R1 visibility admission.
        try:
            rr=self.rt.store.load_artifact_json(run_id,'r3_retrieval_receipt')
            for x in rr.get('items',[]):
                if x.get('artifact_hash'):hashes.append((x.get('snapshot_id'),x['artifact_hash']))
        except Exception:pass
        out=[];seen=set()
        for sid,h in hashes:
            if h in seen:continue
            seen.add(h)
            try:b=self.rt.store.objects.get_bytes(h)
            except Exception:continue
            try:payload={'text':b.decode('utf-8')};enc='UTF8_TEXT'
            except Exception:payload={'content_base64':base64.b64encode(b).decode()};enc='BASE64'
            out.append({'snapshot_id':sid,'artifact_hash':h,'encoding':enc,'byte_length':len(b),**payload})
        return out
    def build(self,job,payload_mode='FILE_REFERENCES'):
        pid=job['process_id'];pm=self.r2.registry.manifest(pid);prompt_path=self.vault/pm['prompt_path'];prompt_bytes=prompt_path.read_bytes();ctx=job['context_bundle'];inputs=[];rows={r['logical_name']:r for r in self.rt.catalog.list_artifacts(job['run_id'])}
        for x in ctx['input_artifacts']:inputs.append(self._artifact_payload(job['run_id'],rows[x['logical_name']]))
        canon=[]
        for rel in ctx['canonical_context_paths']:
            p=(self.vault/rel).resolve()
            if self.vault not in p.parents and p!=self.vault:raise MaterializeError('context path escaped vault')
            b=p.read_bytes();item={'path':rel,'sha256':sha256_bytes(b),'byte_length':len(b)}
            if payload_mode=='INLINE':item['text']=b.decode('utf-8','replace')
            else:item['absolute_path']=str(p)
            canon.append(item)
        outschemas=[]
        for o in pm['outputs']:outschemas.append({'logical_name':o['logical_name'],'schema_ref':o['schema_ref'],'schema':load_json(self.vault/o['schema_ref'])})
        supplemental=self._runtime_evidence(job['run_id'],pid)
        inv={'schema_version':'1.0.0','operation':'MODEL_PROCESS','invocation_id':uid('INV'),'run_id':job['run_id'],'process_id':pid,'job_hash':job['job_hash'],'model_profile':job['model_profile'],'prompt':{'path':pm['prompt_path'],'sha256':job['prompt_sha256'],'text':prompt_bytes.decode('utf-8') if payload_mode=='INLINE' else None,'absolute_path':str(prompt_path) if payload_mode!='INLINE' else None},'context':{'analysis_cutoff_utc':ctx['analysis_cutoff_utc'],'prompt_pack_version':ctx['prompt_pack_version'],'bundle_hash':ctx['bundle_hash'],'input_artifacts':inputs,'canonical_context':canon,'runtime_evidence_snapshots':supplemental,'runtime_evidence_hash':sha256_obj([(x['snapshot_id'],x['artifact_hash']) for x in supplemental]),'forbidden_context_check':ctx['forbidden_context_check']},'output_contract':{'process_version':job['process_version'],'expected_outputs':job['expected_outputs'],'schemas':outschemas,'envelope_schema':load_json(self.vault/'RUNTIME'/'R2 Prompt Execution OS'/'schemas'/'AlphaLab_R2_Process_Output_Envelope.schema.json')},'host_hints':{'stateless':True,'no_free_conversation_memory':True,'strict_point_in_time':True,'proxy_never_promoted_to_fact':True}}
        inv['invocation_hash']=sha256_obj({k:v for k,v in inv.items() if k not in ('invocation_id','invocation_hash')});return inv
