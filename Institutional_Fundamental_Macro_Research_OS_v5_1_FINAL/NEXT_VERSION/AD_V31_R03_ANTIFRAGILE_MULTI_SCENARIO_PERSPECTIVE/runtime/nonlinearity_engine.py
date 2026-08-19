from __future__ import annotations
from .common import cfg

def _root(p08,rid):return next((r for r in p08.get('calibrated_roots') or [] if r.get('root_id')==rid),None)
def evaluate(p08,p03,event_context=None):
    pathways=[];events=((event_context or {}).get('events') or []);reg=p08.get('regime_context','NORMAL');trans=(p03.get('price_transmission') or {}).get('state')
    event_triggered=any(str(e.get('status','')).upper() in ('TRIGGERED','ACTIVE','RELEASED') for e in events)
    for p in cfg('stress_pathway_registry.json').get('pathways',[]):
        state='DORMANT';rid=p.get('source_root');r=_root(p08,rid) if rid else None
        if p['pathway_id']=='FUNDING_TO_FORCED_LIQUIDATION':
            mag=(r or {}).get('magnitude');
            if mag in ('MATERIAL','LARGE','EXTREME'):state='ARMED'
            if state=='ARMED' and reg=='LIQUIDITY_STRESS' and trans in ('NEGATIVE','CONFLICTED'):state='TRIGGERED'
        elif p['pathway_id']=='POLICY_EVENT_TO_REAL_RATE_REPRICING':
            if events:state='ARMED'
            if event_triggered:state='TRIGGERED'
        elif p['pathway_id']=='GEOPOLITICAL_THRESHOLD_TO_INSURANCE_DEMAND':
            g=_root(p08,'GEOPOLITICAL_INSURANCE_RISK')
            if reg=='GEOPOLITICAL_SHOCK':state='ARMED'
            if state=='ARMED' and (g or {}).get('magnitude') in ('LARGE','EXTREME'):state='TRIGGERED'
        pathways.append({'pathway_id':p['pathway_id'],'state':state,'source_root':rid,'intermediate_mechanism':p.get('intermediate_mechanism'),'invalidator':p.get('invalidator')})
    if event_triggered:overall='DISCONTINUOUS_EVENT'
    elif any(x['state']=='TRIGGERED' and x['pathway_id']=='FUNDING_TO_FORCED_LIQUIDATION' for x in pathways):overall='CASCADE_RISK'
    elif any(x['state']=='TRIGGERED' and x['pathway_id']=='GEOPOLITICAL_THRESHOLD_TO_INSURANCE_DEMAND' for x in pathways):overall='THRESHOLD_NONLINEAR'
    else:overall='LINEAR_OR_UNRESOLVED'
    return {'state':overall,'pathways':pathways,'active_pathways':[x for x in pathways if x['state'] in ('ARMED','TRIGGERED')],'cascade_state':'TRIGGERED' if any(x['state']=='TRIGGERED' for x in pathways) else 'ARMED' if any(x['state']=='ARMED' for x in pathways) else 'DORMANT','event_discontinuity':'TRIGGERED' if event_triggered else 'ARMED' if events else 'DORMANT','numeric_convexity_coefficient':None}
