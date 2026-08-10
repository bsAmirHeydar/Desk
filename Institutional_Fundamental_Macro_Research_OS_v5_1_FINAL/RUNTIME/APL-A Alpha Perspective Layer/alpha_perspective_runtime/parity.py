from pathlib import Path
import tempfile, json, sys
from .util import add_paths, shaobj
from .shadow import run_shadow

class FixtureHost:
    def __init__(self, run_id): self.run_id=run_id
    def invoke(self, inv, attempt):
        p=inv['process_id']; rid=inv['run_id']
        payloads={
            'V01_SCOPE_AND_LENS_ROUTER': {
                'apl_lens_activation_receipt': {'schema_version':'1.0.0','run_id':rid,'lenses':[{'lens_id':'EPISTEMIC_FRAGILITY','state':'ACTIVE','reason':'fixture materiality'}],'scope_cards':[{'lens_id':'EPISTEMIC_FRAGILITY','domain':'MARKET_RESEARCH','system_boundary':'RUN_THESIS','stressor':'MODEL_REMOVAL','stressor_range':'ONE_LOAD_BEARING_MODEL','welfare_metric':'EPISTEMIC_INTEGRITY','scale':'RUN','horizon':'DAILY_OPEN_TO_CLOSE','state':'TEST','mechanism':'removal sensitivity','evidence_layer':'D1_ADMITTED','reversal_conditions':['decision survives removal'],'externalities':[]}]}
            },
            'V02_EPISTEMIC_FRAGILITY_AUDITOR': {
                'apl_epistemic_perspective': {'schema_version':'1.0.0','run_id':rid,'states':['MODEL_ROBUST'],'findings':[{'finding':'fixture','evidence_references':['ROOT_A']}],'research_needed':[]}
            },
            'V03_STORY_MODEL_SOURCE_REMOVAL': {
                'apl_removal_audit': {'schema_version':'1.0.0','run_id':rid,'audits':[{'audit_type':'MODEL_REMOVAL','removed_object':'MODEL_A','baseline_conclusion':'UNCHANGED','surviving_evidence':['ROOT_A'],'changed_conclusions':[],'unchanged_conclusions':['THESIS_A'],'fragile_dependencies':[],'robust_dependencies':['ROOT_A'],'decision_sensitive_dependency':False,'invariant_candidates':['INVARIANT_A']}]}
            },
            'V04_INVARIANT_AND_UNKNOWNS_ANALYST': {
                'apl_invariant_set': {'schema_version':'1.0.0','run_id':rid,'invariants':[{'invariant_id':'INV_A','statement':'INVARIANT_A','supporting_model_classes':['MODEL_B'],'surviving_source_roots':['ROOT_A'],'horizon':'DAILY_OPEN_TO_CLOSE','scope':'FIXTURE','break_condition':'ROOT_A_INVALID','evidence_references':['ROOT_A'],'known_limitations':['fixture']}]},
                'apl_unknowns_register': {'schema_version':'1.0.0','run_id':rid,'known_unknowns':['UNKNOWN_A'],'unobservables':[],'unmodeled_driver_candidates':[]}
            },
            'V10_FRAGILITY_GEOMETRY': {
                'apl_fragility_map': {'schema_version':'1.0.0','run_id':rid,'maps':[{'system':'THESIS_A','stressor':'YIELD_SHOCK','stressor_range':'MILD_TO_MEDIUM','state':'TEST','horizon':'DAILY_OPEN_TO_CLOSE','welfare_metric':'THESIS_STABILITY','path':'DIRECT','scale':'RUN','geometry_state':'APPROX_LINEAR','thresholds':[],'tail_orientation':'NONE_ASSERTED','reversal_conditions':['STATE_CHANGE'],'evidence_references':['ROOT_A']}]}
            },
            'V11_EXPOSURE_OPTIONALITY_TAIL': {
                'apl_exposure_optionality_map': {'schema_version':'1.0.0','run_id':rid,'exposures':[{'exposure':'THESIS_A','optionality_state':'EXERCISABLE_OPTIONALITY','reversibility':'REVERSIBLE','tail_state':'BOUNDED_FOR_FIXTURE'}],'ruin_perspective':'NOT_MATERIAL'}
            },
            'V12_NETWORK_COMMON_MODE_FORCED_ACTORS': {
                'apl_network_common_mode_map': {'schema_version':'1.0.0','run_id':rid,'nominal_support_count':2,'independent_root_count':1,'dependencies':[{'root_id':'ROOT_A'}],'common_mode_risks':['ROOT_A'],'forced_actors':[]}
            },
            'V13_INCENTIVE_TRANSFER_INTERVENTION': {
                'apl_agency_intervention_map': {'schema_version':'1.0.0','run_id':rid,'actors':[],'fragility_transfers':[],'interventions':[]},
                'apl_research_requests': {'schema_version':'1.0.0','run_id':rid,'requests':[]}
            }
        }[p]
        return ({'status':'OK','process_output':{'schema_version':'1.0.0','process_id':p,'artifacts':payloads}}, {'schema_version':'1.0.0','provider':'FIXTURE','model':'APL_PARITY','request_hash':shaobj(inv),'response_hash':shaobj(payloads),'attempt':attempt})

def run(vault_root):
    v=Path(vault_root); add_paths(v)
    from alpha_runtime.runtime import AlphaRuntime
    from alpha_runtime.seal_safe import create_decision_seal
    with tempfile.TemporaryDirectory(prefix='alphalab_apla_parity_') as td:
        rt=AlphaRuntime(v,td)
        req={'schema_version':'1.0.0','research_program_id':'APL_A_PARITY','episode_id':None,'run_scope':'INSTRUMENT','subject':'NASDAQ100','instrument':'NASDAQ100','run_mode':'HISTORICAL_REPLAY','analysis_cutoff':'2026-07-01T12:00:00Z','strategy_id':'FUNDAMENTAL_ONLY','active_horizon':'DAILY_OPEN_TO_CLOSE','coverage_mode':'STRICT_FULL','research_depth':'DEEP','output_depth':'FULL','lookahead_policy':'STRICT_POINT_IN_TIME','execution_profile':'SHADOW_ONLY_V1','allow_private_sources':False,'idempotency_policy':'NEW_RUN','tags':['apl-a-parity']}
        m,_=rt.create_run(req,vault_commit='APL_A_PARITY',run_id='RUN_APL_A_PARITY')
        rid=m['run_id']
        rt.lifecycle.transition(rid,'INPUTS_RESOLVED'); rt.lifecycle.transition(rid,'SNAPSHOT_FROZEN'); rt.lifecycle.transition(rid,'EVIDENCE_FROZEN')
        core={
            'decision_evidence_pack':{'schema_version':'1.0.0','facts':[{'fact_id':'F1','root_id':'ROOT_A','epistemic_class':'OBSERVED_FACT','value':'FIXTURE'}]},
            'evidence_integrity_receipt':{'schema_version':'1.0.0','independent_root_ids':['ROOT_A'],'status':'PASS'},
            'market_state_reconciliation':{'schema_version':'1.0.0','instrument':'NASDAQ100','state':'TEST','fundamental_direction':'BULLISH'},
            'hypothesis_set':{'schema_version':'1.0.0','hypotheses':[{'hypothesis_id':'H1','statement':'THESIS_A','status':'SURVIVES'}]},
            'causal_graph':{'schema_version':'1.0.0','nodes':['ROOT_A'],'edges':[]},
            'root_channel_map':{'schema_version':'1.0.0','roots':[{'root_id':'ROOT_A','channels':[]}]},
            'scenario_tree':{'schema_version':'1.0.0','scenarios':[{'scenario_id':'S1','statement':'BASE'}]},
            'final_permission':{'schema_version':'1.0.0','instrument':'NASDAQ100','active_horizon':'DAILY_OPEN_TO_CLOSE','direction_authority':'FUNDAMENTAL_ONLY','permission':'NO_TRADE','validity':{},'review_trigger':{},'invalidation_triggers':[],'outside_strategy_edges_permission_effect':'NONE','operational_execution_gate':'R3_PENDING'},
            'research_intent':{'fundamental_direction':'BULLISH','edge_state':'NO_EDGE','active_horizon':'DAILY_OPEN_TO_CLOSE'},
            'cognitive_adjudication':{'fundamental_direction':'BULLISH'},
            'd3_adjudication':{'pre_d3_permission':'NO_TRADE','final_permission':'NO_TRADE','d3_edge_quality':'CONSTRAINED','deduplicated_root_ids':['ROOT_A']},
            'd4_authority_receipt':{'registry_version':'1.0.0','v19_d3_permission':'NO_TRADE','final_v20_permission':'NO_TRADE','applied_promotion_ids':[],'shadow_candidate_ids':[]},
            'global_reconciliation':{'schema_version':'1.0.0','state':'CONSISTENT'}
        }
        for name,payload in core.items(): rt.store.put_artifact(rid,name,'DECISION','DECISION',payload,'application/json',producer_process_id='APL_PARITY_CORE',producer_version='1.0.0')
        rt.lifecycle.transition(rid,'COGNITION_FROZEN'); create_decision_seal(rid,rt)
        upstream_names=['decision_evidence_pack','evidence_integrity_receipt','market_state_reconciliation','hypothesis_set','causal_graph','root_channel_map','scenario_tree']
        before={r['logical_name']:r['artifact_hash'] for r in rt.catalog.list_artifacts(rid,'DECISION') if r['logical_name'] in upstream_names}
        all_decision_before={r['logical_name']:r['artifact_hash'] for r in rt.catalog.list_artifacts(rid,'DECISION')}
        seal_before=rt.store.load_manifest(rid)['decision_seal_hash']
        out=run_shadow(v,rt,lambda production:None,rid,production=False,fixture_host=FixtureHost(rid))
        after={r['logical_name']:r['artifact_hash'] for r in rt.catalog.list_artifacts(rid,'DECISION') if r['logical_name'] in upstream_names}
        all_decision_after={r['logical_name']:r['artifact_hash'] for r in rt.catalog.list_artifacts(rid,'DECISION')}
        seal_after=rt.store.load_manifest(rid)['decision_seal_hash']
        learning=[r['logical_name'] for r in rt.catalog.list_artifacts(rid,'LEARNING')]
        rt.catalog.checkpoint()
        checks={
            'upstream_hashes_identical': before==after,
            'entire_decision_world_identical': all_decision_before==all_decision_after,
            'decision_seal_identical': seal_before==seal_after,
            'apl_shadow_pass': out.get('status')=='PASS' and out.get('decision_world_unchanged') is True,
            'apl_outputs_learning_only': 'apl_a_shadow_bundle' in learning and 'apl_a_forward_telemetry' in learning,
        }
        return {'schema_version':'1.0.0','status':'PASS' if all(checks.values()) else 'FAIL','run_id':rid,'mode':'APL_DISABLED_VS_APL_ENABLED_SHADOW','upstream_artifacts_before':before,'upstream_artifacts_after':after,'decision_seal_before':seal_before,'decision_seal_after':seal_after,'checks':[{'name':k,'pass':val} for k,val in checks.items()],'learning_artifacts':learning}
