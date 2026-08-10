from pathlib import Path
from .registry import MethodRegistry
from .router import route
from .plan import build as build_plan
from .validator import assess
from .util import validate_schema

BASE_REQ={'schema_version':'1.0.0','research_program_id':'TEST','run_scope':'INSTRUMENT','subject':'NASDAQ100','instrument':'NASDAQ100','run_mode':'HISTORICAL_REPLAY','analysis_cutoff':'2026-08-01T12:00:00Z','analysis_cutoff_utc':'2026-08-01T12:00:00Z','strategy_id':'FUNDAMENTAL_ONLY','active_horizon':'DAILY_OPEN_TO_CLOSE','coverage_mode':'STRICT_FULL','research_depth':'AUTO','output_depth':'MACHINE','lookahead_policy':'STRICT_POINT_IN_TIME','tags':[]}

def ev(eid,**kw):
    x={'evidence_id':eid,'evidence_class':'DIRECT_OBSERVATION','availability_state':'AVAILABLE','materiality':'MATERIAL','source_id':'SRC_'+eid,'root_source_id':'ROOT_'+eid,'publication_time':'2026-08-01T10:00:00Z','first_available_time':'2026-08-01T10:00:00Z','ingestion_time':'2026-08-01T10:05:00Z','value':1}; x.update(kw); return x

def claim(cid,**kw):
    x={'claim_id':cid,'claim_type':'OBSERVATION','lifecycle_state':'ACTIVE','statement':'fixture','evidence_ids':[],'contradictory_evidence_ids':[],'research_mode':'OPERATIONAL','directness':'DIRECT'}; x.update(kw); return x

def run(vault_root):
    v=Path(vault_root); reg=MethodRegistry(v); checks=[]
    def ck(n,c,d=None): checks.append({'name':n,'pass':bool(c),'detail':d})
    ck('manifest_registry',not reg.validate(),reg.validate())
    # Router flexibility
    examples=[
      (dict(BASE_REQ,tags=['descriptive']), 'DESCRIPTIVE_STATE_ESTIMATION'),
      (dict(BASE_REQ,coverage_mode='EVENT_FAST_STRICT',tags=['event:CPI']),'EVENT_ANALYSIS'),
      (dict(BASE_REQ,tags=['research_class:CAUSAL_ATTRIBUTION']),'CAUSAL_ATTRIBUTION'),
      (dict(BASE_REQ,tags=[]),'DIRECTIONAL_FORECAST'),
      (dict(BASE_REQ,tags=['persistence']),'PERSISTENCE_REVERSAL'),
      (dict(BASE_REQ,tags=['narrative']),'NARRATIVE_ATTENTION'),
      (dict(BASE_REQ,tags=['regime']),'REGIME_ANALYSIS'),
      (dict(BASE_REQ,tags=['structural']),'STRUCTURAL_LONG_HORIZON_THESIS'),
      (dict(BASE_REQ,tags=['relative-value']),'CROSS_SECTIONAL_RELATIVE_VALUE'),
      (dict(BASE_REQ,tags=['exposure']),'EXPOSURE_RISK_ANALYSIS'),
      (dict(BASE_REQ,tags=['model-validation']),'MODEL_VALIDATION'),
      (dict(BASE_REQ,tags=['failure-investigation']),'ANOMALY_FAILURE_INVESTIGATION'),
      (dict(BASE_REQ,tags=['new-asset']),'NEW_ASSET_RESEARCH')]
    for i,(rq,exp) in enumerate(examples,1): ck('route_'+str(i),route(v,rq)['research_class']==exp)
    p=build_plan(v,'RUN_TEST',BASE_REQ); ck('plan_schema',validate_schema(v,reg.schema_ref('AlphaLab_Method_Plan.schema.json'),p))
    # R2 bootstrap integration: Method Plan is META and does not add a method-specific lifecycle event.
    import tempfile
    from .util import add_paths
    add_paths(v)
    from alpha_runtime.runtime import AlphaRuntime
    from alpha_prompt_runtime.orchestrator import R2Orchestrator
    with tempfile.TemporaryDirectory(prefix='alphalab_method_hook_') as td:
        rt=AlphaRuntime(v,td); rq=dict(BASE_REQ); rq.pop('analysis_cutoff_utc',None); rq.update({'episode_id':None,'execution_profile':'PERMISSION_ONLY_V1','allow_private_sources':False,'idempotency_policy':'NEW_RUN'})
        m,_=rt.create_run(rq,run_id='RUN_METHOD_HOOK')
        with rt.catalog.connect() as c: before_seq=c.execute('SELECT COALESCE(MAX(sequence),0) FROM run_events WHERE run_id=?',(m['run_id'],)).fetchone()[0]
        R2Orchestrator(rt).bootstrap(m['run_id'])
        names={r['logical_name']:r for r in rt.catalog.list_artifacts(m['run_id'])}
        with rt.catalog.connect() as c: after_seq=c.execute('SELECT COALESCE(MAX(sequence),0) FROM run_events WHERE run_id=?',(m['run_id'],)).fetchone()[0]
        ck('r2_bootstrap_method_plan_meta','method_plan' in names and names['method_plan']['world']=='META')
        ck('r2_method_no_extra_event',after_seq==before_seq+1,{'before':before_seq,'after':after_seq})
    # Adversarial 1 future leakage
    def A(evidence=None,claims=None,req=None): return assess(v,'RUN_TEST',p,{'run_request':req or BASE_REQ,'evidence':evidence or [],'claims':claims or []},'AD_HOC')
    r=A([ev('FUT',publication_time='2026-08-01T13:00:00Z')]); ck('adv_future_leakage',r['status']=='OUTPUT_QUARANTINED' and r['hard_failure_count']>0)
    r=A([ev('A',root_source_id='ROOT_X'),ev('B',root_source_id='ROOT_X')]); ck('adv_same_root',r['status']=='RESEARCH_REQUIRED')
    pe=ev('P',evidence_class='PROXY',proxy_contract_id=None); pc=claim('C',evidence_ids=['P'],directness='DIRECT'); r=A([pe],[pc]); ck('adv_proxy_reification',r['status']=='RESEARCH_REQUIRED')
    pe=ev('PDOM',evidence_class='PROXY',proxy_contract_id='PX_VALID',proxy_domain_state='OUT_OF_DOMAIN'); pc=claim('PDOM_C',evidence_ids=['PDOM'],directness='INDIRECT'); r=A([pe],[pc]); ck('adv_proxy_out_of_domain',r['status']=='RESEARCH_REQUIRED' and any(x['code']=='M015_PROXY_OUT_OF_DOMAIN' for x in r['findings']))
    r=A([ev('U',availability_state='UNAVAILABLE',value=0)]); ck('adv_unknown_zero',r['status']=='OUTPUT_QUARANTINED')
    r=A([], [claim('CA',claim_type='CAUSAL_HYPOTHESIS',mechanism=None,identification_state='NOT_IDENTIFIED',assertion_strength='CAUSAL_ESTABLISHED',directness='INDIRECT')]); ck('adv_correlation_causation',r['status']=='METHOD_INVALID')
    r=A([], [claim('NC',claim_type='NARRATIVE_CLAIM',circular_validation=True,directness='NARRATIVE')]); ck('adv_narrative_circularity',r['status']=='RESEARCH_REQUIRED')
    r=A([], [claim('RG',claim_type='REGIME_CLAIM',regime_label_available_at_cutoff=False,directness='INDIRECT')]); ck('adv_regime_leakage',r['status']=='OUTPUT_QUARANTINED')
    ce=ev('CON',relation='CONTRADICTING'); ce['claim_id']='CC'; r=A([ce],[claim('CC',contradictory_evidence_ids=[])]); ck('adv_contradiction_suppression',r['status']=='METHOD_INVALID')
    r=A([], [claim('PR',claim_type='FORECAST',probability=.87,probability_type='CALIBRATED_PROBABILITY',calibration_id=None,directness='INDIRECT')]); ck('adv_fake_probability',r['status']=='METHOD_INVALID')
    r=A([ev('H1',relation='HORIZON_DEPENDENT'),ev('H2',relation='HORIZON_DEPENDENT')],[claim('HC',evidence_ids=['H1','H2'],directness='INDIRECT')]); ck('adv_horizon_conflict_preserved',r['status'] in ('PASS','WARNING'))
    r=A([], [claim('OV',research_mode='CONFIRMATORY',search_space_size=200,discovered_post_search=True,directness='INDIRECT')]); ck('adv_exploratory_overfit',r['status']=='RESEARCH_REQUIRED')
    simple_req=dict(BASE_REQ,tags=['descriptive']); sp=build_plan(v,'RUN_SIMPLE',simple_req); r=assess(v,'RUN_SIMPLE',sp,{'run_request':simple_req,'evidence':[ev('TS')],'claims':[claim('TS_C',evidence_ids=['TS'])]},'AD_HOC'); ck('adv_valid_simple',r['status']=='PASS')
    # Explicit invariants / boundaries
    ck('no_direction_authority',reg.manifest['authority']['direction']=='NONE')
    ck('no_permission_authority',reg.manifest['authority']['permission']=='NONE')
    ck('no_apl_b',reg.manifest['apl_b']=='NOT_IMPLEMENTED')
    ck('meta_world',reg.manifest['artifact_world']=='META')
    errs=[x['name'] for x in checks if not x['pass']]
    return {'status':'PASS' if not errs else 'FAIL','passed':len(checks)-len(errs),'total':len(checks),'checks':checks,'errors':errs}
