#!/usr/bin/env python3
from pathlib import Path
import copy,json,sys,tempfile
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT.parent))
from AD_V2_PHASE_07_D4_TRUE_FORWARD_PROMOTION.runtime.feature_freeze import freeze,FreezeError
from AD_V2_PHASE_07_D4_TRUE_FORWARD_PROMOTION.runtime.outcome_join import join,OutcomeError,verify_commitment
from AD_V2_PHASE_07_D4_TRUE_FORWARD_PROMOTION.runtime.calibration import calibrate
from AD_V2_PHASE_07_D4_TRUE_FORWARD_PROMOTION.runtime.promotion import evaluate
from AD_V2_PHASE_07_D4_TRUE_FORWARD_PROMOTION.runtime.true_forward import persist_commitment,persist_outcome_link,status,load_links
from AD_V2_PHASE_07_D4_TRUE_FORWARD_PROMOTION.runtime.commissioning import receipt
from AD_V2_PHASE_07_D4_TRUE_FORWARD_PROMOTION.runtime.d4_bridge import forward_observation,d4_outcome

def main():
    checks=[]
    def ck(name,cond): checks.append({'name':name,'status':'PASS' if cond else 'FAIL'})
    state=json.loads((ROOT/'tests/fixtures/p06_gold_run_state.json').read_text())
    pos=json.loads((ROOT/'tests/fixtures/outcome_mature_positive.json').read_text())
    pol=json.loads((ROOT/'config/promotion_policy.json').read_text())
    c=freeze(state,sample_provenance='TRUE_FORWARD',sealed_at_utc='2026-08-14T12:31:00Z',regime='SOFT_DATA')
    ck('freeze_record_type',c['record_type']=='V2_FORWARD_COMMITMENT');ck('freeze_subject',c['subject']=='XAUUSD');ck('freeze_true_forward',c['true_forward_eligible']);ck('freeze_hash',verify_commitment(c));ck('freeze_p06_hash',c['p06_state_hash']==state['canonical_v2_state_hash']);ck('freeze_permission_context',c['features']['v1_permission']=='NO_TRADE');ck('freeze_no_outcome',not any(k in json.dumps(c['features']).lower() for k in ['mfe_r','mae_r','realized_r']));ck('freeze_episode',bool(c['independent_episode_key']));ck('freeze_rootset',isinstance(c['dominant_root_ids'],list));ck('freeze_broker_none',c['authority']['broker']=='NONE')
    d=freeze(state,sample_provenance='DEVELOPMENT_CASE',sealed_at_utc='2026-08-14T12:31:00Z');ck('development_not_tf',not d['true_forward_eligible'])
    h=freeze(state,sample_provenance='HISTORICAL_RECONSTRUCTION',sealed_at_utc='2026-08-14T12:31:00Z');ck('historical_not_tf',not h['true_forward_eligible'])
    ho=freeze(state,sample_provenance='HOLDOUT',sealed_at_utc='2026-08-14T12:31:00Z');ck('holdout_not_tf',not ho['true_forward_eligible'])
    try: freeze(state,sample_provenance='TRUE_FORWARD',sealed_at_utc='2026-08-14T12:00:00Z'); ck('seal_before_analysis_blocked',False)
    except FreezeError: ck('seal_before_analysis_blocked',True)
    o=join(c,pos,joined_at_utc='2026-08-14T18:31:00Z');ck('outcome_link_type',o['record_type']=='V2_OUTCOME_LINK');ck('outcome_mature',o['maturity_state']=='MATURE');ck('outcome_tf_preserved',o['true_forward_eligible']);ck('commitment_not_rewritten',o['integrity']['commitment_rewritten'] is False);ck('outcome_hash',bool(o['outcome_hash']));ck('mfe_preserved',o['metrics']['mfe_r']==5.5);ck('mae_preserved',o['metrics']['mae_r']==0.7);ck('realized_preserved',o['metrics']['realized_r']==3.0)
    bad=copy.deepcopy(pos);bad['run_id']='OTHER'
    try:join(c,bad);ck('run_mismatch_blocked',False)
    except OutcomeError:ck('run_mismatch_blocked',True)
    early=copy.deepcopy(pos);early['matured_at_utc']='2026-08-14T12:00:00Z'
    try:join(c,early);ck('outcome_before_seal_blocked',False)
    except OutcomeError:ck('outcome_before_seal_blocked',True)
    tc=copy.deepcopy(c);tc['features']['release_readiness']='HIGH_READINESS';ck('tamper_detected',not verify_commitment(tc))
    # synthetic cohorts: 10 raw runs but 2 episode keys to prove dependence counts
    rows=[]
    for i in range(10):
        cc=copy.deepcopy(c);cc['commitment_id']=f'C{i}';cc['run_id']=f'R{i}';cc['independent_episode_key']='EP_A' if i<5 else 'EP_B';cc['trading_day']='2026-08-14' if i<5 else '2026-08-15';cc['features']=copy.deepcopy(c['features']);cc['features']['release_readiness']='HIGH_READINESS' if i>=5 else 'WATCH';cc['commitment_hash']='dummy';
        rr={'record_type':'V2_OUTCOME_LINK','commitment_id':cc['commitment_id'],'run_id':cc['run_id'],'sample_provenance':'TRUE_FORWARD','true_forward_eligible':True,'independent_episode_key':cc['independent_episode_key'],'trading_day':cc['trading_day'],'regime':'R1' if i<5 else 'R2','features':cc['features'],'maturity_state':'MATURE','metrics':{'mfe_r':1.0 if i<5 else 4.0,'mae_r':1.2 if i<5 else .5,'realized_r':0.2 if i<5 else 2.0,'time_to_mfe_seconds':4000 if i<5 else 1500}}
        rows.append(rr)
    rep=calibrate(rows);ck('cal_report_type',rep['record_type']=='V2_CALIBRATION_REPORT');ck('raw_tf_10',rep['sample_counts']['true_forward']==10);ck('episodes_2',rep['sample_counts']['true_forward_independent_episodes']==2);ck('days_2',rep['sample_counts']['true_forward_trading_days']==2);ck('incremental_positive',rep['incremental_value']['high_readiness_minus_watch_mean_mfe_r']>0);ck('state_metrics_present','release_readiness' in rep['state_metrics']);ck('tf_not_sufficient_initial',rep['true_forward']['sufficient_for_any_promotion'] is False);ck('historical_not_promotion',rep['true_forward']['historical_rows_count_toward_promotion'] is False)
    dec=evaluate(rep,pol);ck('insufficient_not_promoted',dec['status']=='TRUE_FORWARD_PENDING');ck('no_highest_class',dec['highest_eligible_class'] is None);ck('no_auto_promote',dec['auto_promoted'] is False);ck('no_direction_flip',dec['authority']['direction_flip_allowed'] is False);ck('no_positive_permission',dec['authority']['positive_permission_creation_allowed'] is False);ck('promotion_broker_none',dec['authority']['broker']=='NONE')
    com=receipt(dec,json.loads((ROOT/'config/commissioning_policy.json').read_text()),operator_approved=False);ck('not_commissioned',com['commissioned'] is False);ck('commission_runtime_no_mutation',com['runtime_mutation_performed'] is False);ck('commission_broker_none',com['authority']['broker']=='NONE')
    fwd=forward_observation(c);ck('d4_forward_type',fwd['record_type']=='FORWARD_OBSERVATION');ck('d4_no_ledger_write',fwd['metadata']['write_to_v1_d4_ledger'] is False);ck('d4_direction_from_pressure',fwd['fundamental_direction'] in {'BULLISH','BEARISH','UNRESOLVED'});d4o=d4_outcome(o);ck('d4_outcome_type',d4o['record_type']=='OUTCOME');ck('d4_outcome_no_ledger_write',d4o['metadata']['write_to_v1_d4_ledger'] is False)
    with tempfile.TemporaryDirectory() as td:
        persist_commitment(td,c);persist_outcome_link(td,o);st=status(td);ck('store_commitment',st['commitments_total']==1);ck('store_tf_commitment',st['true_forward_commitments']==1);ck('store_mature_tf',st['mature_true_forward']==1);ck('store_episode_1',st['mature_true_forward_independent_episodes']==1);ck('store_day_1',st['mature_true_forward_trading_days']==1);ck('store_pending_0',st['pending_true_forward']==0);ck('store_links_load',len(load_links(td))==1)
        try:persist_commitment(td,c);ck('duplicate_commitment_blocked',False)
        except RuntimeError:ck('duplicate_commitment_blocked',True)
        try:persist_outcome_link(td,o);ck('duplicate_outcome_blocked',False)
        except RuntimeError:ck('duplicate_outcome_blocked',True)
    # policies & schemas / documentation hard invariants
    feat=json.loads((ROOT/'config/feature_registry.json').read_text());ck('feature_registry_price_separation',all('price' not in f['id'] for f in feat['features']));ck('forbidden_mfe_token','mfe' in feat['forbidden_commitment_tokens']);ck('forbidden_outcome_token','outcome' in feat['forbidden_commitment_tokens'])
    tfp=json.loads((ROOT/'config/true_forward_policy.json').read_text());ck('no_relabel',tfp['allow_relabel_to_true_forward'] is False);ck('immutable_commitment_policy',tfp['immutable_commitment'] is True);ck('append_outcomes',tfp['append_only_outcomes'] is True)
    ck('promotion_validator_required',pol['independent_validator_required'] is True);ck('promotion_operator_required',pol['operator_approval_required'] is True);ck('promotion_auto_false',pol['auto_promote'] is False);ck('permission_create_false',pol['positive_permission_creation_allowed'] is False);ck('permission_min_150',pol['gates']['PERMISSION_MODULATION_CANDIDATE']['min_mature_true_forward_episodes']>=150)
    cp=json.loads((ROOT/'config/commissioning_policy.json').read_text());ck('commission_initial_pending',cp['initial_state']=='NOT_COMMISSIONED_TRUE_FORWARD_PENDING');ck('p07_no_runtime_mutation',cp['runtime_mutation_performed_by_p07'] is False);ck('trade_permission_v1',cp['trade_permission_remains_v1_until_separate_governed_promotion'] is True)
    attacks=json.loads((ROOT/'tests/p07_attack_cases.json').read_text());ck('attack_cases_16',len(attacks['cases'])>=16)
    # Count expected 76+ and output
    failed=[x for x in checks if x['status']!='PASS'];out={'schema_version':'1.0.0','phase':'AD-V2-P07','status':'PASS' if not failed else 'FAIL','passed':len(checks)-len(failed),'failed':len(failed),'checks':checks,'deployment':'SHADOW_ONLY','true_forward_initial_state':'PENDING','authority':{'v1_production':'UNCHANGED','trade_permission':'V1_INHERITED','broker':'NONE'}};print(json.dumps(out,indent=2));return 0 if not failed else 2
if __name__=='__main__':raise SystemExit(main())
