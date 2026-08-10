from pathlib import Path
from .util import add_paths,validate_schema
from .plan import build as build_plan
from .evidence import adapt_decision_evidence_pack
from .validator import assess

class MethodInvalid(RuntimeError): pass

def _names(rt,run_id): return {r['logical_name'] for r in rt.catalog.list_artifacts(run_id)}
def _load(rt,run_id,name,default=None):
    try:return rt.store.load_artifact_json(run_id,name)
    except Exception:return default

def ensure_plan(vault_root,rt,run_id):
    add_paths(vault_root); names=_names(rt,run_id)
    if 'method_plan' in names:return _load(rt,run_id,'method_plan')
    req=_load(rt,run_id,'run_request',{})
    # R1 stores resolved cutoff under analysis_cutoff_utc; preserve original request shape plus resolved manifest cutoff.
    req=dict(req); req['analysis_cutoff_utc']=rt.store.load_manifest(run_id).get('analysis_cutoff_utc')
    plan=build_plan(vault_root,run_id,req)
    rt.store.put_artifact(run_id,'method_plan','META','META',plan,'application/json',producer_process_id='M1_METHOD_ROUTER',producer_version='M1.0.1')
    return plan

def collect_bundle(rt,run_id):
    req=_load(rt,run_id,'run_request',{}) or {}; req=dict(req); req['analysis_cutoff_utc']=rt.store.load_manifest(run_id).get('analysis_cutoff_utc')
    dep=_load(rt,run_id,'decision_evidence_pack',{}) or {}; evidence=adapt_decision_evidence_pack(dep)
    hs=_load(rt,run_id,'hypothesis_set',{}) or {}; claims=[]
    for h in hs.get('hypotheses',[]):
        claims.append({'claim_id':h.get('hypothesis_id'),'claim_type':'CAUSAL_HYPOTHESIS','lifecycle_state':'ACTIVE','statement':h.get('title',''),'mechanism':h.get('mechanism'),'identification_state':'UNDETERMINED','evidence_ids':[x.get('fact_id') or x.get('evidence_id') or x.get('root_id') for x in h.get('supporting_evidence',[]) if isinstance(x,dict)],'contradictory_evidence_ids':[x.get('fact_id') or x.get('evidence_id') or x.get('root_id') for x in h.get('contradicting_evidence',[]) if isinstance(x,dict)],'research_mode':'OPERATIONAL','directness':'INDIRECT'})
    return {'run_request':req,'evidence':evidence,'claims':claims,'decision_evidence_pack':dep,'evidence_integrity_receipt':_load(rt,run_id,'evidence_integrity_receipt',{}) or {},'hypothesis_set':hs,'causal_graph':_load(rt,run_id,'causal_graph',{}) or {},'adversarial_review':_load(rt,run_id,'adversarial_review',{}) or {},'model_disagreement':_load(rt,run_id,'model_disagreement',{}) or {},'global_reconciliation':_load(rt,run_id,'global_reconciliation',{}) or {}}

def validate_phase(vault_root,rt,run_id,phase,logical_name=None,store=True,raise_hard=True):
    plan=ensure_plan(vault_root,rt,run_id); out=assess(vault_root,run_id,plan,collect_bundle(rt,run_id),phase)
    validate_schema(vault_root,'RUNTIME/Core Research Method Kernel/schemas/AlphaLab_Method_Receipt.schema.json',out)
    lname=logical_name or 'method_'+phase.lower()+'_validation_receipt'
    if store and lname not in _names(rt,run_id): rt.store.put_artifact(run_id,lname,'META','META',out,'application/json',producer_process_id='M1_METHOD_VALIDATOR',producer_version='M1.0.1')
    if raise_hard and out['hard_failure_count']>0:
        raise MethodInvalid('method validation '+phase+' failed: '+','.join(x['code'] for x in out['findings'] if x['hard']))
    return out
