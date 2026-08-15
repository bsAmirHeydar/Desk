#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT.parent));from AD_V2_PHASE_07_D4_TRUE_FORWARD_PROMOTION.runtime.promotion import evaluate
p=argparse.ArgumentParser();p.add_argument('--report',required=True);p.add_argument('--policy');p.add_argument('--validator-approved',action='store_true');p.add_argument('--existing-d4-promoted-rule',action='store_true');a=p.parse_args();pol=json.loads(Path(a.policy or ROOT/'config/promotion_policy.json').read_text());r=evaluate(json.loads(Path(a.report).read_text()),pol,independent_validator_approved=a.validator_approved,existing_d4_promoted_rule=a.existing_d4_promoted_rule);print(json.dumps(r,indent=2))
