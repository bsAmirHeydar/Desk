#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT.parent));from AD_V2_PHASE_07_D4_TRUE_FORWARD_PROMOTION.runtime.commissioning import receipt
p=argparse.ArgumentParser();p.add_argument('--promotion-decision',required=True);p.add_argument('--policy');p.add_argument('--operator-approved',action='store_true');a=p.parse_args();pol=json.loads(Path(a.policy or ROOT/'config/commissioning_policy.json').read_text());print(json.dumps(receipt(json.loads(Path(a.promotion_decision).read_text()),pol,operator_approved=a.operator_approved),indent=2))
