from .util import first,sha_obj

def _art(rt,rid,name,default=None):
    try:return rt.store.load_artifact_json(rid,name)
    except Exception:return default

def _lifecycle(ri,cons,driver,fp):
    direction=ri.get('fundamental_direction')
    force=first(ri,'force','force_state','directional_force','force_tier',default=first(driver,'force','strength','state',default='UNKNOWN'))
    consumption=first(cons,'consumption','consumption_state','state','status',default='UNKNOWN')
    remaining=first(ri,'remaining_pressure','remaining_asymmetry',default=first(cons,'remaining_pressure','remaining_asymmetry',default='UNKNOWN'))
    persistence=first(ri,'persistence','persistence_state','durability',default=first(driver,'persistence','persistence_state',default='UNKNOWN'))
    reversal=first(ri,'reversal_risk','reversal_hazard',default='UNKNOWN')
    invalidation=ri.get('invalidation_triggers') or ri.get('invalidation') or fp.get('invalidation_triggers') or []
    review=first(ri,'next_review','review_trigger','review_time','valid_until',default=first(fp,'review_trigger','next_review','valid_until',default='UNKNOWN'))
    return {'direction':direction,'force':force,'consumption':consumption,'remaining_pressure':remaining,'persistence':persistence,'reversal':reversal,'invalidation':invalidation,'next_review':review}

def build(rt,run_id,request_id):
    m=rt.store.load_manifest(run_id);ri=_art(rt,run_id,'research_intent',{}) or {};fp=_art(rt,run_id,'final_permission',{}) or {};cons=_art(rt,run_id,'consumption_state',{}) or {};cog=_art(rt,run_id,'cognitive_adjudication',{}) or {};meth=_art(rt,run_id,'method_predecision_validation_receipt',{}) or {};plan=_art(rt,run_id,'method_plan',{}) or {};apl=_art(rt,run_id,'apl_a_forward_telemetry',{}) or {};retr=_art(rt,run_id,'r3_retrieval_receipt',{}) or {};scenario=_art(rt,run_id,'scenario_tree',{}) or {};causal=_art(rt,run_id,'causal_graph',{}) or {};driver=_art(rt,run_id,'driver_transition',{}) or {};unc=ri.get('uncertainty_profile') or cog.get('decision_critical_uncertainties') or []
    lifecycle=_lifecycle(ri,cons,driver,fp)
    obj={'schema_version':'1.0.0','interface_version':'UI2.1.0','run_contract_version':'RUN2.0.0','run_id':run_id,'request_id':request_id,'subject':m.get('subject'),'analysis_cutoff_utc':m.get('analysis_cutoff_utc'),'run_mode':m.get('run_mode'),'decision':{'fundamental_direction':ri.get('fundamental_direction') or cog.get('fundamental_direction'),'final_direction':cog.get('final_direction') or ri.get('fundamental_direction'),'permission':fp.get('permission') or cog.get('cognitive_permission'),'edge_state':ri.get('edge_state'),'decision_seal_hash':m.get('decision_seal_hash')},'science':{'active_horizon':ri.get('active_horizon') or m.get('active_horizon'),'urgency':ri.get('urgency'),'remaining_asymmetry':ri.get('remaining_asymmetry') or cons.get('remaining_asymmetry'),'reversal_hazard':ri.get('reversal_hazard'),'fragility':ri.get('fragility'),'consumption':cons,'driver_transition':driver,'scenario_tree':scenario,'causal_graph':causal,'uncertainty':unc,'material_gaps':retr.get('gaps',[]),'force_lifecycle':lifecycle},'method_health':{'version':plan.get('method_version'),'research_class':plan.get('research_class'),'protocol_id':plan.get('protocol_id'),'rigor_tier':plan.get('rigor_tier'),'status':meth.get('status'),'findings':meth.get('findings',[]),'hard_failure_count':meth.get('hard_failure_count',0),'source_dependency_graph':meth.get('source_dependency_graph',{})},'apl_a':{'mode':'SHADOW_ONLY','active_lenses':apl.get('active_lenses',[]),'material_findings':apl.get('material_findings',[]),'would_request':apl.get('would_request',[])},'traceability':{'vault_commit':m.get('vault_commit'),'prompt_pack_version':m.get('prompt_pack_version'),'decision_seal_hash':m.get('decision_seal_hash')}}
    obj['canonical_result_hash']=sha_obj(obj);return obj
