#!/usr/bin/env python3
from pathlib import Path
import tempfile,json,subprocess,sys,datetime,shutil
HERE=Path(__file__).resolve().parent; V=HERE.parents[1]; R=V/'94 Institutional Evidence Calibration Portfolio and Model Risk Production Engine'; C=R/'config'
def run(args):
    r=subprocess.run([sys.executable,*map(str,args)],capture_output=True,text=True); return r.returncode,r.stdout+r.stderr
checks=[]
def chk(name,ok,out=''): checks.append((name,bool(ok),out))
rc,o=run([HERE/'alphalab_preflight.py','--vault-root',V,'--mode','deployment']); chk('deployment_preflight',rc==0,o)
rc,o=run([HERE/'alphalab_preflight.py','--vault-root',V,'--mode','runtime']); chk('runtime_preflight',rc==0,o)
with tempfile.TemporaryDirectory() as td0:
    td=Path(td0)
    # decision states
    ip=td/'d.json'; op=td/'do.json'
    base={'fundamental_direction':'BULLISH','fundamental_force_state':'ACTIVE','narrative_clearance':'ALIGNED_EMERGING','evidence_clearance':'CLEAR','timing_clearance':'CLEAR'}
    ip.write_text(json.dumps(base)); rc,o=run([HERE/'alphalab_decision_gate.py','--input',ip,'--output',op]); z=json.loads(op.read_text()); chk('emerging_narrative_allows_early_active_with_cap',rc==0 and z['research_edge']=='EDGE_ACTIVE' and z['permission_before_operational_and_portfolio']=='BUY' and 'NARRATIVE_EMERGING' in z['confidence_caps'],o)
    x=dict(base,fundamental_force_state='WEAK'); ip.write_text(json.dumps(x)); run([HERE/'alphalab_decision_gate.py','--input',ip,'--output',op]); z=json.loads(op.read_text()); chk('narrative_cannot_upgrade_weak_fundamental',z['research_edge']!='EDGE_ACTIVE' and z['permission_before_operational_and_portfolio']=='NO_TRADE',str(z))
    x=dict(base,narrative_clearance='OPPOSING'); ip.write_text(json.dumps(x)); run([HERE/'alphalab_decision_gate.py','--input',ip,'--output',op]); z=json.loads(op.read_text()); chk('opposing_narrative_does_not_flip_direction',z['research_edge']!='EDGE_ACTIVE' and z['fundamental_direction']=='BULLISH',str(z))
    x=dict(base,narrative_clearance='NEUTRAL'); ip.write_text(json.dumps(x)); run([HERE/'alphalab_decision_gate.py','--input',ip,'--output',op]); z=json.loads(op.read_text()); chk('neutral_narrative_is_conditional_not_hard_failure',z['research_edge']=='EDGE_CONDITIONAL',str(z))
    # evidence materiality
    gp=td/'g.json'; go=td/'go.json'
    g={'analysis_id':'T','nodes':[{'evidence_id':'A','root_cause_id':'R1','decision_materiality':'DECISION_CRITICAL'},{'evidence_id':'B','root_cause_id':'R2','decision_materiality':'DECISION_CRITICAL'}],'edges':[{'from':'A','to':'B','relation':'UNKNOWN_DEPENDENCY'}]}; gp.write_text(json.dumps(g)); rc,o=run([HERE/'alphalab_validate_evidence_graph.py',gp,'--output',go]); z=json.loads(go.read_text()); chk('critical_unknown_holds',rc==0 and z['decision_clearance']=='HOLD',o)
    g['nodes'][0]['decision_materiality']=g['nodes'][1]['decision_materiality']='MATERIAL_SECONDARY'; gp.write_text(json.dumps(g)); run([HERE/'alphalab_validate_evidence_graph.py',gp,'--output',go]); z=json.loads(go.read_text()); chk('secondary_unknown_caps_not_blocks',z['decision_clearance']=='CLEAR_WITH_CONFIDENCE_CAP',str(z))
    g['nodes'][0]['decision_materiality']=g['nodes'][1]['decision_materiality']='CONTEXTUAL'; gp.write_text(json.dumps(g)); run([HERE/'alphalab_validate_evidence_graph.py',gp,'--output',go]); z=json.loads(go.read_text()); chk('contextual_unknown_does_not_block',z['decision_clearance']=='CLEAR',str(z))
    # operational
    fut=(datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(minutes=20)).isoformat(); sp=td/'s.json'; sop=td/'sop.json'
    st={'stage':'PERMISSION_INGEST','symbol_mapping_valid':True,'market_state_known':True,'market_open':True,'permission':'BUY','permission_valid_until_utc':fut,'state_checksum_valid':True}; sp.write_text(json.dumps(st)); run([HERE/'alphalab_operational_gate.py','--state',sp,'--policy',C/'operational_gate_policy.json','--output',sop]); z=json.loads(sop.read_text()); chk('missing_clock_drift_blocks_buy',z['hard_block'] and 'MISSING_CLOCK_DRIFT_SECONDS' in z['reasons'],str(z))
    sp.write_text(json.dumps({'stage':'PERMISSION_INGEST','permission':'NO_TRADE'})); run([HERE/'alphalab_operational_gate.py','--state',sp,'--policy',C/'operational_gate_policy.json','--output',sop]); z=json.loads(sop.read_text()); chk('no_trade_does_not_create_useless_operational_alarm',not z['hard_block'] and z['entry_requested'] is False,str(z))
    st.update({'clock_drift_seconds':0,'permission':'BUY','stage':'ENTRY_TRIGGER','feed_connected':True,'quote_timestamp_utc':(datetime.datetime.now(datetime.timezone.utc)-datetime.timedelta(seconds=30)).isoformat(),'price':100,'atr':1,'spread_hard_limit_breached':False,'duplicate_order_detected':False,'position_sync_valid':True}); sp.write_text(json.dumps(st)); run([HERE/'alphalab_operational_gate.py','--state',sp,'--policy',C/'operational_gate_policy.json','--output',sop]); z=json.loads(sop.read_text()); chk('stale_quote_blocks_entry_trigger',z['hard_block'] and 'QUOTE_STALE' in z['reasons'],str(z))
    st['quote_timestamp_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat(); st['atr']=0; sp.write_text(json.dumps(st)); run([HERE/'alphalab_operational_gate.py','--state',sp,'--policy',C/'operational_gate_policy.json','--output',sop]); z=json.loads(sop.read_text()); chk('bad_atr_blocks_entry_trigger',z['hard_block'] and 'ATR_INVALID' in z['reasons'],str(z))
    # direction-aware portfolio
    cand={'candidates':[{'symbol':'EURUSD','side':'BUY','risk_units':1,'factor_loadings':{'USD':'NEGATIVE'},'root_factor_loadings':{'USD_ROOT':'NEGATIVE'}},{'symbol':'USDJPY','side':'BUY','risk_units':1,'factor_loadings':{'USD':'POSITIVE'},'root_factor_loadings':{'USD_ROOT':'POSITIVE'}}]}; cp=td/'c.json'; po=td/'p.json'; cp.write_text(json.dumps(cand)); run([HERE/'alphalab_portfolio_gate.py','--candidates',cp,'--policy',C/'portfolio_gate_policy.json','--output',po]); z=json.loads(po.read_text()); chk('direction_aware_portfolio_netting',abs(z['aggregate_signed_factor_risk_units'].get('USD',999))<1e-9 and not z['violations'],str(z))
    # retrieval firewall
    rp=td/'rp.json'; rc,o=run([HERE/'alphalab_retrieval_plan.py','--vault-root',V,'--symbol','USDJPY','--extra-path','59 Asset-Specific Institutional Driver Books/10 USDJPY Institutional Driver Book.md','--output',rp]); chk('legacy_retrieval_denied',rc!=0,o)
    rc,o=run([HERE/'alphalab_retrieval_plan.py','--vault-root',V,'--symbol','USDJPY','--output',rp]); chk('canonical_smallest_sufficient_plan_passes',rc==0,o)
    # event pack frozen + release envelope
    now=datetime.datetime.now(datetime.timezone.utc); ev={'event_id':'E','event_time_utc':(now+datetime.timedelta(hours=1)).isoformat(),'prepared_at_utc':now.isoformat(),'consensus_vintage_utc':(now-datetime.timedelta(minutes=1)).isoformat(),'scenario_tree':[{'x':1}],'surprise_dimensions':['headline'],'causal_leaders':['rates'],'required_cross_assets':['US2Y'],'invalidations':['bad data'],'source_ids':['OFFICIAL'],'max_pack_age_seconds':7200}; ei=td/'ei.json'; ep=td/'ep.json'; ei.write_text(json.dumps(ev)); rc,o=run([HERE/'alphalab_event_fastpath.py','prepare','--input',ei,'--output',ep]); original=ep.read_bytes(); rc2,o2=run([HERE/'alphalab_event_fastpath.py','validate','--pack',ep]); u={'revision_state':'FIRST_RELEASE','released_at_utc':(now+datetime.timedelta(hours=1)).isoformat(),'surprise':{'headline':1},'immediate_transmission':{'US2Y':'DOWN'}}; ui=td/'u.json'; eo=td/'eo.json'; ui.write_text(json.dumps(u)); rc3,o3=run([HERE/'alphalab_event_fastpath.py','release','--pack',ep,'--release-input',ui,'--output',eo]); env=json.loads(eo.read_text()); chk('event_fastpath_frozen_pack_and_release_envelope',rc==0 and rc2==0 and rc3==0 and ep.read_bytes()==original and env['pre_event_pack_sha256']==json.loads(ep.read_text())['pack_sha256'],o+o2+o3)
    # calibration hierarchy and edge separation
    out=td/'outcomes.jsonl'; rows=[]
    common={'symbol':'NASDAQ100','asset_family':'US_EQUITY_INDEX','horizon':'SHORT_15_60M','matured':True,'recorded_at_utc':now.isoformat(),'root_event_id':'E1','regime_label':'R1','is_holdout':False,'core_direction':'BULLISH','timing_gate':'CLEAR','narrative_clearance':'ALIGNED_EMERGING','driver_family':'RATES','narrative_family':'RATE_RELIEF','evidence_quality_band':'HIGH','execution_profile_version':'DONCHIAN20_M1_4ATR','realized_r':1.0}
    rows.append(dict(common,run_id='R1',edge_class='EDGE_ACTIVE')); rows.append(dict(common,run_id='R2',root_event_id='E2',edge_class='EDGE_CONDITIONAL',realized_r=-1.0))
    out.write_text('\n'.join(json.dumps(x) for x in rows)+'\n'); cal=td/'cal.json'; rc,o=run([HERE/'alphalab_calibrate.py','--outcomes',out,'--policy',C/'calibration_policy.json','--output',cal]); z=json.loads(cal.read_text()); exact=[x for x in z['cohorts'] if x['cohort_level']=='L1_EXACT']; chk('calibration_exact_cohort_separates_edge_class',rc==0 and len(exact)==2,str(exact))
    # state validator
    mk={};
    for sym in ['XAUUSD','NASDAQ100','SP500','DJIA','EURUSD','USDJPY']:
        mk[sym]={'fundamental_direction':'BULLISH','fundamental_force_state':'ACTIVE','narrative_clearance':'ALIGNED_DOMINANT','evidence_clearance':'CLEAR','core_edge_candidate':'ACTIVE_CANDIDATE_BULL','timing_clearance':'CLEAR','research_edge':'EDGE_ACTIVE','calibration_status':'COLD_START','portfolio_gate':'ALLOW','operational_gate':'CLEAR','permission':'BUY','valid_until_utc':fut,'next_review_utc':fut}
    state={'generated_at_utc':now.isoformat(),'run_id':'TEST','markets':mk}; stp=td/'state.json'; stp.write_text(json.dumps(state)); rc,o=run([HERE/'alphalab_validate_state.py','--state',stp]); chk('strict_state_semantics_pass',rc==0,o)
    state['markets']['XAUUSD']['narrative_clearance']='OPPOSING'; stp.write_text(json.dumps(state)); rc,o=run([HERE/'alphalab_validate_state.py','--state',stp]); chk('state_validator_rejects_active_without_narrative_clearance',rc!=0,o)
    # manifest drift detector
    mv=td/'mv'; mv.mkdir();
    for f in ['CURRENT_PRODUCTION_MANIFEST.json','CURRENT_PRODUCTION_MANIFEST.yaml','MANIFEST_MIRROR_HASHES.json']: shutil.copy2(V/f,mv/f)
    (mv/'CURRENT_PRODUCTION_MANIFEST.yaml').write_text((mv/'CURRENT_PRODUCTION_MANIFEST.yaml').read_text()+'# drift\n'); rc,o=run([HERE/'alphalab_manifest_sync.py','--vault-root',mv,'--check']); chk('manifest_drift_detected',rc!=0,o)
print(json.dumps({'status':'PASS' if all(x[1] for x in checks) else 'FAIL','count':len(checks),'checks':[{'name':n,'pass':ok,'output':o[:450]} for n,ok,o in checks]},indent=2)); sys.exit(0 if all(x[1] for x in checks) else 2)
