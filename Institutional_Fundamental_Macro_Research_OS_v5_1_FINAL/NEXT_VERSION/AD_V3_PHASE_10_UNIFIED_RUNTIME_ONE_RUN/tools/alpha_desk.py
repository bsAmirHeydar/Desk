from __future__ import annotations
import argparse,json,pathlib,subprocess,sys,webbrowser
HERE=pathlib.Path(__file__).resolve();PH=HERE.parents[1];NEXT=PH.parent
if str(NEXT) not in sys.path:sys.path.insert(0,str(NEXT))
from AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN.runtime.runtime_router import resolve
from AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN.runtime.gold_orchestrator import run_gold
from AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN.runtime.runtime_status import status as runtime_status

def _v2(repo,args):
    tool=repo/'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL/NEXT_VERSION/AD_V2_PHASE_13_CANONICAL_GOLD_CONTROL_ROOM_OUTPUT/tools/alpha_desk_v2.py'
    cp=subprocess.run([sys.executable,str(tool),'--repo-root',str(repo),*args]);return cp.returncode

def _v3_latest(repo,name):return repo/'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL/NEXT_VERSION/AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN/artifacts/latest'/name

def _v3_report(repo,open_it=False):
    if open_it:
        p=_v3_latest(repo,'latest_control_room.html')
        if not p.exists():print('NO V3 UNIFIED CONTROL ROOM OUTPUT YET');return 2
        try:webbrowser.open(p.resolve().as_uri())
        except Exception:pass
        print(str(p));return 0
    p=_v3_latest(repo,'latest_run.json')
    if not p.exists():print('NO V3 UNIFIED CONTROL ROOM OUTPUT YET');return 2
    print(p.read_text(encoding='utf-8'));return 0

def main():
    ap=argparse.ArgumentParser(prog='AlphaDesk');ap.add_argument('--repo-root',required=True);sp=ap.add_subparsers(dest='cmd')
    r=sp.add_parser('run');r.add_argument('subject');r.add_argument('--horizon',default='SESSION_1_6H')
    c=sp.add_parser('commission');c.add_argument('subject');c.add_argument('--horizon',default='SESSION_1_6H');c.add_argument('--full-refresh',action='store_true');c.add_argument('--cache-only',action='store_true');c.add_argument('--semantic-bundle')
    for n in ('report','open','commission-report','commission-open'):
        q=sp.add_parser(n);q.add_argument('subject',nargs='?',default='Gold')
    for n in ('v3-status','v3-runtime-status','v3-integrity-status','v3-semantic-status','v3-kernel-status','v3-decision-status','v3-forward-status','v3-tf-status','v3-promotion-status','v3-control-room-status','v3-certification-status','v3-freeze-status'):
        sp.add_parser(n)
    pr=sp.add_parser('v3-promote');pr.add_argument('subject',nargs='?',default='Gold');pr.add_argument('--approve',action='store_true');rb=sp.add_parser('v3-rollback');rb.add_argument('subject',nargs='?',default='Gold');sp.add_parser('route-mode');sp.add_parser('help')
    a=ap.parse_args();repo=pathlib.Path(a.repo_root).resolve();cmd=a.cmd or 'help'
    if cmd=='help':
        print('ALPHA DESK - GOLD')
        print('NORMAL OPERATION')
        print('  .\\AlphaDesk.ps1 run Gold')
        print('  .\\AlphaDesk.ps1 report Gold')
        print('  .\\AlphaDesk.ps1 open Gold')
        print('SHADOW / COMMISSIONING')
        print('  .\\AlphaDesk.ps1 commission Gold')
        print('  .\\AlphaDesk.ps1 commission-report Gold')
        print('STATUS')
        print('  .\\AlphaDesk.ps1 v3-runtime-status')
        print('  .\\AlphaDesk.ps1 v3-forward-status')
        print('ADVANCED')
        print('  .\\AlphaDesk.ps1 commission Gold --full-refresh')
        print('Promotion remains explicit and fail-closed.');return 0
    if cmd=='run':
        try:route=resolve(repo,a.subject,'PRODUCTION')
        except ValueError as e:print(str(e),file=sys.stderr);return 4
        if route['selected_runtime']=='V2':return _v2(repo,['run',a.subject])
        out=run_gold(repo,a.horizon,'PRODUCTION');print(json.dumps(out,indent=2,ensure_ascii=False));return 0 if out.get('overall_status')!='BLOCKED' else 3
    if cmd=='commission':
        try:resolve(repo,a.subject,'SHADOW')
        except ValueError as e:print(str(e),file=sys.stderr);return 4
        mode='FULL_REFRESH' if a.full_refresh else ('CACHE_ONLY' if a.cache_only else 'NORMAL')
        try:out=run_gold(repo,a.horizon,'SHADOW',mode,semantic_bundle_path=a.semantic_bundle)
        except Exception as e:print('V3 SHADOW FAILED: '+str(e),file=sys.stderr);return 1
        print(json.dumps(out,indent=2,ensure_ascii=False));return 0 if out.get('overall_status')!='BLOCKED' else 3
    if cmd in ('report','open'):
        try:route=resolve(repo,a.subject,'PRODUCTION')
        except ValueError as e:print(str(e),file=sys.stderr);return 4
        return _v2(repo,[cmd,a.subject]) if route['selected_runtime']=='V2' else _v3_report(repo,cmd=='open')
    if cmd=='commission-report':return _v3_report(repo,False)
    if cmd=='commission-open':return _v3_report(repo,True)
    if cmd=='v3-runtime-status':print(json.dumps(runtime_status(repo),indent=2,ensure_ascii=False));return 0
    # Status dispatches remain read-only.
    if cmd=='v3-integrity-status':tool=NEXT/'AD_V3_PHASE_05_INTEGRITY_ARCHITECTURE_CONSOLIDATION/tools/p05_status.py'
    elif cmd=='v3-semantic-status':tool=NEXT/'AD_V3_PHASE_06_GOVERNED_SEMANTIC_INTELLIGENCE/tools/p06_status.py'
    elif cmd=='v3-kernel-status':tool=NEXT/'AD_V3_PHASE_07_LIVE_INTRADAY_GOLD_DATA_KERNEL/tools/p07_status.py'
    elif cmd=='v3-decision-status':tool=NEXT/'AD_V3_PHASE_08_DECISION_SCIENCE_CALIBRATION/tools/p08_status.py'
    elif cmd=='v3-forward-status':tool=NEXT/'AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0/tools/p09_status.py'
    elif cmd=='v3-control-room-status':tool=NEXT/'AD_V3_PHASE_11_FINAL_INSTITUTIONAL_GOLD_CONTROL_ROOM/tools/p11_status.py'
    else:tool=None
    if tool:return subprocess.run([sys.executable,str(tool)]).returncode
    p12=NEXT/'AD_V3_PHASE_12_FINAL_CERTIFICATION_PRODUCTION_FREEZE'
    if p12.exists():
        if cmd=='v3-certification-status': return subprocess.run([sys.executable,str(p12/'tools/p12_status.py')]).returncode
        if cmd=='v3-freeze-status': return subprocess.run([sys.executable,str(p12/'tools/verify_final_freeze.py')]).returncode
        if cmd=='v3-promotion-status': return subprocess.run([sys.executable,str(p12/'tools/prepare_production_promotion.py')]).returncode
        if cmd=='v3-promote':
            if str(getattr(a,'subject','Gold')).lower() not in ('gold','xau','xauusd'): print('SUBJECT_NOT_ACTIVE_IN_ALPHA_DESK_V3',file=sys.stderr); return 4
            return subprocess.run([sys.executable,str(p12/'tools/promote_gold.py')]+(['--approve'] if getattr(a,'approve',False) else [])).returncode
        if cmd=='v3-rollback': return subprocess.run([sys.executable,str(p12/'tools/rollback_gold.py')]).returncode
    p04=NEXT/'AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING'
    if cmd in ('v3-status','v3-tf-status','v3-promotion-status','route-mode','v3-promote','v3-rollback'):
        old=p04/'tools/alpha_desk_v3.py';mapping={'v3-status':['status'],'v3-tf-status':['tf-status'],'v3-promotion-status':['promotion-status'],'route-mode':['route-mode'],'v3-promote':['promote']+(['--approve'] if getattr(a,'approve',False) else []),'v3-rollback':['rollback']};return subprocess.run([sys.executable,str(old),*mapping[cmd]],env={**__import__('os').environ,'AD_P10_COMPAT_CALL':'1'}).returncode
    return 2
if __name__=='__main__':raise SystemExit(main())
