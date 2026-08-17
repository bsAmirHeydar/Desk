from __future__ import annotations
import argparse,json,pathlib
def main():
 p=argparse.ArgumentParser();p.add_argument('--file');a=p.parse_args();
 if a.file:d=json.loads(pathlib.Path(a.file).read_text(encoding='utf-8-sig'))
 else:
  ph=pathlib.Path(__file__).resolve().parents[1];f=ph.parent/'AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING'/'artifacts'/'latest'/'latest_p08_decision_calibration.json'
  if not f.exists(): print('NO P08 DECISION CALIBRATION OUTPUT YET');return 0
  d=json.loads(f.read_text(encoding='utf-8-sig'))
 print(json.dumps({'decision':{k:d.get(k) for k in ['causal_direction','pressure_strength','dominance_state','dominant_root','breadth','fragility','contradiction','consumption','edge_state','permission_candidate']},'roots':[{k:r.get(k) for k in ['root_id','direction','causal_importance','magnitude','freshness','evidence_quality','independence','persistence','empirical_information_state','authority_rank_tuple']} for r in d.get('calibrated_roots',[])]},indent=2,ensure_ascii=False));return 0
if __name__=='__main__':raise SystemExit(main())
