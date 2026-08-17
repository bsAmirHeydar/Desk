from __future__ import annotations
import json, pathlib, sys
PHASE=pathlib.Path(__file__).resolve().parents[1]; NEXT=PHASE.parent; VAULT=NEXT.parent; REPO=VAULT.parent
sys.path.insert(0,str(NEXT))
from AD_V3_PHASE_06_GOVERNED_SEMANTIC_INTELLIGENCE.runtime.common import load_json, sha256_file
from AD_V3_PHASE_06_GOVERNED_SEMANTIC_INTELLIGENCE.runtime.semantic_request_compiler import semantic_population
from AD_V3_PHASE_06_GOVERNED_SEMANTIC_INTELLIGENCE.runtime.semantic_model_host import host_status

def main():
    p03=NEXT/'AD_V3_PHASE_03_CAUSAL_GOLD_BRAIN_DECISION_ENGINE'; hand=PHASE/'PHASE_06_HANDOFF.json'; h=load_json(hand) if hand.exists() else {}
    last=PHASE/'artifacts/latest_semantic_status.json'; lr=load_json(last) if last.exists() else None
    cfg=load_json(PHASE/'config/semantic_runtime_contract.json'); pop=semantic_population(p03); hs=host_status(REPO)
    out={'phase':'AD-V3-P06','version':'3.6.0-governed-semantic-intelligence','acceptance_status':h.get('p06_status','NOT_YET_RECORDED'),'semantic_population':pop,'active_semantic_configuration':cfg.get('default_mode'),'model_host':hs,'semantic_prompt_version':cfg.get('prompt_version'),'semantic_prompt_sha256':sha256_file(PHASE/cfg['prompt_path']),'last_semantic_run':lr,'v3_state':'SHADOW_COMMISSIONING','production_promotion_performed':False,'trade_execution_authority':'NONE'}
    print(json.dumps(out,indent=2,ensure_ascii=False)); return 0
if __name__=='__main__': raise SystemExit(main())
