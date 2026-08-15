#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT.parent));from AD_V2_PHASE_07_D4_TRUE_FORWARD_PROMOTION.runtime.feature_freeze import freeze
from AD_V2_PHASE_07_D4_TRUE_FORWARD_PROMOTION.runtime.true_forward import persist_commitment
p=argparse.ArgumentParser();p.add_argument('--state',required=True);p.add_argument('--sample-provenance',default='TRUE_FORWARD');p.add_argument('--sealed-at-utc');p.add_argument('--episode-key');p.add_argument('--regime',default='UNKNOWN');p.add_argument('--data-root');p.add_argument('--output');a=p.parse_args();s=json.loads(Path(a.state).read_text());c=freeze(s,sample_provenance=a.sample_provenance,sealed_at_utc=a.sealed_at_utc,episode_key=a.episode_key,regime=a.regime);print(json.dumps(c,indent=2));
if a.output:Path(a.output).write_text(json.dumps(c,indent=2)+'\n',encoding='utf-8')
if a.data_root:print(json.dumps(persist_commitment(a.data_root,c),indent=2))
