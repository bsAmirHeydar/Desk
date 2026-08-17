#!/usr/bin/env python3
import json,pathlib,sys
P=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(P.parent))
from AD_V3_PHASE_12_FINAL_CERTIFICATION_PRODUCTION_FREEZE.runtime.gates import collect
r,e=collect(False,False);print(json.dumps({'record_type':'AD_V3_P12_PROMOTION_PREVIEW','gate_results':r,'eligible_except_approval':all(v for k,v in r.items() if k!='EXPLICIT_OPERATOR_APPROVAL'),'promotion_performed':False,'evidence':{'forward_state':e.get('forward_state')}},ensure_ascii=False,indent=2))
