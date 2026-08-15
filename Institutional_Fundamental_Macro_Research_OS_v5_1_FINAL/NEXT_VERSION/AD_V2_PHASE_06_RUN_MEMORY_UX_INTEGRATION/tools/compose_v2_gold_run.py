#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE.parent))
from AD_V2_PHASE_06_RUN_MEMORY_UX_INTEGRATION.runtime.run_overlay import compose
from AD_V2_PHASE_06_RUN_MEMORY_UX_INTEGRATION.runtime.v2_memory import find_previous,build_extension,persist
from AD_V2_PHASE_06_RUN_MEMORY_UX_INTEGRATION.runtime.report_model_v2 import build as build_report
from AD_V2_PHASE_06_RUN_MEMORY_UX_INTEGRATION.runtime.render_v2 import render_html

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--base-capsule',required=True); ap.add_argument('--pressure',required=True); ap.add_argument('--transmission',required=True); ap.add_argument('--latent',required=True); ap.add_argument('--gold-intelligence',required=True); ap.add_argument('--data-root',required=True); ap.add_argument('--output-dir',required=True); a=ap.parse_args()
 b,p,t,l,g=map(load,[a.base_capsule,a.pressure,a.transmission,a.latent,a.gold_intelligence]); prev=find_previous(a.data_root,'XAUUSD',b.get('mode'),b.get('horizon')); state=compose(b,p,t,l,g,previous=prev); ext=build_extension(state); receipt=persist(a.data_root,ext); report=build_report(state,ext); outdir=Path(a.output_dir); outdir.mkdir(parents=True,exist_ok=True); rp=outdir/(str(state['run_id'])+'_v2_report_model.json'); rp.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); hp=render_html(report,outdir/(str(state['run_id'])+'_v2_explorer.html')); print(json.dumps({'status':'PASS','state':state,'capsule':receipt,'report_model':str(rp),'explorer':hp},ensure_ascii=False,indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
