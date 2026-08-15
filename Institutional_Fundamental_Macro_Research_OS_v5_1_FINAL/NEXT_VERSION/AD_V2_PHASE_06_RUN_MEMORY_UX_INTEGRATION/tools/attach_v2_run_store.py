#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys
BASE=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(BASE.parent))
from AD_V2_PHASE_06_RUN_MEMORY_UX_INTEGRATION.runtime.run_store_bridge import attach

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--vault-root',required=True); ap.add_argument('--data-root',required=True); ap.add_argument('--run-id',required=True); ap.add_argument('--state',required=True); ap.add_argument('--extension',required=True); ap.add_argument('--report-model',required=True); a=ap.parse_args(); s,e,r=map(load,[a.state,a.extension,a.report_model]); o=attach(a.vault_root,a.data_root,a.run_id,s,e,s.get('change_set'),s.get('portable_memory'),r); print(json.dumps(o,ensure_ascii=False,indent=2)); return 0 if o.get('status') in {'PASS','SKIPPED_CLOSE_SEALED','SKIPPED_NO_DECISION_SEAL'} else 2
if __name__=='__main__': raise SystemExit(main())
