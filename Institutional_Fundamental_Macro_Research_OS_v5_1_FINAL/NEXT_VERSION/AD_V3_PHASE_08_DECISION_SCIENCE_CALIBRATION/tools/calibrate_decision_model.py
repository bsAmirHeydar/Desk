from __future__ import annotations
import argparse,json,pathlib,sys
P=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(P.parent))
from AD_V3_PHASE_08_DECISION_SCIENCE_CALIBRATION.runtime.empirical_calibration import calibrate_from_episodes

def main():
 p=argparse.ArgumentParser();p.add_argument('--episodes');p.add_argument('--output');a=p.parse_args(); eps=[]
 if a.episodes:
  d=json.loads(pathlib.Path(a.episodes).read_text(encoding='utf-8-sig'));eps=d if isinstance(d,list) else d.get('episodes',[])
 reg=calibrate_from_episodes(eps)
 if a.output:pathlib.Path(a.output).write_text(json.dumps(reg,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
 print(json.dumps(reg,indent=2,ensure_ascii=False));return 0
if __name__=='__main__':raise SystemExit(main())
