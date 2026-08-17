from __future__ import annotations
import json, pathlib, sys
PH=pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0,str(PH.parent))
from AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING.runtime.promotion import load_state
from AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING.runtime.commissioning import load_state as cstate
print(json.dumps({'phase':'AD-V3-P04','promotion':load_state(PH),'commissioning':cstate(PH)},indent=2,ensure_ascii=False))
