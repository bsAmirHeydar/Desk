from __future__ import annotations
import copy, pathlib, sys, tempfile
HERE=pathlib.Path(__file__).resolve();PH=HERE.parents[1];NEXT=PH.parent;REPO=NEXT.parents[1]
sys.path.insert(0,str(NEXT))
from AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN.runtime.gold_orchestrator import run_gold
from AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN.runtime.common import load

def base_input(tmp_root: pathlib.Path, as_of='2026-08-17T10:00:00Z'):
    p02=NEXT/'AD_V3_PHASE_02_TOTAL_LIVE_DATA_OBSERVABILITY_FABRIC'
    fix=p02/'tests/fixtures/generated'
    data=tmp_root/'data'; art=tmp_root/'art'; kout=tmp_root/'kernel'; p09=tmp_root/'p09'
    run_gold(REPO,'SESSION_1_6H','FIXTURE','NORMAL',p02_data_root_override=data,artifact_root_override=art,kernel_fixture_dir=fix,kernel_output_root_override=kout,p09_state_root_override=p09,as_of_utc=as_of,fixture_mode=True,update_latest=False,quiet=True)
    rd=next((art/'runs').iterdir())
    return load(rd/'control_room_input.json'), rd, p09

def scenario(cri: dict, name: str)->dict:
    x=copy.deepcopy(cri); d=x.setdefault('decision_calibration',{}); kh=x.setdefault('data_kernel',{}).setdefault('kernel_health',{}); f=x.setdefault('forward_validation',{}); stats=f.setdefault('statistics',{}); sem=x.setdefault('semantic',{}).setdefault('bundle',{})
    d.setdefault('calibrated_roots',[])
    def root(rid, direction, imp='PRIMARY', mag='LARGE', fresh='FRESH_FOR_HORIZON', persistence='PERSISTENT', facts=None):
        return {'root_id':rid,'direction':direction,'background_bias':'UNKNOWN','evidence_fact_ids':facts or [],'causal_importance':imp,'magnitude':mag,'freshness':fresh,'evidence_quality':'DIRECT_HIGH','independence':'CANONICAL_ROOT_FAMILY_SINGLE_VOTE','persistence':persistence,'semantic_unknown_count':0,'empirical_information_state':'UNAVAILABLE'}
    if name in {'bullish_buy','dense'}:
        d.update({'causal_direction':'BULLISH_GOLD','pressure_strength':'STRONG','dominance_state':'BULLISH_DOMINANT','dominant_root':'REAL_RATE_OPPORTUNITY_COST','supporting_roots':['US_POLICY_EXPECTATIONS'],'opposing_roots':['USD_AUTONOMOUS'],'breadth':'MODERATE','fragility':'LOW' if name=='bullish_buy' else 'HIGH','fragility_reasons':[] if name=='bullish_buy' else ['NARROW_BREADTH','DATA_DEGRADATION'],'contradiction':'MEANINGFUL' if name=='dense' else 'LOW','consumption':'LOW' if name=='bullish_buy' else 'HIGH','edge_state':'ACTIONABLE_EDGE' if name=='bullish_buy' else 'CONDITIONAL_EDGE','permission_candidate':'BUY' if name=='bullish_buy' else 'WAIT','blockers':[] if name=='bullish_buy' else ['HIGH_CONSUMPTION'],'missing_driver_risk':'LOW'})
        d['calibrated_roots']=[root('REAL_RATE_OPPORTUNITY_COST','BULLISH_GOLD',facts=['UST_10Y_REAL_YIELD']),root('US_POLICY_EXPECTATIONS','BULLISH_GOLD',facts=['FED_FUNDS_POLICY_PATH']),root('USD_AUTONOMOUS','BEARISH_GOLD',imp='SECONDARY',mag='MATERIAL',facts=['DXY_INDEX'])]
    elif name=='bearish_sell':
        d.update({'causal_direction':'BEARISH_GOLD','pressure_strength':'STRONG','dominance_state':'BEARISH_DOMINANT','dominant_root':'USD_AUTONOMOUS','supporting_roots':['REAL_RATE_OPPORTUNITY_COST'],'opposing_roots':[],'breadth':'MODERATE','fragility':'LOW','fragility_reasons':[],'contradiction':'LOW','consumption':'LOW','edge_state':'ACTIONABLE_EDGE','permission_candidate':'SELL','blockers':[],'missing_driver_risk':'LOW'})
        d['calibrated_roots']=[root('USD_AUTONOMOUS','BEARISH_GOLD',facts=['DXY_INDEX']),root('REAL_RATE_OPPORTUNITY_COST','BEARISH_GOLD',facts=['UST_10Y_REAL_YIELD'])]
    elif name=='true_mixed':
        d.update({'causal_direction':'MIXED','pressure_strength':'MODERATE','dominance_state':'BALANCED','dominant_root':None,'supporting_roots':[],'opposing_roots':[],'breadth':'MODERATE','fragility':'HIGH','fragility_reasons':['PRIMARY_ROOT_CONFLICT'],'contradiction':'PRIMARY_ROOT_CONFLICT','consumption':'MODERATE','edge_state':'NO_EDGE','permission_candidate':'WAIT','blockers':['TRUE_MIXED'],'missing_driver_risk':'MEDIUM'})
        d['calibrated_roots']=[root('REAL_RATE_OPPORTUNITY_COST','BULLISH_GOLD'),root('USD_AUTONOMOUS','BEARISH_GOLD')]
    elif name=='blocked':
        kh['overall_analysis_admission']='BLOCK';kh['live_kernel_health']='BLOCKED';d.update({'causal_direction':'UNKNOWN','pressure_strength':'UNKNOWN','dominance_state':'UNKNOWN','dominant_root':None,'breadth':'NONE','fragility':'HIGH','contradiction':'UNKNOWN','consumption':'UNKNOWN','edge_state':'NO_EDGE','permission_candidate':'NO_AUTHORITY','blockers':['CRITICAL_DATA_GAP']})
    elif name=='unknown':
        d.update({'causal_direction':'UNKNOWN','pressure_strength':'UNKNOWN','dominance_state':'UNKNOWN','dominant_root':None,'breadth':'NONE','fragility':'HIGH','contradiction':'NONE','consumption':'UNKNOWN','edge_state':'NO_EDGE','permission_candidate':'WAIT','blockers':['NO_CLEAR_DIRECTION']})
    elif name=='degraded':
        kh['overall_analysis_admission']='DEGRADED_ALLOW';kh['live_kernel_health']='DEGRADED';d['permission_candidate']='WAIT';d['blockers']=['CRITICAL_DATA_GAP']
    elif name=='semantic_conservative':
        sem['adjudication_mode']='CONSERVATIVE_EVIDENCE_ONLY';d['permission_candidate']='WAIT'
    if name=='forward_provisional':
        stats.update({'raw_prediction_count':65,'episode_count':55,'mature_episode_count':50,'pending_prediction_count':10,'forward_evidence_state':'PROVISIONAL','direction_calibration_state':'EARLY','permission_calibration_state':'EARLY','wait_calibration_state':'EARLY','strength_calibration_state':'EARLY','dominance_calibration_state':'EARLY','edge_calibration_state':'EARLY','consumption_calibration_state':'EARLY','fragility_calibration_state':'EARLY','missing_driver_calibration_state':'EARLY'})
    if name=='dense':
        # governed event fixture
        f.setdefault('prediction',{})['event_context']={'events':[{'event':'CPI','label':'CPI آمریکا','event_time':'2026-08-17T12:30:00Z','materiality':'THESIS_CRITICAL','affected_roots':['US_POLICY_EXPECTATIONS'],'status':'UPCOMING'}]}
        kh['important_live_gaps']=['DXY_INDEX','UST_10Y_REAL_YIELD']
    return x
