from __future__ import annotations
import json,sys,argparse
from pathlib import Path
HERE=Path(__file__).resolve();NEXT=HERE.parents[2]
if str(NEXT) not in sys.path:sys.path.insert(0,str(NEXT))
from AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0.runtime.forward_ledger import load_state
from AD_V31_R04_INSTITUTIONAL_DATA_EDGE_OUTCOME_INFRASTRUCTURE.runtime.outcome_recovery import recover_for_prediction
ap=argparse.ArgumentParser();ap.add_argument('--prediction',required=True);a=ap.parse_args();st=load_state(None);p=next((x for x in st.get('predictions',[]) if x.get('prediction_id')==a.prediction),None)
if not p:raise SystemExit('PREDICTION_NOT_FOUND')
r=recover_for_prediction(p,allow_network=False);r.pop('observations',None);print(json.dumps({'prediction_id':a.prediction,'T0':p.get('precommit_time'),'maturity':p.get('maturity_time'),'instrument':(p.get('price_anchor') or {}).get('instrument_key'),**r},indent=2))
