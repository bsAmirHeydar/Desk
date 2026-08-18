from __future__ import annotations
from collections import Counter
from .common import cfg

VALID={'FRESH_LIVE','FRESH_FOR_HORIZON','CONTEXT_VALID'};CURRENT={'FRESH_LIVE','FRESH_FOR_HORIZON'};GAPS={'UNAVAILABLE','PROVIDER_GAP','PRIVATE_GAP','PAID_GAP','EXPIRED'}
def _resolved(r):return bool(r and r.get('resolution') in ('RESOLVED','SEMANTICALLY_ADJUDICATED','ACCOUNTED_NON_DIRECTIONAL','ACCOUNTED_HORIZON_INACTIVE','ACCOUNTED_REQUIRES_SEMANTIC'))
def assess(root_id,expected_facts,rows,freshness_by_fact,contract_map,fact_magnitudes,current_direction='UNKNOWN'):
    pol=cfg('root_health_policy.json'); reg=cfg('root_critical_evidence_registry.json')['roots'].get(root_id,{'required_any_of':[],'independence_groups':{}}); rmap={r.get('fact_id'):r for r in rows};counts=Counter();resolved=0;direct=0;proxy=0;semantic=0;mag=0;groups=set();observed=[]
    for fid in expected_facts:
        row=rmap.get(fid);has_obs=bool(row and row.get('observation_id'));fr=freshness_by_fact.get(fid,'UNKNOWN') if has_obs else 'UNKNOWN';counts['total']+=1
        if has_obs:counts['observed']+=1;observed.append(fid)
        if _resolved(row):resolved+=1
        if fr in CURRENT:counts['current']+=1
        elif fr=='CONTEXT_VALID':counts['context']+=1
        elif fr=='STALE_FOR_HORIZON':counts['stale']+=1
        elif fr=='EXPIRED':counts['expired']+=1
        elif fr in GAPS:counts['gap']+=1
        else:counts['unknown']+=1
        c=contract_map.get(fid,{})
        dr=c.get('p02_directness')
        if dr=='DIRECT':direct+=1
        elif dr in ('PROXY','DERIVED','PAID_GAP'):proxy+=1
        if row and (row.get('reason_code')=='SEMANTIC_ADJUDICATION_REQUIRED' or row.get('resolution')=='SEMANTICALLY_ADJUDICATED'):semantic+=1
        fm=(fact_magnitudes or {}).get(fid) or {}
        if fm.get('state') not in (None,'UNKNOWN'):mag+=1
        if row and row.get('observation_id'):
            groups.add(reg.get('independence_groups',{}).get(fid,fid))
    missing=[]
    for group in reg.get('required_any_of') or []:
        ok=False
        for fid in group:
            row=rmap.get(fid);fr=freshness_by_fact.get(fid,'UNKNOWN')
            if row and _resolved(row) and row.get('effect_on_gold') not in ('UNKNOWN',None) and fr in VALID:ok=True;break
        if not ok:missing.append(group)
    n=max(1,len(expected_facts));valid=(counts['current']+counts['context'])/n;bad=(counts['stale']+counts['expired']+counts['gap']+counts['unknown'])/n;resolved_share=resolved/n;direct_share=direct/n;proxy_share=proxy/n;mag_share=mag/n
    active=current_direction in ('BULLISH_GOLD','BEARISH_GOLD','MIXED')
    if counts['observed']==0:state='UNKNOWN'
    elif active and missing:state='CRITICAL_GAP'
    elif valid<.40 or bad>float(pol['thresholds']['degraded_max_unknown_or_gap_share']):state='DEGRADED'
    elif valid<float(pol['thresholds']['healthy_min_valid_share']) or proxy_share>=float(pol['thresholds']['proxy_heavy_share']) or (active and mag_share<.50):state='PARTIAL'
    else:state='HEALTHY'
    if counts['current']/n>=.5:fresh='FRESH_FOR_HORIZON'
    elif valid>=.5:fresh='CONTEXT_VALID'
    elif counts['stale']>0:fresh='STALE_FOR_HORIZON'
    else:fresh='UNKNOWN'
    if direct and not proxy:directness='DIRECT'
    elif proxy and not direct:directness='PROXY_ONLY'
    elif proxy_share>=.5:directness='PROXY_HEAVY'
    elif direct or proxy:directness='MIXED'
    else:directness='UNKNOWN'
    if direct_share>=.75 and resolved_share>=.75:quality='HIGH'
    elif resolved_share>=.5:quality='MEDIUM'
    elif counts['observed']>0:quality='LOW'
    else:quality='UNKNOWN'
    return {'state':state,'expected_evidence_count':len(expected_facts),'observed_evidence_count':counts['observed'],'resolved_evidence_count':resolved,'current_evidence_count':counts['current'],'context_evidence_count':counts['context'],'stale_evidence_count':counts['stale'],'expired_evidence_count':counts['expired'],'gap_evidence_count':counts['gap'],'unknown_evidence_count':counts['unknown'],'valid_share':round(valid,4),'unknown_or_gap_share':round(bad,4),'direct_evidence_count':direct,'proxy_evidence_count':proxy,'directness_state':directness,'semantic_evidence_count':semantic,'magnitude_covered_count':mag,'magnitude_coverage_share':round(mag_share,4),'critical_evidence_missing':missing,'critical_evidence_present':not missing,'independent_evidence_count':len(groups),'same_shock_manifestation_count':max(0,counts['observed']-len(groups)),'freshness_summary':fresh,'evidence_quality_summary':quality,'direction_authority':False}
