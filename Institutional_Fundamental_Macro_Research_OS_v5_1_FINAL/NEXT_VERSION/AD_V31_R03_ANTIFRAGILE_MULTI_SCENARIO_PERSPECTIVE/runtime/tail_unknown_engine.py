from __future__ import annotations

def _dom(p08):
    rid=p08.get('dominant_root');return next((r for r in p08.get('calibrated_roots') or [] if r.get('root_id')==rid),None)
def _level(v):return {'LOW':0,'PRESENT':1,'ELEVATED':2,'SEVERE':3,'UNKNOWN':-1}.get(v,-1)
def evaluate(p08,p03,event_context=None,fragility=None):
    d=_dom(p08);h=(d or {}).get('root_health') or {};trans=(p03.get('price_transmission') or {}).get('state');miss=p08.get('missing_driver_risk','UNKNOWN');model=p08.get('model_sensitivity','NOT_APPLICABLE');reg=p08.get('regime_context','NORMAL');events=((event_context or {}).get('events') or [])
    reasons=[]
    if miss in ('ELEVATED','HIGH'):reasons.append('MISSING_DRIVER_RISK_'+miss)
    if trans in ('NEGATIVE','CONFLICTED'):reasons.append('UNEXPLAINED_PRICE_PRESSURE_DIVERGENCE')
    if h.get('state') in ('DEGRADED','CRITICAL_GAP'):reasons.append('DOMINANT_ROOT_'+h.get('state'))
    if h.get('directness_state') in ('PROXY_HEAVY','PROXY_ONLY'):reasons.append('PROXY_HEAVY_DOMINANT_ROOT')
    if model=='HIGH':reasons.append('HIGH_MODEL_SENSITIVITY')
    if reg not in (None,'NORMAL'):reasons.append('NON_NORMAL_REGIME_'+str(reg))
    if miss=='HIGH' and (trans in ('NEGATIVE','CONFLICTED') or h.get('state')=='CRITICAL_GAP'):env='CRITICAL'
    elif sum(x in reasons for x in ('HIGH_MODEL_SENSITIVITY','UNEXPLAINED_PRICE_PRESSURE_DIVERGENCE')) and len(reasons)>=2:env='WIDE'
    elif reasons:env='OPEN'
    else:env='CONTAINED'
    event_tail='ELEVATED' if any(str(e.get('status','')).upper() in ('TRIGGERED','ACTIVE','RELEASED') for e in events) else 'PRESENT' if events else 'LOW'
    liquidity='ELEVATED' if reg=='LIQUIDITY_STRESS' else 'LOW';model_tail='ELEVATED' if model=='HIGH' else 'PRESENT' if model=='ELEVATED' else 'LOW';data_tail='SEVERE' if h.get('state')=='CRITICAL_GAP' else 'ELEVATED' if h.get('state')=='DEGRADED' else 'PRESENT' if h.get('state')=='PARTIAL' else 'LOW';reg_tail='ELEVATED' if reg not in (None,'NORMAL') else 'LOW';unk='SEVERE' if env=='CRITICAL' else 'ELEVATED' if env=='WIDE' else 'PRESENT' if env=='OPEN' else 'LOW'
    epistemic=(env=='CRITICAL' and p08.get('contradiction') not in (None,'NONE','MINOR_OFFSET')) or (env=='CRITICAL' and trans in ('NEGATIVE','CONFLICTED'))
    return {'unknown_envelope':env,'primary_reasons':reasons,'epistemic_shock':bool(epistemic),'tail_exposure':{'EVENT_TAIL':event_tail,'LIQUIDITY_TAIL':liquidity,'MODEL_TAIL':model_tail,'DATA_TAIL':data_tail,'REGIME_TAIL':reg_tail,'UNKNOWN_TAIL':unk},'tail_is_not_probability':True,'unknown_unknown_specific_event_named':False}
