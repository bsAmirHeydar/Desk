#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT.parent));from AD_V2_PHASE_07_D4_TRUE_FORWARD_PROMOTION.runtime.outcome_join import join
from AD_V2_PHASE_07_D4_TRUE_FORWARD_PROMOTION.runtime.true_forward import persist_outcome_link
p=argparse.ArgumentParser();p.add_argument('--commitment',required=True);p.add_argument('--outcome',required=True);p.add_argument('--data-root');p.add_argument('--output');a=p.parse_args();c=json.loads(Path(a.commitment).read_text());o=json.loads(Path(a.outcome).read_text());x=join(c,o);print(json.dumps(x,indent=2));
if a.output:Path(a.output).write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8')
if a.data_root:print(json.dumps(persist_outcome_link(a.data_root,x),indent=2))
