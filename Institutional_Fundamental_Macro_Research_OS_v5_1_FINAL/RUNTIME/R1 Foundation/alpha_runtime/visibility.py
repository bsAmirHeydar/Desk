from .timeutil import parse_aware, utc_now
from .canonical import sha256_obj

STRICT={"ORIGINAL_CAPTURE","OFFICIAL_VINTAGE_ARCHIVE"}; LIMITED={"RECONSTRUCTED_WITH_PROVENANCE"}

def replay_admissibility(snapshot,mode):
    v=snapshot.get('vintage_integrity','UNDETERMINED')
    if mode in ('LIVE','SHADOW_LIVE'):
        return 'STRICT_ADMISSIBLE' if v!='UNDETERMINED' else 'UNDETERMINED'
    if v in STRICT: return 'STRICT_ADMISSIBLE'
    if v in LIMITED: return 'LIMITED_ADMISSIBLE'
    if v=='CURRENT_ONLY': return 'FORBIDDEN'
    return 'UNDETERMINED'

def visible(snapshot,cutoff,mode):
    try: fa=parse_aware(snapshot['first_available_time']); co=parse_aware(cutoff)
    except Exception: return False,'UNDETERMINED_TIME'
    try:
        pub=parse_aware(snapshot['publication_time']) if snapshot.get('publication_time') else None
        ret=parse_aware(snapshot['retrieved_at']) if snapshot.get('retrieved_at') else None
        ing=parse_aware(snapshot['ingested_at']) if snapshot.get('ingested_at') else None
        if pub and fa < pub: return False,'TEMPORAL_ORDER_INVALID'
        if ret and ret < fa: return False,'TEMPORAL_ORDER_INVALID'
        if ing and ret and ing < ret: return False,'TEMPORAL_ORDER_INVALID'
    except Exception: return False,'UNDETERMINED_TIME'
    if fa>co: return False,'INVISIBLE_FUTURE'
    if mode in ('LIVE','SHADOW_LIVE'):
        try:
            if snapshot.get('retrieved_at') and parse_aware(snapshot['retrieved_at'])>co: return False,'NOT_RETRIEVED_AT_CUTOFF'
            if snapshot.get('ingested_at') and parse_aware(snapshot['ingested_at'])>co: return False,'NOT_INGESTED_AT_CUTOFF'
        except Exception: return False,'UNDETERMINED_RETRIEVAL_TIME'
    adm=replay_admissibility(snapshot,mode)
    if mode not in ('LIVE','SHADOW_LIVE') and adm!='STRICT_ADMISSIBLE': return False,('FORBIDDEN_VINTAGE' if adm=='FORBIDDEN' else 'LIMITED_OR_UNDETERMINED_VINTAGE')
    sup=snapshot.get('superseded_at')
    if sup and parse_aware(sup)<=co: return False,'SUPERSEDED_AT_CUTOFF'
    return True,'VISIBLE'

def build_receipt(run_id,cutoff,mode,requirements,snapshots):
    byreq={}
    for s in snapshots: byreq.setdefault(s.get('requirement_id'),[]).append(s)
    rows=[]
    for r in requirements:
        rid=r['requirement_id']; apps=r.get('applicability','APPLICABLE')
        candidates=byreq.get(rid,[])
        evals=[]
        for s in candidates:
            ok,reason=visible(s,cutoff,mode); evals.append({"snapshot_id":s.get('snapshot_id'),"artifact_hash":s.get('artifact_hash'),"visible":ok,"reason":reason,"first_available_time":s.get('first_available_time'),"vintage_id":s.get('vintage_id'),"vintage_integrity":s.get('vintage_integrity')})
        visible_candidates=[s for s in candidates if visible(s,cutoff,mode)[0]]
        visible_candidates.sort(key=lambda s: parse_aware(s['first_available_time']))
        selected=visible_candidates[-1] if visible_candidates else None
        if apps=='NOT_APPLICABLE': status='NOT_APPLICABLE'; selected=None
        elif selected: status='PRESENT'
        elif candidates: status='UNAVAILABLE_AT_CUTOFF'
        else: status='UNAVAILABLE'
        rows.append({"requirement_id":rid,"fact_family":r.get('fact_family'),"materiality":r.get('materiality'),"applicability":apps,"status":status,"selected_snapshot_id":selected.get('snapshot_id') if selected else None,"selected_artifact_hash":selected.get('artifact_hash') if selected else None,"candidate_evaluations":evals})
    receipt={"schema_version":"1.0.0","run_id":run_id,"analysis_cutoff_utc":cutoff,"lookahead_policy":"STRICT_POINT_IN_TIME","requirements":rows,"created_at_utc":utc_now()}
    hash_basis=dict(receipt); hash_basis.pop('created_at_utc',None); receipt['receipt_hash']=sha256_obj(hash_basis)
    return receipt
