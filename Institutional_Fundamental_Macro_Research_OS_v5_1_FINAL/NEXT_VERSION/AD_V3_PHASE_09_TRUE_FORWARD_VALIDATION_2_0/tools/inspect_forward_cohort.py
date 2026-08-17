#!/usr/bin/env python3
from pathlib import Path
import sys,json
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P.parent))
from AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0.runtime.forward_runtime import status
r=status(P);print(json.dumps({'active_cohort':r['active_cohort'],'statistics':r['statistics'],'legacy':r['legacy'],'promotion_gate_satisfied':r['promotion_gate_satisfied']},ensure_ascii=False,indent=2))
