#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys
PH=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(PH))
from runtime.operations import status
from runtime.store import root,read_jsonl
from runtime.report import render
ap=argparse.ArgumentParser();ap.add_argument('--data-root',required=True);ap.add_argument('--output',required=True);a=ap.parse_args();rt=root(a.data_root);idx=read_jsonl(rt/'queue/index.jsonl');q={'items':[]}
if idx:
 p=Path(idx[-1]['path'])
 if p.is_file():q=json.loads(p.read_text())
Path(a.output).write_text(render(status(a.data_root),q),encoding='utf-8');print(a.output)
