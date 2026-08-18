#!/usr/bin/env python3
from pathlib import Path
import json,sys
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P.parent))
from AD_V31_R02_DECISION_SCIENCE_2_0.runtime.status import status
print(json.dumps({'note':'Run-time decision robustness is stored in the latest P08 decision; variant frequencies are diagnostics, not probabilities.','status':status()},indent=2,ensure_ascii=False))
