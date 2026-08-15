#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'runtime'))
from latent_release import build_latent_release

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--pressure',required=True); ap.add_argument('--transmission',required=True); ap.add_argument('--evidence',required=True); ap.add_argument('--out'); a=ap.parse_args()
    load=lambda p: json.loads(Path(p).read_text(encoding='utf-8'))
    out=build_latent_release(load(a.pressure),load(a.transmission),load(a.evidence))
    txt=json.dumps(out,ensure_ascii=False,indent=2)
    if a.out: Path(a.out).write_text(txt+'\n',encoding='utf-8')
    else: print(txt)
    return 0 if out.get('status')=='PASS' else 2
if __name__=='__main__': raise SystemExit(main())
