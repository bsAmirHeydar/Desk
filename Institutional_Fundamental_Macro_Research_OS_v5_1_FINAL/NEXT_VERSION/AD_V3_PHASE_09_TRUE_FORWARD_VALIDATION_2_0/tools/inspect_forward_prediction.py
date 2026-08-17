#!/usr/bin/env python3
from pathlib import Path
import argparse,sys,json
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P.parent))
from AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0.runtime.forward_ledger import load_state
p=argparse.ArgumentParser();p.add_argument('--id',required=True);a=p.parse_args();s=load_state();x=next((q for q in s['predictions'] if q['prediction_id']==a.id),None);o=next((q for q in s['outcomes'] if q['prediction_id']==a.id),None);print(json.dumps({'prediction':x,'outcome':o},ensure_ascii=False,indent=2));raise SystemExit(0 if x else 2)
