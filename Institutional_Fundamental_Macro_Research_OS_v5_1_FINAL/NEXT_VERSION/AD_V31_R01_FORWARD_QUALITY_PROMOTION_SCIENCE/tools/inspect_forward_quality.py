#!/usr/bin/env python3
import json,pathlib,sys
P=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(P.parent))
from AD_V31_R01_FORWARD_QUALITY_PROMOTION_SCIENCE.runtime.qualification_engine import qualify
q=qualify();print(json.dumps(q,ensure_ascii=False,indent=2))
