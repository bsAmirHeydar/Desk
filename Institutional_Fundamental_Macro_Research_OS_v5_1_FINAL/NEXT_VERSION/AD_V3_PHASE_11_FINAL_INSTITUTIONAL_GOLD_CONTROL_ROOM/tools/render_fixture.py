from __future__ import annotations
import argparse,pathlib,tempfile,sys,json
HERE=pathlib.Path(__file__).resolve();PH=HERE.parents[1];NEXT=PH.parent;sys.path.insert(0,str(NEXT))
from AD_V3_PHASE_11_FINAL_INSTITUTIONAL_GOLD_CONTROL_ROOM.tools.fixture_factory import base_input,scenario
from AD_V3_PHASE_11_FINAL_INSTITUTIONAL_GOLD_CONTROL_ROOM.runtime.report_runtime import render_report

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--scenario',default='dense');ap.add_argument('--output',required=True);a=ap.parse_args();out=pathlib.Path(a.output).resolve();out.mkdir(parents=True,exist_ok=True)
 with tempfile.TemporaryDirectory() as td:
  cri,_,_=base_input(pathlib.Path(td)); cri=scenario(cri,a.scenario); r=render_report(cri,out,fixture=True,visual_state='FIXTURE')
 print(json.dumps({'scenario':a.scenario,'html':r['html_path'],'view_model':r['view_model_path'],'fixture':True},ensure_ascii=False,indent=2));return 0
if __name__=='__main__':raise SystemExit(main())
