#!/usr/bin/env python3
from pathlib import Path
import argparse, importlib.util, json, sys

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--repo-root',required=True); ap.add_argument('--json',action='store_true'); a=ap.parse_args()
    repo=Path(a.repo_root).resolve(); vault=repo/'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL'
    p=vault/'RUNTIME/Unified Research Interface/alpha_interface_runtime/result.py'
    spec=importlib.util.spec_from_file_location('v1_result_probe',p); mod=importlib.util.module_from_spec(spec)
    # result.py uses relative import, so source-text probe is more deterministic and avoids importing the whole V1 package.
    src=p.read_text(encoding='utf-8')
    checks={
      'force_can_fallback_to_driver_state': "first(driver,'force','strength','state'" in src,
      'consumption_ignores_lifecycle_state': "'lifecycle_state'" not in src.split('def _lifecycle',1)[1].split('def build',1)[0],
      'remaining_can_fallback_to_asymmetry': "'remaining_pressure','remaining_asymmetry'" in src,
      'persistence_can_query_driver': "default=first(driver,'persistence','persistence_state'" in src,
    }
    ok=all(checks.values())
    out={'status':'PASS' if ok else 'FAIL','meaning':'Known closed-V1 semantic ambiguity reproduced; P01 does not mutate it.','checks':checks}
    print(json.dumps(out,indent=2) if a.json else ('LEGACY V1 DEFECT PROBE: '+out['status']))
    return 0 if ok else 3
if __name__=='__main__': sys.exit(main())
