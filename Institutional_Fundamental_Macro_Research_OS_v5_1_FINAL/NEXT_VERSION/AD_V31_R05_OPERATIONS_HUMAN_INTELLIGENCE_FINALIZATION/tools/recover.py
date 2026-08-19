#!/usr/bin/env python3
from pathlib import Path
import json,sys
P=Path(__file__).resolve().parents[1];NEXT=P.parent;REPO=NEXT.parents[1];sys.path.insert(0,str(NEXT))
from AD_V31_R05_OPERATIONS_HUMAN_INTELLIGENCE_FINALIZATION.runtime.recovery import recover
print(json.dumps(recover(REPO),ensure_ascii=False,indent=2))
