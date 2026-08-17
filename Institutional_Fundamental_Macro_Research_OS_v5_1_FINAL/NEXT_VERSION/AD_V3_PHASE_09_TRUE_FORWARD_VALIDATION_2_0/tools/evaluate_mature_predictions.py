#!/usr/bin/env python3
from pathlib import Path
import sys,json
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P.parent))
from AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0.runtime.forward_runtime import observe_and_evaluate
r=observe_and_evaluate(P,None);print(json.dumps({'new_outcomes':r['new_outcomes'],'statistics':r['statistics']},ensure_ascii=False,indent=2))
