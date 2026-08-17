from __future__ import annotations
import json, pathlib, sys, tempfile
PHASE=pathlib.Path(__file__).resolve().parents[1]; NEXT=PHASE.parent; VAULT=NEXT.parent; REPO=VAULT.parent
sys.path.insert(0,str(NEXT))
from AD_V3_PHASE_06_GOVERNED_SEMANTIC_INTELLIGENCE.runtime.common import load_json
from AD_V3_PHASE_06_GOVERNED_SEMANTIC_INTELLIGENCE.runtime.semantic_model_host import host_status
from AD_V3_PHASE_06_GOVERNED_SEMANTIC_INTELLIGENCE.runtime.semantic_runtime import run_semantics

def main():
    hs=host_status(REPO)
    if not hs.get('configured'):
        print(json.dumps({'phase':'AD-V3-P06','live_semantic_smoke':'NOT_RUN_MODEL_HOST_UNAVAILABLE','model_host':hs},indent=2,ensure_ascii=False)); return 0
    packet=load_json(PHASE/'fixtures/live_smoke_semantic_packet.json')
    with tempfile.TemporaryDirectory() as td:
        r=run_semantics(REPO,packet,mode='AUTO_GOVERNED',artifact_dir=td,use_cache=False)
    b=r['bundle']; v=r['validation_receipt']; mode=b.get('adjudication_mode'); ok=mode=='AUTO_GOVERNED' and v.get('status') in ('PASS','DEGRADED')
    out={'phase':'AD-V3-P06','live_semantic_smoke':'PASS' if ok else 'FAIL','model_host':hs,'semantic_mode':mode,'semantic_request_count':v.get('request_count'),'validated_count':v.get('validated_count'),'unknown_count':v.get('unknown_count'),'rejected_count':v.get('rejected_count'),'fallback_count':v.get('fallback_count'),'prompt_hash':(b.get('p06_semantic') or {}).get('prompt_sha256'),'bundle_hash':r['capsule'].get('bundle_sha256'),'model_meta':r['capsule'].get('model_meta')}
    print(json.dumps(out,indent=2,ensure_ascii=False)); return 0 if ok else 2
if __name__=='__main__': raise SystemExit(main())
