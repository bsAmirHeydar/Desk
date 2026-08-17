from __future__ import annotations
import json, pathlib, tempfile, sys, shutil, subprocess
P=pathlib.Path(__file__).resolve().parents[1]; N=P.parent; sys.path.insert(0,str(N))
from AD_V3_PHASE_03_CAUSAL_GOLD_BRAIN_DECISION_ENGINE.runtime.engine import execute

def load(p): return json.loads(pathlib.Path(p).read_text(encoding='utf-8-sig'))
def write(p,o): pathlib.Path(p).parent.mkdir(parents=True,exist_ok=True); pathlib.Path(p).write_text(json.dumps(o,indent=2)+'\n')
def check(name,ok,detail=None): return {'name':name,'status':'PASS' if ok else 'FAIL','detail':detail}

def build_store(root,scenario):
    p01=load(N/'AD_V3_PHASE_01_TOTAL_GOLD_KNOWLEDGE_SCIENCE_FOUNDATION/config/gold_master_fact_registry.json')['facts']
    now='2026-08-16T21:00:00Z'; prev='2026-08-16T20:00:00Z'; prev_run='P02RUN_PREV_'+scenario; cur_run='P02RUN_CUR_'+scenario; rows=[]
    # default all facts accounted but unresolved/static-like.
    for f in p01:
        rows.append({'record_type':'AD_V3_P02_FACT_OBSERVATION','observation_id':'PREV_'+f['fact_id'],'phase':'AD-V3-P02','subject':'XAUUSD','fact_id':f['fact_id'],'source_id':'FIX','epistemic_state':'LATEST_VALID','value_type':'NONE','value':None,'unit':None,'reference_period':None,'event_time':None,'published_at':None,'first_seen_at':prev,'retrieved_at':prev,'revision_number':0,'supersedes_observation_id':None,'directness':'DIRECT','provenance_ref':'fixture','raw_sha256':'a','metadata':{},'warnings':[],'acquisition_run_id':prev_run})
        rows.append({'record_type':'AD_V3_P02_FACT_OBSERVATION','observation_id':'CUR_'+f['fact_id'],'phase':'AD-V3-P02','subject':'XAUUSD','fact_id':f['fact_id'],'source_id':'FIX','epistemic_state':'OBSERVED_CURRENT','value_type':'NONE','value':None,'unit':None,'reference_period':None,'event_time':None,'published_at':None,'first_seen_at':now,'retrieved_at':now,'revision_number':0,'supersedes_observation_id':None,'directness':'DIRECT','provenance_ref':'fixture','raw_sha256':'b','metadata':{},'warnings':[],'acquisition_run_id':cur_run})
    by={(r['observation_id']):r for r in rows}
    def setv(fid,pv,cv):
        a=by['PREV_'+fid]; b=by['CUR_'+fid]; a['value']=pv; b['value']=cv; a['value_type']=b['value_type']='NUMBER' if isinstance(cv,(int,float)) else 'OBJECT'; a['unit']=b['unit']='fixture'
    setv('UST_5Y_REAL_YIELD',-0.3,-0.5); setv('UST_10Y_REAL_YIELD',-0.2,-0.4); setv('UST_30Y_REAL_YIELD',-0.1,-0.3)
    setv('FED_BROAD_DOLLAR',120.0,119.0); setv('XAUUSD_SPOT_PRICE',4300.0,4350.0)
    if scenario=='neutral': setv('UST_5Y_REAL_YIELD',0.0,0.0); setv('UST_10Y_REAL_YIELD',0.0,0.0); setv('UST_30Y_REAL_YIELD',0.0,0.0)
    if scenario=='price_divergence': setv('XAUUSD_SPOT_PRICE',4350.0,4300.0)
    if scenario=='bearish_real': setv('UST_5Y_REAL_YIELD',0.2,0.4); setv('UST_10Y_REAL_YIELD',0.3,0.5); setv('UST_30Y_REAL_YIELD',0.4,0.6)
    if scenario=='static_positive_real': setv('UST_5Y_REAL_YIELD',2.12,2.12); setv('UST_10Y_REAL_YIELD',2.41,2.41); setv('UST_30Y_REAL_YIELD',3.0,3.0)
    if scenario=='positive_falling_real': setv('UST_5Y_REAL_YIELD',2.3,2.12); setv('UST_10Y_REAL_YIELD',2.6,2.41); setv('UST_30Y_REAL_YIELD',3.2,3.0)
    od=pathlib.Path(root)/'observations'; od.mkdir(parents=True,exist_ok=True)
    with (od/'gold_fact_observations.jsonl').open('w') as fh:
        for r in rows: fh.write(json.dumps(r)+'\n')
    receipt={'record_type':'AD_V3_P02_COVERAGE_RECEIPT','receipt_id':'FIXCOV_'+scenario,'phase':'AD-V3-P02','subject':'XAUUSD','as_of_utc':now,'generated_at_utc':now,'acquisition_run_id':cur_run,'acquisition_started_at_utc':'2026-08-16T20:59:00Z','observation_cutoff_utc':now,'acquisition_completed_at_utc':now,'horizon':'ALL','analysis_admission':'DEGRADED','analysis_may_start':True,'direction_authority_granted':False,'trade_permission_authority_granted':False,'fact_counts':{'p01_total':192,'applicable':192,'mandatory_attempt':126,'observations':192,'private_gaps':6,'paid_gaps':9,'provider_gaps':2,'unattempted_blocking':0,'failed_blocking':0},'source_counts':{},'zero_silent_omission':True,'observability_completeness_cap_applies':True}
    rd=pathlib.Path(root)/'receipts'; rd.mkdir(parents=True,exist_ok=True); write(rd/(receipt['receipt_id']+'.json'),receipt)
    return receipt, rows

def bundle(root,items):
    p=pathlib.Path(root)/'bundle.json'; write(p,{'record_type':'AD_V3_P03_SEMANTIC_ADJUDICATION_BUNDLE','subject':'XAUUSD','items':items}); return str(p)

def main():
    checks=[]
    v=subprocess.run([sys.executable,str(P/'tools/validate_phase03.py')],capture_output=True,text=True); checks.append(check('static validation',v.returncode==0,v.stdout[-500:]))
    with tempfile.TemporaryDirectory() as td:
        cov,rows=build_store(td,'bullish')
        r=execute(P,td)
        checks.append(check('all 192 facts in reasoning ledger',r['reasoning_ledger']['fact_count']==192 and r['reasoning_ledger']['zero_silent_omission']))
        checks.append(check('exact current acquisition run handoff complete',r.get('handoff_integrity',{}).get('exact_run_bound') is True and r.get('handoff_integrity',{}).get('current_observations_loaded')==192 and r.get('handoff_integrity',{}).get('missing_current_fact_ids')==[],r.get('handoff_integrity')))
        checks.append(check('all reasoning rows bind current observations',all(x.get('observation_id') is not None for x in r['reasoning_ledger']['rows']),sum(1 for x in r['reasoning_ledger']['rows'] if x.get('observation_id') is not None)))
        checks.append(check('real yield auto rule produces bullish root',next(x for x in r['pressure_planes']['causal_fundamental']['root_states'] if x['root_id']=='REAL_RATE_OPPORTUNITY_COST')['direction']=='BULLISH_GOLD'))
        checks.append(check('usd pathway cannot become additive root vote',next(x for x in r['reasoning_ledger']['rows'] if x['fact_id']=='FED_BROAD_DOLLAR')['is_additive'] is False))
        checks.append(check('price does not rewrite causal pressure',r['pressure_planes']['causal_fundamental']['direction']=='BULLISH_GOLD'))
        checks.append(check('free gaps cap completeness',r['model_quality']['model_completeness']!='HIGH'))
        checks.append(check('production authorities remain false',r['production_direction_authority_granted'] is False and r['production_trade_permission_authority_granted'] is False))
        checks.append(check('consumption vector emitted',set(r['lifecycle']['consumption_vector'])>=set(load(P/'config/consumption_persistence_policy.json')['consumption_components'])))
        checks.append(check('persistence stack emitted',r['lifecycle']['persistence_stack']['freshness_is_not_persistence'] is True))
        checks.append(check('remaining pressure emitted without scalar score',r['lifecycle']['remaining_pressure']['state'] in ('PRESENT','PARTIAL','CONTESTED','UNKNOWN')))
        checks.append(check('semantic adjudication request emitted',isinstance(r['semantic_adjudication_request'],list)))
    with tempfile.TemporaryDirectory() as td:
        build_store(td,'price_divergence'); r=execute(P,td)
        checks.append(check('negative price transmission detected',r['price_transmission']['state']=='NEGATIVE'))
        checks.append(check('negative transmission leaves causal direction bullish',r['pressure_planes']['causal_fundamental']['direction']=='BULLISH_GOLD'))
        checks.append(check('negative transmission raises missing driver risk',r['model_quality']['missing_driver_risk']=='HIGH'))
        checks.append(check('negative transmission forces wait candidate',r['shadow_decision']['action_candidate']=='WAIT'))
    with tempfile.TemporaryDirectory() as td:
        build_store(td,'bearish_real'); r=execute(P,td)
        checks.append(check('rising real yields bearish causal direction',r['pressure_planes']['causal_fundamental']['direction']=='BEARISH_GOLD'))
    with tempfile.TemporaryDirectory() as td:
        build_store(td,'static_positive_real'); r=execute(P,td,horizon='SESSION_1_6H')
        rr=next(x for x in r['pressure_planes']['causal_fundamental']['root_states'] if x['root_id']=='REAL_RATE_OPPORTUNITY_COST')
        real_rows=[x for x in r['reasoning_ledger']['rows'] if x['fact_id'] in ('UST_5Y_REAL_YIELD','UST_10Y_REAL_YIELD','UST_30Y_REAL_YIELD')]
        checks.append(check('static positive real yields remain bearish background only',rr.get('direction')=='UNKNOWN' and rr.get('background_bias')=='BEARISH_GOLD',rr))
        checks.append(check('static real-yield stock cannot refire session direction',r['pressure_planes']['causal_fundamental']['direction']=='UNKNOWN' and all(x.get('is_additive') is False for x in real_rows),[(x['fact_id'],x['effect_on_gold'],x['is_additive']) for x in real_rows]))
        checks.append(check('static real yields do not claim expectations repricing',r['lifecycle']['consumption_vector']['expectations_repricing']=='ABSENT',r['lifecycle']['consumption_vector']))
        checks.append(check('static real yields do not create persistence stack',r['lifecycle']['persistence_stack']['overall']=='UNKNOWN',r['lifecycle']['persistence_stack']))
        checks.append(check('static background only cannot create sell candidate',r['shadow_decision']['direction_candidate']=='UNKNOWN' and r['shadow_decision']['action_candidate']=='WAIT',r['shadow_decision']))
    with tempfile.TemporaryDirectory() as td:
        build_store(td,'positive_falling_real'); r=execute(P,td,horizon='SESSION_1_6H')
        rr=next(x for x in r['pressure_planes']['causal_fundamental']['root_states'] if x['root_id']=='REAL_RATE_OPPORTUNITY_COST')
        checks.append(check('positive but falling real yields are stock impulse conflict',rr['direction']=='MIXED' and rr.get('background_bias')=='BEARISH_GOLD' and rr.get('impulse_direction')=='BULLISH_GOLD',rr))
        checks.append(check('session real-yield impulse persistence is not structural',r['lifecycle']['persistence_stack']['overall']=='SESSION',r['lifecycle']['persistence_stack']))
    with tempfile.TemporaryDirectory() as td:
        cov,rows=build_store(td,'bullish'); cp=pathlib.Path(td)/'blocked.json'; cov['analysis_admission']='BLOCKED'; cov['analysis_may_start']=False; write(cp,cov); r=execute(P,td,str(cp))
        checks.append(check('blocked p02 coverage blocks p03',r['analysis_admission']=='BLOCKED'))
    with tempfile.TemporaryDirectory() as td:
        cov,rows=build_store(td,'bullish')
        # Attempt illegal additive semantic vote on positioning.
        bp=bundle(td,[{'fact_id':'CFTC_MANAGED_MONEY','observation_id':'CUR_CFTC_MANAGED_MONEY','effect_on_gold':'BULLISH_GOLD','effect_kind':'STOCK','strength':'HIGH','is_additive':True,'causal_owner_id':'US_POLICY_EXPECTATIONS','rationale_summary':'attack'}]); r=execute(P,td,adjudication_path=bp)
        row=next(x for x in r['reasoning_ledger']['rows'] if x['fact_id']=='CFTC_MANAGED_MONEY'); checks.append(check('illegal positioning additive vote rejected',row.get('adjudication_error')=='ADDITIVE_AUTHORITY_VIOLATION'))
    with tempfile.TemporaryDirectory() as td:
        cov,rows=build_store(td,'bullish')
        bp=bundle(td,[{'fact_id':'FOMC_POLICY_STANCE','observation_id':'CUR_FOMC_POLICY_STANCE','effect_on_gold':'BULLISH_GOLD','effect_kind':'STOCK','strength':'HIGH','is_additive':True,'causal_owner_id':'US_POLICY_EXPECTATIONS','rationale_summary':'certified semantic stance'}]); r=execute(P,td,adjudication_path=bp)
        root=next(x for x in r['pressure_planes']['causal_fundamental']['root_states'] if x['root_id']=='US_POLICY_EXPECTATIONS'); checks.append(check('certified semantic root adjudication accepted',root['direction']=='BULLISH_GOLD'))
    with tempfile.TemporaryDirectory() as td:
        build_store(td,'bullish'); bp=bundle(td,[{'fact_id':'FOMC_POLICY_STANCE','observation_id':'WRONG_OBS','effect_on_gold':'BULLISH_GOLD','effect_kind':'STOCK','strength':'HIGH','is_additive':True,'causal_owner_id':'US_POLICY_EXPECTATIONS','rationale_summary':'attack'}]); r=execute(P,td,adjudication_path=bp)
        row=next(x for x in r['reasoning_ledger']['rows'] if x['fact_id']=='FOMC_POLICY_STANCE'); checks.append(check('semantic observation mismatch rejected',row.get('adjudication_error')=='OBSERVATION_REFERENCE_MISMATCH'))
    with tempfile.TemporaryDirectory() as td:
        build_store(td,'bullish'); bp=bundle(td,[{'fact_id':'FOMC_POLICY_STANCE','observation_id':'CUR_FOMC_POLICY_STANCE','effect_on_gold':'BULLISH_GOLD','effect_kind':'STOCK','strength':'HIGH','is_additive':True,'causal_owner_id':'REAL_RATE_OPPORTUNITY_COST','rationale_summary':'attack'}]); r=execute(P,td,adjudication_path=bp)
        row=next(x for x in r['reasoning_ledger']['rows'] if x['fact_id']=='FOMC_POLICY_STANCE'); checks.append(check('wrong causal owner rejected',row.get('adjudication_error')=='CAUSAL_OWNER_MISMATCH'))
    with tempfile.TemporaryDirectory() as td:
        build_store(td,'bullish'); bp=bundle(td,[{'fact_id':'FOMC_POLICY_STANCE','observation_id':'CUR_FOMC_POLICY_STANCE','effect_on_gold':'BEARISH_GOLD','effect_kind':'STOCK','strength':'HIGH','is_additive':True,'causal_owner_id':'US_POLICY_EXPECTATIONS','rationale_summary':'opposing root'}]); r=execute(P,td,adjudication_path=bp)
        checks.append(check('conflicting independent roots produce mixed causal plane',r['pressure_planes']['causal_fundamental']['direction']=='MIXED'))
    with tempfile.TemporaryDirectory() as td:
        build_store(td,'neutral'); bp=bundle(td,[{'fact_id':'CENTRAL_BANK_NET_GOLD_PURCHASES','observation_id':'CUR_CENTRAL_BANK_NET_GOLD_PURCHASES','effect_on_gold':'BULLISH_GOLD','effect_kind':'STOCK','strength':'HIGH','is_additive':False,'causal_owner_id':None,'rationale_summary':'structural demand'}]); r=execute(P,td,adjudication_path=bp)
        checks.append(check('structural bullish state cannot create session direction',r['pressure_planes']['structural_carry']['direction']=='BULLISH_GOLD' and r['pressure_planes']['causal_fundamental']['direction']=='UNKNOWN'))
    with tempfile.TemporaryDirectory() as td:
        cov,rows=build_store(td,'neutral')
        # ETF holdings levels must use change, while an explicit global net-flow
        # object may carry signed transaction semantics.
        p=pathlib.Path(td)/'observations'/'gold_fact_observations.jsonl'; data=[json.loads(x) for x in p.read_text().splitlines() if x.strip()]
        for o in data:
            if o['fact_id']=='GLOBAL_GOLD_ETF_HOLDINGS_FLOW':
                o['value']={'net_flow':5.0} if o['observation_id'].startswith('CUR_') else {'net_flow':1.0}; o['value_type']='OBJECT'
            if o['fact_id'] in ('GLD_HOLDINGS_SHARES','IAU_HOLDINGS_SHARES'):
                o['value']=110.0 if o['observation_id'].startswith('CUR_') else 100.0; o['value_type']='NUMBER'
        p.write_text('\n'.join(json.dumps(x) for x in data)+'\n')
        r=execute(P,td)
        etf=[x for x in r['pressure_planes']['realized_transaction']['clusters'] if x['cluster_id']=='ETF_GLOBAL']
        checks.append(check('related ETF facts deduplicated to one transaction cluster',len(etf)==1 and len(etf[0]['facts'])==3,etf))
        checks.append(check('transaction flow alone cannot create causal direction',r['pressure_planes']['realized_transaction']['direction']=='BULLISH_GOLD' and r['pressure_planes']['causal_fundamental']['direction']=='UNKNOWN'))
        gld=next(x for x in r['reasoning_ledger']['rows'] if x['fact_id']=='GLD_HOLDINGS_SHARES')
        checks.append(check('holdings level uses delta not positive absolute level',gld['effect_on_gold']=='BULLISH_GOLD' and gld.get('details',{}).get('flow_semantics')=='LEVEL_DELTA' and gld.get('details',{}).get('flow_value')==10.0,gld))
    with tempfile.TemporaryDirectory() as td:
        build_store(td,'neutral')
        p=pathlib.Path(td)/'observations'/'gold_fact_observations.jsonl'; data=[json.loads(x) for x in p.read_text().splitlines() if x.strip()]
        for o in data:
            if o['fact_id']=='SGE_WITHDRAWALS':
                o['value']=80.0; o['value_type']='NUMBER'; o['epistemic_state']='PUBLIC_PROXY'; o['directness']='PROXY'
        p.write_text('\n'.join(json.dumps(x) for x in data)+'\n')
        r=execute(P,td,horizon='SESSION_1_6H')
        sge=next(x for x in r['reasoning_ledger']['rows'] if x['fact_id']=='SGE_WITHDRAWALS')
        checks.append(check('slow SGE withdrawals cannot leak into session transaction pressure',sge['resolution']=='ACCOUNTED_HORIZON_INACTIVE' and sge.get('horizon_active') is False and r['pressure_planes']['realized_transaction']['direction']=='UNKNOWN',{'row':sge,'plane':r['pressure_planes']['realized_transaction']}))
    with tempfile.TemporaryDirectory() as td:
        build_store(td,'neutral')
        p=pathlib.Path(td)/'observations'/'gold_fact_observations.jsonl'; data=[json.loads(x) for x in p.read_text().splitlines() if x.strip()]
        for o in data:
            if o['fact_id']=='SGE_WITHDRAWALS':
                o['value']=80.0 if o['observation_id'].startswith('CUR_') else 80.0; o['value_type']='NUMBER'; o['epistemic_state']='PUBLIC_PROXY'; o['directness']='PROXY'
        p.write_text('\n'.join(json.dumps(x) for x in data)+'\n')
        r=execute(P,td,horizon='MULTI_DAY_2_10D')
        sge=next(x for x in r['reasoning_ledger']['rows'] if x['fact_id']=='SGE_WITHDRAWALS')
        checks.append(check('positive gross SGE level does not refire bullish multi-day flow',sge['effect_on_gold']=='NEUTRAL' and sge.get('details',{}).get('flow_value')==0.0 and r['pressure_planes']['realized_transaction']['direction']=='UNKNOWN',{'row':sge,'plane':r['pressure_planes']['realized_transaction']}))
    with tempfile.TemporaryDirectory() as td:
        build_store(td,'neutral')
        p=pathlib.Path(td)/'observations'/'gold_fact_observations.jsonl'; data=[json.loads(x) for x in p.read_text().splitlines() if x.strip()]
        for o in data:
            if o['fact_id']=='SGE_WITHDRAWALS':
                o['value']=80.0 if o['observation_id'].startswith('CUR_') else 70.0; o['value_type']='NUMBER'; o['epistemic_state']='PUBLIC_PROXY'; o['directness']='PROXY'
        p.write_text('\n'.join(json.dumps(x) for x in data)+'\n')
        r=execute(P,td,horizon='MULTI_DAY_2_10D')
        sge=next(x for x in r['reasoning_ledger']['rows'] if x['fact_id']=='SGE_WITHDRAWALS')
        checks.append(check('SGE direction comes from period change not absolute positivity',sge['effect_on_gold']=='BULLISH_GOLD' and sge.get('details',{}).get('flow_value')==10.0 and sge.get('strength')=='LOW',sge))
    with tempfile.TemporaryDirectory() as td:
        build_store(td,'neutral')
        p=pathlib.Path(td)/'observations'/'gold_fact_observations.jsonl'; data=[json.loads(x) for x in p.read_text().splitlines() if x.strip()]
        for o in data:
            if o['fact_id']=='COMEX_DELIVERY_NOTICES':
                o['value']=500.0; o['value_type']='NUMBER'
        p.write_text('\n'.join(json.dumps(x) for x in data)+'\n')
        r=execute(P,td,horizon='SESSION_1_6H')
        comex=next(x for x in r['reasoning_ledger']['rows'] if x['fact_id']=='COMEX_DELIVERY_NOTICES')
        checks.append(check('positive gross delivery activity is not directional flow',comex['resolution']=='ACCOUNTED_NON_DIRECTIONAL' and comex['effect_on_gold']=='NO_DIRECTION' and r['pressure_planes']['realized_transaction']['direction']=='UNKNOWN',comex))
    with tempfile.TemporaryDirectory() as td:
        build_store(td,'bullish'); bp=bundle(td,[{'fact_id':'FORCED_CASH_LIQUIDATION','observation_id':'CUR_FORCED_CASH_LIQUIDATION','effect_on_gold':'BEARISH_GOLD','effect_kind':'IMPULSE','strength':'HIGH','is_additive':False,'causal_owner_id':None,'rationale_summary':'forced selling'}]); r=execute(P,td,adjudication_path=bp)
        checks.append(check('mechanical pressure cannot rewrite causal direction',r['pressure_planes']['mechanical_forced']['direction']=='BEARISH_GOLD' and r['pressure_planes']['causal_fundamental']['direction']=='BULLISH_GOLD'))
        checks.append(check('opposing strong mechanical pressure constrains action',r['shadow_decision']['action_candidate']=='WAIT'))
    with tempfile.TemporaryDirectory() as td:
        build_store(td,'bullish')
        # Make FOMC observation proxy then request HIGH semantic strength: must cap LOW.
        p=pathlib.Path(td)/'observations'/'gold_fact_observations.jsonl'; data=[json.loads(x) for x in p.read_text().splitlines() if x.strip()]
        for o in data:
            if o['observation_id']=='CUR_FOMC_POLICY_STANCE': o['epistemic_state']='PUBLIC_PROXY'; o['directness']='PROXY'
        p.write_text('\n'.join(json.dumps(x) for x in data)+'\n')
        bp=bundle(td,[{'fact_id':'FOMC_POLICY_STANCE','observation_id':'CUR_FOMC_POLICY_STANCE','effect_on_gold':'BULLISH_GOLD','effect_kind':'STOCK','strength':'HIGH','is_additive':True,'causal_owner_id':'US_POLICY_EXPECTATIONS','rationale_summary':'proxy semantic'}]); r=execute(P,td,adjudication_path=bp)
        row=next(x for x in r['reasoning_ledger']['rows'] if x['fact_id']=='FOMC_POLICY_STANCE'); checks.append(check('proxy semantic strength capped by evidence',row['strength']=='LOW' and row.get('strength_capped_by_evidence')=='LOW'))
    with tempfile.TemporaryDirectory() as td:
        build_store(td,'bullish'); r=execute(P,td)
        rr=next(x for x in r['pressure_planes']['causal_fundamental']['root_states'] if x['root_id']=='REAL_RATE_OPPORTUNITY_COST')
        checks.append(check('three real-yield facts remain one additive root unit',rr['direction']=='BULLISH_GOLD' and r['pressure_planes']['causal_fundamental']['strength']=='LOW'))

    with tempfile.TemporaryDirectory() as td:
        cov,rows=build_store(td,'bullish')
        # Simulate the original live bug: receipt generated-at is earlier than all
        # current observations. Exact run-id binding must still load all 192.
        cov['generated_at_utc']='2026-08-16T20:00:00Z'; cov['acquisition_completed_at_utc']='2026-08-16T21:01:00Z'; cov['observation_cutoff_utc']='2026-08-16T21:00:00Z'
        cp=pathlib.Path(td)/'early_receipt.json'; write(cp,cov); r=execute(P,td,str(cp))
        checks.append(check('early receipt timestamp cannot drop current-run observations',r.get('analysis_admission')!='BLOCKED' and r.get('handoff_integrity',{}).get('current_observations_loaded')==192,r.get('handoff_integrity')))
    with tempfile.TemporaryDirectory() as td:
        cov,rows=build_store(td,'bullish')
        cov['acquisition_run_id']='P02RUN_TAMPERED'; cp=pathlib.Path(td)/'tampered_run.json'; write(cp,cov); r=execute(P,td,str(cp))
        checks.append(check('tampered acquisition run id fails closed',r.get('analysis_admission')=='BLOCKED' and r.get('reason')=='P02_P03_OBSERVATION_HANDOFF_INCOMPLETE',r.get('handoff_integrity')))

    with tempfile.TemporaryDirectory() as td:
        cov,rows=build_store(td,'neutral')
        # Give one derived semantic fact an explicit dependency declaration so
        # the evidence-packet closure can be tested against exact observations.
        op=pathlib.Path(td)/'observations'/'gold_fact_observations.jsonl'; data=[json.loads(x) for x in op.read_text().splitlines() if x.strip()]
        usd_deps=['FED_BROAD_DOLLAR','FED_AFE_DOLLAR','FED_EME_DOLLAR','FOMC_POLICY_STANCE','UST_2Y_NOMINAL_YIELD']
        for o in data:
            if o['fact_id']=='USD_AUTONOMOUS_SHOCK':
                o['value']={'dependencies':usd_deps,'available_dependencies':usd_deps,'missing_dependencies':[],'semantic_derivation_deferred_to_p03':True}; o['value_type']='OBJECT'; o['epistemic_state']='MODEL_DERIVED'; o['directness']='DERIVED'
            if o['fact_id']=='FED_BROAD_DOLLAR':
                o['value']=119.0; o['value_type']='NUMBER'; o['reference_period']='2026-08-07'
            if o['fact_id']=='UST_2Y_NOMINAL_YIELD':
                o['value']=4.17; o['value_type']='NUMBER'; o['reference_period']='2026-08-14'
        # Older distinct economic state for Broad Dollar. It is intentionally
        # older than the previous fetch and carries a different reference period.
        data.append({'record_type':'AD_V3_P02_FACT_OBSERVATION','observation_id':'ECON_FED_BROAD_DOLLAR','phase':'AD-V3-P02','subject':'XAUUSD','fact_id':'FED_BROAD_DOLLAR','source_id':'FIX','epistemic_state':'LATEST_VALID','value_type':'NUMBER','value':118.5,'unit':'index','reference_period':'2026-08-06','event_time':None,'published_at':None,'first_seen_at':'2026-08-16T19:00:00Z','retrieved_at':'2026-08-16T19:00:00Z','revision_number':0,'supersedes_observation_id':None,'directness':'DIRECT','provenance_ref':'fixture','raw_sha256':'econ-broad','metadata':{},'warnings':[],'acquisition_run_id':'P02RUN_ECON_neutral'})
        op.write_text('\n'.join(json.dumps(x) for x in data)+'\n')
        r=execute(P,td,horizon='SESSION_1_6H')
        from AD_V3_PHASE_03_CAUSAL_GOLD_BRAIN_DECISION_ENGINE.runtime.loader import observation_history, current_previous_for_receipt
        from AD_V3_PHASE_03_CAUSAL_GOLD_BRAIN_DECISION_ENGINE.runtime.semantic_packet import build_semantic_evidence_packet
        hist=observation_history(td,None); pairs,_=current_previous_for_receipt(hist,cov)
        cmap={x['fact_id']:x for x in load(P/'config/fact_reasoning_registry.json')['contracts']}
        pkt=build_semantic_evidence_packet(r,pairs,cmap,cov)
        checks.append(check('semantic evidence packet count matches adjudication requests',pkt['item_count']==len(r['semantic_adjudication_request']) and pkt['item_count']>0,{'packet':pkt['item_count'],'requests':len(r['semantic_adjudication_request'])}))
        checks.append(check('semantic packet binds exact acquisition run',pkt['acquisition_run_id']==r['handoff_integrity']['acquisition_run_id']==cov['acquisition_run_id'],pkt['acquisition_run_id']))
        checks.append(check('semantic packet carries exact current and previous observations',all(x.get('current_observation',{}).get('observation_id')==x.get('requested_observation_id') and x.get('previous_observation') is not None for x in pkt['items'])))
        checks.append(check('semantic packet exposes epistemic provenance and authority scope',all(x.get('current_observation',{}).get('epistemic_state') and 'provenance_ref' in x.get('current_observation',{}) and x.get('authority_scope') for x in pkt['items'])))
        sf=next((x for x in pkt['items'] if x['fact_id']=='US_FISCAL_DEFICIT_DEBT'),None)
        checks.append(check('structural semantic evidence explicitly has no session direction authority',sf is not None and sf['authority_scope']=='STRUCTURAL_BACKGROUND_ONLY' and sf['may_add_to_current_causal_direction'] is False,sf))
        fomc=next((x for x in pkt['items'] if x['fact_id']=='FOMC_POLICY_STANCE'),None)
        checks.append(check('current-horizon causal semantic evidence labels additive authority explicitly',fomc is not None and fomc['authority_scope']=='CAUSAL_CURRENT_HORIZON' and fomc['may_add_to_current_causal_direction'] is True,fomc))
        usd=next((x for x in pkt['items'] if x['fact_id']=='USD_AUTONOMOUS_SHOCK'),None)
        deps=(usd or {}).get('dependency_evidence',[])
        checks.append(check('derived semantic packet attaches declared dependency evidence',usd is not None and len(deps)==5 and {x['fact_id'] for x in deps}=={'FED_BROAD_DOLLAR','FED_AFE_DOLLAR','FED_EME_DOLLAR','FOMC_POLICY_STANCE','UST_2Y_NOMINAL_YIELD'},deps))
        checks.append(check('derived dependency evidence binds exact acquisition run',usd is not None and all(x.get('current_observation',{}).get('acquisition_run_id')==cov['acquisition_run_id'] for x in deps),deps))
        checks.append(check('derived dependency evidence carries previous observations',usd is not None and all(x.get('previous_observation') is not None for x in deps),deps))
        checks.append(check('semantic packet exposes evidence diagnostics',all(isinstance(x.get('evidence_diagnostics'),dict) and 'current_previous_value_equal' in x['evidence_diagnostics'] and 'declared_dependency_count' in x['evidence_diagnostics'] for x in pkt['items'])))
        checks.append(check('direct semantic item has no fabricated dependency closure',fomc is not None and fomc.get('dependency_evidence')==[] and fomc.get('evidence_diagnostics',{}).get('declared_dependency_count')==0,fomc))
        broad=next((x for x in deps if x['fact_id']=='FED_BROAD_DOLLAR'),None)
        y2=next((x for x in deps if x['fact_id']=='UST_2Y_NOMINAL_YIELD'),None)
        checks.append(check('previous fetch is explicitly separated from previous economic observation',broad is not None and broad.get('previous_fetch_observation',{}).get('observation_id')=='PREV_FED_BROAD_DOLLAR' and broad.get('previous_economic_observation',{}).get('observation_id')=='ECON_FED_BROAD_DOLLAR',broad))
        checks.append(check('repeated fetch equality is not economic delta',broad is not None and broad.get('comparison_diagnostics',{}).get('previous_fetch_value_equal') is True and broad.get('comparison_diagnostics',{}).get('fetch_equality_is_not_economic_delta') is True,broad.get('comparison_diagnostics') if broad else None))
        checks.append(check('distinct economic reference-period anchor is discovered',broad is not None and broad.get('comparison_diagnostics',{}).get('economic_anchor_status')=='DISTINCT_ECONOMIC_ANCHOR_AVAILABLE' and broad.get('comparison_diagnostics',{}).get('current_economic_marker',{}).get('value')=='2026-08-07' and broad.get('comparison_diagnostics',{}).get('previous_economic_marker',{}).get('value')=='2026-08-06',broad.get('comparison_diagnostics') if broad else None))
        checks.append(check('same-reference repeated fetch without older period reports no economic anchor',y2 is not None and y2.get('comparison_diagnostics',{}).get('economic_anchor_status')=='NO_DISTINCT_ECONOMIC_ANCHOR' and y2.get('previous_economic_observation') is None,y2))
        checks.append(check('text evidence without economic clock cannot fabricate economic delta',fomc is not None and fomc.get('evidence_diagnostics',{}).get('economic_anchor_status')=='NO_CURRENT_ECONOMIC_MARKER' and fomc.get('previous_economic_observation') is None,fomc.get('evidence_diagnostics') if fomc else None))

    with tempfile.TemporaryDirectory() as td:
        cov,rows=build_store(td,'neutral')
        # An inactive CAUSAL_FUNDAMENTAL fact must not be reintroduced through a manual semantic bundle.
        bp=bundle(td,[{'fact_id':'MONETARY_FISCAL_CREDIBILITY','observation_id':'CUR_MONETARY_FISCAL_CREDIBILITY','effect_on_gold':'BULLISH_GOLD','effect_kind':'STOCK','strength':'HIGH','is_additive':False,'causal_owner_id':None,'rationale_summary':'attempted horizon bypass'}])
        r=execute(P,td,adjudication_path=bp,horizon='SESSION_1_6H')
        row=next(x for x in r['reasoning_ledger']['rows'] if x['fact_id']=='MONETARY_FISCAL_CREDIBILITY')
        checks.append(check('semantic bundle cannot bypass inactive current-horizon authority',row.get('adjudication_error')=='HORIZON_AUTHORITY_VIOLATION',row))

    checks += [
      check('event shocks never direct additive',all(not c['can_add_to_session_causal_direction'] for c in load(P/'config/fact_reasoning_registry.json')['contracts'] if c['role']=='EVENT_SHOCK')),
      check('positioning never direct additive',all(not c['can_add_to_session_causal_direction'] for c in load(P/'config/fact_reasoning_registry.json')['contracts'] if c['role']=='POSITIONING_STATE')),
      check('structural carry no session authority',all(not c['can_add_to_session_causal_direction'] for c in load(P/'config/fact_reasoning_registry.json')['contracts'] if c['pressure_plane']=='STRUCTURAL_CARRY')),
      check('consumption vector has eight components', len(load(P/'config/consumption_persistence_policy.json')['consumption_components'])==8),
      check('unknown no renormalization rule present', any('renormal' in x.lower() for x in load(P/'config/causal_brain_policy.json')['hard_rules'])),
      check('all realized-flow contracts declare flow semantics', all(c.get('flow_semantics') for c in load(P/'config/fact_reasoning_registry.json')['contracts'] if c['role']=='REALIZED_FLOW')),
      check('slow realized-flow facts cannot contribute outside active horizons', all(c.get('active_horizons') for c in load(P/'config/fact_reasoning_registry.json')['contracts'] if c['role']=='REALIZED_FLOW')),
    ]
    status='PASS' if all(x['status']=='PASS' for x in checks) else 'FAIL'; out={'phase':'AD-V3-P03','acceptance_status':status,'check_count':len(checks),'checks':checks,'p04_handoff':{'ready':status=='PASS','next_phase':'AD-V3-P04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING','production_authority_still_false':True}}
    print(json.dumps(out,indent=2)); return 0 if status=='PASS' else 2
if __name__=='__main__': raise SystemExit(main())
