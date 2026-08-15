#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys
PH=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(PH))
from runtime.experiments import create
from runtime.store import root,create as persist,append
ap=argparse.ArgumentParser();ap.add_argument('--data-root',required=True);ap.add_argument('--challenger',required=True);ap.add_argument('--sealed-at-utc',required=True);a=ap.parse_args();c=json.loads(Path(a.challenger).read_text());pol=json.loads((PH/'config/experiment_policy.json').read_text());e=create(c,pol,a.sealed_at_utc);rt=root(a.data_root);p=rt/'experiments'/e['experiment_id']/'experiment.json';persist(p,e);append(rt/'experiments/index.jsonl',{'experiment_id':e['experiment_id'],'challenger_id':e['challenger_id'],'path':str(p),'experiment_hash':e['experiment_hash']});print(json.dumps(e,ensure_ascii=False,indent=2))
