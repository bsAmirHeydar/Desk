from __future__ import annotations
from .common import iso,parse_dt,cfg,canonical_hash
from .forward_ledger import load_state,save_state,append_unique
from .cohort_manager import ensure_cohort,current_fingerprint
from .outcome_data import observation_from_anchor,add_observation
from .outcome_evaluator import evaluate_prediction
from .precommit import build_prediction
from .episode_manager import assign_episode
from .forward_statistics import compute
from .maturity import is_mature
from .legacy_migration import audit_legacy

def observe_and_evaluate(phase_root,current_price_anchor=None,now=None,state_root=None,r04_state_root=None):
    state=load_state(state_root);state,cohort,_=ensure_cohort(state,now);obs=observation_from_anchor(current_price_anchor);add_observation(state,obs);created=[];mature_uneval=[];recovery_receipts=[]
    existing={o['prediction_id'] for o in state['outcomes']}
    for p in state['predictions']:
        if p.get('cohort_id')!=cohort['cohort_id'] or p['prediction_id'] in existing:continue
        if not is_mature(p['maturity_time'],now or iso()):continue
        out=evaluate_prediction(p,state['market_observations'],evaluation_time=now)
        if out is None:
            # R04 supplies historical observations only; P09 remains sole outcome classifier.
            try:
                from AD_V31_R04_INSTITUTIONAL_DATA_EDGE_OUTCOME_INFRASTRUCTURE.runtime.outcome_recovery import recover_for_prediction
                rr=recover_for_prediction(p,state_root=r04_state_root,allow_network=True);recovery_receipts.append({'prediction_id':p['prediction_id'],**{k:v for k,v in rr.items() if k!='observations'}})
                for ro in rr.get('observations',[]):
                    x={'record_type':'AD_V3_P09_MARKET_OBSERVATION','observed_at_utc':ro['observed_at_utc'],'value':float(ro['value']),'source_fact_id':(p.get('price_anchor') or {}).get('source_fact_id'),'source_id':ro.get('provider_id'),'provider_id':ro.get('provider_id'),'instrument_key':ro.get('instrument_key') or (p.get('price_anchor') or {}).get('instrument_key'),'scientific_series_id':ro.get('scientific_series_id'),'outcome_evaluation_only':True,'causal_direction_authority':False,'outcome_acquisition_mode':'HISTORICALLY_RECOVERED','metadata':{'resolution':ro.get('metadata',{}).get('resolution') if isinstance(ro.get('metadata'),dict) else None}}
                    x['observation_id']=ro.get('record_checksum') or canonical_hash(x);add_observation(state,x)
                out=evaluate_prediction(p,state['market_observations'],evaluation_time=now)
            except Exception as e:
                recovery_receipts.append({'prediction_id':p['prediction_id'],'state':'RECOVERY_ERROR','error':type(e).__name__+':'+str(e)[:160]})
        if out:
            if append_unique(state,'outcomes',out,'outcome_id'):created.append(out)
        else:mature_uneval.append(p['prediction_id'])
    save_state(state,state_root);stats=compute(state,cohort['cohort_id'],as_of=now or iso());stats['legacy']=audit_legacy();return {'state':state,'cohort':cohort,'new_outcomes':created,'statistics':stats,'historical_recovery_receipts':recovery_receipts}

def precommit_current(phase_root,run_id,p08,p03,p07,semantic_bundle,price_anchor,now=None,state_root=None,event_context=None,perspective=None):
    state=load_state(state_root);state,cohort,cohort_changed=ensure_cohort(state,now);pred=build_prediction(run_id,p08,p03,p07,semantic_bundle,price_anchor,cohort,event_context=event_context,now=now,perspective=perspective);state,pred,ep=assign_episode(state,pred,now)
    # Immutable record hash is recomputed after T0 episode/sample-role assignment; all of this occurs before outcome.
    pred['immutable_hash']=canonical_hash({k:v for k,v in pred.items() if k!='immutable_hash'})
    append_unique(state,'predictions',pred,'prediction_id');save_state(state,state_root);stats=compute(state,cohort['cohort_id'],as_of=now or iso());return {'prediction':pred,'episode':ep,'cohort':cohort,'cohort_changed':cohort_changed,'statistics':stats,'state':state}

def status(phase_root,state_root=None):
    state=load_state(state_root);active=next((x for x in reversed(state['cohorts']) if x.get('state')=='OPEN'),None);fp=current_fingerprint();stats=compute(state,active.get('cohort_id') if active else None);return {'record_type':'AD_V3_P09_STATUS','implementation_status':'PASS','version':'3.9.0-true-forward-validation-2.0','active_cohort':active,'current_fingerprint':fp,'cohort_change_required':bool(active and active.get('fingerprint')!=fp),'statistics':stats,'legacy':audit_legacy(),'promotion_gate_satisfied':stats['forward_evidence_state'] in ('PROVISIONAL','MATURE'),'V3_state':'SHADOW_COMMISSIONING','trade_execution_authority':'NONE','integrity_failures':int(state.get('integrity_failures',0)),'test_fixture_samples_included':False}
