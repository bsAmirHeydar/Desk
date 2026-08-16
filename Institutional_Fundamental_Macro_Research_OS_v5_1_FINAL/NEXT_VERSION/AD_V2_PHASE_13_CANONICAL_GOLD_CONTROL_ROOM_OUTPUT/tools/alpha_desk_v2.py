#!/usr/bin/env python3
from pathlib import Path
import argparse,sys,json,subprocess,webbrowser
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE))
from runtime.common import data_root,load_json
from runtime.model import build_control_room
from runtime.persistence import persist,latest,root
from runtime.terminal import render as render_terminal

def _p11(repo):
    nv=Path(repo)/'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL/NEXT_VERSION'
    if str(nv) not in sys.path: sys.path.insert(0,str(nv))
    from AD_V2_PHASE_11_UNIFIED_COMMAND_RESEARCH_ORCHESTRATION.runtime.unified_launcher import run_gold
    return run_gold,nv/'AD_V2_PHASE_11_UNIFIED_COMMAND_RESEARCH_ORCHESTRATION'

def _delegate(repo,args):
    tool=Path(repo)/'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL/NEXT_VERSION/AD_V2_PHASE_11_UNIFIED_COMMAND_RESEARCH_ORCHESTRATION/tools/alpha_desk_v2.py'
    return subprocess.run([sys.executable,str(tool),'--repo-root',str(repo),*args]).returncode

def main():
    ap=argparse.ArgumentParser(prog='AlphaDesk');ap.add_argument('--repo-root',required=True);sp=ap.add_subparsers(dest='cmd',required=True)
    r=sp.add_parser('run');r.add_argument('subject');r.add_argument('--input-pack');r.add_argument('--window-seconds',type=int,default=60);r.add_argument('--output-dir');r.add_argument('--no-persist',action='store_true')
    rep=sp.add_parser('report');rep.add_argument('subject',nargs='?',default='Gold');rep.add_argument('which',nargs='?',default='latest')
    op=sp.add_parser('open');op.add_argument('subject',nargs='?',default='Gold')
    os=sp.add_parser('output-status');os.add_argument('subject',nargs='?',default='Gold')
    for c in ['cluster','status','health','tf-status','learning-status','rc-status']:
        q=sp.add_parser(c);q.add_argument('subject',nargs='?') if c=='cluster' else None
    a=ap.parse_args();repo=Path(a.repo_root).resolve();dr=data_root(repo);dr.mkdir(parents=True,exist_ok=True)
    if a.cmd=='run':
        if str(a.subject).upper() not in {'GOLD','XAU','XAUUSD'}:raise SystemExit('P13 canonical output is Gold-only')
        run_gold,_=_p11(repo);p11=run_gold(repo,input_pack=a.input_pack,window_seconds=a.window_seconds,output_dir=a.output_dir,persist=not a.no_persist)
        pack=None
        if a.input_pack:pack=load_json(a.input_pack)
        elif p11.get('input_pack_path') and Path(p11['input_pack_path']).exists():pack=load_json(p11['input_pack_path'])
        model=build_control_room(repo,p11,input_pack=pack,data_root=dr)
        if a.no_persist:
            print(render_terminal(model));print(json.dumps(model,ensure_ascii=False,indent=2));return 0
        rec=persist(dr,model);print(render_terminal(model,rec['latest_html'],rec['latest_json']));return 0
    if a.cmd=='report':
        m=latest(dr)
        if not m: raise SystemExit('No canonical Gold Control Room output exists yet.')
        rec={'latest_html':str(root(dr)/'latest/control_room.html'),'latest_json':str(root(dr)/'latest/control_room.json')};print(render_terminal(m,rec['latest_html'],rec['latest_json']));return 0
    if a.cmd=='open':
        p=root(dr)/'latest/control_room.html'
        if not p.exists():raise SystemExit('No latest Control Room HTML exists yet.')
        try: webbrowser.open(p.resolve().as_uri())
        except Exception: pass
        print(str(p));return 0
    if a.cmd=='output-status':
        m=latest(dr);print(json.dumps({'schema_version':'1.0.0','phase':'AD-V2-P13','status':'PASS' if m else 'NO_OUTPUT','root':str(root(dr)),'latest_run':((m or {}).get('run') or {}).get('run_id'),'schema_id':(m or {}).get('schema_id'),'contract':(m or {}).get('contract')},ensure_ascii=False,indent=2));return 0
    # Existing operational commands remain owned by P11/P08/P09/P10.
    args=[a.cmd]
    if a.cmd=='cluster' and a.subject:args.append(a.subject)
    return _delegate(repo,args)
if __name__=='__main__':raise SystemExit(main())
