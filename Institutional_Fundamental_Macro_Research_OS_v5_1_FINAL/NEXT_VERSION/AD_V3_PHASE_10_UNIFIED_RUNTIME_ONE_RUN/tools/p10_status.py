from __future__ import annotations
import json,pathlib,sys
HERE=pathlib.Path(__file__).resolve();PH=HERE.parents[1];NEXT=PH.parent;REPO=NEXT.parents[1];sys.path.insert(0,str(NEXT))
from AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN.runtime.runtime_status import status
if __name__=='__main__':print(json.dumps(status(REPO),indent=2,ensure_ascii=False))
