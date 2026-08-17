from __future__ import annotations
import argparse,json,pathlib

def main():
 ap=argparse.ArgumentParser();ap.add_argument('view_model');a=ap.parse_args();o=json.loads(pathlib.Path(a.view_model).read_text(encoding='utf-8'));e=o.get('executive',{});print(json.dumps({'run_id':(o.get('run') or {}).get('run_id'),'direction':e.get('direction'),'strength':e.get('pressure_strength'),'dominance':e.get('dominance'),'permission':e.get('permission'),'edge':e.get('edge'),'consumption':e.get('consumption'),'fragility':e.get('fragility'),'drivers':len(o.get('drivers') or []),'roots':len(o.get('roots') or []),'evidence':len(o.get('evidence') or []),'forward':o.get('forward'),'data_health':o.get('data_health')},ensure_ascii=False,indent=2));return 0
if __name__=='__main__':raise SystemExit(main())
