from __future__ import annotations
import json, pathlib, sys, hashlib
PHASE=pathlib.Path(__file__).resolve().parents[1]; NEXT=PHASE.parent; VAULT=NEXT.parent; REPO=VAULT.parent
sys.path.insert(0,str(NEXT))
from AD_V3_PHASE_06_GOVERNED_SEMANTIC_INTELLIGENCE.runtime.common import load_json, sha256_file
from AD_V3_PHASE_06_GOVERNED_SEMANTIC_INTELLIGENCE.runtime.semantic_request_compiler import semantic_population
from AD_V3_PHASE_06_GOVERNED_SEMANTIC_INTELLIGENCE.runtime.semantic_model_host import host_status

def check(name,ok,detail=None): return {'name':name,'status':'PASS' if ok else 'FAIL','detail':detail}

def main():
    checks=[]; p03=NEXT/'AD_V3_PHASE_03_CAUSAL_GOLD_BRAIN_DECISION_ENGINE'; p04=NEXT/'AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING'; p05=NEXT/'AD_V3_PHASE_05_INTEGRITY_ARCHITECTURE_CONSOLIDATION'
    required=['config/semantic_runtime_contract.json','config/semantic_authority_policy.json','config/semantic_model_config.json','prompts/governed_semantic_system.md','schemas/semantic_request.schema.json','schemas/semantic_model_response.schema.json','schemas/semantic_validation_receipt.schema.json','schemas/semantic_bundle.schema.json','runtime/semantic_runtime.py','runtime/semantic_validator.py','runtime/semantic_model_host.py']
    checks.append(check('required P06 surfaces present',all((PHASE/x).exists() for x in required),[x for x in required if not (PHASE/x).exists()]))
    pop=semantic_population(p03); checks.append(check('semantic population derives from P03 registry',pop['canonical_semantic_facts']>0 and pop['session_semantic_facts']>0,pop))
    ap=load_json(PHASE/'config/semantic_authority_policy.json'); checks.append(check('canonical semantic population rule matches P03',ap['canonical_semantic_population_rule']['reasoning_mode']=='SEMANTIC_ADJUDICATION_REQUIRED'))
    checks.append(check('all P03 request-producing semantic modes governed',set(ap['governable_p03_request_modes'])=={'SEMANTIC_ADJUDICATION_REQUIRED','STRUCTURAL_PRIOR_ONLY','MECHANICAL_SEMANTIC'},ap['governable_p03_request_modes']))
    rt=load_json(PHASE/'config/semantic_runtime_contract.json'); prompt=PHASE/rt['prompt_path']; checks.append(check('canonical prompt contract hashable',prompt.exists() and len(sha256_file(prompt))==64,sha256_file(prompt) if prompt.exists() else None))
    checks.append(check('no model final direction or trade authority',rt.get('model_final_direction_authority') is False and rt.get('model_trade_action_authority') is False and rt.get('p03_final_authority')=='EXCLUSIVE'))
    checks.append(check('outside evidence and web authority forbidden',rt.get('outside_evidence_authority') is False and rt.get('web_search_authority') is False and rt.get('conversation_memory_authority') is False))
    pipeline=(p04/'runtime/pipeline.py').read_text(encoding='utf-8'); p10=NEXT/'AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN/runtime/gold_orchestrator.py'; runtime_src=p10.read_text(encoding='utf-8-sig') if p10.exists() else pipeline; checks.append(check('P04 commissioning wired to P06 runtime','run_semantics' in runtime_src and 'semantic_adjudication_bundle.json' in runtime_src and 'SEMANTIC' in runtime_src))
    launcher=(REPO/'AlphaDesk.ps1').read_text(encoding='utf-8-sig'); checks.append(check('launcher exposes v3 semantic status','AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN' in launcher))
    own=load_json(p05/'config/architecture_surface_registry.json'); joined=json.dumps(own); checks.append(check('P05 ownership classifies P06 surfaces','AD_V3_PHASE_06_GOVERNED_SEMANTIC_INTELLIGENCE' in joined))
    hs=host_status(REPO); checks.append(check('semantic host status is truthful and secret-free','OPENAI_API_KEY' not in json.dumps(hs) and 'token' not in json.dumps(hs).lower(),hs))
    status='PASS' if all(x['status']=='PASS' for x in checks) else 'FAIL'
    out={'phase':'AD-V3-P06','validation_status':status,'check_count':len(checks),'checks':checks,'semantic_population':pop,'prompt_sha256':sha256_file(prompt) if prompt.exists() else None,'host_status':hs}
    print(json.dumps(out,indent=2,ensure_ascii=False)); return 0 if status=='PASS' else 2
if __name__=='__main__': raise SystemExit(main())
