#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P.parent))
from AD_V31_R02_DECISION_SCIENCE_2_0.runtime.common import cfg
ap=argparse.ArgumentParser();ap.add_argument('--root',required=True);a=ap.parse_args();r=cfg('root_critical_evidence_registry.json')['roots'].get(a.root)
print(json.dumps({'root_id':a.root,'critical_evidence_registry':r,'policy':cfg('root_health_policy.json')},indent=2,ensure_ascii=False));raise SystemExit(0 if r else 2)
