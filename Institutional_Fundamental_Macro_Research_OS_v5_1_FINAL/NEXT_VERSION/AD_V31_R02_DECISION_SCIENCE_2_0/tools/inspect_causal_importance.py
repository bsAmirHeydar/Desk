#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P.parent))
from AD_V31_R02_DECISION_SCIENCE_2_0.runtime.causal_importance_engine import importance
from AD_V31_R02_DECISION_SCIENCE_2_0.runtime.common import cfg
ap=argparse.ArgumentParser();ap.add_argument('--root');ap.add_argument('--horizon',default='SESSION_1_6H');ap.add_argument('--regime',default='NORMAL');a=ap.parse_args();roots=[a.root] if a.root else sorted(cfg('causal_importance_matrix.json')['matrix'])
print(json.dumps({'horizon':a.horizon,'regime':a.regime,'roots':[importance(r,a.horizon,a.regime) for r in roots]},indent=2,ensure_ascii=False))
