from __future__ import annotations
import json,sys
from pathlib import Path
HERE=Path(__file__).resolve(); PH=HERE.parents[1]; NEXT=PH.parent
if str(NEXT) not in sys.path: sys.path.insert(0,str(NEXT))
from AD_V31_R05_OPERATIONS_HUMAN_INTELLIGENCE_FINALIZATION.runtime.r05_freeze import build
from AD_V31_R05_OPERATIONS_HUMAN_INTELLIGENCE_FINALIZATION.runtime.common import atomic_json
m=build(); atomic_json(PH/'qualification/R05_IMPLEMENTATION_FREEZE.json',m); print(json.dumps(m,ensure_ascii=False,indent=2))
