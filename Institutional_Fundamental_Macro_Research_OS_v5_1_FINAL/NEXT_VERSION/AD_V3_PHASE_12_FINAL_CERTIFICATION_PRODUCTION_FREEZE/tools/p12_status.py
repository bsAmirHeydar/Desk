#!/usr/bin/env python3
import json,pathlib,sys
P=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(P.parent))
from AD_V3_PHASE_12_FINAL_CERTIFICATION_PRODUCTION_FREEZE.runtime.status import status
print(json.dumps(status(),ensure_ascii=False,indent=2))
