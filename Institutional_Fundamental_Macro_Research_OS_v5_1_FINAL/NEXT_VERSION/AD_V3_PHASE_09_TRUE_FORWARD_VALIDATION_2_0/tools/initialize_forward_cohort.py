#!/usr/bin/env python3
from pathlib import Path
import sys,json
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P.parent))
from AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0.runtime.forward_ledger import load_state,save_state
from AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0.runtime.cohort_manager import ensure_cohort
s=load_state();s,c,created=ensure_cohort(s);save_state(s);print(json.dumps({'status':'PASS','cohort':c,'created':created,'predictions':len(s['predictions']),'outcomes':len(s['outcomes'])},ensure_ascii=False,indent=2))
