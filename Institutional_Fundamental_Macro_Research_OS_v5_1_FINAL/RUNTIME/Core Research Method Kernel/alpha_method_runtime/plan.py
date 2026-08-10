from .util import now, validate_schema
from .registry import MethodRegistry
from .router import route

def build(vault_root, run_id, run_request):
    reg=MethodRegistry(vault_root); r=route(vault_root,run_request); p=r['protocol']
    out={
      'schema_version':'1.0.0','method_version':'M1.0.0','run_id':run_id,'research_class':r['research_class'],'protocol_id':p['protocol_id'],'selection_basis':r['selection_basis'],'alternative_protocols':r['alternative_protocols'],'rigor_tier':r['rigor_tier'],'asset_family':r['asset_family'],'active_horizon':str(run_request.get('active_horizon') or 'UNSPECIFIED'),'analysis_cutoff_utc':run_request.get('analysis_cutoff_utc') or run_request.get('analysis_cutoff'),'invariants':[x['id'] for x in reg.constitution['invariants']],'required_evidence':p['required_evidence'],'minimum_evidence':p['minimum_evidence'],'update_cadence':p['update_cadence'],'invalidation_criteria':p['invalidation'],'authority':'METHOD_GOVERNANCE_ONLY','created_at_utc':now()
    }
    validate_schema(vault_root,reg.schema_ref('AlphaLab_Method_Plan.schema.json'),out); return out
