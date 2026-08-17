from __future__ import annotations
from collections import defaultdict
from .common import max_strength

def _direction(rows):
    bulls=[r for r in rows if r.get('effect_on_gold')=='BULLISH_GOLD']
    bears=[r for r in rows if r.get('effect_on_gold')=='BEARISH_GOLD']
    mixed=[r for r in rows if r.get('effect_on_gold')=='MIXED']
    if mixed or (bulls and bears): return 'MIXED'
    if bulls: return 'BULLISH_GOLD'
    if bears: return 'BEARISH_GOLD'
    return 'UNKNOWN'

def _strength_from_units(units):
    resolved=[u for u in units if u.get('direction') in ('BULLISH_GOLD','BEARISH_GOLD','MIXED')]
    if not resolved: return 'UNKNOWN'
    if len(resolved)>=3: return 'HIGH'
    if len(resolved)>=2: return 'MEDIUM'
    return 'LOW'

def _background_bias(rr):
    proxy=[]
    for r in rr:
        b=(r.get('details') or {}).get('background_bias')
        if b in ('BULLISH_GOLD','BEARISH_GOLD','MIXED'):
            proxy.append({'effect_on_gold':b})
    return _direction(proxy)

def _impulse_direction(rr):
    proxy=[]
    for r in rr:
        b=(r.get('details') or {}).get('impulse_effect')
        if b in ('BULLISH_GOLD','BEARISH_GOLD','MIXED'):
            proxy.append({'effect_on_gold':b})
    return _direction(proxy)

def build_root_states(rows,root_registry,plane):
    out=[]
    for root in root_registry['roots']:
        all_rr=[r for r in rows if r.get('causal_root_family')==root['root_id'] and r.get('pressure_plane')==plane]
        if plane=='CAUSAL_FUNDAMENTAL': rr=[r for r in all_rr if r.get('is_additive') and r.get('horizon_active',True)]
        else: rr=[r for r in all_rr if r.get('resolution') in ('RESOLVED','SEMANTICALLY_ADJUDICATED')]
        direction=_direction(rr)
        out.append({'root_id':root['root_id'],'direction':direction,'strength':max_strength([r.get('strength','UNKNOWN') for r in rr]),'evidence_fact_ids':[r['fact_id'] for r in rr],'conflict':direction=='MIXED','background_bias':_background_bias(all_rr),'impulse_direction':_impulse_direction(all_rr),'background_evidence_fact_ids':[r['fact_id'] for r in all_rr if (r.get('details') or {}).get('background_bias') in ('BULLISH_GOLD','BEARISH_GOLD','MIXED')]})
    return out

def causal_plane(rows,root_registry):
    roots=build_root_states(rows,root_registry,'CAUSAL_FUNDAMENTAL')
    d=_direction([{'effect_on_gold':r['direction']} for r in roots])
    bg=_direction([{'effect_on_gold':r.get('background_bias')} for r in roots])
    return {'plane':'CAUSAL_FUNDAMENTAL','direction':d,'strength':_strength_from_units(roots),'background_bias':bg,'root_states':roots,'additive_unit':'CANONICAL_ROOT_FAMILY','static_background_cannot_refire_direction':True}

def structural_plane(rows,root_registry):
    roots=build_root_states(rows,root_registry,'STRUCTURAL_CARRY')
    d=_direction([{'effect_on_gold':r['direction']} for r in roots])
    return {'plane':'STRUCTURAL_CARRY','direction':d,'strength':_strength_from_units(roots),'root_states':roots,'session_direction_authority':False}

def transaction_plane(rows,contracts):
    cmap={c['fact_id']:c for c in contracts}
    groups=defaultdict(list)
    for r in rows:
        if r.get('pressure_plane')!='REALIZED_TRANSACTION' or r.get('resolution') not in ('RESOLVED','SEMANTICALLY_ADJUDICATED') or not r.get('horizon_active',True): continue
        cid=cmap[r['fact_id']].get('transaction_cluster_id') or ('FACT:'+r['fact_id'])
        groups[cid].append(r)
    clusters=[]
    for cid,rr in groups.items(): clusters.append({'cluster_id':cid,'direction':_direction(rr),'strength':max_strength([x.get('strength','UNKNOWN') for x in rr]),'facts':[x['fact_id'] for x in rr]})
    return {'plane':'REALIZED_TRANSACTION','direction':_direction([{'effect_on_gold':x['direction']} for x in clusters]),'strength':_strength_from_units(clusters),'clusters':clusters,'upstream_causal_authority':False}

def mechanical_plane(rows,contracts):
    cmap={c['fact_id']:c for c in contracts}; groups=defaultdict(list)
    for r in rows:
        if r.get('pressure_plane')!='MECHANICAL_FORCED' or r.get('resolution') not in ('RESOLVED','SEMANTICALLY_ADJUDICATED') or not r.get('horizon_active',True): continue
        cid=cmap[r['fact_id']].get('transaction_cluster_id') or ('FACT:'+r['fact_id']); groups[cid].append(r)
    clusters=[]
    for cid,rr in groups.items(): clusters.append({'cluster_id':cid,'direction':_direction(rr),'strength':max_strength([x.get('strength','UNKNOWN') for x in rr]),'facts':[x['fact_id'] for x in rr]})
    return {'plane':'MECHANICAL_FORCED','direction':_direction([{'effect_on_gold':x['direction']} for x in clusters]),'strength':_strength_from_units(clusters),'clusters':clusters,'can_rewrite_causal_pressure':False}
