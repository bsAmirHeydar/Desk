from __future__ import annotations
from .common import cfg
from .historical_normalizer import normalize

def _entries():return {x['fact_id']:x for x in cfg('magnitude_method_registry.json')['entries']}
def _rank():return cfg('magnitude_threshold_policy.json')['rank']
def _band(x,profile):
    p=cfg('magnitude_threshold_policy.json')['profiles'][profile];a=abs(float(x))
    if a>=p['EXTREME_min_abs']:return 'EXTREME'
    if a>=p['LARGE_min_abs']:return 'LARGE'
    if a>=p['MATERIAL_min_abs']:return 'MATERIAL'
    return 'MINOR'
def _standardized(details):
    for k in ('z_score','surprise_z','normalized_change_z'):
        if isinstance(details.get(k),(int,float)):return _band(details[k],'GENERIC_Z'),'STANDARDIZED_NUMERIC_FIELD:'+k,{'normalized_value':float(details[k])}
    for k in ('historical_percentile','percentile'):
        v=details.get(k)
        if isinstance(v,(int,float)):
            q=float(v);a=max(q,1-q)
            st='EXTREME' if a>=.99 else 'LARGE' if a>=.95 else 'MATERIAL' if a>=.80 else 'MINOR'
            return st,'HISTORICAL_PERCENTILE:'+k,{'percentile':q}
    return None

def fact_magnitude(row,history=None,as_of=None):
    fid=row.get('fact_id');ent=_entries().get(fid);d=row.get('details') or {}
    if not ent:return {'fact_id':fid,'state':'UNKNOWN','source':'NO_METHOD_REGISTRY','status':'UNKNOWN_MAGNITUDE','temporal_role':'UNKNOWN'}
    std=_standardized(d)
    if std and ent['status'] not in ('NOT_APPLICABLE',):
        st,src,diag=std;return {'fact_id':fid,'state':st,'source':src,'status':ent['status'],'method':ent['method'],'temporal_role':ent['temporal_role'],'diagnostic':diag}
    method=ent['method'];state='UNKNOWN';src=method;diag={}
    if ent['status']=='NOT_APPLICABLE':return {'fact_id':fid,'state':'UNKNOWN','source':method,'status':'NOT_APPLICABLE','method':method,'temporal_role':ent['temporal_role'],'diagnostic':{}}
    if method=='DETAIL_BPS_CHANGE':
        v=d.get(ent.get('detail_field'))
        if isinstance(v,(int,float)):
            bp=float(v)*100.0;state=_band(bp,ent['threshold_profile']);diag={'raw_change':float(v),'basis_points':bp}
        else:src+=':MISSING_DETAIL'
    elif method=='DETAIL_ABS_CHANGE':
        v=d.get(ent.get('detail_field'))
        if isinstance(v,(int,float)):
            state=_band(v,ent['threshold_profile']);diag={'raw_change':float(v)}
        else:src+=':MISSING_DETAIL'
    elif method=='HISTORY_NORMALIZED_DETAIL':
        v=d.get(ent.get('detail_field'))
        if isinstance(v,(int,float)):
            h=(history or {}).get(fid,[]) if isinstance(history,dict) else []
            norm=normalize(float(v),h,as_of)
            diag=norm
            if norm['state']=='AVAILABLE':state=_band(norm['z_score'],'GENERIC_Z');src+=':POINT_IN_TIME_Z'
            else:src+=':'+norm['state']
        else:src+=':MISSING_DETAIL'
    elif method=='VALIDATED_SEMANTIC_BAND':
        v=d.get('magnitude_band')
        if row.get('resolution')=='SEMANTICALLY_ADJUDICATED' and v in cfg('magnitude_threshold_policy.json')['semantic_states_allowed']:
            state=v;diag={'semantic_categorical_only':True}
        else:src+=':NO_VALIDATED_MAGNITUDE_BAND'
    elif method in ('STRUCTURAL_CONTEXT_ONLY','CONTEXT_ONLY'):
        src+=':NO_CURRENT_IMPULSE_AUTHORITY'
    else:src+=':UNSUPPORTED_CURRENT_INPUT'
    return {'fact_id':fid,'state':state,'source':src,'status':ent['status'],'method':method,'data_family':ent['data_family'],'temporal_role':ent['temporal_role'],'diagnostic':diag,'direction_inferred':False}

def root_magnitude(root,rows,history=None,as_of=None):
    facts=[fact_magnitude(r,history,as_of) for r in rows]
    current=[x for x in facts if x.get('temporal_role') in ('CURRENT_IMPULSE','SLOW_IMPULSE') and x['state']!='UNKNOWN']
    if not current:
        context=[x for x in facts if x.get('temporal_role')=='STRUCTURAL_CONTEXT' and x['state']!='UNKNOWN']
        return {'state':'UNKNOWN','source':'NO_SUPPORTED_CURRENT_IMPULSE_MAGNITUDE','temporal_role':'STRUCTURAL_CONTEXT' if context else 'UNKNOWN','fact_magnitudes':facts,'normalized_fact_count':sum(1 for x in facts if 'POINT_IN_TIME_Z' in x.get('source',''))}
    r=_rank();best=max(current,key=lambda x:r.get(x['state'],0))
    return {'state':best['state'],'source':best['source'],'temporal_role':best.get('temporal_role'),'fact_magnitudes':facts,'normalized_fact_count':sum(1 for x in facts if 'POINT_IN_TIME_Z' in x.get('source',''))}
