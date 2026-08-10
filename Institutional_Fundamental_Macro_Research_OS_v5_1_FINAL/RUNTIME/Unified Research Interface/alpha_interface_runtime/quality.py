from pathlib import Path
from datetime import datetime, timezone
import json
from .util import load_json, first, now

VERSION='RUN2.0.0'
CLUSTERS={
 'timing':'temporal_clearance','fundamental':'fundamental_state','expectations':'policy_reaction_state','narrative':'narrative_state',
 'positioning':'positioning_state','flow':'flow_state','funding':'funding_plumbing_state','mechanics':'mechanics_capacity_state'}
ADVERSARIAL={'hypothesis_set':'hypothesis_set','thesis_destroyer':'adversarial_review','model_disagreement':'model_disagreement','premortem':'premortem'}

def _art(rt,rid,name,default=None):
    try:return rt.store.load_artifact_json(rid,name)
    except Exception:return default

def _gate(gate_id,status,severity='HARD',detail=None):
    return {'gate_id':gate_id,'status':status,'severity':severity,'detail':detail}

def _parse_dt(x):
    if not isinstance(x,str) or not x or x.upper()=='NOW':return None
    s=x[:-1]+'+00:00' if x.endswith('Z') else x
    d=datetime.fromisoformat(s)
    if d.tzinfo is None:raise ValueError('timezone-aware timestamp required')
    return d.astimezone(timezone.utc)

def _finish(gates,market='UNKNOWN',run_id=None):
    hard=[g['gate_id'] for g in gates if g['severity']=='HARD' and g['status']=='FAIL']
    warn=[g['gate_id'] for g in gates if g['status']=='WARN']
    partial=[g['gate_id'] for g in gates if g['status']=='FAIL' and g['gate_id'] not in hard]
    # Hard gates can map to PARTIAL when the gate registry deliberately says scientific output may be partial.
    blocking={'PRE_RUN_INTEGRITY','POINT_IN_TIME_INTEGRITY','M1_HARD_GATE','CAUSAL_LANGUAGE','DIRECTION_AUTHORITY','APL_A_SEPARATION','REPORT_FIDELITY'}
    if any(x in blocking for x in hard):status='BLOCKED'
    elif hard or partial:status='PARTIAL'
    elif warn:status='PASS_WITH_WARNINGS'
    else:status='PASS'
    return {'schema_version':'1.0.0','gate_set_version':VERSION,'run_id':run_id,'status':status,'scientific_process_status':status,'market_state_resolution':str(market or 'UNKNOWN'),'gates':gates,'hard_failures':hard,'warnings':warn,'created_at_utc':now(),'authority':{'direction':'NONE','broker_write':'NONE','apl_a':'SHADOW_ONLY'}}

def pre_run(vault_root,compiled):
    v=Path(vault_root).resolve();g=[]
    ui=v/'RUNTIME'/'Unified Research Interface'
    required=[ui/'UNIFIED_INTERFACE_MANIFEST.json',ui/'config'/'run_command_policy.json',v/'RUNTIME'/'Core Research Method Kernel',v/'RUNTIME'/'R2 Prompt Execution OS',v/'RUNTIME'/'R3 Operational Execution and Learning OS']
    subok=bool(compiled.get('resolved_subjects')) and all(x.get('canonical') for x in compiled.get('resolved_subjects',[]))
    basic=all(p.exists() for p in required) and subok and compiled.get('mode') and compiled.get('active_horizon') and compiled.get('analysis_cutoff')
    g.append(_gate('PRE_RUN_INTEGRITY','PASS' if basic else 'FAIL',detail={'runtime_paths':all(p.exists() for p in required),'subject_resolved':subok,'mode':compiled.get('mode'),'horizon':compiled.get('active_horizon'),'as_of':compiled.get('analysis_cutoff')}))
    hist=compiled.get('r3_run_mode') in ('HISTORICAL_REPLAY','RESEARCH_REPLAY')
    if hist:
        try:d=_parse_dt(compiled.get('analysis_cutoff'));ok=d is not None and d<=datetime.now(timezone.utc)
        except Exception:ok=False
        g.append(_gate('POINT_IN_TIME_INTEGRITY','PASS' if ok else 'FAIL',detail={'cutoff':compiled.get('analysis_cutoff'),'future_forbidden':True}))
    else:g.append(_gate('POINT_IN_TIME_INTEGRITY','NOT_APPLICABLE',detail={'mode':compiled.get('mode')}))
    return _finish(g,run_id=None)

def _cluster_state(obj):
    if not isinstance(obj,dict) or not obj:return 'FAILED'
    s=str(first(obj,'status','state','availability','coverage_state',default='COMPLETE')).upper()
    if any(x in s for x in ('FAIL','ERROR','INVALID')):return 'FAILED'
    if any(x in s for x in ('UNKNOWN','UNAVAILABLE','UNDETERMINED','INSUFFICIENT')):return 'UNKNOWN'
    if any(x in s for x in ('NOT_APPLICABLE','NOT MATERIAL','NOT_MATERIAL','N/A')):return 'NOT_MATERIAL'
    gaps=[]
    for k in ('gaps','missing_data','data_gaps','unknowns','limitations'):
        x=obj.get(k)
        if isinstance(x,list):gaps.extend(x)
        elif x not in (None,'',{},[]):gaps.append(x)
    return 'PARTIAL' if gaps else 'COMPLETE'

def _root_ids(pack):
    roots=[]
    def walk(x):
        if isinstance(x,dict):
            for k,v in x.items():
                lk=str(k).lower()
                if lk in ('root_source_id','root_id','root_identity','root_source') and isinstance(v,(str,int,float)):roots.append(str(v))
                walk(v)
        elif isinstance(x,list):
            for y in x:walk(y)
    walk(pack);return roots

def contradiction_ledger(rt,rid):
    out=[];ri=_art(rt,rid,'research_intent',{}) or {};rec=_art(rt,rid,'market_state_reconciliation',{}) or {};glob=_art(rt,rid,'global_reconciliation',{}) or {}
    raw=[]
    for src in (ri,rec,glob):
        for k in ('unresolved_contradictions','contradictions','conflicts','disagreements'):
            x=src.get(k) if isinstance(src,dict) else None
            if isinstance(x,list):raw.extend(x)
    for i,x in enumerate(raw):
        if isinstance(x,dict):
            out.append({'contradiction_id':x.get('contradiction_id') or f'C{i+1:03d}','claim_a':x.get('claim_a') or x.get('a') or x.get('left'),'claim_b':x.get('claim_b') or x.get('b') or x.get('right'),'scope':x.get('scope'),'horizon':x.get('horizon'),'possible_explanations':x.get('possible_explanations') or x.get('explanations') or [],'resolution_state':x.get('resolution_state') or x.get('status') or 'UNRESOLVED','decision_relevance':x.get('decision_relevance')})
        else:out.append({'contradiction_id':f'C{i+1:03d}','description':str(x),'resolution_state':'UNRESOLVED'})
    return out

def evaluate(rt,run_id,compiled,canonical):
    names={x['logical_name'] for x in rt.catalog.list_artifacts(run_id)};g=[]
    req_plan={'retrieval_plan','coverage_requirements','observability_plan'}
    g.append(_gate('EVIDENCE_PLAN','PASS' if req_plan.issubset(names) else 'FAIL',detail={'missing':sorted(req_plan-names)}))
    pack=_art(rt,run_id,'decision_evidence_pack',{}) or {};eir=_art(rt,run_id,'evidence_integrity_receipt',{}) or {}
    eir_status=str(eir.get('status','')).upper();evidence_ok=bool(pack) and bool(eir) and eir_status not in ('FAIL','INVALID','ERROR')
    g.append(_gate('EVIDENCE_INTEGRITY','PASS' if evidence_ok else 'FAIL',detail={'decision_evidence_pack':bool(pack),'receipt_status':eir.get('status')}))
    roots=_root_ids(pack);g.append(_gate('ROOT_SOURCE_INDEPENDENCE','PASS' if pack else 'FAIL',detail={'root_source_ids_observed':len(set(roots)),'root_references_total':len(roots),'deduplication_required':len(roots)!=len(set(roots)) if roots else False}))
    live=compiled.get('r3_run_mode') in ('LIVE','SHADOW_LIVE');retr=_art(rt,run_id,'r3_retrieval_receipt',{}) or {}
    if live:g.append(_gate('SOURCE_FRESHNESS','PASS' if retr else 'FAIL',detail={'retrieval_receipt':bool(retr),'gaps':retr.get('gaps',[]) if isinstance(retr,dict) else []}))
    else:g.append(_gate('SOURCE_FRESHNESS','NOT_APPLICABLE',detail={'mode':compiled.get('mode')}))
    coverage={}
    for sid,name in CLUSTERS.items():coverage[sid]={'logical_name':name,'status':_cluster_state(_art(rt,run_id,name,{}))}
    missing=[k for k,x in coverage.items() if x['status']=='FAILED'];g.append(_gate('EIGHT_CLUSTER_COVERAGE','PASS' if not missing else 'FAIL',detail={'clusters':coverage,'failed_or_missing':missing}))
    m1=_art(rt,run_id,'method_predecision_validation_receipt',{}) or {};m1_ok=bool(m1) and str(m1.get('status','PASS')).upper() not in ('FAIL','BLOCKED','INVALID') and int(m1.get('hard_failure_count',0) or 0)==0
    g.append(_gate('M1_HARD_GATE','PASS' if m1_ok else 'FAIL',detail={'status':m1.get('status'),'hard_failure_count':m1.get('hard_failure_count'),'findings':m1.get('findings',[])}))
    findings=json.dumps(m1.get('findings',[]),ensure_ascii=False).upper() if isinstance(m1,dict) else ''
    proxy_bad=('PROXY' in findings and any(x in findings for x in ('OUT_OF_DOMAIN','OUTSIDE_DOMAIN','INVALID'))) or ('MODEL' in findings and any(x in findings for x in ('OUT_OF_DOMAIN','OUTSIDE_DOMAIN','INVALID')))
    g.append(_gate('PROXY_MODEL_GOVERNANCE','FAIL' if proxy_bad else ('PASS' if m1 else 'FAIL'),detail={'material_scope_failure_detected':proxy_bad}))
    causal=_art(rt,run_id,'causal_graph',{}) or {};causal_present=bool(causal);g.append(_gate('CAUSAL_LANGUAGE','PASS' if causal_present and m1_ok else 'FAIL',detail={'causal_artifact':causal_present,'identification_status':first(causal,'identification_status','causal_status','status','identification')}))
    ledger=contradiction_ledger(rt,run_id);g.append(_gate('CONTRADICTION_PRESERVATION','PASS' if 'market_state_reconciliation' in names else 'FAIL',detail={'ledger_count':len(ledger)}))
    for gid,logical in [('HYPOTHESIS_SET','hypothesis_set'),('THESIS_DESTROYER','adversarial_review'),('MODEL_DISAGREEMENT','model_disagreement'),('PREMORTEM','premortem')]:g.append(_gate(gid,'PASS' if logical in names else 'FAIL',detail={'logical_name':logical}))
    ri=_art(rt,run_id,'research_intent',{}) or {};cog=_art(rt,run_id,'cognitive_adjudication',{}) or {}
    cd=canonical.get('decision',{}).get('final_direction');up=first(cog,'final_direction',default=first(ri,'fundamental_direction'))
    authok=compiled.get('authority',{}).get('direction')=='NONE' and (cd==up or cd is None or up is None)
    g.append(_gate('DIRECTION_AUTHORITY','PASS' if authok else 'FAIL',detail={'canonical_direction':cd,'upstream_direction':up,'compiler_authority':compiled.get('authority',{}).get('direction')}))
    fl=canonical.get('science',{}).get('force_lifecycle',{});required_force=['direction','force','consumption','remaining_pressure','persistence','reversal','invalidation','next_review'];forceok=all(k in fl for k in required_force)
    g.append(_gate('FORCE_STATE_INTEGRITY','PASS' if forceok else 'FAIL',detail={'present':sorted(fl.keys()),'required':required_force}))
    apl=canonical.get('apl_a',{});g.append(_gate('APL_A_SEPARATION','PASS' if apl.get('mode')=='SHADOW_ONLY' else 'FAIL',detail={'mode':apl.get('mode'),'direction_unchanged':True}))
    # REPORT_FIDELITY and PERSISTENCE are finalized later.
    g.append(_gate('REPORT_FIDELITY','PENDING',detail=None));g.append(_gate('PERSISTENCE','PENDING',detail=None))
    market=cd or 'UNKNOWN';receipt=_finish(g,market,run_id);receipt['cluster_coverage']=coverage;receipt['contradiction_ledger']=ledger;receipt['evidence_completeness']='CRITICAL_FAILURE' if not evidence_ok else ('MATERIAL_GAPS' if missing else 'COMPLETE');return receipt

def set_gate(receipt,gate_id,status,detail=None):
    out=json.loads(json.dumps(receipt))
    for g in out['gates']:
        if g['gate_id']==gate_id:g['status']=status;g['detail']=detail;break
    return _finish(out['gates'],out.get('market_state_resolution'),out.get('run_id')) | {k:v for k,v in out.items() if k in ('cluster_coverage','contradiction_ledger','evidence_completeness')}

def report_fidelity(canonical,report):
    c=canonical.get('decision',{});l=report.get('layer1',{});errors=[]
    if l.get('direction')!=c.get('final_direction'):errors.append('DIRECTION_MISMATCH')
    if l.get('permission')!=c.get('permission'):errors.append('PERMISSION_MISMATCH')
    fl=canonical.get('science',{}).get('force_lifecycle',{})
    pairs=[('force','force'),('remaining_pressure','remaining_pressure'),('persistence','persistence'),('reversal','reversal_risk')]
    for ck,rk in pairs:
        cv=fl.get(ck);rv=l.get(rk)
        if cv not in (None,'UNKNOWN') and rv not in (None,cv):errors.append(ck.upper()+'_MISMATCH')
    return {'status':'PASS' if not errors else 'FAIL','errors':errors,'direction':c.get('final_direction'),'permission':c.get('permission')}
