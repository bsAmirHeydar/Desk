from collections import defaultdict
from .util import parse_utc

CLASS_MAP={
 'OBSERVED_FACT':'DIRECT_OBSERVATION','OBSERVED_MARKET_DATA':'DIRECT_OBSERVATION','OFFICIAL_REPORTED_FACT':'SOURCE_REPORT','CONTRACTUAL_FACT':'SOURCE_REPORT','IDENTIFIED_FLOW_FACT':'DIRECT_OBSERVATION','IDENTIFIED_POSITIONING_FACT':'DIRECT_OBSERVATION','MARKET_IMPLIED_FACT':'MEASUREMENT','PUBLIC_PROXY':'PROXY','DERIVED_FACT':'DERIVED','MODEL_INFERENCE':'MODEL_OUTPUT','NARRATIVE_INFERENCE':'NARRATIVE','SCENARIO_ASSUMPTION':'CONTEXTUAL'
}

def adapt_fact(f):
    src=f.get('source') or {}; tm=f.get('time') or {}
    root=f.get('release_family_id') or src.get('root_source_id') or src.get('source_id') or f.get('root_cause_id')
    value=None
    for k in ('value','observed_value','current_value','numeric_value'):
        if k in f: value=f.get(k); break
    return {
      'evidence_id':str(f.get('fact_id') or f.get('evidence_id') or 'UNNAMED'),
      'evidence_class':CLASS_MAP.get(f.get('primary_class'),'CONTEXTUAL'),
      'availability_state':f.get('availability_state','UNDETERMINED'),
      'materiality':f.get('decision_materiality','CONTEXTUAL'),
      'source_id':src.get('source_id'),'root_source_id':root,'dataset_id':src.get('dataset_id'),
      'publication_time':tm.get('publication_time'),'first_available_time':tm.get('first_available_time') or tm.get('first_seen_time'),'first_seen_time':tm.get('first_seen_time'),'ingestion_time':tm.get('ingestion_time'),
      'value':value,'proxy_contract_id':f.get('proxy_contract_id'),'model_version':f.get('derivation_method_version') if f.get('primary_class')=='MODEL_INFERENCE' else None,
      'original_primary_class':f.get('primary_class')
    }

def adapt_decision_evidence_pack(pack): return [adapt_fact(x) for x in (pack or {}).get('fact_records',[])]

def dependency_graph(run_id,evidence):
    groups=defaultdict(list)
    for e in evidence:
        root=e.get('root_source_id') or e.get('dataset_id') or e.get('source_id') or ('UNRESOLVED:'+e.get('evidence_id','?'))
        groups[str(root)].append(str(e.get('evidence_id')))
    rows=[]
    for root,ids in sorted(groups.items()):
        typ='INDEPENDENT_ROOT' if len(ids)==1 else 'COMMON_ROOT'
        if root.startswith('UNRESOLVED:'): typ='UNKNOWN'
        rows.append({'root_id':root,'evidence_ids':ids,'dependency_type':typ})
    return {'schema_version':'1.0.0','run_id':run_id,'nominal_count':len(evidence),'independent_root_count':len(groups),'groups':rows,'pseudo_independence_found':any(len(x['evidence_ids'])>1 and x['dependency_type']!='UNKNOWN' for x in rows)}

def time_after_cutoff(e, cutoff):
    c=parse_utc(cutoff); bad=[]
    if c is None: return ['INVALID_CUTOFF']
    for k in ('publication_time','first_available_time','first_seen_time'):
        d=parse_utc(e.get(k))
        if d is not None and d>c: bad.append(k)
    return bad
