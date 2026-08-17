from __future__ import annotations
import argparse, json, pathlib, sys
PHASE=pathlib.Path(__file__).resolve().parents[1]; NEXT=PHASE.parent; sys.path.insert(0,str(NEXT))
from AD_V3_PHASE_03_CAUSAL_GOLD_BRAIN_DECISION_ENGINE.runtime.engine import execute
from AD_V3_PHASE_03_CAUSAL_GOLD_BRAIN_DECISION_ENGINE.runtime.loader import latest_receipt, observation_history, current_previous_for_receipt
from AD_V3_PHASE_03_CAUSAL_GOLD_BRAIN_DECISION_ENGINE.runtime.common import load_json
from AD_V3_PHASE_03_CAUSAL_GOLD_BRAIN_DECISION_ENGINE.runtime.semantic_packet import build_semantic_evidence_packet

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--p02-data-root',default=str(NEXT/'AD_V3_PHASE_02_TOTAL_LIVE_DATA_OBSERVABILITY_FABRIC'/'artifacts'/'live_store'))
    p.add_argument('--coverage')
    p.add_argument('--horizon',default='SESSION_1_6H')
    p.add_argument('--output',required=True)
    a=p.parse_args()
    coverage=load_json(a.coverage) if a.coverage else latest_receipt(a.p02_data_root)
    receipt=execute(PHASE,a.p02_data_root,a.coverage,None,a.horizon)
    if receipt.get('analysis_admission')=='BLOCKED':
        print(json.dumps(receipt,indent=2)); return 2
    hist=observation_history(a.p02_data_root,None); pairs,_=current_previous_for_receipt(hist,coverage)
    reg=load_json(PHASE/'config/fact_reasoning_registry.json'); cmap={x['fact_id']:x for x in reg['contracts']}
    packet=build_semantic_evidence_packet(receipt,pairs,cmap,coverage)
    out=pathlib.Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(packet,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':'PASS','output':str(out),'packet_id':packet['packet_id'],'item_count':packet['item_count'],'horizon':packet['horizon']},indent=2))
    return 0

if __name__=='__main__': raise SystemExit(main())
