#!/usr/bin/env python3
from pathlib import Path
import sys,json
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P.parent))
from AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0.runtime.legacy_migration import audit_legacy
print(json.dumps(audit_legacy(),ensure_ascii=False,indent=2))
