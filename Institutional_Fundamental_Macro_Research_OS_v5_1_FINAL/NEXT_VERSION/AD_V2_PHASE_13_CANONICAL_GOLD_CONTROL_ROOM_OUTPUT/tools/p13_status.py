#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE))
from runtime.common import data_root
from runtime.persistence import latest,root
from runtime.environment_gate import environment_status

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo-root',required=True);ap.add_argument('--data-root');a=ap.parse_args();repo=Path(a.repo_root).resolve();dr=Path(a.data_root).resolve() if a.data_root else data_root(repo);m=latest(dr);am=dr/'alpha_desk_v2/p13_control_room/latest_amendment.json';vault=repo/'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL';env=environment_status(vault,dr);out={'schema_version':'1.0.0','phase':'AD-V2-P13','status':'PASS' if m else 'NO_OUTPUT','contract':'ALPHA_DESK_V2_GOLD_CONTROL_ROOM_V1','schema_id':'alpha_desk_v2.gold_control_room.v1','root':str(root(dr)),'latest_run':((m or {}).get('run') or {}).get('run_id'),'latest_html':str(root(dr)/'latest/control_room.html'),'latest_json':str(root(dr)/'latest/control_room.json'),'amendment_receipt':str(am) if am.exists() else None,'environment':env,'authority':{'presentation_science_authority':'NONE','trade_permission':'V1_INHERITED','broker':'NONE'}};print(json.dumps(out,ensure_ascii=False,indent=2));return 0
if __name__=='__main__':raise SystemExit(main())
