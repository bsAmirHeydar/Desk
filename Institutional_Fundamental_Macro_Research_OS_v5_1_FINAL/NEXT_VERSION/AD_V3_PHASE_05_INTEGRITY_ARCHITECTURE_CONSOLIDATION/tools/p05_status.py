#!/usr/bin/env python3
from pathlib import Path
import sys,json
P=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(P.parent))
from AD_V3_PHASE_05_INTEGRITY_ARCHITECTURE_CONSOLIDATION.runtime.integrity import compile_integrity
r=compile_integrity(False)
out={'phase':r['phase'],'version':r['version'],'status':r['status'],'scientific_surface_status':r['scientific_surface_status'],'deployment_surface_status':r['deployment_surface_status'],'counts':r['counts'],'v3_state':r['expected_v3_state'],'v3_promotion_performed':False,'trade_execution_authority':'NONE','drift_counts':{'architecture':len(r['architecture_drift']),'freeze':len(r['freeze_conflicts']),'metadata':len(r['registry_metadata_drift']),'command':len(r['command_contract_drift']),'promotion':len(r['promotion_gate_drift']),'artifact':len(r['artifact_governance_errors']),'science':len(r['science_drift'])}}
print(json.dumps(out,ensure_ascii=False,indent=2)); raise SystemExit(0 if r['status']=='PASS' else 2)
