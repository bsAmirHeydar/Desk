from __future__ import annotations
import argparse,json,os,pathlib,subprocess,sys,webbrowser
HERE=pathlib.Path(__file__).resolve();PH=HERE.parents[1];REPO=PH.parents[2];NEXT=PH.parent
if str(NEXT) not in sys.path:sys.path.insert(0,str(NEXT))
from AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING.runtime.promotion import load_state,promote,rollback
from AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING.runtime.commissioning import load_state as load_commissioning

def main():
    p=argparse.ArgumentParser();sub=p.add_subparsers(dest='cmd');r=sub.add_parser('run');r.add_argument('subject');r.add_argument('--horizon',default='SESSION_1_6H');r.add_argument('--full-refresh',action='store_true');r.add_argument('--cache-only',action='store_true');r.add_argument('--semantic-bundle');
    for c in ('report','open'):q=sub.add_parser(c);q.add_argument('subject')
    sub.add_parser('status');sub.add_parser('tf-status');sub.add_parser('forward-status');sub.add_parser('promotion-status');pr=sub.add_parser('promote');pr.add_argument('--approve',action='store_true');sub.add_parser('rollback');sub.add_parser('route-mode');a=p.parse_args()
    compat=os.environ.get('AD_P10_COMPAT_CALL')=='1'
    if a.cmd in ('run','report','open') and not compat:
        tool=NEXT/'AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN/tools/alpha_desk.py';mapping={'run':['commission',a.subject,'--horizon',a.horizon]+(['--full-refresh'] if a.full_refresh else [])+(['--cache-only'] if a.cache_only else [])+(['--semantic-bundle',a.semantic_bundle] if a.semantic_bundle else []),'report':['commission-report',a.subject],'open':['commission-open',a.subject]};return subprocess.run([sys.executable,str(tool),'--repo-root',str(REPO),*mapping[a.cmd]]).returncode
    if a.cmd=='tf-status':print(json.dumps(load_commissioning(PH),indent=2,ensure_ascii=False));return 0
    if a.cmd=='forward-status':
        from AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0.runtime.forward_runtime import status
        print(json.dumps(status(NEXT/'AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0'),indent=2,ensure_ascii=False));return 0
    if a.cmd=='promotion-status':print(json.dumps(load_state(PH),indent=2,ensure_ascii=False));return 0
    if a.cmd=='route-mode':print(load_state(PH).get('state','SHADOW_COMMISSIONING'));return 0
    if a.cmd=='promote':print(json.dumps(promote(PH,load_commissioning(PH),a.approve),indent=2,ensure_ascii=False));return 0
    if a.cmd=='rollback':print(json.dumps(rollback(PH),indent=2,ensure_ascii=False));return 0
    if a.cmd=='status' or not a.cmd:print(json.dumps({'phase':'AD-V3-P04','version':'4.0.0-commissioning','stabilization':'FINAL_RC2','canonical_v3_runtime':'AD-V3-P10','promotion':load_state(PH),'commissioning':load_commissioning(PH),'production_trade_execution_authority':False},indent=2,ensure_ascii=False));return 0
    return 2
if __name__=='__main__':raise SystemExit(main())
