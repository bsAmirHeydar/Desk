from __future__ import annotations
import argparse,json,pathlib,sys
HERE=pathlib.Path(__file__).resolve();NEXT=HERE.parents[2];REPO=NEXT.parents[1];sys.path.insert(0,str(NEXT));from AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN.runtime.runtime_router import resolve
p=argparse.ArgumentParser();p.add_argument('--command',required=True);a=p.parse_args();parts=a.command.split();cmd=parts[0].lower();subject=parts[1] if len(parts)>1 else 'Gold';intent='SHADOW' if cmd=='commission' else 'PRODUCTION';print(json.dumps(resolve(REPO,subject,intent),indent=2,ensure_ascii=False))
