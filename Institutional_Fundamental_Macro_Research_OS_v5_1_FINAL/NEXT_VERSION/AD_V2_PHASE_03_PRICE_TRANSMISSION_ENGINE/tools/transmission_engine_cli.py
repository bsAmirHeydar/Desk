#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys
HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE/'runtime'))
from price_transmission import build_transmission

def main():
    p=argparse.ArgumentParser();p.add_argument('--pressure',required=True);p.add_argument('--signature',required=True);p.add_argument('--actual',required=True);p.add_argument('--output');p.add_argument('--divergence-history-count',type=int,default=0);p.add_argument('--candidates');a=p.parse_args()
    candidates=None if not a.candidates else json.loads(Path(a.candidates).read_text(encoding='utf-8'))
    out=build_transmission(json.loads(Path(a.pressure).read_text(encoding='utf-8')),json.loads(Path(a.signature).read_text(encoding='utf-8')),json.loads(Path(a.actual).read_text(encoding='utf-8')),divergence_history_count=a.divergence_history_count,missing_driver_candidates=candidates)
    s=json.dumps(out,ensure_ascii=False,indent=2)
    if a.output: Path(a.output).write_text(s+'\n',encoding='utf-8')
    else: print(s)
    return 0 if out.get('status')=='PASS' else 2
if __name__=='__main__': raise SystemExit(main())
