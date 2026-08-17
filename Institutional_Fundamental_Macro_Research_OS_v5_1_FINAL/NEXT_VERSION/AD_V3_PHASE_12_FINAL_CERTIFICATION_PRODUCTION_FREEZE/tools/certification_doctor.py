#!/usr/bin/env python3
import json,pathlib,sys
P=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(P.parent))
from AD_V3_PHASE_12_FINAL_CERTIFICATION_PRODUCTION_FREEZE.runtime.status import status
s=status();print(json.dumps({'status':'PASS' if s.get('implementation_status')=='PASS' and s.get('science_freeze')=='PASS' and s.get('runtime_freeze')=='PASS' and s.get('report_freeze')=='PASS' else 'FAIL','certification':s},ensure_ascii=False,indent=2));raise SystemExit(0 if s.get('implementation_status')=='PASS' else 2)
