from __future__ import annotations
import argparse, json, pathlib, sys, webbrowser
HERE=pathlib.Path(__file__).resolve(); PH=HERE.parents[1]; REPO=PH.parents[2]; sys.path.insert(0,str(PH.parent))
from AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING.runtime.pipeline import run
from AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING.runtime.common import load_json
from AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING.runtime.promotion import load_state, promote, rollback
from AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING.runtime.commissioning import load_state as load_commissioning

def latest(name): return PH/'artifacts'/'latest'/name
def main():
    p=argparse.ArgumentParser(); sub=p.add_subparsers(dest='cmd')
    r=sub.add_parser('run'); r.add_argument('subject'); r.add_argument('--horizon',default='SESSION_1_6H'); r.add_argument('--skip-p02',action='store_true'); r.add_argument('--semantic-bundle')
    for c in ('report','open'): q=sub.add_parser(c); q.add_argument('subject')
    sub.add_parser('status'); sub.add_parser('tf-status'); sub.add_parser('promotion-status'); pr=sub.add_parser('promote'); pr.add_argument('--approve',action='store_true'); sub.add_parser('rollback'); sub.add_parser('route-mode')
    a=p.parse_args()
    if a.cmd=='run':
        if a.subject.lower() not in ('gold','xauusd'): raise SystemExit('P04 supports Gold only.')
        out=run(REPO,a.horizon,a.skip_p02,a.semantic_bundle); print(json.dumps(out,indent=2,ensure_ascii=False)); return 0
    if a.cmd=='report':
        f=latest('latest_brief.txt'); print(f.read_text(encoding='utf-8') if f.exists() else 'NO V3 CONTROL ROOM OUTPUT YET'); return 0
    if a.cmd=='open':
        f=latest('latest_control_room.html');
        if not f.exists(): print('NO V3 CONTROL ROOM OUTPUT YET'); return 2
        webbrowser.open(f.resolve().as_uri()); print(str(f)); return 0
    if a.cmd=='tf-status': print(json.dumps(load_commissioning(PH),indent=2,ensure_ascii=False)); return 0
    if a.cmd=='promotion-status': print(json.dumps(load_state(PH),indent=2,ensure_ascii=False)); return 0
    if a.cmd=='route-mode': print(load_state(PH).get('state','SHADOW_COMMISSIONING')); return 0
    if a.cmd=='promote': print(json.dumps(promote(PH,load_commissioning(PH),a.approve),indent=2,ensure_ascii=False)); return 0
    if a.cmd=='rollback': print(json.dumps(rollback(PH),indent=2,ensure_ascii=False)); return 0
    if a.cmd=='status' or not a.cmd:
        print(json.dumps({'phase':'AD-V3-P04','version':'4.0.0-commissioning','promotion':load_state(PH),'commissioning':load_commissioning(PH),'latest_output_exists':latest('latest_control_room.html').exists(),'production_trade_execution_authority':False},indent=2,ensure_ascii=False)); return 0
if __name__=='__main__': raise SystemExit(main())
