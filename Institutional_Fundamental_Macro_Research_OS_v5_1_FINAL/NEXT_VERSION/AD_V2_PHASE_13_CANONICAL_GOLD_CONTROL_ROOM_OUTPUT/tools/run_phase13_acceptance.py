#!/usr/bin/env python3
from pathlib import Path
import argparse,sys,json,tempfile,subprocess,copy
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE))
from runtime.common import load_json
from runtime.model import build_control_room
from runtime.persistence import persist,latest
from runtime.terminal import render as term

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo-root',required=True);a=ap.parse_args();repo=Path(a.repo_root).resolve();pp=repo/'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL/NEXT_VERSION';sys.path.insert(0,str(pp));from AD_V2_PHASE_10_INTEGRATED_SHADOW_COMMISSIONING_RC.runtime.shadow_pipeline import run
 pack=load_json(pp/'AD_V2_PHASE_10_INTEGRATED_SHADOW_COMMISSIONING_RC/tests/fixtures/integrated_gold_shadow_input.json')
 with tempfile.TemporaryDirectory() as td:
  dr=Path(td)/'data';p10=run(pack,phase_parent=pp,data_root=dr,output_dir=Path(td)/'out',persist_state=False);p11={'status':'PASS','phase':'AD-V2-P11','mode':'EXPLICIT_INPUT_PACK','p10_receipt':p10};m=build_control_room(repo,p11,input_pack=pack,data_root=dr);rec=persist(dr,m);old=(Path(rec['archive_json']).read_bytes(),Path(rec['archive_html']).read_bytes());rec2=persist(dr,m);new=(Path(rec2['archive_json']).read_bytes(),Path(rec2['archive_html']).read_bytes());checks=[
   {'name':'canonical_json','status':'PASS' if Path(rec['latest_json']).exists() else 'FAIL'},
   {'name':'rtl_html','status':'PASS' if Path(rec['latest_html']).exists() and 'dir="rtl"' in Path(rec['latest_html']).read_text(encoding='utf-8') else 'FAIL'},
   {'name':'archive_immutable_idempotent','status':'PASS' if old==new else 'FAIL'},
   {'name':'latest_same_model','status':'PASS' if latest(dr).get('canonical_content_hash')==m.get('canonical_content_hash') else 'FAIL'},
   {'name':'terminal_same_model','status':'PASS' if str(m['overview']['directional_pressure']) in term(m) and str(m['overview']['trade_permission']) in term(m) else 'FAIL'},
   {'name':'human_first_terminal','status':'PASS' if all(x in term(m) for x in ['جمع‌بندی:','چرا؟','رفتار قیمت:','وضعیت حرکت و ورود:']) else 'FAIL'},
   {'name':'human_brief_in_html','status':'PASS' if all(x in Path(rec['latest_html']).read_text(encoding='utf-8') for x in ['چرا این سمت؟','قیمت چه می‌گوید؟','برای منِ تریدر یعنی چه؟']) else 'FAIL'},
   {'name':'tabs_present','status':'PASS' if all(x in Path(rec['latest_html']).read_text(encoding='utf-8') for x in ['نمای کلی','فشار و جهت','انتقال و آزادشدن','هشت لایه تحلیل','زمان‌بندی و رویدادها','ران‌ها و حافظه','گزارش و بررسی','سلامت داده']) else 'FAIL'}]
  bad=[x for x in checks if x['status']!='PASS'];out={'schema_version':'1.0.0','phase':'AD-V2-P13','status':'PASS' if not bad else 'FAIL','checks':checks};print(json.dumps(out,ensure_ascii=False,indent=2));return 0 if not bad else 1
if __name__=='__main__':raise SystemExit(main())
