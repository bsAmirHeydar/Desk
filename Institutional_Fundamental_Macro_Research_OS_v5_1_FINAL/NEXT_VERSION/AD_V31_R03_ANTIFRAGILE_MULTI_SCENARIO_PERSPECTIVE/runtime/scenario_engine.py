from __future__ import annotations
from .common import cfg,stable_id

def _dom(p08):
    rid=p08.get('dominant_root');return next((r for r in p08.get('calibrated_roots') or [] if r.get('root_id')==rid),None)
def _event_family(e):
    s=' '.join(str(e.get(k,'')) for k in ('event_id','event','label')).upper()
    for f in cfg('scenario_trigger_policy.json').get('registered_event_families',[]):
        if f in s:return f
    return None
def _make(cls,status,relation,horizon,roots,evidence,triggers,invalidators,fragility,nonlin,unknown,implication,summary,relevance='WATCH',independence='INDEPENDENT'):
    core={'class':cls,'roots':roots,'triggers':triggers,'status':status,'h':horizon}
    return {'scenario_id':stable_id('R03SCN',core),'scenario_class':cls,'status':status,'horizon':horizon,'relation_to_canonical_direction':relation,'causal_roots':roots,'evidence_ids':sorted(set(evidence)),'trigger_conditions':triggers,'invalidating_conditions':invalidators,'fragility_pathways':fragility,'nonlinearity_state':nonlin,'unknown_dependency':unknown,'permission_implication':implication,'human_summary':summary,'decision_relevance':relevance,'independence':independence,'probability':None}
def build(p08,p03,event_context=None,unknown=None,nonlinearity=None):
    horizon=p08.get('horizon') or p03.get('horizon') or 'SESSION_1_6H';direction=p08.get('causal_direction','UNKNOWN');d=_dom(p08);sc=[];nonlin=(nonlinearity or {}).get('state','LINEAR_OR_UNRESOLVED');env=(unknown or {}).get('unknown_envelope','UNKNOWN')
    evidence=list((d or {}).get('evidence_fact_ids') or [])
    if direction in ('BULLISH_GOLD','BEARISH_GOLD'):
        sc.append(_make('CANONICAL_CONTINUATION','ACTIVE','SUPPORTS',horizon,[p08.get('dominant_root')] if p08.get('dominant_root') else [],evidence,['DOMINANT_CAUSAL_STRUCTURE_PERSISTS'],list(p08.get('invalidation_conditions') or []),['ROOT_HEALTH','MODEL_ROBUSTNESS'],nonlin,env,'NO_CHANGE','ادامه‌ی مشروط فشار فعلی؛ این سناریو احتمال نیست و فقط در صورت تداوم ساختار علّی معتبر است.','IMMEDIATE'))
        if d and d.get('magnitude') in ('LARGE','EXTREME') and d.get('causal_importance') in ('PRIMARY','SYSTEMIC') and (d.get('root_health') or {}).get('state') in ('HEALTHY','PARTIAL'):
            sc.append(_make('ACCELERATION','ARMED','SUPPORTS',horizon,[d.get('root_id')],evidence,['DOMINANT_ROOT_MAGNITUDE_INTENSIFIES','ADDITIONAL_INDEPENDENT_SUPPORT_ACTIVATES'],['DOMINANT_ROOT_FADES','CONSUMPTION_EXHAUSTED'],['CAUSAL_CONCENTRATION'],nonlin,env,'NO_CHANGE','اگر محرک غالب تشدید شود یا حمایت مستقل جدید وارد شود، فشار می‌تواند تقویت شود.'))
        sc.append(_make('REVERSAL_OR_BREAK','ARMED','OPPOSES',horizon,[d.get('root_id')] if d else [],evidence,['DOMINANT_ROOT_REVERSES','OPPOSING_PRIMARY_ROOT_ACTIVATES','DOMINANT_ROOT_HEALTH_COLLAPSES'],['CURRENT_DOMINANT_ROOT_REMAINS_HEALTHY_AND_DIRECTIONAL'],['MODEL_FRAGILITY','DATA_FRAGILITY'],nonlin,env,'CAP_TO_CONDITIONAL','این سناریو پیش‌بینی برگشت نیست؛ شرایطی را نگه می‌دارد که در آن thesis فعلی دیگر قابل اتکا نخواهد بود.','WATCH'))
    trans=(p03.get('price_transmission') or {}).get('state');fund=next((r for r in p08.get('calibrated_roots') or [] if r.get('root_id')=='FUNDING_COLLATERAL_STRESS'),None);confirmed=(p08.get('regime_context')=='LIQUIDITY_STRESS' or ((fund or {}).get('magnitude') in ('MATERIAL','LARGE','EXTREME') and (fund or {}).get('direction') not in (None,'UNKNOWN')))
    if direction in ('BULLISH_GOLD','BEARISH_GOLD') and trans in ('NEGATIVE','CONFLICTED'):
        if confirmed:
            m=_make('MECHANICAL_LIQUIDITY_DISLOCATION','ACTIVE','TRANSIENT_CONFLICT',horizon,['FUNDING_COLLATERAL_STRESS'],list((fund or {}).get('evidence_fact_ids') or []),['CONFIRMED_LIQUIDITY_OR_FUNDING_STRESS','OPPOSING_PRICE_TRANSMISSION'],['LIQUIDITY_STRESS_RESOLVES'],['LIQUIDITY_FRAGILITY','TRANSMISSION_FRAGILITY'],nonlin,env,'CAP_TO_CONDITIONAL','رفتار قیمت می‌تواند موقتاً با فشار بنیادی در تضاد باشد و شواهد مستقل مکانیکی/نقدینگی این تعارض را تأیید می‌کنند.','IMMEDIATE');m['explanation_state']='CONFIRMED_MECHANICAL_LIQUIDITY_DISLOCATION';sc.append(m)
        else:
            m=_make('MECHANICAL_LIQUIDITY_DISLOCATION','UNRESOLVED','TRANSIENT_CONFLICT',horizon,[],[],['PRICE_PRESSURE_CONFLICT'],['KNOWN_CAUSAL_DRIVER_EXPLAINS_CONFLICT'],['TRANSMISSION_FRAGILITY','UNKNOWN_DRIVER_FRAGILITY'],nonlin,env,'CAP_TO_CONDITIONAL','تعارض قیمت و فشار دیده می‌شود، اما شواهد کافی برای نسبت‌دادن آن به نقدینگی یا مکانیک بازار وجود ندارد.','WATCH');m['explanation_state']='UNEXPLAINED_TRANSMISSION_CONFLICT';sc.append(m)
    events=((event_context or {}).get('events') or [])
    if events:
        e=events[0];fam=_event_family(e);status=cfg('scenario_trigger_policy.json').get('event_status_map',{}).get(str(e.get('status','UPCOMING')).upper(),'ARMED')
        sc.append(_make('SCHEDULED_EVENT_DISCONTINUITY',status,'ORTHOGONAL',horizon,list(e.get('affected_roots') or []),[str(e.get('event_id') or e.get('event') or fam or 'REGISTERED_EVENT')],['REGISTERED_EVENT_'+str(fam or 'MATERIAL')],['EVENT_PASSES_WITHOUT_MATERIAL_REPRICING'],['EVENT_FRAGILITY'], 'DISCONTINUOUS_EVENT' if status=='TRIGGERED' else nonlin,env,'CAP_TO_CONDITIONAL','رویداد ثبت‌شده می‌تواند ساختار فعلی را گسسته کند؛ این به معنی پیش‌بینی جهت رویداد نیست.','IMMEDIATE' if status=='TRIGGERED' else 'WATCH'))
    if env in ('OPEN','WIDE','CRITICAL'):
        sc.append(_make('TAIL_UNKNOWN','ACTIVE' if env in ('WIDE','CRITICAL') else 'ARMED','UNKNOWN',horizon,[],[],['OUTSIDE_MODEL_VULNERABILITY_REMAINS'],['UNKNOWN_ENVELOPE_CONTAINED'],['UNKNOWN_DRIVER_FRAGILITY'],nonlin,env,'FORCE_WAIT' if env=='CRITICAL' else 'CAP_TO_CONDITIONAL','این سناریو حادثه‌ای را نام‌گذاری نمی‌کند؛ فقط مرز توضیح‌پذیری مدل و آسیب‌پذیری در برابر محرک‌های بیرون از شواهد فعلی را نشان می‌دهد.','TAIL'))
    # bounded, group-aware and deterministic; canonical then alternatives, stress, tail
    limits=cfg('scenario_construction_policy.json')['operator_group_limits'];group={'CANONICAL_CONTINUATION':'CANONICAL','ACCELERATION':'ALTERNATIVE','REVERSAL_OR_BREAK':'ALTERNATIVE','MECHANICAL_LIQUIDITY_DISLOCATION':'STRESS','SCHEDULED_EVENT_DISCONTINUITY':'STRESS','TAIL_UNKNOWN':'TAIL'};out=[];counts={}
    for x in sc:
        g=group[x['scenario_class']];counts[g]=counts.get(g,0)
        if counts[g]>=limits[g]:continue
        # Deduplicate same root/class only; current generator already bounded
        out.append(x);counts[g]+=1
        if len(out)>=6:break
    return {'scenarios':out,'scenario_count':len(out),'bounded':len(out)<=6,'canonical_scenario_id':next((x['scenario_id'] for x in out if x['scenario_class']=='CANONICAL_CONTINUATION'),None),'active_alternatives':[x['scenario_id'] for x in out if x['scenario_class'] in ('ACCELERATION','REVERSAL_OR_BREAK')],'stress_scenarios':[x['scenario_id'] for x in out if x['scenario_class'] in ('MECHANICAL_LIQUIDITY_DISLOCATION','SCHEDULED_EVENT_DISCONTINUITY')],'tail_scenario_id':next((x['scenario_id'] for x in out if x['scenario_class']=='TAIL_UNKNOWN'),None),'scenario_counts_are_not_probabilities':True}
