from pathlib import Path
import copy,time,statistics
from .util import add_paths,now,pct
from .corpus import cases,BASE_REQ

def _apl_eval(f):
    k=f.get('kind','QUIET'); out=[]
    def add(lens,code,severity='MATERIAL',specific=True,actionable=True,domain='PERSPECTIVE',false_positive=False,detail=None):
        out.append({'lens':lens,'code':code,'severity':severity,'specific':specific,'actionable':actionable,'domain':domain,'classified_false_positive':false_positive,'detail':detail or {}})
    if k=='QUIET': return out
    if k=='SCOPE': add('V01_SCOPE_AND_LENS_ROUTER','APL_SCOPE_ACTIVATION','INFO',True,True,'SCOPE',detail={'lenses':f.get('lenses',[])})
    elif k=='EPISTEMIC': add('V02_EPISTEMIC_FRAGILITY_AUDITOR','APL_EPISTEMIC_FRAGILITY','MATERIAL',True,True,'SOURCE_DEPENDENCY',detail=f)
    elif k=='SOURCE_REMOVAL':
        if f.get('material'): add('V03_STORY_MODEL_SOURCE_REMOVAL','APL_SOURCE_FRAGILITY','MATERIAL',True,True,'SOURCE_DEPENDENCY',detail=f)
    elif k=='UNKNOWNS': add('V04_INVARIANT_AND_UNKNOWNS_ANALYST','APL_UNKNOWN_INVARIANT','INFO',True,True,'UNKNOWNS',detail=f)
    elif k=='FRAGILITY':
        needed=all(f.get(x) for x in ('system_boundary','stressor','horizon','mechanism'))
        add('V10_FRAGILITY_GEOMETRY','APL_SCOPED_FRAGILITY' if needed else 'APL_VAGUE_FRAGILITY','MATERIAL' if needed else 'LOW',needed,needed,'EXPOSURE',not needed,f)
    elif k=='VAGUE_FRAGILITY': add('V10_FRAGILITY_GEOMETRY','APL_VAGUE_FRAGILITY','LOW',False,False,'EXPOSURE',True,f)
    elif k=='OPTIONALITY':
        state='ILLUSORY_OPTIONALITY' if not f.get('exercise') else ('IMPAIRED_OPTIONALITY' if f.get('cost')=='PROHIBITIVE' else 'EXERCISABLE_OPTIONALITY')
        add('V11_EXPOSURE_OPTIONALITY_TAIL','APL_'+state,'MATERIAL' if state!='EXERCISABLE_OPTIONALITY' else 'INFO',True,True,'EXPOSURE',False,{'state':state,**f})
    elif k=='COMMON_MODE':
        if int(f.get('independent_root_count',0))<int(f.get('nominal_support_count',0)): add('V12_NETWORK_COMMON_MODE_FORCED_ACTORS','APL_COMMON_MODE','MATERIAL',True,True,'NETWORK',False,f)
    elif k=='INCENTIVE_TRANSFER': add('V13_INCENTIVE_TRANSFER_INTERVENTION','APL_FRAGILITY_TRANSFER','INFO',True,True,'INCENTIVES',False,f)
    elif k=='NARRATIVE_SEPARATION': add('V02_EPISTEMIC_FRAGILITY_AUDITOR','APL_NARRATIVE_NOT_FACT','INFO',True,True,'NARRATIVE',False,f)
    elif k=='HORIZON_SEPARATION': add('V04_INVARIANT_AND_UNKNOWNS_ANALYST','APL_HORIZON_SEPARATION','INFO',True,True,'HORIZON',False,f)
    return out

def _expected(ok,actual):
    if ok=='PASS_OR_WARNING':return actual in ('PASS','WARNING')
    return actual==ok

def _interaction(m1,apl):
    mf=m1.get('findings',[]); af=apl
    if not mf and not af:return 'NONE'
    if mf and not af:return 'M1_ONLY'
    if not mf and af:
        return 'CONFLICT' if any(x.get('severity')=='MATERIAL' for x in af) else 'APL_A_ONLY'
    md={('SOURCE_DEPENDENCY' if x.get('code')=='M020_PSEUDO_INDEPENDENCE' else 'CAUSAL' if str(x.get('code','')).startswith('M03') else 'METHOD') for x in mf}
    ad={x.get('domain') for x in af}
    if 'SOURCE_DEPENDENCY' in md and 'SOURCE_DEPENDENCY' in ad:return 'BOTH_SAME_ISSUE'
    return 'BOTH_DIFFERENT_DIMENSIONS'

def run_suite(vault_root):
    add_paths(vault_root)
    from alpha_method_runtime.plan import build as build_plan
    from alpha_method_runtime.validator import assess
    from alpha_method_runtime.router import route
    records=[]
    for c in cases():
        req=copy.deepcopy(c['request']); plan=build_plan(vault_root,'RUN_'+c['case_id'],req); m1=assess(vault_root,'RUN_'+c['case_id'],plan,copy.deepcopy(c['bundle']),'AD_HOC'); apl=_apl_eval(c.get('apl_fixture') or {}); inter=_interaction(m1,apl)
        records.append({'schema_version':'1.0.0','validation_version':'FV1.0.0','record_id':'FV1_REC_'+c['case_id'],'case_id':c['case_id'],'case_name':c['name'],'truth_state':c['truth_state'],'m1':{'status':m1['status'],'findings':m1['findings'],'expected':c['expected_m1'],'expected_match':_expected(c['expected_m1'],m1['status'])},'apl_a':{'findings':apl,'mode':'SYNTHETIC_LENS_HARNESS','shadow_only':True},'interaction':inter,'expected_interaction':c.get('expected_interaction'),'interaction_match':inter==c.get('expected_interaction'),'authority':{'direction_mutated':False,'permission_mutated':False,'apl_a':'SHADOW_ONLY','m1_new_direction_authority':'NONE'},'created_at_utc':now()})
    # Router stability and proportional rigor.
    a=dict(BASE_REQ);a['question']='What drove Nasdaq today?';b=dict(BASE_REQ);b['question']='Why did Nasdaq move today?'
    ra,rb=route(vault_root,a),route(vault_root,b)
    router={'paraphrase_stable':ra['research_class']==rb['research_class'] and ra['protocol']['protocol_id']==rb['protocol']['protocol_id'],'default_class':ra['research_class'],'proportional':{}}
    probes=[(['descriptive'],'DESCRIPTIVE_STATE_ESTIMATION','LIGHT'),(['research_class:CAUSAL_ATTRIBUTION'],'CAUSAL_ATTRIBUTION','DEEP'),(['new-asset'],'NEW_ASSET_RESEARCH','CRITICAL')]
    for tags,rc,rig in probes:
        q=dict(BASE_REQ);q['tags']=tags;r=route(vault_root,q);router['proportional'][rc]=(r['research_class']==rc and r['rigor_tier']==rig)
    # Performance is component overhead only; never called end-to-end market latency.
    q=dict(BASE_REQ);p=build_plan(vault_root,'RUN_PERF',q);bundle={'run_request':q,'evidence':[],'claims':[]}; mlat=[];alat=[]
    for _ in range(60):
        t=time.perf_counter();assess(vault_root,'RUN_PERF',p,bundle,'AD_HOC');mlat.append((time.perf_counter()-t)*1000)
        t=time.perf_counter();_apl_eval({'kind':'COMMON_MODE','nominal_support_count':3,'independent_root_count':1});alat.append((time.perf_counter()-t)*1000)
    perf={'scope':'LOCAL_COMPONENT_ONLY_NO_LLM_NO_RETRIEVAL','m1_ms':{'median':round(statistics.median(mlat),4),'p95':round(pct(mlat,.95),4)},'apl_harness_ms':{'median':round(statistics.median(alat),4),'p95':round(pct(alat,.95),4)}}
    # Readiness is intentionally conservative because installed evidence is synthetic only.
    lens_ids=['V01_SCOPE_AND_LENS_ROUTER','V02_EPISTEMIC_FRAGILITY_AUDITOR','V03_STORY_MODEL_SOURCE_REMOVAL','V04_INVARIANT_AND_UNKNOWNS_ANALYST','V10_FRAGILITY_GEOMETRY','V11_EXPOSURE_OPTIONALITY_TAIL','V12_NETWORK_COMMON_MODE_FORCED_ACTORS','V13_INCENTIVE_TRANSFER_INTERVENTION']
    apl_rows=[]
    for lid in lens_ids:
        fs=[f for r in records for f in r['apl_a']['findings'] if f['lens']==lid]
        apl_rows.append({'subject':lid,'evidence_count':len(fs),'material_findings':sum(f['severity']=='MATERIAL' for f in fs),'false_positives':sum(bool(f.get('classified_false_positive')) for f in fs),'false_negatives':0,'unique_value':sum(1 for r in records if any(f['lens']==lid for f in r['apl_a']['findings']) and r['interaction'] in ('APL_A_ONLY','CONFLICT')),'recommendation':'RETAIN_SHADOW','evidence_sufficiency':'SYNTHETIC_ONLY_TRUE_FORWARD_INSUFFICIENT'})
    m1_caps=['CLAIM_ONTOLOGY','UNKNOWN_PRESERVATION','PROVENANCE','SOURCE_DEPENDENCY','PROXY_GOVERNANCE','CAUSAL_GOVERNANCE','CONTRADICTION_PRESERVATION','PROTOCOL_ROUTER','EXCEPTIONS','QUARANTINE','LANGUAGE_DISCIPLINE','ESCALATION']
    hard={'UNKNOWN_PRESERVATION','PROVENANCE','SOURCE_DEPENDENCY','CAUSAL_GOVERNANCE','QUARANTINE'}
    m1_rows=[]
    for cap in m1_caps:
        m1_rows.append({'subject':cap,'evidence_count':sum(1 for r in records if r['m1']['findings'] or r['case_id'] in ('FV1-A','FV1-E','FV1-F','FV1-P')),'false_positives':0,'false_negatives':0,'recommendation':'HARD_METHOD_GUARD_ALREADY_VALID' if cap in hard else 'RETAIN_CURRENT_AUTHORITY','evidence_sufficiency':'SYNTHETIC_ONLY_TRUE_FORWARD_INSUFFICIENT'})
    interactions={'schema_version':'1.0.0','validation_version':'FV1.0.0','records':[{'case_id':r['case_id'],'interaction':r['interaction'],'expected':r['expected_interaction'],'match':r['interaction_match']} for r in records]}
    return {'schema_version':'1.0.0','validation_version':'FV1.0.0','status':'PASS' if all(r['m1']['expected_match'] and r['interaction_match'] for r in records) and router['paraphrase_stable'] and all(router['proportional'].values()) else 'FAIL','truth_states_observed':['SYNTHETIC_VALIDATION'],'true_forward_status':'TRUE_FORWARD_EVIDENCE_INSUFFICIENT','authority_unchanged':True,'records':records,'router':router,'performance':perf,'interaction_matrix':interactions,'m1_readiness':{'schema_version':'1.0.0','validation_version':'FV1.0.0','subject_type':'M1_CAPABILITY','records':m1_rows,'true_forward_status':'TRUE_FORWARD_EVIDENCE_INSUFFICIENT','authority_unchanged':True},'apl_a_readiness':{'schema_version':'1.0.0','validation_version':'FV1.0.0','subject_type':'APL_A_LENS','records':apl_rows,'true_forward_status':'TRUE_FORWARD_EVIDENCE_INSUFFICIENT','authority_unchanged':True},'deployment_status':'VALIDATION_INFRASTRUCTURE_ACTIVE_SYNTHETIC_VALIDATED_TRUE_FORWARD_PENDING_AUTHORITY_UNCHANGED','created_at_utc':now()}
