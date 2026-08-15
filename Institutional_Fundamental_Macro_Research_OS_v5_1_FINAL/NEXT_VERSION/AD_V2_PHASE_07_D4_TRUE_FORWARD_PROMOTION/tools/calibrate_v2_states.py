#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT.parent));from AD_V2_PHASE_07_D4_TRUE_FORWARD_PROMOTION.runtime.calibration import calibrate
from AD_V2_PHASE_07_D4_TRUE_FORWARD_PROMOTION.runtime.true_forward import load_links
p=argparse.ArgumentParser();p.add_argument('--data-root');p.add_argument('--input');p.add_argument('--output');a=p.parse_args();
rows=load_links(a.data_root) if a.data_root else json.loads(Path(a.input).read_text());r=calibrate(rows);print(json.dumps(r,indent=2));
if a.output:Path(a.output).write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
