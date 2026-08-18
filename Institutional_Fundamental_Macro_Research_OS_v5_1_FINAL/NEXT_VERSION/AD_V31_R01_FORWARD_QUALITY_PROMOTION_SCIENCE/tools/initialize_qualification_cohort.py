#!/usr/bin/env python3
import argparse,json,pathlib,sys
P=pathlib.Path(__file__).resolve().parents[1];N=P.parent;sys.path.insert(0,str(N))
from AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0.runtime.forward_runtime import status as p09_status
from AD_V31_R01_FORWARD_QUALITY_PROMOTION_SCIENCE.runtime.cohort import initialize
ap=argparse.ArgumentParser();ap.add_argument('--baseline-commit');a=ap.parse_args();s=p09_status(N/'AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0');print(json.dumps(initialize(s,baseline_commit=a.baseline_commit),ensure_ascii=False,indent=2))
