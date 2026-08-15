#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE));from runtime.shadow_pipeline import run

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--input-pack',required=True);ap.add_argument('--data-root',required=True);ap.add_argument('--output-dir',required=True);ap.add_argument('--no-persist',action='store_true');a=ap.parse_args();pack=json.loads(Path(a.input_pack).read_text(encoding='utf-8'));out=run(pack,phase_parent=BASE.parent,data_root=a.data_root,output_dir=a.output_dir,persist_state=not a.no_persist);print(json.dumps(out,ensure_ascii=False,indent=2));return 0
if __name__=='__main__':raise SystemExit(main())
