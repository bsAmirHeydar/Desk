#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys
try:
    import jsonschema
except Exception:
    jsonschema=None
p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--schema',default=None);a=p.parse_args()
mod=Path(__file__).resolve().parent.parent
schema=Path(a.schema) if a.schema else mod/'schemas/AlphaLab_Cognitive_Input.schema.json'
try: data=json.loads(Path(a.input).read_text(encoding='utf-8')); sch=json.loads(schema.read_text(encoding='utf-8'))
except Exception as e: print(json.dumps({'status':'FAIL','errors':[str(e)]},indent=2));sys.exit(2)
errors=[]
if jsonschema:
    try:
        reg=jsonschema.validators.validator_for(sch)
        reg.check_schema(sch)
        resolver=jsonschema.RefResolver(base_uri=(mod/'schemas').resolve().as_uri()+'/', referrer=sch)
        jsonschema.validate(data,sch,resolver=resolver)
    except Exception as e: errors.append('SCHEMA: '+str(e))
# semantic guards beyond JSON Schema
hs=data.get('hypothesis_set') or {}; hyps=hs.get('hypotheses') or []
if len(hyps)==1 and not hs.get('single_hypothesis_justification'):errors.append('Single-hypothesis run requires explicit rival-search justification.')
if len(hyps)>6:errors.append('More than six active hypotheses is disallowed in the production cognitive pack; merge near-duplicates or move weak ideas to context.')
ids=[h.get('hypothesis_id') for h in hyps]
if len(ids)!=len(set(ids)):errors.append('Duplicate hypothesis_id.')
sc=((data.get('scenario_tree') or {}).get('scenarios') or [])
if len(sc)<2:errors.append('Scenario tree requires at least two explicit paths.')
if (data.get('scenario_tree') or {}).get('numeric_probabilities_used') is not False:errors.append('Numeric scenario probabilities are not authorized.')
if (data.get('uncertainty_profile') or {}).get('single_confidence_score_used') is not False:errors.append('Single confidence score is not the V21 production uncertainty representation.')
if (data.get('meta_edge_router') or {}).get('outside_strategy_permission_effect')!='NONE':errors.append('Outside-strategy edges cannot affect Fundamental permission.')
print(json.dumps({'status':'PASS' if not errors else 'FAIL','errors':errors},indent=2));sys.exit(0 if not errors else 2)
