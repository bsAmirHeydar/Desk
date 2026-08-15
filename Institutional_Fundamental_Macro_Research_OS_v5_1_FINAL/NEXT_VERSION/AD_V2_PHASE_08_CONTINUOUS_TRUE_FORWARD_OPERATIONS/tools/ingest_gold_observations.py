#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT.parent))
from AD_V2_PHASE_08_CONTINUOUS_TRUE_FORWARD_OPERATIONS.runtime.observations import ingest
p=argparse.ArgumentParser();p.add_argument('--data-root',required=True);p.add_argument('--input',required=True);p.add_argument('--now-utc');a=p.parse_args();obj=json.loads(Path(a.input).read_text(encoding='utf-8'));rows=obj if isinstance(obj,list) else [obj];pol=json.loads((ROOT/'config/observation_policy.json').read_text());r=ingest(a.data_root,rows,pol,now_utc=a.now_utc);print(json.dumps(r,indent=2))
