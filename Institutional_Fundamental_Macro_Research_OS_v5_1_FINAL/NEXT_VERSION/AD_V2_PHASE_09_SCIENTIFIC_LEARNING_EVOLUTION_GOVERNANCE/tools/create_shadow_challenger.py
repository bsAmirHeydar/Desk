#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys
PH=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(PH))
from runtime.challengers import create
from runtime.store import root,create as persist,append
ap=argparse.ArgumentParser();ap.add_argument('--data-root',required=True);ap.add_argument('--hypothesis',required=True);ap.add_argument('--spec',required=True);ap.add_argument('--sealed-at-utc',required=True);a=ap.parse_args();h=json.loads(Path(a.hypothesis).read_text());spec=json.loads(Path(a.spec).read_text());pol=json.loads((PH/'config/challenger_policy.json').read_text());c=create(h,spec,pol,a.sealed_at_utc);rt=root(a.data_root);p=rt/'challengers'/c['challenger_id']/'challenger.json';persist(p,c);append(rt/'challengers/index.jsonl',{'challenger_id':c['challenger_id'],'family':c['family'],'path':str(p),'challenger_hash':c['challenger_hash']});print(json.dumps(c,ensure_ascii=False,indent=2))
