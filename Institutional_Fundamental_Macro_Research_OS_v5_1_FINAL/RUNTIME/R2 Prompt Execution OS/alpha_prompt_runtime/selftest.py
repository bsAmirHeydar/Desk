import tempfile, json, sys, shutil
from pathlib import Path
from .registry import PromptRegistry
from .graph import ProcessGraph
from .context import ContextCompiler, ContextError
from .jobs import make_job

class TestFailure(RuntimeError): pass

def run(vault_root):
    v=Path(vault_root); checks=[]
    reg=PromptRegistry(v); errs=reg.validate(); checks.append(('registry_25',len(reg.process_ids())==25)); checks.append(('registry_integrity',not errs))
    g=ProcessGraph(reg.graph); ge=g.validate(); checks.append(('graph_acyclic',not ge))
    # independent worker isolation
    inds=[p for p in reg.process_ids() if reg.manifest(p).get('independence_group')=='INDEPENDENT_STATE_CONSTRUCTION']
    checks.append(('independent_worker_count',len(inds)==8)); checks.append(('independent_worker_isolation',all(not any(d in inds for d in reg.manifest(p)['dependencies']) for p in inds)))
    checks.append(('direction_authority', [p for p in reg.process_ids() if 'fundamental_direction' in reg.manifest(p)['authority']['can_create']]==['W31_FUNDAMENTAL']))
    checks.append(('permission_authority', [p for p in reg.process_ids() if 'final_permission' in reg.manifest(p)['authority']['can_create']]==['P63_FINAL_DECISION']))
    # coverage map
    cov=json.loads((v/'RUNTIME'/'R2 Prompt Execution OS'/'config'/'full_vault_coverage_map.json').read_text(encoding='utf-8'))
    required={'91_INSTRUMENT','95_D1_FACT','93_TIMING','89_FUNDAMENTAL','90_NARRATIVE','96_POSITIONING','97_ACTUAL_FLOW','98_FUNDING','99_MECHANICS_CAPACITY','100_D2_ROUTER','103_COGNITIVE','101_D3','102_D4','94_OPERATIONAL'}
    checks.append(('full_vault_authority_coverage',required.issubset(set(cov['authorities'])))); checks.append(('fact_families_16',cov['fact_observability_families']==16))
    # prompt hash/job determinism
    pid='P10_SCOPE'; ph=reg.prompt_hash(pid); checks.append(('prompt_hash_sha256',ph.startswith('sha256:')))
    # graph initial ready set only P10
    ready=g.ready({p:'PENDING' for p in reg.process_ids()}); checks.append(('initial_ready_scope_only',ready==['P10_SCOPE']))
    # forbidden inputs declarations in all processes
    checks.append(('outcome_forbidden_all',all('outcome' in reg.manifest(p)['forbidden_inputs'] for p in reg.process_ids())))
    # adversaries don't depend on final decision
    checks.append(('adversarial_predecision',all('P63_FINAL_DECISION' not in reg.manifest(p)['dependencies'] for p in ['P50_THESIS_DESTROYER','P51_MODEL_DISAGREEMENT','P52_PREMORTEM','P53_GLOBAL_RECONCILIATION'])))
    # all output schema refs exist
    checks.append(('output_schemas_exist',all((v/o['schema_ref']).exists() for p in reg.process_ids() for o in reg.manifest(p)['outputs'])))
    # R1 runtime present
    rm=json.loads((v/'RUNTIME'/'RUNTIME_MANIFEST.json').read_text(encoding='utf-8')); checks.append(('runtime_r2_active',rm.get('runtime_version')=='R2.0.0')); checks.append(('scientific_stack_v213',rm.get('scientific_stack')=='V21.3.0'))
    checks.append(('zero_new_direction_authority',rm['authority']['direction']=='NONE')); checks.append(('zero_new_permission_authority',rm['authority']['permission']=='NONE'))
    errors=[n for n,ok in checks if not ok]
    return {'status':'PASS' if not errors else 'FAIL','checks':[{'name':n,'pass':ok} for n,ok in checks],'errors':errors+(errs or [])+(ge or [])}
