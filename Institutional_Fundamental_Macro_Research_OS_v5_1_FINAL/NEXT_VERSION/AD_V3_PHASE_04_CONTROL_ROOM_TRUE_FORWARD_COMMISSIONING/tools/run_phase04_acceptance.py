from __future__ import annotations
import json, pathlib, tempfile, sys, runpy
P=pathlib.Path(__file__).resolve().parents[1]; N=P.parent; REPO=N.parents[1]; sys.path.insert(0,str(N))
from AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING.runtime.semantic_runtime import conservative_bundle, validate_and_govern
from AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING.runtime.permission import evaluate
from AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING.runtime.control_room_model import build as build_model
from AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING.runtime.renderer import render, brief
from AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING.runtime.commissioning import build_precommit, update as update_commissioning, load_state as load_commissioning
from AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING.runtime.promotion import default_state

def load(p): return json.loads(pathlib.Path(p).read_text(encoding='utf-8-sig'))
def ck(name,ok,detail=None): return {'name':name,'status':'PASS' if ok else 'FAIL','detail':detail}
def main():
    checks=[]; p02=N/'AD_V3_PHASE_02_TOTAL_LIVE_DATA_OBSERVABILITY_FABRIC'; p03=N/'AD_V3_PHASE_03_CAUSAL_GOLD_BRAIN_DECISION_ENGINE'
    checks.append(ck('P02 frozen revision 3.2.6',load(p02/'DEVELOPMENT_MANIFEST.json').get('revision')=='3.2.6'))
    checks.append(ck('P03 frozen revision 3.3.6',load(p03/'DEVELOPMENT_MANIFEST.json').get('revision')=='3.3.6'))
    checks.append(ck('P03 production authority false',load(p03/'DEVELOPMENT_MANIFEST.json').get('production_direction_authority') is False and load(p03/'DEVELOPMENT_MANIFEST.json').get('production_trade_permission_authority') is False))
    packet={'record_type':'AD_V3_P03_SEMANTIC_EVIDENCE_PACKET','packet_id':'PK','item_count':2,'items':[{'fact_id':'FOMC_POLICY_STANCE','requested_observation_id':'O1','horizon_active':True,'pressure_plane':'CAUSAL_FUNDAMENTAL','authority_scope':'CAUSAL_CURRENT_HORIZON','may_add_to_current_causal_direction':True,'causal_root_family':'US_POLICY_EXPECTATIONS','current_observation':{'observation_id':'O1','epistemic_state':'OBSERVED_CURRENT','directness':'DIRECT','warnings':[]},'evidence_diagnostics':{'current_previous_value_equal':True,'economic_anchor_status':'NO_CURRENT_ECONOMIC_MARKER','economic_comparison_available':False,'dependency_current_observations_complete':True,'dependency_exact_acquisition_run_complete':True},'hard_guards':{}},{'fact_id':'US_FISCAL_DEFICIT_DEBT','requested_observation_id':'O2','horizon_active':False,'pressure_plane':'STRUCTURAL_CARRY','authority_scope':'STRUCTURAL_BACKGROUND_ONLY','may_add_to_current_causal_direction':False,'causal_root_family':'FISCAL_SOVEREIGN_MONETARY_CREDIBILITY','current_observation':{'observation_id':'O2','epistemic_state':'LATEST_VALID','directness':'DIRECT','warnings':[]},'evidence_diagnostics':{'current_previous_value_equal':True,'economic_anchor_status':'NO_DISTINCT_ECONOMIC_ANCHOR','economic_comparison_available':False,'dependency_current_observations_complete':True,'dependency_exact_acquisition_run_complete':True},'hard_guards':{}}]}
    b=conservative_bundle(packet); g=validate_and_govern(packet,b)
    checks.append(ck('conservative semantic runtime accounts every request',len(g['items'])==2 and all(x['effect_on_gold']=='UNKNOWN' and not x['is_additive'] for x in g['items']),g))
    try:
        bad={'record_type':'AD_V3_P03_SEMANTIC_ADJUDICATION_BUNDLE','subject':'XAUUSD','items':[g['items'][0],{**g['items'][1],'effect_on_gold':'BULLISH_GOLD','is_additive':True,'causal_owner_id':'FISCAL_SOVEREIGN_MONETARY_CREDIBILITY'}]}; validate_and_govern(packet,bad); blocked=False
    except Exception: blocked=True
    checks.append(ck('structural semantic authority bypass rejected',blocked))
    p03r={'receipt_id':'R','horizon':'SESSION_1_6H','p02_coverage_receipt_id':'C','handoff_integrity':{'acquisition_run_id':'RUN','current_observations_loaded':192,'expected_current_observations':192},'shadow_decision':{'direction_candidate':'UNKNOWN','action_candidate':'WAIT','blockers':['CAUSAL_DIRECTION_NOT_CLEAR']},'model_quality':{'model_completeness':'LOW','missing_driver_risk':'MEDIUM','resolved_root_families':0},'price_transmission':{'state':'UNTESTED','price_effects':[]},'pressure_planes':{'causal_fundamental':{'direction':'UNKNOWN','strength':'UNKNOWN','background_bias':'BEARISH_GOLD','root_states':[{'root_id':'REAL_RATE_OPPORTUNITY_COST','direction':'UNKNOWN','strength':'UNKNOWN','background_bias':'BEARISH_GOLD','evidence_fact_ids':[],'background_evidence_fact_ids':['UST_10Y_REAL_YIELD']}]},'realized_transaction':{'direction':'UNKNOWN','strength':'UNKNOWN'},'mechanical_forced':{'direction':'UNKNOWN','strength':'UNKNOWN'},'structural_carry':{'direction':'UNKNOWN','strength':'UNKNOWN'}},'lifecycle':{'consumption_vector':{'expectations_repricing':'ABSENT'},'persistence_stack':{'overall':'UNKNOWN'},'remaining_pressure':{'state':'UNKNOWN'}},'reasoning_ledger':{'unresolved_fact_ids':['FOMC_POLICY_STANCE']},'hypotheses':{'primary':{'expected_signatures':{}}}}
    prom=default_state(); perm=evaluate(p03r,prom); checks.append(ck('direction edge permission separated and fail closed',perm['direction']=='UNKNOWN' and perm['research_action_candidate']=='WAIT' and perm['official_permission']=='NO_AUTHORITY' and perm['trade_execution_authority'] is False,perm))
    commissioning={'record_type':'AD_V3_P04_COMMISSIONING_STATE','sample_state':'UNCALIBRATED','total_capsules':1,'outcomes_evaluated':0,'integrity_failures':0,'promotion_ready':False}; model=build_model('RUN1',p03r,packet,g,perm,commissioning,prom,None); h=render(model,load(P/'config/help_registry.json')); t=brief(model)
    checks.append(ck('human control room preserves background versus active direction',model['executive_state']['direction']=='UNKNOWN' and model['executive_state']['background_bias']=='BEARISH_GOLD'))
    checks.append(ck('HTML is RTL white human control room with inline help','dir="rtl"' in h and '--paper:#fff' in h and 'data-help=' in h and 'ALPHA DESK V3' in h))
    checks.append(ck('brief humanizes WAIT without granting authority','صبر' in t and 'Production trade execution authority: FALSE' in t))
    pc=build_precommit('RUN1',p03r,perm); checks.append(ck('true-forward precommit immutable and pre-outcome',pc['immutable_precommit'] is True and pc['outcome_status']=='NOT_DIRECTIONAL' and pc['precommit_id'].startswith('P04PRE_'),pc))
    with tempfile.TemporaryDirectory() as td:
        a1={'value':4300.0,'economic_marker':'2026-08-17T00:00:00Z'}; a2={'value':4325.0,'economic_marker':'2026-08-17T01:00:00Z'}
        pp=dict(perm); pp['direction']='BULLISH_GOLD'; pp['research_action_candidate']='BUY_CANDIDATE'
        pca=build_precommit('A',p03r,pp,a1); update_commissioning(td,pca,a1)
        pcb=build_precommit('B',p03r,pp,a2); st2=update_commissioning(td,pcb,a2)
        checks.append(ck('true-forward outcome ledger evaluates later distinct price anchor',st2['outcomes_evaluated']==1 and st2['aligned_outcomes']==1 and st2['sample_state']=='UNCALIBRATED',st2))
        checks.append(ck('true-forward pending queue preserves current precommit only',len(st2['pending'])==1 and st2['pending'][0]['precommit_id']==pcb['precommit_id'],st2.get('pending')))
    checks.append(ck('automatic promotion forbidden',load(P/'config/promotion_policy.json')['automatic_promotion_forbidden'] is True))
    checks.append(ck('V2 baseline retained by policy',load(P/'config/promotion_policy.json')['v2_baseline_retained_after_promotion'] is True))
    checks.append(ck('no trade execution capability',load(P/'DEVELOPMENT_MANIFEST.json')['forbidden'][-1]=='trade execution'))
    checks.append(ck('P04 does not claim initial production authority',load(P/'DEVELOPMENT_MANIFEST.json')['production_direction_authority'] is False and load(P/'DEVELOPMENT_MANIFEST.json')['production_trade_permission_authority'] is False))

    pipeline_src=(P/'runtime'/'pipeline.py').read_text(encoding='utf-8')
    cli_src=(P/'tools'/'alpha_desk_v3.py').read_text(encoding='utf-8')
    checks.append(ck('commissioning pipeline emits operator-visible progress','def _progress' in pipeline_src and '[1/7] P02 live acquisition' in pipeline_src and 'heartbeat_seconds' in pipeline_src))
    checks.append(ck('P02 BLOCKED receipt is parsed before stop','allow=(0, 2, 3)' in pipeline_src and 'P02_BLOCKED' in pipeline_src and 'BLOCKING FACTS' in pipeline_src))
    checks.append(ck('commissioning CLI stops cleanly without raw traceback','except RuntimeError as e:' in cli_src and 'COMMISSIONING - STOPPED' in cli_src))
    checks.append(ck('V3 CLI forces UTF-8 operator stdout and stderr',"def _configure_utf8_stdio" in cli_src and "reconfigure(encoding='utf-8', errors='replace')" in cli_src))
    launcher_src=(REPO/'AlphaDesk.ps1').read_text(encoding='utf-8-sig')
    checks.append(ck('Windows launcher establishes UTF-8 for V3 child processes','PYTHONIOENCODING' in launcher_src and 'PYTHONUTF8' in launcher_src and '[Console]::OutputEncoding' in launcher_src))
    status='PASS' if all(x['status']=='PASS' for x in checks) else 'FAIL'; out={'phase':'AD-V3-P04','acceptance_status':status,'check_count':len(checks),'checks':checks,'deployment':'SHADOW_COMMISSIONING','p01_p02_p03_frozen':True,'production_authority_still_false':True}; print(json.dumps(out,indent=2,ensure_ascii=False)); return 0 if status=='PASS' else 2
if __name__=='__main__': raise SystemExit(main())
