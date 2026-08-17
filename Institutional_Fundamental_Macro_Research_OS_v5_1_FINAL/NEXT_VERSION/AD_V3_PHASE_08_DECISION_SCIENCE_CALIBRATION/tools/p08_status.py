from __future__ import annotations
import json,pathlib,sys
P=pathlib.Path(__file__).resolve().parents[1]; N=P.parent; sys.path.insert(0,str(N))
def load(p): return json.loads(pathlib.Path(p).read_text(encoding='utf-8-sig'))
def main():
    latest=P.parent/'AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING'/'artifacts'/'latest'/'latest_p08_decision_calibration.json'
    last=load(latest) if latest.exists() else None; hand=load(P/'PHASE_08_HANDOFF.json') if (P/'PHASE_08_HANDOFF.json').exists() else {}
    out={'phase':'AD-V3-P08','version':'3.8.0-decision-science-calibration','acceptance_status':hand.get('p08_status','PASS'),'default_horizon':'SESSION_1_6H','last_decision':None if not last else {k:last.get(k) for k in ['causal_direction','pressure_strength','dominance_state','dominant_root','breadth','fragility','contradiction','consumption','edge_state','permission_candidate','missing_driver_risk']},'historical_calibration_state':(last or {}).get('empirical_calibration',{}).get('overall_sample_state',hand.get('historical_calibration_sample_state','UNAVAILABLE')),'historical_episode_count':(last or {}).get('empirical_calibration',{}).get('episode_count',hand.get('historical_episode_count',0)),'v3_state':'SHADOW_COMMISSIONING','production_promotion_performed':False,'trade_execution_authority':'NONE'}
    print(json.dumps(out,indent=2,ensure_ascii=False));return 0
if __name__=='__main__':raise SystemExit(main())
