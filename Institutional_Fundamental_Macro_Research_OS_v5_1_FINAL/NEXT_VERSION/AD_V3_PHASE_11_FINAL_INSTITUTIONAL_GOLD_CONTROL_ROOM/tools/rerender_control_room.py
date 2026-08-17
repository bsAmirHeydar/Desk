from __future__ import annotations
import argparse,json,pathlib,sys
HERE=pathlib.Path(__file__).resolve();PH=HERE.parents[1];NEXT=PH.parent;sys.path.insert(0,str(NEXT))
from AD_V3_PHASE_11_FINAL_INSTITUTIONAL_GOLD_CONTROL_ROOM.runtime.report_runtime import render_report

def main():
 ap=argparse.ArgumentParser();ap.add_argument('control_room_input');ap.add_argument('--output',required=True);ap.add_argument('--previous');a=ap.parse_args();load=lambda p:json.loads(pathlib.Path(p).read_text(encoding='utf-8'));r=render_report(load(a.control_room_input),a.output,load(a.previous) if a.previous else None,fixture=False,visual_state='RERENDER');print(json.dumps({'html':r['html_path'],'receipt':r['receipt']},ensure_ascii=False,indent=2));return 0
if __name__=='__main__':raise SystemExit(main())
