from __future__ import annotations
from .common import config

def _vec(r):
    pol=config('dominance_policy.json'); ranks=pol['ordinal_ranks']; return tuple(ranks[k].get(r.get(k if k!='quality' else 'evidence_quality','UNKNOWN'),0) for k in pol['authority_vector_order'])
def _breadth(n): return 'NONE' if n<=0 else 'NARROW' if n==1 else 'MODERATE' if n==2 else 'BROAD'
def _primary_material(r):
    pol=config('dominance_policy.json')['ordinal_ranks']; return r.get('causal_importance')=='PRIMARY' and pol['magnitude'].get(r.get('magnitude'),0)>=2 and pol['freshness'].get(r.get('freshness'),0)>=2

def reconcile(roots):
    bull=[r for r in roots if r.get('direction')=='BULLISH_GOLD']; bear=[r for r in roots if r.get('direction')=='BEARISH_GOLD']; mixed=[r for r in roots if r.get('direction')=='MIXED']
    for r in roots:r['authority_rank_tuple']=list(_vec(r))
    bb=max(bull,key=_vec) if bull else None; br=max(bear,key=_vec) if bear else None
    if mixed and not (bull or bear): return {'causal_direction':'MIXED','dominance_state':'BALANCED','dominant_root':mixed[0]['root_id'],'supporting_roots':[],'opposing_roots':[x['root_id'] for x in mixed],'contradiction':'BALANCED_CONFLICT','breadth':'NONE'}
    if not bull and not bear:return {'causal_direction':'UNKNOWN','dominance_state':'UNKNOWN','dominant_root':None,'supporting_roots':[],'opposing_roots':[],'contradiction':'NONE','breadth':'NONE'}
    if bb and br:
        if _primary_material(bb) and _primary_material(br):
            return {'causal_direction':'MIXED','dominance_state':'BALANCED','dominant_root':None,'supporting_roots':[],'opposing_roots':[bb['root_id'],br['root_id']],'contradiction':'PRIMARY_ROOT_CONFLICT','breadth':'NONE'}
        vb,vr=_vec(bb),_vec(br)
        if vb==vr:
            return {'causal_direction':'MIXED','dominance_state':'BALANCED','dominant_root':None,'supporting_roots':[],'opposing_roots':[bb['root_id'],br['root_id']],'contradiction':'BALANCED_CONFLICT','breadth':'NONE'}
        win,lose,side=(bb,br,'BULLISH_GOLD') if vb>vr else (br,bb,'BEARISH_GOLD')
        support=bull if side=='BULLISH_GOLD' else bear; opp=bear if side=='BULLISH_GOLD' else bull
        return {'causal_direction':side,'dominance_state':'BULLISH_FRAGILE' if side=='BULLISH_GOLD' else 'BEARISH_FRAGILE','dominant_root':win['root_id'],'supporting_roots':[x['root_id'] for x in support if x['root_id']!=win['root_id']],'opposing_roots':[x['root_id'] for x in opp],'contradiction':'MEANINGFUL_CONTRADICTION','breadth':_breadth(len(support))}
    side='BULLISH_GOLD' if bull else 'BEARISH_GOLD'; arr=bull or bear; win=max(arr,key=_vec)
    return {'causal_direction':side,'dominance_state':'BULLISH_DOMINANT' if side=='BULLISH_GOLD' else 'BEARISH_DOMINANT','dominant_root':win['root_id'],'supporting_roots':[x['root_id'] for x in arr if x['root_id']!=win['root_id']],'opposing_roots':[],'contradiction':'MINOR_OFFSET' if mixed else 'NONE','breadth':_breadth(len(arr))}
