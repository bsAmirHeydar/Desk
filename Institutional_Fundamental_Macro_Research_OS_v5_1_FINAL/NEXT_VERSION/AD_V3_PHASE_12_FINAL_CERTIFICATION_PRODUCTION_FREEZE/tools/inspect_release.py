#!/usr/bin/env python3
import json,pathlib,sys
P=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(P.parent))
from AD_V3_PHASE_12_FINAL_CERTIFICATION_PRODUCTION_FREEZE.runtime.common import load,git_commit
from AD_V3_PHASE_12_FINAL_CERTIFICATION_PRODUCTION_FREEZE.runtime.status import status
print(json.dumps({'release':load(P/'release/ALPHA_DESK_V3_FINAL_RELEASE_MANIFEST.json',{}),'current_git_commit':git_commit(),'status':status()},ensure_ascii=False,indent=2))
