from .util import first

def _art(rt,rid,name,default=None):
    try:return rt.store.load_artifact_json(rid,name)
    except Exception:return default

def _state_summary(name,obj):
    if not isinstance(obj,dict) or not obj:return {'id':name,'state':'UNKNOWN','stance':'UNKNOWN','summary_fa':'داده یا نتیجه قابل اتکا برای این لایه در دسترس نیست.','detail':obj or {}}
    # Prefer explicit status/state/direction fields without inventing science.
    st=first(obj,'state','status','direction','bias','signal','clearance','regime','narrative_state','flow_state','positioning_state',default='AVAILABLE')
    stance='UNKNOWN'
    s=str(st).upper()
    if any(x in s for x in ('BULL','BUY','POSITIVE','SUPPORT')):stance='SUPPORTIVE'
    elif any(x in s for x in ('BEAR','SELL','NEGATIVE','OPPOSE')):stance='OPPOSING'
    elif any(x in s for x in ('NEUTRAL','MIXED','CONTESTED','UNRESOLVED')):stance='MIXED_OR_NEUTRAL'
    # Keep summary factual and generic if no dedicated natural-language field exists.
    reasons=first(obj,'summary','reason','rationale','interpretation','key_findings','drivers','notes',default=None)
    if isinstance(reasons,list):txt='؛ '.join(str(x) for x in reasons[:3])
    elif isinstance(reasons,dict):txt='؛ '.join(f'{k}: {v}' for k,v in list(reasons.items())[:3])
    else:txt=str(reasons) if reasons else f'وضعیت ثبت‌شده این لایه: {st}'
    return {'id':name,'state':st,'stance':stance,'summary_fa':txt,'detail':obj}

def build(rt,run_id,canonical,compiled):
    names=[('Timing','temporal_clearance'),('Fundamental','fundamental_state'),('Expectations / Policy / Regime','policy_reaction_state'),('Narrative / Reflexivity / Consumption','narrative_state'),('Positioning','positioning_state'),('Actual Flow','flow_state'),('Funding / Plumbing','funding_plumbing_state'),('Mechanics / Capacity / Volatility','mechanics_capacity_state')]
    cards=[_state_summary(label,_art(rt,run_id,art,{})) for label,art in names]
    ri=_art(rt,run_id,'research_intent',{}) or {};cons=_art(rt,run_id,'consumption_state',{}) or {};dt=_art(rt,run_id,'driver_transition',{}) or {};sc=_art(rt,run_id,'scenario_tree',{}) or {};hyp=_art(rt,run_id,'hypothesis_set',{}) or {};meth=canonical['method_health'];apl=canonical['apl_a'];retr=_art(rt,run_id,'r3_retrieval_receipt',{}) or {};cog=_art(rt,run_id,'cognitive_adjudication',{}) or {}
    scenarios=[]
    for x in sc.get('scenarios',[])[:4]:scenarios.append({'role':x.get('role'),'plausibility':x.get('plausibility_band'),'direction':x.get('direction'),'conditions':x.get('required_conditions',[]),'confirmation':x.get('confirmation_triggers',[]),'invalidation':x.get('invalidation_triggers',[]),'horizon':x.get('horizon')})
    primary_driver=first(dt,'dominant_driver','current_driver','primary_driver',default=None)
    secondary=first(dt,'secondary_driver','challenger_driver',default=None)
    opposing=first(dt,'opposing_force','counter_force',default=None)
    next_review=cog.get('next_review_trigger') or ri.get('review_trigger')
    report={'schema_version':'1.0.0','report_model_version':'1.0.0','header':{'request_id':compiled['request_id'],'original_request':compiled['original_request'].get('request_text'),'subject':canonical['subject'],'mode':compiled['mode'],'as_of':canonical['analysis_cutoff_utc'],'horizon':canonical['science'].get('active_horizon'),'research_classes':compiled['research_classes'],'locale':compiled['locale']},'decision_strip':{'direction':canonical['decision'].get('final_direction') or canonical['decision'].get('fundamental_direction'),'fundamental_direction':canonical['decision'].get('fundamental_direction'),'permission':canonical['decision'].get('permission'),'edge_state':canonical['decision'].get('edge_state'),'pressure_strength':ri.get('urgency') or 'UNDETERMINED','consumption':cons.get('lifecycle_state') or 'UNDETERMINED','remaining_pressure':canonical['science'].get('remaining_asymmetry'),'persistence':first(ri,'validity_action',default='UNDETERMINED'),'reversal_risk':canonical['science'].get('reversal_hazard'),'next_review':next_review},'analytical_cards':cards,'drivers':{'primary':primary_driver,'secondary':secondary,'opposing':opposing,'transition':dt},'pressure':{'force':ri.get('urgency'),'consumption':cons.get('lifecycle_state'),'remaining_pressure':cons.get('remaining_asymmetry') or ri.get('remaining_asymmetry'),'remaining_pressure_reasons':cons.get('remaining_asymmetry_reasons',[]),'persistence':ri.get('validity_action'),'reversal':ri.get('reversal_hazard'),'invalidation_triggers':ri.get('invalidation_triggers',[])},'scenarios':scenarios,'method_health':{'status':meth.get('status'),'research_class':meth.get('research_class'),'rigor_tier':meth.get('rigor_tier'),'hard_failure_count':meth.get('hard_failure_count'),'findings':meth.get('findings',[]),'material_gaps':retr.get('gaps',[]),'uncertainty':canonical['science'].get('uncertainty')},'perspective':{'mode':'SHADOW_ONLY','active_lenses':apl.get('active_lenses',[]),'material_findings':apl.get('material_findings',[]),'quiet':not bool(apl.get('material_findings'))},'evidence_explorer':{'decision_artifacts':[{'logical_name':x['logical_name'],'artifact_hash':x['artifact_hash'],'world':x['world'],'stage':x['stage']} for x in rt.catalog.list_artifacts(run_id) if x.get('world') in ('EVIDENCE','COGNITION','DECISION','META')]},'audit':{'run_id':run_id,'request_id':compiled['request_id'],'compiled_intent':compiled,'vault_commit':canonical['traceability'].get('vault_commit'),'prompt_pack_version':canonical['traceability'].get('prompt_pack_version'),'method_version':meth.get('version'),'apl_a_mode':'SHADOW_ONLY','decision_seal_hash':canonical['decision'].get('decision_seal_hash'),'canonical_result_hash':canonical.get('canonical_result_hash'),'direction_authority':{'request_compiler':'NONE','report_composer':'NONE','apl_a':'NONE'}}}
    return report
