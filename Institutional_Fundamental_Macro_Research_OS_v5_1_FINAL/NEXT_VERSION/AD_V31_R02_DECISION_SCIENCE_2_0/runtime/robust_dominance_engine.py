from __future__ import annotations
from .common import cfg

IR={'UNKNOWN':0,'BACKGROUND':1,'SECONDARY':2,'PRIMARY':3,'SYSTEMIC':4};MR={'UNKNOWN':0,'MINOR':1,'MATERIAL':2,'LARGE':3,'EXTREME':4};HR={'UNKNOWN':0,'CRITICAL_GAP':0,'DEGRADED':1,'PARTIAL':2,'HEALTHY':3};FR={'UNKNOWN':0,'UNAVAILABLE':0,'PROVIDER_GAP':0,'PRIVATE_GAP':0,'PAID_GAP':0,'EXPIRED':0,'STALE_FOR_HORIZON':1,'CONTEXT_VALID':2,'FRESH_FOR_HORIZON':3,'FRESH_LIVE':3};QR={'UNKNOWN':0,'LOW':1,'MEDIUM':2,'HIGH':3};PR={'UNKNOWN':0,'REVERSING':0,'FADING':1,'NEW':2,'PERSISTENT':2,'BUILDING':3,'MATURE':3}
def _breadth(n):return 'NONE' if n<=0 else 'NARROW' if n==1 else 'MODERATE' if n==2 else 'BROAD'
def _vals(r,v):
    imp=IR.get(r.get('causal_importance'),0)
    if v.get('context_importance_cap') and r.get('freshness') not in ('FRESH_LIVE','FRESH_FOR_HORIZON'):imp=min(imp,IR['SECONDARY'])
    return {'importance':imp,'magnitude':MR.get(r.get('magnitude'),0),'health':HR.get((r.get('root_health') or {}).get('state'),0),'freshness':FR.get(r.get('freshness'),0),'quality':QR.get(r.get('evidence_quality'),0),'persistence':PR.get(r.get('persistence'),0)}
def compare(a,b,v):
    va,vb=_vals(a,v),_vals(b,v)
    if v.get('critical_gap_veto'):
        ac=(a.get('root_health') or {}).get('state')=='CRITICAL_GAP';bc=(b.get('root_health') or {}).get('state')=='CRITICAL_GAP'
        if ac!=bc:return -1 if ac else 1
    if abs(va['importance']-vb['importance'])>=int(v.get('importance_decisive_gap',2)):return 1 if va['importance']>vb['importance'] else -1
    if va['importance']==vb['importance'] and abs(va['magnitude']-vb['magnitude'])>=int(v.get('magnitude_decisive_gap',2)):return 1 if va['magnitude']>vb['magnitude'] else -1
    wins=sum(va[k]>vb[k] for k in va);loss=sum(va[k]<vb[k] for k in va);net=wins-loss
    margin=int(v.get('net_dimension_margin',2))
    return 1 if net>=margin else -1 if net<=-margin else 0
def _best(arr,v):
    if not arr:return None
    wins=[]
    for r in arr:
        w=sum(compare(r,o,v)>0 for o in arr if o is not r);l=sum(compare(r,o,v)<0 for o in arr if o is not r);wins.append((w-l,_vals(r,v)['importance'],_vals(r,v)['magnitude'],_vals(r,v)['health'],r.get('root_id'),r))
    return max(wins,key=lambda x:(x[0],x[1],x[2],x[3],str(x[4])))[-1]
def _primary_material_healthy(r):return IR.get(r.get('causal_importance'),0)>=IR['PRIMARY'] and MR.get(r.get('magnitude'),0)>=MR['MATERIAL'] and HR.get((r.get('root_health') or {}).get('state'),0)>=HR['PARTIAL']
def reconcile(roots,variant=None):
    v=variant or cfg('dominance_robustness_policy.json')['variants'][0];bull=[r for r in roots if r.get('direction')=='BULLISH_GOLD'];bear=[r for r in roots if r.get('direction')=='BEARISH_GOLD'];mixed=[r for r in roots if r.get('direction')=='MIXED'];bb=_best(bull,v);br=_best(bear,v)
    for r in roots:r['authority_rank_tuple']=[_vals(r,v)[k] for k in ('importance','magnitude','health','freshness','quality','persistence')]
    if mixed and not (bull or bear):return {'causal_direction':'MIXED','dominance_state':'BALANCED','dominant_root':mixed[0].get('root_id'),'supporting_roots':[],'opposing_roots':[x.get('root_id') for x in mixed],'contradiction':'BALANCED_CONFLICT','breadth':'NONE','variant_id':v['variant_id']}
    if not bb and not br:return {'causal_direction':'UNKNOWN','dominance_state':'UNKNOWN','dominant_root':None,'supporting_roots':[],'opposing_roots':[],'contradiction':'NONE','breadth':'NONE','variant_id':v['variant_id']}
    if bb and br:
        if _primary_material_healthy(bb) and _primary_material_healthy(br):
            return {'causal_direction':'MIXED','dominance_state':'BALANCED','dominant_root':None,'supporting_roots':[],'opposing_roots':[bb['root_id'],br['root_id']],'contradiction':'PRIMARY_ROOT_CONFLICT','breadth':'NONE','variant_id':v['variant_id']}
        if v.get('contradiction_strict') and IR.get(bb.get('causal_importance'),0)>=3 and IR.get(br.get('causal_importance'),0)>=3:
            return {'causal_direction':'MIXED','dominance_state':'BALANCED','dominant_root':None,'supporting_roots':[],'opposing_roots':[bb['root_id'],br['root_id']],'contradiction':'BALANCED_CONFLICT','breadth':'NONE','variant_id':v['variant_id']}
        c=compare(bb,br,v)
        if c==0:return {'causal_direction':'MIXED','dominance_state':'BALANCED','dominant_root':None,'supporting_roots':[],'opposing_roots':[bb['root_id'],br['root_id']],'contradiction':'BALANCED_CONFLICT','breadth':'NONE','variant_id':v['variant_id']}
        win,side=(bb,'BULLISH_GOLD') if c>0 else (br,'BEARISH_GOLD');support=bull if side=='BULLISH_GOLD' else bear;opp=bear if side=='BULLISH_GOLD' else bull
        return {'causal_direction':side,'dominance_state':'BULLISH_FRAGILE' if side=='BULLISH_GOLD' else 'BEARISH_FRAGILE','dominant_root':win['root_id'],'supporting_roots':[x['root_id'] for x in support if x['root_id']!=win['root_id']],'opposing_roots':[x['root_id'] for x in opp],'contradiction':'MEANINGFUL_CONTRADICTION','breadth':_breadth(len(support)),'variant_id':v['variant_id']}
    arr=bull or bear;side='BULLISH_GOLD' if bull else 'BEARISH_GOLD';win=bb or br
    return {'causal_direction':side,'dominance_state':'BULLISH_DOMINANT' if side=='BULLISH_GOLD' else 'BEARISH_DOMINANT','dominant_root':win['root_id'],'supporting_roots':[x['root_id'] for x in arr if x['root_id']!=win['root_id']],'opposing_roots':[],'contradiction':'MINOR_OFFSET' if mixed else 'NONE','breadth':_breadth(len(arr)),'variant_id':v['variant_id']}
