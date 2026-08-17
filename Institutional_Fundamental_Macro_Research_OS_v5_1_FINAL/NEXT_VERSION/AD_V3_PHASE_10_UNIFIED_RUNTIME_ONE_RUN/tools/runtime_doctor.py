from __future__ import annotations
import json,pathlib,sys,os
HERE=pathlib.Path(__file__).resolve();PH=HERE.parents[1];NEXT=PH.parent;REPO=NEXT.parents[1];sys.path.insert(0,str(NEXT))
from AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN.runtime.runtime_status import status
from AD_V3_PHASE_06_GOVERNED_SEMANTIC_INTELLIGENCE.runtime.semantic_model_host import host_status
r=status(REPO);r['model_host']=host_status(REPO);r['required_configs_ok']=all((PH/'config'/x).exists() for x in ['runtime_contract.json','route_policy.json','stage_dag.json','artifact_policy.json']);print(json.dumps(r,indent=2,ensure_ascii=False))
