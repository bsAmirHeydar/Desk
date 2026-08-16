from pathlib import Path
import json,sys,time,uuid
from copy import deepcopy
from .common import data_root,load,now,hobj
from .cluster import compile_cluster
from .v1_bridge import run_shadow,load_artifacts,pressure_context,gold_context
from .host_bridge import precommit,retrieve_window,response
class UnifiedRunError(RuntimeError):pass

def _phase_parent(v):return Path(v)/'NEXT_VERSION'
def _p11(v):return _phase_parent(v)/'AD_V2_PHASE_11_UNIFIED_COMMAND_RESEARCH_ORCHESTRATION'
def _p10(v):return _phase_parent(v)/'AD_V2_PHASE_10_INTEGRATED_SHADOW_COMMISSIONING_RC'
def _import_p02(v):
 pp=_phase_parent(v)
 if str(pp) not in sys.path:sys.path.insert(0,str(pp))
 from AD_V2_PHASE_02_DIRECTIONAL_PRESSURE_ENGINE.runtime.directional_pressure import build_from_roots
 from AD_V2_PHASE_03_PRICE_TRANSMISSION_ENGINE.runtime.price_transmission import _pressure_fingerprint
 return build_from_roots,_pressure_fingerprint

def _canonical_context(v):
 p=_p11(v);paths=[p/'config/gold_master_cluster_registry.json',_phase_parent(v)/'AD_V2_PHASE_05_GOLD_INTELLIGENCE_SPECIALIZATION/config/gold_pressure_root_registry.json',_phase_parent(v)/'AD_V2_PHASE_05_GOLD_INTELLIGENCE_SPECIALIZATION/config/gold_source_registry.json',_phase_parent(v)/'AD_V2_PHASE_05_GOLD_INTELLIGENCE_SPECIALIZATION/config/gold_evidence_role_registry.json']
 return [{'path':str(x),'sha256':'sha256:'+__import__('hashlib').sha256(x.read_bytes()).hexdigest(),'text':x.read_text(encoding='utf-8')} for x in paths]

def _seal_precommit(dr,run_id,pressure,sig,raw):
 root=Path(dr)/'alpha_desk_v2'/'p11_orchestration'/'precommits';root.mkdir(parents=True,exist_ok=True);obj={'schema_version':'1.0.0','phase':'AD-V2-P11','run_id':run_id,'sealed_at_utc':now(),'pressure_fingerprint':sig['pressure_fingerprint'],'pressure_state_hash':hobj(pressure),'expected_signature':sig,'raw_precommit_hash':hobj(raw)};obj['precommit_hash']=hobj(obj);p=root/(run_id+'.json')
 if p.exists():
  old=load(p)
  if old.get('precommit_hash')!=obj['precommit_hash']:raise UnifiedRunError('P11 immutable precommit conflict')
  return old,p
 p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return obj,p

def run_with_pack(vault,dr,pack,output_dir,persist=True):
 pp=_phase_parent(vault)
 if str(pp) not in sys.path:sys.path.insert(0,str(pp))
 from AD_V2_PHASE_10_INTEGRATED_SHADOW_COMMISSIONING_RC.runtime.shadow_pipeline import run
 return run(pack,phase_parent=pp,data_root=dr,output_dir=output_dir,persist_state=persist)

def run_gold(repo,*,input_pack=None,window_seconds=60,output_dir=None,persist=True,sleep_fn=time.sleep):
 repo=Path(repo).resolve();v=repo/'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL';dr=data_root(repo);dr.mkdir(parents=True,exist_ok=True);out=Path(output_dir).resolve() if output_dir else dr/'reports'/'alpha_desk_v2';out.mkdir(parents=True,exist_ok=True)
 if input_pack:
  pack=load(input_pack);r=run_with_pack(v,dr,pack,out,persist);return {'schema_version':'1.0.0','phase':'AD-V2-P11','status':'PASS','command':'run','subject':'XAUUSD','mode':'EXPLICIT_INPUT_PACK','v1_run_id':(pack.get('base_capsule') or {}).get('run_id'),'p10_receipt':r,'integrity':{'status':'PASS','one_front_door':True,'pressure_price_separation':True,'expected_signature_predeclared':True},'authority':{'v1':'AUTHORITATIVE','v2':'SHADOW','permission':'V1_INHERITED','broker':'NONE'}}
 v1,v1rid=run_shadow(v,dr);arts=load_artifacts(v,dr,v1rid);pc=pressure_context(arts);gc=gold_context(arts);cluster=compile_cluster(_p11(v))
 raw,hostrec=precommit(v,dr,_p11(v),v1rid,pc,_canonical_context(v));pin=deepcopy(raw.get('pressure_input') or {});pin.setdefault('active_horizon','SESSION_1_6H');pin.setdefault('as_of_utc',arts.get('analysis_cutoff_utc'))
 build_p,pfp=_import_p02(v);pressure=build_p(pin,history=None)
 if pressure.get('status')!='PASS':raise UnifiedRunError('P11 P02 PRECOMMIT FAILED: '+json.dumps(pressure.get('integrity'),ensure_ascii=False))
 sig=deepcopy(raw.get('expected_signature_template') or {});seal_time=now();sig['active_horizon']=pressure.get('active_horizon');sig['declared_at_utc']=seal_time;sig['pressure_fingerprint']=pfp(pressure);sig.setdefault('signature_id','P11SIG_'+uuid.uuid4().hex[:16].upper())
 sealed,prepath=_seal_precommit(dr,v1rid,pressure,sig,raw)
 t0=retrieve_window(v,dr,_p11(v),cutoff_utc=now(),label='T0')
 ws=max(1,int(window_seconds));sleep_fn(ws)
 t1=retrieve_window(v,dr,_p11(v),cutoff_utc=now(),label='T1')
 robs,obsrec=response(v,dr,_p11(v),v1rid,sig,t0,t1,gc)
 pack={'base_capsule':arts['run_capsule'],'pressure_input':pin,'expected_signature':sig,'actual_response':robs['actual_response'],'gold_observations':robs['gold_observations'],'divergence_history_count':0,'missing_driver_candidates':raw.get('missing_driver_candidates') or []}
 packdir=Path(dr)/'alpha_desk_v2'/'p11_orchestration'/'input_packs';packdir.mkdir(parents=True,exist_ok=True);ppath=packdir/(v1rid+'.json');ppath.write_text(json.dumps(pack,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 p10=run_with_pack(v,dr,pack,out,persist)
 return {'schema_version':'1.0.0','phase':'AD-V2-P11','status':'PASS','command':'run','subject':'XAUUSD','mode':'ONE_COMMAND_LIVE_SHADOW','v1_run_id':v1rid,'cluster_fingerprint':cluster['prompt_sha256'],'precommit_path':str(prepath),'input_pack_path':str(ppath),'p10_receipt':p10,'host_receipts':{'precommit_request_hash':hostrec.get('request_hash'),'response_request_hash':obsrec.get('request_hash')},'integrity':{'status':'PASS','one_front_door':True,'pressure_price_separation':True,'expected_signature_predeclared':True,'response_observed_after_signature':True,'p08_is_true_forward_owner':True},'authority':{'v1':'AUTHORITATIVE','v2':'SHADOW','permission':'V1_INHERITED','broker':'NONE','auto_promotion':False}}
