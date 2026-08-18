#!/usr/bin/env python3
import json,pathlib,sys
P=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(P.parent))
from AD_V3_PHASE_12_FINAL_CERTIFICATION_PRODUCTION_FREEZE.runtime.gates import collect
r,e=collect(False,False);q=e.get('R01') or {};print(json.dumps({'record_type':'AD_V3_P12_PROMOTION_PREVIEW','gate_results':r,'eligible_except_approval':all(v for k,v in r.items() if k!='EXPLICIT_OPERATOR_APPROVAL'),'promotion_performed':False,'evidence':{'sample_maturity':q.get('sample_maturity'),'forward_quality':q.get('forward_quality_state'),'coverage':q.get('coverage_state'),'critical_subgroups':q.get('critical_subgroup_state'),'production_qualification':q.get('production_qualification_state'),'qualifying_evaluated_episodes':q.get('qualifying_evaluated_episodes')}},ensure_ascii=False,indent=2))
