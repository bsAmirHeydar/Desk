from __future__ import annotations
from pathlib import Path
import json, hashlib, collections, fnmatch, importlib.util, sys, importlib

PHASE=Path(__file__).resolve().parents[1]
NEXT=PHASE.parent
VAULT=NEXT.parent
REPO=VAULT.parent
P1=NEXT/'AD_V3_PHASE_01_TOTAL_GOLD_KNOWLEDGE_SCIENCE_FOUNDATION'
P2=NEXT/'AD_V3_PHASE_02_TOTAL_LIVE_DATA_OBSERVABILITY_FABRIC'
P3=NEXT/'AD_V3_PHASE_03_CAUSAL_GOLD_BRAIN_DECISION_ENGINE'
P4=NEXT/'AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING'
VERSION='3.5.0-integrity-consolidation'

def load(path): return json.loads(Path(path).read_text(encoding='utf-8-sig'))
def digest(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def rel(path): return Path(path).relative_to(REPO).as_posix()
def _cfg(name): return load(PHASE/'config'/name)

def canonical_counts():
    facts=load(P1/'config/gold_master_fact_registry.json')
    sources=load(P2/'config/source_contract_registry.json')
    acq=load(P2/'config/fact_acquisition_registry.json')
    reasoning=load(P3/'config/fact_reasoning_registry.json')
    sem=[x for x in reasoning['contracts'] if x.get('reasoning_mode')=='SEMANTIC_ADJUDICATION_REQUIRED']
    sem_session=[x for x in sem if 'SESSION_1_6H' in (x.get('active_horizons') or [])]
    return {
      'gold_facts':len(facts['facts']),'source_contracts':len(sources['sources']),
      'fact_acquisition_contracts':len(acq['contracts']),'semantic_adjudication_population':len(sem),
      'semantic_adjudication_session_population':len(sem_session),
      'mandatory_attempt_contracts':sum(1 for x in acq['contracts'] if x.get('must_attempt_when_applicable')),
      'declared':{'gold_facts':facts.get('fact_count'),'source_contracts':sources.get('source_count'),'fact_acquisition_contracts':acq.get('contract_count'),'reasoning_contracts':reasoning.get('contract_count')}
    }

def metadata_models():
    sr=load(P2/'config/source_contract_registry.json'); fr=load(P2/'config/fact_acquisition_registry.json')
    counts=canonical_counts()
    shas={'source_contract_registry':digest(P2/'config/source_contract_registry.json'),'fact_acquisition_registry':digest(P2/'config/fact_acquisition_registry.json')}
    modes=collections.Counter(x.get('acquisition_mode') for x in fr['contracts'])
    access=collections.Counter(x.get('access_class') for x in sr['sources'])
    collectors=collections.Counter(x.get('collector_type') for x in sr['sources'])
    provenance={'classification':'DERIVED_GENERATED_METADATA','generated_from':['config/source_contract_registry.json','config/fact_acquisition_registry.json'],'generator':'AD-V3-P05/tools/generate_current_metadata.py','canonical_registry_sha256':shas,'deterministic':True}
    summary={'phase':'AD-V3-P02','revision':'3.2.6','operational_build':'3.2.6+c2-price-anchor-closure.1','generated_metadata':provenance,'facts':counts['gold_facts'],'sources':counts['source_contracts'],'fact_acquisition_contracts':counts['fact_acquisition_contracts'],'fact_acquisition_modes':dict(sorted(modes.items())),'source_access_classes':dict(sorted(access.items())),'collector_types':dict(sorted(collectors.items())),'mandatory_attempt_contracts':counts['mandatory_attempt_contracts'],'source_ids':[x['source_id'] for x in sr['sources']],'hardening_note':sr.get('hardening_note')}
    handoff={'phase':'AD-V3-P02','status':'READY_FOR_ACCEPTANCE','deployment':'SHADOW_ONLY','generated_metadata':provenance,'p01_fact_count':counts['gold_facts'],'source_contract_count':counts['source_contracts'],'fact_acquisition_contract_count':counts['fact_acquisition_contracts'],'mandatory_public_fact_attempt_contracts':counts['mandatory_attempt_contracts'],'direction_authority':False,'trade_permission_authority':False,'p03_required_inputs':['fact observations with acquisition_run_id','coverage receipt with exact acquisition_run_id','raw snapshot provenance','P01 causal ontology and role registry'],'hard_rule':'P03 analysis MUST NOT start when P02 coverage receipt is BLOCKED.','revision':'3.2.6','operational_build':'3.2.6+c2-price-anchor-closure.1','live_hardening_note':sr.get('hardening_note')}
    return summary,handoff

def write_metadata():
    summary,handoff=metadata_models()
    for p,obj in [(P2/'P02_SOURCE_COVERAGE_SUMMARY.json',summary),(P2/'PHASE_02_HANDOFF.json',handoff)]:
        p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return summary,handoff

def audit_architecture():
    reg=_cfg('architecture_surface_registry.json'); allowed=set(reg['mutability_classes']); seen=set(); errors=[]
    for x in reg['surfaces']:
        p=x['path']
        if p in seen: errors.append('DUPLICATE_SURFACE:'+p)
        seen.add(p)
        if x['class'] not in allowed: errors.append('UNKNOWN_CLASS:'+p)
        if x.get('required',True) and not (REPO/p).exists(): errors.append('MISSING_SURFACE:'+p)
    mutable={x['path'] for x in reg['surfaces'] if x['class']=='DEPLOYMENT_MUTABLE'}
    if 'AlphaDesk.ps1' not in mutable: errors.append('LAUNCHER_NOT_DEPLOYMENT_MUTABLE')
    return {'status':'PASS' if not errors else 'FAIL_CLOSED','errors':errors,'surface_count':len(reg['surfaces']),'pattern_rule_count':len(reg.get('pattern_rules',[]))}

def _load_p01_module():
    path=P1/'runtime/knowledge_compiler.py'; spec=importlib.util.spec_from_file_location('p01_kc_p05',path); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def audit_freeze():
    kc=_load_p01_module(); p01=kc.verify_v2_freeze()
    original=PHASE/'baseline/P01_v2_frozen_surface_manifest_ORIGINAL.json'; current=P1/'baseline/v2_frozen_surface_manifest.json'
    historical_preserved=digest(original)==digest(current)
    p02m=load(P2/'baseline/P02_IMMUTABLE_HASHES.json'); drift=[]
    for rp,want in p02m.get('files',{}).items():
        p=P2/rp; got=digest(p) if p.exists() else None
        if got!=want: drift.append({'file':rp,'expected':want,'actual':got})
    generated=set(p02m.get('generated_metadata_excluded') or [])
    generated_boundary_ok={'P02_SOURCE_COVERAGE_SUMMARY.json','PHASE_02_HANDOFF.json'}.issubset(generated)
    errors=[]
    if p01.get('status')!='PASS': errors.append('P01_SCIENTIFIC_FREEZE_FAIL')
    if not historical_preserved: errors.append('P01_HISTORICAL_MANIFEST_REWRITTEN')
    if drift: errors.append('P02_ACQUISITION_FREEZE_DRIFT')
    if not generated_boundary_ok: errors.append('P02_GENERATED_METADATA_STILL_IMMUTABLE')
    return {'status':'PASS' if not errors else 'FAIL_CLOSED','errors':errors,'p01':p01,'p01_historical_manifest_preserved':historical_preserved,'p02_current_freeze_drift':drift,'p02_generated_metadata_boundary_ok':generated_boundary_ok}

def audit_metadata():
    exp_s,exp_h=metadata_models(); act_s=load(P2/'P02_SOURCE_COVERAGE_SUMMARY.json'); act_h=load(P2/'PHASE_02_HANDOFF.json'); counts=canonical_counts(); errors=[]
    if act_s!=exp_s: errors.append('P02_SOURCE_SUMMARY_NOT_CANONICAL')
    if act_h!=exp_h: errors.append('P02_HANDOFF_NOT_CANONICAL')
    if counts['declared']['source_contracts']!=counts['source_contracts']: errors.append('SOURCE_REGISTRY_DECLARED_COUNT_DRIFT')
    if counts['declared']['gold_facts']!=counts['gold_facts']: errors.append('FACT_REGISTRY_DECLARED_COUNT_DRIFT')
    if counts['declared']['fact_acquisition_contracts']!=counts['fact_acquisition_contracts']: errors.append('ACQUISITION_REGISTRY_DECLARED_COUNT_DRIFT')
    return {'status':'PASS' if not errors else 'FAIL_CLOSED','errors':errors,'counts':counts}

def audit_command_contract():
    c=_cfg('canonical_runtime_contract.json'); launcher=(REPO/'AlphaDesk.ps1').read_text(encoding='utf-8-sig'); run=(REPO/'RUN.md').read_text(encoding='utf-8-sig'); v2=(REPO/'ALPHA_DESK_V2_RUN.md').read_text(encoding='utf-8-sig'); errors=[]
    if c.get('active_subject')!='Gold': errors.append('ACTIVE_SUBJECT_NOT_GOLD')
    if c.get('chat_semantics',{}).get('Run')!='Run Gold': errors.append('RUN_ALIAS_DRIFT')
    if 'run NASDAQ100' in run or 'NEW_ASSET_RESEARCH' in run: errors.append('LEGACY_MULTI_ASSET_CONTRACT_STILL_CURRENT')
    p10=NEXT/'AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN'
    if p10.exists():
        for token in ['AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN','alpha_desk.py','PYTHONIOENCODING','PYTHONUTF8']:
            if token not in launcher: errors.append('LAUNCHER_CONTRACT_MISSING:'+token)
        router=(p10/'runtime/runtime_router.py').read_text(encoding='utf-8-sig')
        for token in ['selected_runtime','V2','V3']:
            if token not in router: errors.append('P10_ROUTER_MISSING:'+token)
        route_policy=load(p10/'config/route_policy.json')
        routes=route_policy.get('routes') or {}
        expected_routes={
            'SHADOW_COMMISSIONING': {'PRODUCTION':'V2','SHADOW':'V3'},
            'PRODUCTION_V3': {'PRODUCTION':'V3','SHADOW':'V3'},
            'ROLLED_BACK_V2': {'PRODUCTION':'V2','SHADOW':'V3'},
        }
        for state,want in expected_routes.items():
            got=routes.get(state) or {}
            for intent,runtime in want.items():
                if got.get(intent)!=runtime:
                    errors.append(f'P10_ROUTE_POLICY_DRIFT:{state}:{intent}:{got.get(intent)}!={runtime}')
        if route_policy.get('routing_authority')!='AD-V3-P10': errors.append('P10_ROUTING_AUTHORITY_DRIFT')
        cli=(p10/'tools/alpha_desk.py').read_text(encoding='utf-8-sig')
        if "resolve(repo,a.subject,'PRODUCTION')" not in cli or "resolve(repo,a.subject,'SHADOW')" not in cli: errors.append('P10_ROUTE_INTENTS_MISSING')
    else:
        for token in ['Get-V3RouteMode','PRODUCTION_V3','Invoke-V2','commission','v3-integrity-status']:
            if token not in launcher: errors.append('LAUNCHER_CONTRACT_MISSING:'+token)
    if 'V2' not in v2 or ('fallback' not in v2.lower() and 'rollback' not in v2.lower()): errors.append('V2_FALLBACK_NOT_DOCUMENTED')
    return {'status':'PASS' if not errors else 'FAIL_CLOSED','errors':errors,'active_subject':c.get('active_subject'),'expected_v3_state':c.get('current_expected_v3_state')}

def audit_promotion_contract():
    policy=load(P4/'config/promotion_policy.json'); gate_cfg=_cfg('integrity_gate_registry.json'); errors=[]
    declared=policy.get('promotion_requires') or []; registered=[x['gate_id'] for x in gate_cfg['gates']]
    if declared!=registered: errors.append('DECLARED_REGISTERED_GATE_DRIFT')
    if policy.get('automatic_promotion_forbidden') is not True: errors.append('AUTOMATIC_PROMOTION_NOT_FORBIDDEN')
    if str(NEXT) not in sys.path: sys.path.insert(0,str(NEXT))
    m=importlib.import_module('AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING.runtime.promotion')
    machine=list(m.machine_enforced_gate_ids(P4))
    if machine!=declared: errors.append('POLICY_IMPLEMENTATION_GATE_DRIFT')
    return {'status':'PASS' if not errors else 'FAIL_CLOSED','errors':errors,'declared_gates':declared,'machine_enforced_gates':machine,'automatic_promotion_forbidden':policy.get('automatic_promotion_forbidden')}

def audit_artifacts():
    p=_cfg('artifact_governance_policy.json'); gi=(REPO/'.gitignore').read_text(encoding='utf-8-sig'); missing=[x for x in p['required_gitignore_patterns'] if x not in gi]; errors=[]
    if missing: errors.append('MISSING_GITIGNORE_PATTERNS')
    blanket=[line for line in gi.splitlines() if line.strip() in {'*.json','**/*.json','config/','**/config/'}]
    if blanket: errors.append('AUTHORITATIVE_CONFIG_BLANKET_IGNORED')
    return {'status':'PASS' if not errors else 'FAIL_CLOSED','errors':errors,'missing_gitignore_patterns':missing}

def audit_science_unchanged():
    base=load(PHASE/'baseline/PRE_P05_SCIENCE_HASHES.json'); drift=[]
    for rp,meta in base['files'].items():
        p=REPO/rp; got=digest(p) if p.exists() else None
        if got!=meta['sha256']: drift.append({'file':rp,'expected':meta['sha256'],'actual':got})
    return {'status':'PASS' if not drift else 'FAIL_CLOSED','drift':drift}

def compile_integrity(write=False):
    audits={'architecture':audit_architecture(),'freeze':audit_freeze(),'metadata':audit_metadata(),'command_contract':audit_command_contract(),'promotion_governance':audit_promotion_contract(),'artifact_governance':audit_artifacts(),'science_unchanged':audit_science_unchanged()}
    mapping={'architecture_drift':audits['architecture']['errors'],'freeze_conflicts':audits['freeze']['errors'],'registry_metadata_drift':audits['metadata']['errors'],'command_contract_drift':audits['command_contract']['errors'],'promotion_gate_drift':audits['promotion_governance']['errors'],'artifact_governance_errors':audits['artifact_governance']['errors'],'science_drift':audits['science_unchanged']['drift']}
    ok=all(v['status']=='PASS' for v in audits.values())
    out={'schema_version':'1.0.0','phase':'AD-V3-P05','version':VERSION,'status':'PASS' if ok else 'FAIL_CLOSED',**mapping,'scientific_surface_status':'PASS' if audits['freeze']['status']=='PASS' and audits['science_unchanged']['status']=='PASS' else 'FAIL_CLOSED','deployment_surface_status':'PASS' if audits['command_contract']['status']=='PASS' else 'FAIL_CLOSED','counts':canonical_counts(),'audits':audits,'v3_promotion_performed':False,'expected_v3_state':'SHADOW_COMMISSIONING','trade_execution_authority':'NONE'}
    if write:
        p=PHASE/'artifacts/P05_INTEGRITY_RECEIPT.json'; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return out
