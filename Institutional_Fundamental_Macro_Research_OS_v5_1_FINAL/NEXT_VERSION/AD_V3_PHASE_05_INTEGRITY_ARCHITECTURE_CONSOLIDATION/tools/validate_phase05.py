#!/usr/bin/env python3
from pathlib import Path
import sys,json
P=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(P.parent))
from AD_V3_PHASE_05_INTEGRITY_ARCHITECTURE_CONSOLIDATION.runtime.integrity import compile_integrity
r=compile_integrity(False); print(json.dumps(r,ensure_ascii=False,indent=2)); raise SystemExit(0 if r['status']=='PASS' else 2)
