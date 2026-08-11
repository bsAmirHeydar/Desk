from .util import first
from .simple_language import to_fa,simplify_text,flatten_text,relation_fa,SECTION_TITLES,causal_status_text

def _art(rt,rid,name,default=None):
    try:return rt.store.load_artifact_json(rid,name)
    except Exception:return default

def _vals(obj,*keys,limit=5):
    if not isinstance(obj,dict):return []
    for k in keys:
        if obj.get(k) not in (None,'',[],{}):
            return [simplify_text(x) for x in flatten_text(obj.get(k),limit) if simplify_text(x)]
    return []

def _state(obj):
    return first(obj,'state','status','direction','bias','signal','clearance','regime','narrative_state','flow_state','positioning_state',default='UNKNOWN') if isinstance(obj,dict) else 'UNKNOWN'

def _stance(obj):
    if not isinstance(obj,dict):return 'UNKNOWN'
    raw=first(obj,'direction','bias','signal','stance','clearance','state','status',default='UNKNOWN')
    s=str(raw).upper()
    if any(x in s for x in ('BULL','BUY','POSITIVE','SUPPORT','FAVORABLE')):return 'SUPPORTIVE'
    if any(x in s for x in ('BEAR','SELL','NEGATIVE','OPPOSE','UNFAVORABLE')):return 'OPPOSING'
    if any(x in s for x in ('NEUTRAL','MIXED','CONTESTED','UNRESOLVED','BALANCED')):return 'MIXED_OR_NEUTRAL'
    return 'UNKNOWN'

def _summary(obj,state):
    if not isinstance(obj,dict) or not obj:return 'داده یا نتیجه قابل اتکا برای این بخش در دسترس نیست.'
    vals=_vals(obj,'summary_fa','summary','interpretation','rationale','reason','key_findings','drivers','notes',limit=3)
    if vals:return ' '.join(vals[:3])
    return f'وضعیت ثبت‌شده این بخش: {to_fa(state)}.'

def _deep(section_id,obj,canonical,evidence_refs):
    obj=obj if isinstance(obj,dict) else {}
    state=_state(obj); summary=_summary(obj,state)
    observations=_vals(obj,'observations','facts','key_findings','signals','components','evidence',limit=8)
    support=_vals(obj,'supporting_evidence','supports','confirmation','confirming_evidence','evidence_supporting',limit=8)
    opposition=_vals(obj,'contradictions','opposing_evidence','challenges','counterevidence','evidence_against',limit=8)
    unknowns=_vals(obj,'unknowns','gaps','limitations','missing_data','data_gaps','uncertainties',limit=8)
    mechanism=_vals(obj,'mechanism','causal_chain','transmission','drivers','channels',limit=8)
    invalidation=_vals(obj,'invalidation_triggers','invalidation','failure_conditions','reversal_triggers',limit=8)
    horizon=first(obj,'horizon','active_horizon','time_horizon',default=canonical.get('science',{}).get('active_horizon'))
    return {
      'section_id':section_id,'title_fa':SECTION_TITLES[section_id],'state':state,'state_fa':to_fa(state),
      'simple_result_fa':summary,'observations_fa':observations,
      'why_it_matters_fa':_vals(obj,'why_it_matters','market_relevance','implication','meaning',limit=5),
      'support_fa':support,'opposition_fa':opposition,'unknowns_fa':unknowns,'mechanism_fa':mechanism,
      'relation_to_direction_fa':relation_fa(_stance(obj)),'horizon':horizon,'horizon_fa':to_fa(horizon),
      'invalidation_fa':invalidation,'evidence_refs':evidence_refs,'technical_detail':obj
    }

def _causal_chain(causal):
    if not isinstance(causal,dict):return {'identified':False,'status':'UNKNOWN','status_fa':causal_status_text(None),'steps':[]}
    st=first(causal,'identification_status','causal_status','status','identification',default='UNKNOWN')
    ss=str(st).upper(); identified=('IDENTIFIED' in ss and 'NOT_IDENTIFIED' not in ss and 'UNIDENTIFIED' not in ss)
    steps=[]
    for chain_key in ('chain','causal_chain','transmission_chain','path'):
        x=causal.get(chain_key)
        if isinstance(x,list):
            steps=[simplify_text(y) for y in x if simplify_text(y)][:7];break
    if not steps and isinstance(causal.get('edges'),list):
        for e in causal['edges'][:6]:
            if not isinstance(e,dict):continue
            a=first(e,'source','from','cause');b=first(e,'target','to','effect')
            if a and (not steps or steps[-1]!=simplify_text(a)):steps.append(simplify_text(a))
            if b:steps.append(simplify_text(b))
        ded=[]
        for x in steps:
            if x and (not ded or x!=ded[-1]):ded.append(x)
        steps=ded[:7]
    return {'identified':identified,'status':st,'status_fa':causal_status_text(st),'steps':steps}

def _focus(compiled,direction,remaining,primary_driver,cards,method_health):
    classes=compiled.get('research_classes') or []
    primary=compiled.get('primary_research_class') or (classes[0] if classes else None)
    if primary=='CAUSAL_ATTRIBUTION':
        return {'kind':'CAUSE','label_fa':'اصلی‌ترین توضیح فعلی','answer_fa':simplify_text(primary_driver) or 'علت غالب هنوز با اطمینان کافی مشخص نشده است.'}
    if primary=='PERSISTENCE_REVERSAL':
        return {'kind':'PERSISTENCE','label_fa':'فشار باقی‌مانده','answer_fa':f'وضعیت فشار باقی‌مانده: {to_fa(remaining)}.'}
    if primary=='NARRATIVE_ATTENTION':
        c=next((x for x in cards if x['section_id']=='narrative'),None)
        return {'kind':'NARRATIVE','label_fa':'ذهن بازار','answer_fa':(c or {}).get('summary_fa') or 'روایت غالب هنوز روشن نیست.'}
    if primary=='ANOMALY_FAILURE_INVESTIGATION':
        fs=method_health.get('findings') or []
        return {'kind':'FAILURE','label_fa':'مهم‌ترین مسئله بررسی','answer_fa':simplify_text(fs[0]) if fs else 'برای تشخیص علت خطا، داده postmortem کافی در این snapshot ثبت نشده است.'}
    if primary=='EVENT_ANALYSIS':
        return {'kind':'EVENT','label_fa':'اثر اصلی رویداد','answer_fa':simplify_text(primary_driver) or 'اثر غالب رویداد هنوز روشن نیست.'}
    return {'kind':'STATE','label_fa':'وضعیت فعلی','answer_fa':f'جهت فعلی {to_fa(direction)} است و فشار باقی‌مانده {to_fa(remaining)} ارزیابی شده است.'}

def build(rt,run_id,canonical,compiled,run_quality=None,capsule=None,changes=None):
    specs=[('timing','temporal_clearance'),('fundamental','fundamental_state'),('expectations','policy_reaction_state'),('narrative','narrative_state'),('positioning','positioning_state'),('flow','flow_state'),('funding','funding_plumbing_state'),('mechanics','mechanics_capacity_state')]
    artifacts={sid:_art(rt,run_id,name,{}) or {} for sid,name in specs}
    ri=_art(rt,run_id,'research_intent',{}) or {};cons=_art(rt,run_id,'consumption_state',{}) or {};dt=_art(rt,run_id,'driver_transition',{}) or {};sc=_art(rt,run_id,'scenario_tree',{}) or {};meth=canonical['method_health'];apl=canonical['apl_a'];retr=_art(rt,run_id,'r3_retrieval_receipt',{}) or {};cog=_art(rt,run_id,'cognitive_adjudication',{}) or {};causal=_art(rt,run_id,'causal_graph',{}) or {};fl=canonical.get('science',{}).get('force_lifecycle',{})
    all_evidence=[{'logical_name':x['logical_name'],'artifact_hash':x['artifact_hash'],'world':x['world'],'stage':x['stage']} for x in rt.catalog.list_artifacts(run_id) if x.get('world') in ('EVIDENCE','COGNITION','DECISION','META')]
    cards=[];deep={}
    for sid,name in specs:
        obj=artifacts[sid]; st=_state(obj); stance=_stance(obj); refs=[x for x in all_evidence if x['logical_name']==name]
        d=_deep(sid,obj,canonical,refs);deep[sid]=d
        cards.append({'section_id':sid,'id':SECTION_TITLES[sid],'title_fa':SECTION_TITLES[sid],'state':st,'state_fa':to_fa(st),'stance':stance,'relation_fa':relation_fa(stance),'summary_fa':d['simple_result_fa'],'important_point_fa':(d['why_it_matters_fa'] or d['observations_fa'] or [d['simple_result_fa']])[0],'detail':obj,'deep_dive':d})
    scenarios=[]
    for x in sc.get('scenarios',[])[:4]:
        scenarios.append({'role':x.get('role'),'role_fa':to_fa(x.get('role')),'plausibility':x.get('plausibility_band'),'direction':x.get('direction'),'direction_fa':to_fa(x.get('direction')),'conditions':[simplify_text(y) for y in x.get('required_conditions',[]) if simplify_text(y)],'confirmation':[simplify_text(y) for y in x.get('confirmation_triggers',[]) if simplify_text(y)],'invalidation':[simplify_text(y) for y in x.get('invalidation_triggers',[]) if simplify_text(y)],'horizon':x.get('horizon')})
    primary_driver=first(dt,'dominant_driver','current_driver','primary_driver',default=None);secondary=first(dt,'secondary_driver','challenger_driver',default=None);opposing=first(dt,'opposing_force','counter_force',default=None)
    next_review=fl.get('next_review') if fl.get('next_review') not in (None,'UNKNOWN') else (cog.get('next_review_trigger') or ri.get('review_trigger'))
    direction=canonical['decision'].get('final_direction') or canonical['decision'].get('fundamental_direction');permission=canonical['decision'].get('permission');remaining=fl.get('remaining_pressure',canonical['science'].get('remaining_asymmetry'))
    method_health={'status':meth.get('status'),'research_class':meth.get('research_class'),'rigor_tier':meth.get('rigor_tier'),'hard_failure_count':meth.get('hard_failure_count'),'findings':meth.get('findings',[]),'material_gaps':retr.get('gaps',[]),'uncertainty':canonical['science'].get('uncertainty'),'simple_summary_fa':('تحلیل از نظر روش تحقیق سالم است.' if str(meth.get('status')).upper()=='PASS' else 'در روش یا شواهد این تحلیل محدودیت مهمی ثبت شده است.')}
    focus=_focus(compiled,direction,remaining,primary_driver,cards,method_health)
    invalidation=[simplify_text(x) for x in (ri.get('invalidation_triggers') or []) if simplify_text(x)]
    transition_changes=_vals(dt,'changes','changed_components','transition_reasons','new_information',limit=6)
    layer2_pressure={'force':fl.get('force','UNKNOWN'),'force_fa':to_fa(fl.get('force','UNKNOWN')),'consumption':fl.get('consumption','UNKNOWN'),'consumption_fa':to_fa(fl.get('consumption','UNKNOWN')),'remaining_pressure':remaining,'remaining_pressure_fa':to_fa(remaining),'remaining_pressure_reasons':[simplify_text(x) for x in cons.get('remaining_asymmetry_reasons',[]) if simplify_text(x)],'persistence':fl.get('persistence','UNKNOWN'),'persistence_fa':to_fa(fl.get('persistence','UNKNOWN')),'reversal':fl.get('reversal','UNKNOWN'),'reversal_fa':to_fa(fl.get('reversal','UNKNOWN')),'invalidation_triggers':fl.get('invalidation') or invalidation}
    report={'schema_version':'1.0.0','report_model_version':'2.0.0','interface_version':'UX3.0.0',
      'header':{'request_id':compiled['request_id'],'original_request':compiled['original_request'].get('request_text'),'subject':canonical['subject'],'mode':compiled['mode'],'as_of':canonical['analysis_cutoff_utc'],'horizon':canonical['science'].get('active_horizon'),'research_classes':compiled['research_classes'],'locale':compiled['locale']},
      'layer1':{'focus':focus,'direction':direction,'direction_fa':to_fa(direction),'permission':permission,'permission_fa':to_fa(permission),'force':fl.get('force','UNKNOWN'),'force_fa':to_fa(fl.get('force','UNKNOWN')),'consumption':fl.get('consumption','UNKNOWN'),'consumption_fa':to_fa(fl.get('consumption','UNKNOWN')),'remaining_pressure':remaining,'remaining_pressure_fa':to_fa(remaining),'persistence':fl.get('persistence','UNKNOWN'),'persistence_fa':to_fa(fl.get('persistence','UNKNOWN')),'reversal_risk':fl.get('reversal','UNKNOWN'),'reversal_risk_fa':to_fa(fl.get('reversal','UNKNOWN')),'dominant_driver':simplify_text(primary_driver) or None,'what_matters_now_fa':('مهم‌ترین عامل فعلی: '+simplify_text(primary_driver)+'.') if simplify_text(primary_driver) else 'عامل غالب هنوز با اطمینان کافی مشخص نشده است.','what_would_change_this_fa':('این تحلیل باید بازبینی شود اگر '+invalidation[0]) if invalidation else 'عامل مشخص و قابل اتکایی برای ابطال تحلیل در این snapshot ثبت نشده است.','next_review':next_review,'next_review_fa':to_fa(next_review)},
      'decision_strip':{'direction':direction,'fundamental_direction':canonical['decision'].get('fundamental_direction'),'permission':permission,'edge_state':canonical['decision'].get('edge_state'),'pressure_strength':fl.get('force','UNKNOWN'),'consumption':fl.get('consumption','UNKNOWN'),'remaining_pressure':remaining,'persistence':fl.get('persistence','UNKNOWN'),'reversal_risk':fl.get('reversal','UNKNOWN'),'next_review':next_review},
      'layer2':{'cards':cards,'drivers':{'primary':primary_driver,'primary_fa':simplify_text(primary_driver),'secondary':secondary,'secondary_fa':simplify_text(secondary),'opposing':opposing,'opposing_fa':simplify_text(opposing),'transition':dt},'causal_chain':_causal_chain(causal),'pressure':layer2_pressure,'changes':{'items':transition_changes,'has_comparison':bool(transition_changes),'empty_message_fa':'مقایسه معتبر با اجرای قبلی در این snapshot ثبت نشده است.'},'scenarios':scenarios},
      'analytical_cards':cards,'drivers':{'primary':primary_driver,'secondary':secondary,'opposing':opposing,'transition':dt},'pressure':layer2_pressure,'scenarios':scenarios,
      'layer3':{'sections':deep},'method_health':method_health,
      'perspective':{'mode':'SHADOW_ONLY','active_lenses':apl.get('active_lenses',[]),'material_findings':apl.get('material_findings',[]),'material_findings_fa':[simplify_text(x) for x in apl.get('material_findings',[]) if simplify_text(x)],'quiet':not bool(apl.get('material_findings'))},
      'evidence_explorer':{'decision_artifacts':all_evidence},
      'audit':{'run_id':run_id,'request_id':compiled['request_id'],'compiled_intent':compiled,'vault_commit':canonical['traceability'].get('vault_commit'),'prompt_pack_version':canonical['traceability'].get('prompt_pack_version'),'method_version':meth.get('version'),'apl_a_mode':'SHADOW_ONLY','decision_seal_hash':canonical['decision'].get('decision_seal_hash'),'canonical_result_hash':canonical.get('canonical_result_hash'),'interface_version':'UX3.0.0','direction_authority':{'request_compiler':'NONE','report_composer':'NONE','apl_a':'NONE'}},
      'ux':{'schema':'UX3_RESEARCH_EXPERIENCE_V1','layers':['COMMAND_CENTER','MARKET_WORKSPACE','ANALYTICAL_LENS_INDEX','SECTION_DEEP_DIVE'],'primary_language':'fa-IR','rtl':True,'presentation_authority_only':True,'single_reusable_deep_drawer':True,'scenario_navigator':True,'visible_engineering_metadata':False}}
    rq=run_quality or {}
    status=rq.get('status')
    if status=='PASS': qtext='همه کنترل‌های اصلی این تحلیل پاس شده‌اند.'
    elif status in ('PASS_WITH_WARNINGS','PARTIAL'): qtext='تحلیل قابل استفاده است، اما محدودیت‌های علمی ثبت‌شده دارد.'
    elif status=='BLOCKED': qtext='تحلیل به دلیل شکست یک کنترل سخت، آماده استفاده عادی نیست.'
    else: qtext='وضعیت کنترل کیفیت هنوز نهایی نشده است.'
    report['run_quality']={
      'status':status,
      'simple_summary_fa':qtext,
      'receipt':rq,
      'capsule':{'run_id':(capsule or {}).get('run_id'),'capsule_hash':(capsule or {}).get('capsule_hash'),'reproducibility_state':(capsule or {}).get('reproducibility_state')},
      'changes':changes or (capsule or {}).get('changes_since_previous') or {'has_comparison':False,'items':[]}
    }
    # Prefer canonical run-memory delta over internal driver-transition prose when available.
    memchg=report['run_quality']['changes']
    if memchg.get('has_comparison'):
        report['layer2']['changes']={'items':[str(x.get('label') or x.get('field'))+': '+str(x.get('from'))+' → '+str(x.get('to')) for x in memchg.get('items',[]) if isinstance(x,dict) and x.get('field')!='unknown'] + [str(x.get('value')) for x in memchg.get('items',[]) if isinstance(x,dict) and x.get('field')=='unknown'],'has_comparison':True,'empty_message_fa':''}
    report['audit']['run_quality']=rq
    report['audit']['run_capsule']=report['run_quality']['capsule']
    return report
