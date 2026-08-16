from pathlib import Path
import sys,json
from .common import load
class V1BridgeError(RuntimeError):pass

def _paths(v):
 for p in [v/'RUNTIME/Unified Research Interface',v/'RUNTIME/R1 Foundation']:
  if str(p) not in sys.path:sys.path.insert(0,str(p))

def run_shadow(vault,data_root):
 v=Path(vault);_paths(v)
 from alpha_interface_runtime.compiler import compile_request
 from alpha_interface_runtime.executor import execute
 req={'schema_version':'1.0.0','subject':'XAUUSD','request_text':'Analyze Gold comprehensively for the current session with daily carry context. Preserve fundamental Direction, active causal force, consumption, remaining pressure, persistence, contradictions, positioning, actual flow, funding, mechanics, expected signatures and missing-driver risk. Price must not determine fundamental Direction.','mode':'SHADOW','horizon':'SESSION_1_6H','depth':'DEEP','output_profile':'EXPLORER','locale':'fa-IR'}
 c=compile_request(v,req);out=execute(v,c,data_root=data_root,truth_state='SHADOW_LIVE')
 if out.get('status') not in {'PASS','PASS_WITH_WARNINGS'}:raise V1BridgeError('V1 SHADOW RUN FAILED: '+json.dumps(out,ensure_ascii=False)[:3000])
 if len(out.get('results') or [])!=1:raise V1BridgeError('V1 shadow expected exactly one Gold result')
 return out,out['results'][0]['run_id']

def load_artifacts(vault,data_root,run_id):
 v=Path(vault);_paths(v)
 from alpha_runtime.runtime import AlphaRuntime
 rt=AlphaRuntime(v,Path(data_root));names=['run_capsule','decision_evidence_pack','evidence_integrity_receipt','fundamental_state','surprise_state','policy_reaction_state','regime_state','narrative_state','reflexivity_state','consumption_state','driver_transition','positioning_state','flow_state','funding_plumbing_state','mechanics_capacity_state','market_state_reconciliation','causal_graph','root_channel_map','model_disagreement','global_reconciliation','research_intent','final_permission']
 out={}
 for n in names:
  try:out[n]=rt.store.load_artifact_json(run_id,n)
  except Exception:pass
 try:m=rt.store.load_manifest(run_id);out['analysis_cutoff_utc']=m.get('analysis_cutoff_utc');out['horizon']=m.get('active_horizon') or 'SESSION_1_6H'
 except Exception:pass
 if 'run_capsule' not in out:raise V1BridgeError('V1 run_capsule missing')
 return out

def pressure_context(arts):
 keep=['fundamental_state','surprise_state','policy_reaction_state','regime_state','causal_graph','root_channel_map','model_disagreement','global_reconciliation','evidence_integrity_receipt','decision_evidence_pack']
 out={'analysis_cutoff_utc':arts.get('analysis_cutoff_utc')}
 for k in keep:
  if k not in arts:continue
  x=arts[k]
  if k=='decision_evidence_pack' and isinstance(x,dict):
   x=dict(x);rows=[]
   for r in x.get('fact_records') or []:
    # Target-market observed price/technical response is never Pressure authority in P11 precommit context.
    rr=dict(r);role=str(rr.get('direction_role') or '').upper();pc=str(rr.get('primary_class') or '').upper();fid=str(rr.get('fact_id') or '').upper()
    if role=='TRANSMISSION' and ('XAU' in fid or 'GOLD' in fid):continue
    if pc=='OBSERVED_MARKET_DATA' and ('XAU' in fid or 'GOLD' in fid):continue
    rows.append(rr)
   x['fact_records']=rows
  out[k]=x
 return out

def gold_context(arts):
 keep=['positioning_state','flow_state','funding_plumbing_state','mechanics_capacity_state','narrative_state','consumption_state','driver_transition','market_state_reconciliation','evidence_integrity_receipt']
 return {k:arts[k] for k in keep if k in arts}
