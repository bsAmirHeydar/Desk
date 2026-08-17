from __future__ import annotations
from pathlib import Path
import time, json
from .common import load_json, write_json, sha256_obj, sha256_file, stable_id, iso
from .semantic_request_compiler import compile_request_packet
from .semantic_bundle import conservative_response, model_response_from_bundle
from .semantic_validator import validate_response
from .semantic_model_host import invoke as invoke_host, host_status, SemanticHostError

def _phase(repo_root): return Path(repo_root)/'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL'/'NEXT_VERSION'/'AD_V3_PHASE_06_GOVERNED_SEMANTIC_INTELLIGENCE'
def _p03(repo_root): return Path(repo_root)/'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL'/'NEXT_VERSION'/'AD_V3_PHASE_03_CAUSAL_GOLD_BRAIN_DECISION_ENGINE'

def fingerprints(repo_root,packet,request_packet):
    phase=_phase(repo_root); cfg=load_json(phase/'config/semantic_model_config.json')
    return {'evidence_packet_sha256':sha256_obj(packet),'request_packet_sha256':sha256_obj(request_packet),'prompt_sha256':sha256_file(phase/'prompts/governed_semantic_system.md'),'model_config_sha256':sha256_obj(cfg),'schema_sha256':sha256_file(phase/'schemas/semantic_model_response.schema.json'),'schema_version':'1.0.0'}

def cache_key(fp): return sha256_obj(fp)

def _cache_path(phase,fp): return phase/'artifacts'/'cache'/(cache_key(fp)+'.json')

def _write_artifacts(artifact_dir,request_packet,raw,receipt,bundle,capsule):
    if not artifact_dir: return
    d=Path(artifact_dir); d.mkdir(parents=True,exist_ok=True)
    write_json(d/'semantic_request_packet.json',request_packet)
    if raw is not None: write_json(d/'semantic_raw_response.json',raw)
    write_json(d/'semantic_validation_receipt.json',receipt); write_json(d/'semantic_validated_bundle.json',bundle); write_json(d/'semantic_run_capsule.json',capsule)

def run_semantics(repo_root,packet,external_bundle_path=None,mode=None,artifact_dir=None,model_host=None,use_cache=True):
    phase=_phase(repo_root); t0=time.monotonic(); tc=time.monotonic(); request_packet=compile_request_packet(packet,_p03(repo_root)); compile_ms=round((time.monotonic()-tc)*1000,3); fp=fingerprints(repo_root,packet,request_packet); requested_mode=mode or load_json(phase/'config/semantic_runtime_contract.json').get('default_mode','AUTO_GOVERNED_IF_HOST_AVAILABLE')
    raw=None; model_meta={}; host_rec=None; fallback_reason=None; actual_mode=None
    if external_bundle_path:
        actual_mode='EXTERNAL_VALIDATED_BUNDLE'
        ext=load_json(external_bundle_path)
        raw=model_response_from_bundle(ext) if ext.get('record_type')=='AD_V3_P03_SEMANTIC_ADJUDICATION_BUNDLE' else ext
    elif requested_mode=='CONSERVATIVE_EVIDENCE_ONLY':
        actual_mode='CONSERVATIVE_EVIDENCE_ONLY'; fallback_reason='CONSERVATIVE_MODE_REQUESTED'; raw=conservative_response(request_packet,'INSUFFICIENT_EVIDENCE')
    else:
        cp=_cache_path(phase,fp)
        if use_cache and cp.exists():
            cached=load_json(cp)
            if cached.get('fingerprints')==fp and isinstance(cached.get('bundle'),dict):
                actual_mode='REPLAY_VALIDATED_BUNDLE'; bundle=cached['bundle']; receipt=cached['validation_receipt']; raw=cached.get('raw_response'); model_meta=cached.get('model_meta') or {}; receipt=dict(receipt); receipt['mode']='REPLAY_VALIDATED_BUNDLE'; bundle=dict(bundle); bundle['adjudication_mode']='REPLAY_VALIDATED_BUNDLE'; bundle.setdefault('p06_semantic',{})['replay_cache_hit']=True
                capsule={'record_type':'AD_V3_P06_SEMANTIC_RUN_CAPSULE','capsule_id':stable_id('P06CAP',{'fp':fp,'mode':actual_mode}),'generated_at_utc':iso(),'mode':actual_mode,'fingerprints':fp,'request_packet_id':request_packet['packet_id'],'validation_receipt_id':receipt.get('receipt_id'),'bundle_sha256':sha256_obj(bundle),'timing_ms':{'request_compilation':compile_ms,'model_latency':0.0,'validation':0.0,'total':round((time.monotonic()-t0)*1000,3)},'model_meta':model_meta}
                bundle['p06_semantic'].update({'fingerprints':fp,'capsule_id':capsule['capsule_id'],'prompt_version':'P06_SEMANTIC_PROMPT_1.0.0','prompt_sha256':fp['prompt_sha256'],'model_host_state':'REPLAY'})
                _write_artifacts(artifact_dir,request_packet,raw,receipt,bundle,capsule); return {'bundle':bundle,'validation_receipt':receipt,'request_packet':request_packet,'raw_response':raw,'capsule':capsule}
        st=host_status(repo_root)
        if model_host is not None:
            actual_mode='AUTO_GOVERNED'; tm=time.monotonic(); raw,model_meta=model_host(request_packet); model_meta=dict(model_meta or {}); model_meta.setdefault('model_latency_ms',round((time.monotonic()-tm)*1000,3))
        elif st.get('configured'):
            actual_mode='AUTO_GOVERNED'; tm=time.monotonic()
            try: raw,model_meta,host_rec=invoke_host(repo_root,request_packet)
            except SemanticHostError as e:
                actual_mode='CONSERVATIVE_EVIDENCE_ONLY'; fallback_reason='MODEL_HOST_ERROR:'+str(e); raw=conservative_response(request_packet,'INSUFFICIENT_EVIDENCE'); model_meta={'host_state':'DEGRADED','error':str(e),'model':st.get('model')}
        else:
            actual_mode='CONSERVATIVE_EVIDENCE_ONLY'; fallback_reason='MODEL_HOST_UNAVAILABLE'; raw=conservative_response(request_packet,'INSUFFICIENT_EVIDENCE'); model_meta={'host_state':'UNAVAILABLE','model':st.get('model')}
    tv=time.monotonic(); bundle,receipt=validate_response(request_packet,raw,phase,actual_mode,model_meta,fallback_reason)
    if actual_mode=='AUTO_GOVERNED' and receipt.get('request_count',0)>0 and receipt.get('rejected_count')==receipt.get('request_count'):
        # A wholly invalid model response receives no semantic authority. Preserve the raw
        # response for audit, but feed P03 a fresh conservative bundle and label the mode honestly.
        actual_mode='CONSERVATIVE_EVIDENCE_ONLY'; fallback_reason='MODEL_RESPONSE_INVALID'; conservative=conservative_response(request_packet,'INSUFFICIENT_EVIDENCE')
        bundle,receipt=validate_response(request_packet,conservative,phase,actual_mode,model_meta,fallback_reason)
        bundle.setdefault('p06_semantic',{})['invalid_model_response_preserved_for_audit']=True
    validation_ms=round((time.monotonic()-tv)*1000,3)
    total_ms=round((time.monotonic()-t0)*1000,3); model_ms=float((model_meta or {}).get('model_latency_ms') or (model_meta or {}).get('latency_ms') or 0.0)
    capsule={'record_type':'AD_V3_P06_SEMANTIC_RUN_CAPSULE','capsule_id':stable_id('P06CAP',{'fp':fp,'mode':actual_mode,'bundle':sha256_obj(bundle)}),'generated_at_utc':iso(),'mode':actual_mode,'fingerprints':fp,'request_packet_id':request_packet['packet_id'],'validation_receipt_id':receipt.get('receipt_id'),'raw_response_sha256':sha256_obj(raw),'bundle_sha256':sha256_obj(bundle),'timing_ms':{'request_compilation':compile_ms,'model_latency':model_ms,'validation':validation_ms,'total':total_ms},'model_meta':model_meta}
    bundle.setdefault('p06_semantic',{}).update({'fingerprints':fp,'capsule_id':capsule['capsule_id'],'prompt_version':'P06_SEMANTIC_PROMPT_1.0.0','prompt_sha256':fp['prompt_sha256'],'model_host_state':('AVAILABLE' if actual_mode=='AUTO_GOVERNED' else 'CONSERVATIVE' if actual_mode=='CONSERVATIVE_EVIDENCE_ONLY' else actual_mode),'timing_ms':capsule['timing_ms']})
    if actual_mode=='AUTO_GOVERNED' and receipt.get('status') in ('PASS','DEGRADED') and use_cache:
        cp=_cache_path(phase,fp); cp.parent.mkdir(parents=True,exist_ok=True); write_json(cp,{'fingerprints':fp,'bundle':bundle,'validation_receipt':receipt,'raw_response':raw,'model_meta':model_meta})
    _write_artifacts(artifact_dir,request_packet,raw,receipt,bundle,capsule)
    return {'bundle':bundle,'validation_receipt':receipt,'request_packet':request_packet,'raw_response':raw,'capsule':capsule,'host_receipt':host_rec}
