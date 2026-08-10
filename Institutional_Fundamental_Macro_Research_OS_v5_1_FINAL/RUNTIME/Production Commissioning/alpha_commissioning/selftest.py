from pathlib import Path
import json, ast, os
from .util import load_json,host_command_json

def run(vault_root):
    v=Path(vault_root).resolve();c=v/'RUNTIME'/'Production Commissioning';checks=[];errors=[]
    rm=load_json(v/'RUNTIME'/'RUNTIME_MANIFEST.json');checks += [('runtime_r4',rm.get('runtime_version')=='R4.0.0'),('scientific_v213',rm.get('scientific_stack')=='V21.3.0'),('commissioning_c1',rm.get('commissioning',{}).get('version')=='C1.0.0'),('broker_write_none',rm.get('commissioning',{}).get('broker_write_authority')=='NONE')]
    mb=load_json(c/'config'/'model_bindings.json');checks += [('model_gpt_5_6_sol',mb.get('default_model')=='gpt-5.6-sol'),('no_auto_downgrade',mb.get('automatic_model_downgrade') is False),('max_profiles',all(x.get('reasoning',{}).get('mode')=='pro' and x.get('reasoning',{}).get('effort') in ('xhigh','max') for x in mb['profiles'].values())),('store_false',mb.get('store') is False),('max_output_128k',mb.get('output_policy',{}).get('max_output_tokens')==128000),('retrieval_unlimited_budget',mb.get('retrieval_profile',{}).get('return_token_budget')=='unlimited'),('overflow_fail_closed',mb.get('context_policy',{}).get('overflow')=='FAIL_CLOSED_NO_TRUNCATION'),('reasoning_stateless_current_turn',all(x.get('reasoning',{}).get('context')=='current_turn' for x in mb['profiles'].values()) and mb.get('retrieval_profile',{}).get('reasoning',{}).get('context')=='current_turn')]
    src=load_json(v/'100 Six-Market D2 Fact Books and Production Shadow Engine'/'config'/'d2_source_registry.json');sp=load_json(c/'config'/'source_domain_policy.json');ids={x['source_id'] for x in src['sources']};checks += [('source_count_57',len(ids)==57),('source_policy_complete',not (ids-set(sp['sources']))),('synthetic_discovery_four',len(sp.get('synthetic_discovery_ids',[]))==4 and 'ALPHALAB_INSTITUTIONAL_MACRO_WEB' in sp.get('synthetic_discovery_ids',[]))]
    sub=[k for k,x in sp['sources'].items() if x.get('access_mode')=='SUBSCRIPTION_UNBOUND'];lic=[k for k,x in sp['sources'].items() if x.get('access_mode')=='LICENSED_UNBOUND'];checks += [('subscription_explicit_unbound',len(sub)>=5),('licensed_explicit_unbound',len(lic)>=8)]
    # Worker transport defect regression
    wids=['W30_TEMPORAL','W31_FUNDAMENTAL','W32_EXPECTATIONS_POLICY_REGIME','W33_NARRATIVE_REFLEXIVITY_CONSUMPTION','W34_POSITIONING','W35_ACTUAL_FLOW','W36_FUNDING_PLUMBING','W37_MECHANICS_CAPACITY_VOL'];ok=True
    for pid in wids:
        m=load_json(v/'RUNTIME'/'R2 Prompt Execution OS'/'prompt_registry'/pid/'manifest.json');ok=ok and 'decision_evidence_pack' in m['required_inputs'] and 'evidence_integrity_receipt' in m['required_inputs']
    checks.append(('s3_decision_evidence_pack_transport',ok))
    ctx=(v/'RUNTIME'/'R2 Prompt Execution OS'/'alpha_prompt_runtime'/'context.py').read_text(encoding='utf-8');checks.append(('dynamic_retrieval_plan_execution','plan.get(\'selected_paths\'' in ctx and 'canonical_context_hashes' in ctx))
    host=(v/'RUNTIME'/'R3 Operational Execution and Learning OS'/'alpha_operational_runtime'/'host.py').read_text(encoding='utf-8');checks.append(('json_argv_host_contract','t.startswith(\'[\')' in host and 'json.loads(t)' in host))
    ret=(v/'RUNTIME'/'R3 Operational Execution and Learning OS'/'alpha_operational_runtime'/'retrieval.py').read_text(encoding='utf-8');checks += [('discovery_prefetch_present','ALPHALAB_OFFICIAL_MACRO_WEB' in ret and 'ALPHALAB_INSTITUTIONAL_MACRO_WEB' in ret and 'ALPHALAB_NARRATIVE_WEB' in ret and 'ALPHALAB_EVENT_WEB' in ret),('discovery_not_direct_candidate',"role in ('DIRECT','LICENSED')" in ret)]
    hp=load_json(v/'RUNTIME'/'R3 Operational Execution and Learning OS'/'config'/'host_policy.json');checks += [('host_timeout_3600',hp['bindings']['PRODUCTION_COMMAND']['timeout_seconds']>=3600),('accuracy_serial',hp.get('scheduler_default')=='SERIAL_DETERMINISTIC' and hp['bindings']['PRODUCTION_COMMAND'].get('max_parallel')==1)]
    lp=load_json(v/'RUNTIME'/'R3 Operational Execution and Learning OS'/'config'/'launcher_profiles.json');checks.append(('default_deep',lp['defaults']['research_depth']=='DEEP'))
    cp=load_json(c/'config'/'commissioning_policy.json');checks += [('readiness_manual_signoff',cp['manual_signoff_required'] is True),('readiness_zero_dc_gap',cp['readiness_requires_zero_decision_critical_gaps_in_shadow_basket'] is True)]
    # syntax in memory, no pyc
    pyerr=[]
    for p in c.rglob('*.py'):
        try:ast.parse(p.read_text(encoding='utf-8-sig'))
        except Exception as e:pyerr.append(str(p.relative_to(v))+': '+str(e))
    checks.append(('commissioning_python_syntax_in_memory',not pyerr));errors+=pyerr
    # command encoding roundtrip
    try:a=json.loads(host_command_json(v));cmdok=isinstance(a,list) and len(a)==2 and Path(a[1]).name=='openai_host.py'
    except Exception:cmdok=False
    checks.append(('host_command_json_argv_roundtrip',cmdok))
    launch=(c/'alpha_commissioning'/'launcher.py').read_text(encoding='utf-8');checks.append(('live_requires_signed_current_readiness','PRODUCTION_READY_PERMISSION_ONLY' in launch and 'readiness receipt is stale' in launch and 'Git commit/working tree differs' in launch))
    try:
        rb=[c/'wrappers'/'AlphaLab.ps1',c/'wrappers'/'AlphaLab_Commission.ps1'];wrapok=all(p.is_file() and all(b<128 for b in p.read_bytes()) for p in rb)
    except Exception:wrapok=False
    checks.append(('wrapper_templates_ascii',wrapok))
    # TF1 true-forward activation is source/runtime observability only; no new authority.
    try:
        tf=load_json(c/'TRUE_FORWARD_MANIFEST.json');tp=load_json(c/'config'/'true_forward_policy.json')
        checks += [('tf1_manifest',tf.get('true_forward_version')=='TF1.0.1'),('tf1_broker_none',tf.get('authority',{}).get('broker_write')=='NONE' and tp.get('broker_write') is False),('tf1_apla_shadow_only',tf.get('authority',{}).get('apl_a')=='SHADOW_ONLY'),('tf1_mutable_records_outside_r4',tp.get('mutable_forward_records_in_r4_source_fingerprint') is False)]
        from .true_forward import selftest as tf_selftest
        tr=tf_selftest(v);checks.append(('tf1_true_forward_selftest',tr.get('status')=='PASS'))
    except Exception as e:
        checks.append(('tf1_true_forward_selftest',False));errors.append('TF1: '+str(e))
    # TF3 continuous forward operations: operations only, no authority.
    try:
        tf3=load_json(c/'TF3_CONTINUOUS_FORWARD_OPERATIONS_MANIFEST.json');t3p=load_json(c/'config'/'continuous_forward_policy.json')
        checks += [('tf3_manifest',tf3.get('version')=='TF3.0.0'),('tf3_broker_none',tf3.get('authority',{}).get('broker_write')=='NONE' and t3p.get('broker_write') is False),('tf3_apla_shadow_only',tf3.get('authority',{}).get('apl_a')=='SHADOW_ONLY'),('tf3_mutable_records_outside_r4',t3p.get('mutable_forward_records_in_r4_source_fingerprint') is False)]
        from .continuous_forward import selftest as tf3_selftest
        t3=tf3_selftest(v);checks.append(('tf3_continuous_forward_selftest',t3.get('status')=='PASS'))
    except Exception as e:
        checks.append(('tf3_continuous_forward_selftest',False));errors.append('TF3: '+str(e))
    errors += [n for n,ok in checks if not ok]
    return {'schema_version':'1.0.0','status':'PASS' if not errors else 'FAIL','passed':sum(1 for _,x in checks if x),'total':len(checks),'checks':[{'name':n,'pass':bool(ok)} for n,ok in checks],'errors':errors}
