#!/usr/bin/env python3
from pathlib import Path
import argparse, importlib.util, json, sys
sys.dont_write_bytecode=True

def load(path):
    spec=importlib.util.spec_from_file_location('ad_p02_pressure',path); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--input',required=True); ap.add_argument('--output'); ap.add_argument('--mode',choices=['explicit'],default='explicit'); a=ap.parse_args()
    phase=Path(__file__).resolve().parents[1]; mod=load(phase/'runtime/directional_pressure.py'); inp=json.loads(Path(a.input).read_text(encoding='utf-8'))
    out=mod.build_from_roots(inp)
    txt=json.dumps(out,ensure_ascii=False,indent=2)
    if a.output: Path(a.output).write_text(txt+'\n',encoding='utf-8')
    else: print(txt)
    return 0 if out.get('status')=='PASS' else 3
if __name__=='__main__': sys.exit(main())
