from __future__ import annotations
from .common import cfg

def _dom(p08):
    rid=p08.get('dominant_root');return next((r for r in p08.get('calibrated_roots') or [] if r.get('root_id')==rid),None)
def _semantic_level(bundle,health):
    mode=(bundle or {}).get('adjudication_mode') or ((bundle or {}).get('bundle') or {}).get('adjudication_mode')
    sem=(health or {}).get('semantic_evidence_count',0)
    if mode=='CONSERVATIVE_EVIDENCE_ONLY' and sem:return 'HIGH'
    if mode=='CONSERVATIVE_EVIDENCE_ONLY':return 'MODERATE'
    return 'MODERATE' if sem else 'LOW'
def evaluate(p08,p03,kernel=None,semantic_bundle=None,event_context=None,unknown=None,scenarios=None):
    pol=cfg('fragility_dimension_policy.json');d=_dom(p08);h=(d or {}).get('root_health') or {};model=pol['model_map'].get(p08.get('model_sensitivity'),'UNKNOWN');data=pol['root_health_map'].get(h.get('state'),'UNKNOWN');conc=pol['breadth_map'].get(p08.get('breadth'),'UNKNOWN');reg='MODERATE' if p08.get('regime_context') not in (None,'NORMAL') else 'LOW';events=((event_context or {}).get('events') or []);ev='HIGH' if any(str(e.get('status','')).upper() in ('TRIGGERED','ACTIVE','RELEASED') for e in events) else 'MODERATE' if events else 'LOW';trans='HIGH' if (p03.get('price_transmission') or {}).get('state') in pol['transmission_high_states'] else 'LOW';liq='HIGH' if p08.get('regime_context')=='LIQUIDITY_STRESS' else 'LOW';narr='HIGH' if p08.get('breadth')=='NARROW' and ((h.get('same_shock_manifestation_count') or 0)>0 or len(p08.get('supporting_roots') or [])<=1) else 'MODERATE' if p08.get('breadth')=='NARROW' else 'LOW';unk=pol['missing_driver_map'].get(p08.get('missing_driver_risk'),'UNKNOWN');sem=_semantic_level(semantic_bundle,h)
    if unknown and unknown.get('unknown_envelope')=='CRITICAL':unk='CRITICAL'
    dims={'MODEL_FRAGILITY':model,'DATA_FRAGILITY':data,'CAUSAL_CONCENTRATION_FRAGILITY':conc,'REGIME_FRAGILITY':reg,'EVENT_FRAGILITY':ev,'TRANSMISSION_FRAGILITY':trans,'LIQUIDITY_FRAGILITY':liq,'NARRATIVE_FRAGILITY':narr,'UNKNOWN_DRIVER_FRAGILITY':unk,'SEMANTIC_FRAGILITY':sem}
    vals=list(dims.values())
    if 'CRITICAL' in vals:overall='CRITICALLY_FRAGILE'
    elif vals.count('HIGH')>=2:overall='FRAGILE'
    elif 'HIGH' in vals or vals.count('MODERATE')>=3:overall='WATCH'
    elif all(v=='UNKNOWN' for v in vals):overall='UNKNOWN'
    else:overall='ROBUST'
    return {'dimensions':dims,'overall':overall,'critical_not_averageable':True,'largest_dimensions':[k for k,v in dims.items() if v in ('CRITICAL','HIGH')][:4]}
