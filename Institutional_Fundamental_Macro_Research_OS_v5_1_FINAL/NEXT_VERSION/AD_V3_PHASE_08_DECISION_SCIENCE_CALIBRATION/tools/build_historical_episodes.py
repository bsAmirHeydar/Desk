from __future__ import annotations
import argparse,json,pathlib,sys
P=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(P.parent))
from AD_V3_PHASE_08_DECISION_SCIENCE_CALIBRATION.runtime.episode_builder import build_episodes

def main():
 p=argparse.ArgumentParser();p.add_argument('--input');p.add_argument('--output');a=p.parse_args(); rows=[]
 if a.input:
  d=json.loads(pathlib.Path(a.input).read_text(encoding='utf-8-sig'));rows=d if isinstance(d,list) else d.get('decisions',[])
 else:
  runs=P.parent/'AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING'/'artifacts'/'runs'
  for f in sorted(runs.glob('*/p08_decision_calibration.json')) if runs.exists() else []: rows.append(json.loads(f.read_text(encoding='utf-8-sig')))
 eps=build_episodes(rows);out={'record_type':'AD_V3_P08_HISTORICAL_EPISODES','episode_count':len(eps),'episodes':eps,'boundary_uses_future_outcome':False}
 if a.output:pathlib.Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
 print(json.dumps(out,indent=2,ensure_ascii=False));return 0
if __name__=='__main__':raise SystemExit(main())
