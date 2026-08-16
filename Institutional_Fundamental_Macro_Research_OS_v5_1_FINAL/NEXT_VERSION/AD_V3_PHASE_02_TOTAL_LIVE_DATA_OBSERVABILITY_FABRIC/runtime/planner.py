from __future__ import annotations
from .common import stable_id, iso

class PlanError(ValueError): pass

def build_plan(fact_registry:dict, source_registry:dict, horizon:str, as_of_utc:str|None=None):
    src={x['source_id']:x for x in source_registry['sources']}
    items=[]; source_ids=set()
    for c in fact_registry['contracts']:
        applicable=horizon in c.get('active_horizons',[]) or horizon=='ALL'
        item={
          'fact_id':c['fact_id'],'applicable':applicable,'acquisition_mode':c['acquisition_mode'],'must_attempt':bool(c['must_attempt_when_applicable'] and applicable),
          'source_ids':c['source_ids'],'block_on_unattempted':c['block_on_unattempted'],'block_on_failure':c['block_on_fetch_or_parse_failure_when_material'],
          'default_role':c['default_role'],'default_materiality':c['default_materiality'],'dependencies':c.get('dependencies',[])
        }
        if applicable and c['must_attempt_when_applicable']:
            for s in c['source_ids']:
                if s not in src: raise PlanError(f"unknown source {s} for {c['fact_id']}")
                source_ids.add(s)
        items.append(item)
    seed={'horizon':horizon,'as_of_utc':as_of_utc or iso(),'facts':[x['fact_id'] for x in items if x['applicable']]}
    return {'record_type':'AD_V3_P02_ACQUISITION_PLAN','plan_id':stable_id('P02PLAN',seed),'phase':'AD-V3-P02','subject':'XAUUSD','horizon':horizon,'as_of_utc':as_of_utc or iso(),'fact_items':items,'source_ids_to_attempt':sorted(source_ids)}
