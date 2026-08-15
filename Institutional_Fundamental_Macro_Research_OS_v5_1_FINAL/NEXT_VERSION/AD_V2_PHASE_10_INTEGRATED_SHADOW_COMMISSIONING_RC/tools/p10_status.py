#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE));from runtime.health import integrated_health

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--data-root',required=True);a=ap.parse_args();h=integrated_health(a.data_root,BASE.parent);p=Path(a.data_root)/'alpha_desk_v2/p10_commissioning/latest_commissioning_receipt.json';rec=None
 if p.is_file():
  try:rec=json.loads(p.read_text(encoding='utf-8'))
  except Exception:rec={'status':'INVALID'}
 o={'schema_version':'1.0.0','phase':'AD-V2-P10','status':'PASS' if h['status']!='FAIL_CLOSED' else 'FAIL_CLOSED','rc_id':'ALPHA_DESK_V2_RC1_SHADOW','health':h,'latest_commissioning':rec,'authority':{'trade_permission':'V1_INHERITED','broker':'NONE','mainline_override':False,'deployment':'V2_RC_SHADOW_ONLY'}};print(json.dumps(o,ensure_ascii=False,indent=2));return 0 if o['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
