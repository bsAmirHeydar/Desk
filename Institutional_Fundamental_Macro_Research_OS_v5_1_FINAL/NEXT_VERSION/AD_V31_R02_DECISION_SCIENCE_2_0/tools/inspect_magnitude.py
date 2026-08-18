#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P.parent))
from AD_V31_R02_DECISION_SCIENCE_2_0.runtime.magnitude_engine import fact_magnitude
from AD_V31_R02_DECISION_SCIENCE_2_0.runtime.common import cfg
ap=argparse.ArgumentParser();ap.add_argument('--fact-id');a=ap.parse_args()
entries=cfg('magnitude_method_registry.json')['entries'];sel=[x for x in entries if not a.fact_id or x['fact_id']==a.fact_id]
print(json.dumps({'policy_version':cfg('magnitude_threshold_policy.json').get('schema_version'),'facts':[{'registry':x,'example_without_inputs':fact_magnitude({'fact_id':x['fact_id'],'details':{}})} for x in sel]},indent=2,ensure_ascii=False))
