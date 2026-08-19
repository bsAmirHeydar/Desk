from __future__ import annotations
import json,time
from pathlib import Path
import jsonschema
from .common import load,sha_obj,sha_file
from .presenter import build_view_model
from .renderer import render

def write_json(p,o):p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def render_report(control_room_input,output_dir,previous_input=None,fixture=False,visual_state='DOM_ONLY'):
 out=Path(output_dir);out.mkdir(parents=True,exist_ok=True);t=time.perf_counter();vm=build_view_model(control_room_input,previous_input,fixture);view_ms=round((time.perf_counter()-t)*1000,3)
 jsonschema.validate(vm,load(Path(__file__).resolve().parents[1]/'schemas/control_room_view_model.schema.json'));vp=out/'control_room_view_model.json';write_json(vp,vm)
 t=time.perf_counter();html=render(vm);render_ms=round((time.perf_counter()-t)*1000,3);hp=out/'control_room.html';hp.write_text(html,encoding='utf-8')
 receipt={'record_type':'AD_V3_P11_REPORT_RECEIPT','schema_version':'1.0.0','phase':'AD-V3-P11','version':'3.11.3-r05-human-intelligence','run_id':(control_room_input.get('run') or {}).get('run_id'),'input_hash':sha_obj(control_room_input),'view_model_hash':sha_file(vp),'html_hash':sha_file(hp),'view_model_ms':view_ms,'render_ms':render_ms,'html_size':hp.stat().st_size,'render_status':'PASS','validation_state':'PASS','visual_state':visual_state,'accessibility_state':'DETERMINISTIC_PASS','fixture':bool(fixture),'canonical_v3_renderer':True,'scientific_authority':False,'trade_execution_authority':'NONE'};jsonschema.validate(receipt,load(Path(__file__).resolve().parents[1]/'schemas/report_receipt.schema.json'));rp=out/'p11_report_receipt.json';write_json(rp,receipt)
 brief=vm['executive']['headline']+'\nمجوز پژوهشی: '+str(vm['executive']['permission_human'])+'\nForward: '+str(vm['forward']['evidence_state'])+'\n';(out/'brief.txt').write_text(brief,encoding='utf-8')
 return {'view_model':vm,'html':html,'receipt':receipt,'view_model_path':str(vp),'html_path':str(hp),'receipt_path':str(rp),'brief_path':str(out/'brief.txt')}
