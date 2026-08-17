#!/usr/bin/env python3
from pathlib import Path
import sys,json
P=Path(__file__).resolve().parents[1];N=P.parent;sys.path.insert(0,str(N))
from AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0.runtime.common import cfg,sha_file,P03,P04,P06,P07,P08

def main():
    errs=[]
    for f in ['forward_validation_policy.json','horizon_evaluation_policy.json','episode_policy.json','outcome_price_policy.json','permission_evaluation_policy.json','sample_maturity_policy.json','cohort_policy.json']:
        try:cfg(f)
        except Exception as e:errs.append(f+':'+str(e))
    if cfg('forward_validation_policy.json').get('trade_execution_authority')!='NONE':errs.append('TRADE_AUTHORITY')
    if cfg('forward_validation_policy.json').get('automatic_promotion_forbidden') is not True:errs.append('AUTO_PROMOTION')
    out={'phase':'AD-V3-P09','status':'PASS' if not errs else 'FAIL','errors':errs,'version':'3.9.0-true-forward-validation-2.0'};print(json.dumps(out,indent=2));return 0 if not errs else 2
if __name__=='__main__':raise SystemExit(main())
