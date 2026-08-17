from __future__ import annotations
import json,pathlib,sys,tempfile,datetime
P=pathlib.Path(__file__).resolve().parents[1];N=P.parent;REPO=N.parents[1];sys.path.insert(0,str(N))
from AD_V3_PHASE_08_DECISION_SCIENCE_CALIBRATION.runtime.decision_runtime import calibrate
from AD_V3_PHASE_08_DECISION_SCIENCE_CALIBRATION.runtime.dominance_engine import reconcile
from AD_V3_PHASE_08_DECISION_SCIENCE_CALIBRATION.runtime.episode_builder import build_episodes
from AD_V3_PHASE_08_DECISION_SCIENCE_CALIBRATION.runtime.empirical_calibration import calibrate_from_episodes
from AD_V3_PHASE_08_DECISION_SCIENCE_CALIBRATION.runtime.feature_builder import build_root_features
from AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING.runtime.control_room_model import build as build_model

def load(p):return json.loads(pathlib.Path(p).read_text(encoding='utf-8-sig'))
def ck(n,o,d=None):return {'name':n,'status':'PASS' if o else 'FAIL','detail':d}
def root(rid,d,mag='MATERIAL',imp='PRIMARY',fresh='FRESH_FOR_HORIZON',q='HIGH',pers='NEW',sem=0):return {'root_id':rid,'direction':d,'causal_importance':imp,'magnitude':mag,'freshness':fresh,'evidence_quality':q,'persistence':pers,'semantic_unknown_count':sem,'empirical_information_state':'UNAVAILABLE'}
def fake_p03(direction='BULLISH_GOLD',roots=None,trans='ALIGNED',missing='LOW',cons=None):
 roots=roots or [{'root_id':'US_POLICY_EXPECTATIONS','direction':direction,'strength':'HIGH','evidence_fact_ids':['FED_POLICY_PATH_PRICING'],'background_bias':'UNKNOWN'}]
 rows=[]
 for r in roots:
  for i,f in enumerate(r.get('evidence_fact_ids') or []): rows.append({'fact_id':f,'observation_id':'O_'+f,'causal_root_family':r['root_id'],'resolution':'RESOLVED','reason_code':'TEST','effect_on_gold':r['direction'],'strength':r.get('strength','HIGH'),'details':{},'horizon_active':True})
 return {'receipt_id':'P03_TEST','horizon':'SESSION_1_6H','pressure_planes':{'causal_fundamental':{'direction':direction,'root_states':roots},'realized_transaction':{'direction':'UNKNOWN'},'mechanical_forced':{'direction':'UNKNOWN'},'structural_carry':{'direction':'UNKNOWN'}},'reasoning_ledger':{'rows':rows},'model_quality':{'missing_driver_risk':missing,'model_completeness':'HIGH'},'price_transmission':{'state':trans},'lifecycle':{'consumption_vector':cons or {'information_absorption':'ABSENT','expectations_repricing':'ABSENT','flow_propagation':'ABSENT','position_adjustment':'ABSENT','narrative_saturation':'ABSENT'}}}
def kernel(gaps=None):return {'kernel_health':{'important_live_gaps':gaps or [],'live_kernel_health':'HEALTHY','context_health':'HEALTHY','live_kernel_unfresh_fact_ids':[],'context_invalid_fact_ids':[]},'known_provider_gap_facts':[],'known_private_gap_facts':[],'known_paid_gap_facts':[]}
def main():
 checks=[]
 # Prior phases must have acceptance tools and baseline state.
 for i in range(1,8):
  hits=list(N.glob(f'AD_V3_PHASE_{i:02d}_*/tools/run_phase{i:02d}_acceptance.py'));checks.append(ck(f'P{i:02d} prerequisite acceptance tool present',bool(hits)))
 # Root-level dominance attacks (fact count absent from vectors).
 a=[root('R1','BULLISH_GOLD','MINOR','SECONDARY','CONTEXT_VALID'),root('R2','BULLISH_GOLD','MINOR','SECONDARY','CONTEXT_VALID'),root('R3','BULLISH_GOLD','MINOR','SECONDARY','CONTEXT_VALID'),root('R4','BEARISH_GOLD','LARGE','PRIMARY','FRESH_FOR_HORIZON')]
 d=reconcile(a);checks.append(ck('weak many cannot beat one fresh high-importance large opposing root',d['causal_direction']=='BEARISH_GOLD',d))
 b=[root('FED','BULLISH_GOLD','LARGE'),root('USD','BEARISH_GOLD','LARGE')];d2=reconcile(b);checks.append(ck('opposing primary material roots produce true mixed conflict',d2['causal_direction']=='MIXED' and d2['contradiction']=='PRIMARY_ROOT_CONFLICT',d2))
 five=[root('ONE_ROOT','BULLISH_GOLD','LARGE')];d3=reconcile(five);checks.append(ck('single root can dominate without fact-count breadth inflation',d3['causal_direction']=='BULLISH_GOLD' and d3['breadth']=='NARROW',d3))
 checks.append(ck('authority vector contains no raw fact count',all(len(x.get('authority_rank_tuple',[]))==5 for x in a+five)))
 # Full runtime scenarios using actual P03-compatible facts.
 r=calibrate(fake_p03(),kernel(),promotion_state={'state':'SHADOW_COMMISSIONING'});checks.append(ck('P08 cannot invent causal direction',r['causal_direction']=='BULLISH_GOLD' and r['raw_p03_causal_direction']=='BULLISH_GOLD',r))
 checks.append(ck('decision dimensions machine readable',all(k in r for k in ['pressure_strength','dominance_state','breadth','fragility','contradiction','consumption','edge_state','permission_candidate'])))
 checks.append(ck('magnitude is separate from direction',all(x.get('magnitude') in ('UNKNOWN','MINOR','MATERIAL','LARGE','EXTREME') and x.get('current_direction_from_p03_only') is True for x in r['calibrated_roots'])))
 checks.append(ck('root independence uses deterministic canonical ownership',all(x.get('independence')=='CANONICAL_ROOT_FAMILY_SINGLE_VOTE' for x in r['calibrated_roots'])))
 # Horizon-aware importance: session override is live-primary; structural horizon falls back to slow/context authority.
 realroot=[{'root_id':'REAL_RATE_OPPORTUNITY_COST','direction':'BULLISH_GOLD','strength':'HIGH','evidence_fact_ids':['UST_10Y_REAL_YIELD'],'background_bias':'BEARISH_GOLD'}]
 ps=fake_p03(roots=realroot); ps['horizon']='SESSION_1_6H'; pst=fake_p03(roots=realroot); pst['horizon']='STRUCTURAL'
 fs=build_root_features(ps,kernel(),None,{'entries':[]}); ft=build_root_features(pst,kernel(),None,{'entries':[]})
 checks.append(ck('causal importance is horizon-aware',fs[1]['causal_importance'] if len(fs)>1 else fs[0]['causal_importance']))
 # locate real-rate root explicitly because P03-compatible fake state contains only supplied root states.
 rs=next(x for x in fs if x['root_id']=='REAL_RATE_OPPORTUNITY_COST'); rt=next(x for x in ft if x['root_id']=='REAL_RATE_OPPORTUNITY_COST')
 checks[-1]=ck('causal importance is horizon-aware',rs['causal_importance']=='PRIMARY' and rt['causal_importance'] in ('SECONDARY','BACKGROUND','CONDITIONAL'),{'session':rs['causal_importance'],'structural':rt['causal_importance']})
 checks.append(ck('freshness authority inherited from P07',rs['freshness'] in ('FRESH_FOR_HORIZON','FRESH_LIVE','CONTEXT_VALID'),rs))
 checks.append(ck('single-root strong state can coexist with fragility',r['pressure_strength'] in ('STRONG','DOMINANT') and r['breadth']=='NARROW' and r['fragility'] in ('ELEVATED','HIGH'),r))
 structural=[{'root_id':'OFFICIAL_SECTOR_DEMAND','direction':'BULLISH_GOLD','strength':'HIGH','evidence_fact_ids':['CENTRAL_BANK_NET_GOLD_PURCHASES'],'background_bias':'BULLISH_GOLD'}]; st=calibrate(fake_p03(roots=structural),kernel(),promotion_state={'state':'SHADOW_COMMISSIONING'})
 checks.append(ck('structural context cannot masquerade as dominant current session impulse',st['pressure_strength'] not in ('DOMINANT','STRONG') and st['permission_candidate']=='WAIT',st))
 highcons={'information_absorption':'PRESENT','expectations_repricing':'PRESENT','flow_propagation':'PRESENT','position_adjustment':'PRESENT','narrative_saturation':'ABSENT'};hc=calibrate(fake_p03(cons=highcons),kernel(),promotion_state={'state':'SHADOW_COMMISSIONING'});checks.append(ck('high consumption preserves pressure but caps permission',hc['causal_direction']=='BULLISH_GOLD' and hc['consumption'] in ('HIGH','EXHAUSTED') and hc['permission_candidate']=='WAIT',hc))
 neg=calibrate(fake_p03(trans='NEGATIVE'),kernel(),promotion_state={'state':'SHADOW_COMMISSIONING'});checks.append(ck('price against pressure cannot rewrite causal direction',neg['causal_direction']=='BULLISH_GOLD' and neg['edge_state']!='ACTIONABLE_EDGE',neg))
 gap=calibrate(fake_p03(),kernel(['DXY_INDEX']),promotion_state={'state':'SHADOW_COMMISSIONING'});checks.append(ck('critical live gap caps edge and permission',gap['edge_state']!='ACTIONABLE_EDGE' and gap['permission_candidate']=='WAIT',gap))
 stale_kernel=kernel(); stale_kernel['kernel_health']['live_kernel_unfresh_fact_ids']=['FED_POLICY_PATH_PRICING']; stale=calibrate(fake_p03(),stale_kernel,promotion_state={'state':'SHADOW_COMMISSIONING'})
 checks.append(ck('stale large move keeps magnitude but caps current authority',next(x for x in stale['calibrated_roots'] if x['root_id']=='US_POLICY_EXPECTATIONS')['magnitude']=='LARGE' and stale['edge_state']!='ACTIONABLE_EDGE',stale))
 semroots=[{'root_id':'US_POLICY_EXPECTATIONS','direction':'BULLISH_GOLD','strength':'HIGH','evidence_fact_ids':['FED_POLICY_PATH_PRICING'],'background_bias':'UNKNOWN'}];sp=fake_p03(roots=semroots);sp['reasoning_ledger']['rows'].append({'fact_id':'FOMC_POLICY_STANCE','observation_id':'S','causal_root_family':'US_POLICY_EXPECTATIONS','resolution':'SEMANTICALLY_ADJUDICATED','reason_code':'SEMANTIC_ADJUDICATION_REQUIRED','effect_on_gold':'UNKNOWN','strength':'UNKNOWN','details':{},'horizon_active':True});sr=calibrate(sp,kernel(),promotion_state={'state':'SHADOW_COMMISSIONING'});checks.append(ck('semantic UNKNOWN/rejected caps authority',sr['fragility'] in ('ELEVATED','HIGH') and sr['edge_state']!='ACTIONABLE_EDGE' and sr['permission_candidate']=='WAIT',sr))
 # Persistence does not inflate on repeated same economic fingerprint.
 first=calibrate(fake_p03(),kernel(),promotion_state={'state':'SHADOW_COMMISSIONING'});second=calibrate(fake_p03(),kernel(),previous=first,promotion_state={'state':'SHADOW_COMMISSIONING'});pr=next(x for x in second['calibrated_roots'] if x['root_id']=='US_POLICY_EXPECTATIONS');checks.append(ck('repeated identical economic observation is persistence not reinforcement',pr['persistence']=='PERSISTENT',pr))
 # Historical episode overlap & no lookahead.
 t0=datetime.datetime(2026,1,1,tzinfo=datetime.timezone.utc); rows=[]
 for i in range(10):rows.append({'generated_at_utc':(t0+datetime.timedelta(hours=i)).isoformat().replace('+00:00','Z'),'run_id':str(i),'horizon':'SESSION_1_6H','causal_direction':'BULLISH_GOLD','dominant_root':'FED','pressure_strength':'STRONG','dominance_state':'BULLISH_DOMINANT'})
 eps=build_episodes(rows);checks.append(ck('ten overlapping unchanged hourly runs collapse to one episode',len(eps)==1 and eps[0]['run_count']==10,eps))
 try:build_episodes([{**rows[0],'future_price_reversal':True}]);blocked=False
 except ValueError:blocked=True
 checks.append(ck('future-defined episode boundary rejected',blocked))
 small=calibrate_from_episodes([{**eps[0],'outcome_alignment':'ALIGNED'} for _ in range(4)]); checks.append(ck('small sample overconfidence prevented',small['entries'][0]['empirical_authority']=='NEUTRAL' and small['entries'][0]['sample_state']=='INSUFFICIENT',small))
 empty=calibrate_from_episodes([]);checks.append(ck('empirical calibration unavailable safely',empty['overall_sample_state']=='UNAVAILABLE' and not empty['entries'],empty))
 # Underperformance cannot flip root direction because empirical state is not an input to direction reconciliation.
 under=[{**eps[0],'outcome_alignment':'OPPOSED'} for _ in range(60)];reg=calibrate_from_episodes(under);checks.append(ck('historical underperformance only produces caution authority',reg['entries'][0]['empirical_authority']=='CAUTION',reg['entries'][0]))
 largehist=[]
 for i in range(120):
  e={**eps[0],'episode_id':'H'+str(i),'start_utc':(t0+datetime.timedelta(days=i)).isoformat().replace('+00:00','Z'),'end_utc':(t0+datetime.timedelta(days=i,hours=1)).isoformat().replace('+00:00','Z'),'outcome_alignment':'ALIGNED' if i%2==0 else 'OPPOSED'};largehist.append(e)
 splitreg=calibrate_from_episodes(largehist);checks.append(ck('calibration/evaluation split enforced when data permits',splitreg['holdout_state']=='TIME_ORDERED_70_30' and splitreg['holdout_episode_count']>0,{'calibration':splitreg['calibration_episode_count'],'holdout':splitreg['holdout_episode_count']}))
 with tempfile.TemporaryDirectory() as td:
  rp=pathlib.Path(td)/'emp.json'; rp.write_text(json.dumps({'overall_sample_state':'USABLE','episode_count':60,'entries':[{'root_id':'US_POLICY_EXPECTATIONS','horizon':'SESSION_1_6H','sample_count':60,'sample_state':'USABLE','empirical_authority':'CAUTION'}]}),encoding='utf-8')
  cr=calibrate(fake_p03(),kernel(),promotion_state={'state':'SHADOW_COMMISSIONING'},empirical_registry_path=rp)
  checks.append(ck('historical performance cannot flip causal direction',cr['causal_direction']=='BULLISH_GOLD' and cr['edge_state']!='ACTIONABLE_EDGE',cr))
 # Monotonicity.
 clean=calibrate(fake_p03(),kernel(),promotion_state={'state':'SHADOW_COMMISSIONING'}); worse=calibrate(fake_p03(),kernel(['DXY_INDEX']),promotion_state={'state':'SHADOW_COMMISSIONING'});order=['NO_EDGE','LOW_EDGE','CONDITIONAL_EDGE','ACTIONABLE_EDGE'];checks.append(ck('worse data freshness/health cannot improve edge',order.index(worse['edge_state'])<=order.index(clean['edge_state'])))
 checks.append(ck('WAIT is first-class decision',gap['permission_candidate']=='WAIT'))
 checks.append(ck('no user-facing probability semantics',r['audit']['no_user_facing_probability'] is True and 'probability' not in r))
 checks.append(ck('raw P03 state retained for audit',r['audit']['p03_raw_direction_retained'] is True))
 checks.append(ck('official permission remains no authority in shadow',r['permission']['official_permission']=='NO_AUTHORITY' and r['permission']['trade_execution_authority'] is False))
 # P04 interface integration: raw P03 retained, calibrated permission and decision view reach the human model.
 model_fixture=build_model('P08_FIXTURE',fake_p03(),{'item_count':0},{'items':[],'adjudication_mode':'CONSERVATIVE_EVIDENCE_ONLY'},clean['permission'],{'sample_state':'UNCALIBRATED','outcomes_evaluated':0},{'state':'SHADOW_COMMISSIONING'},None,data_kernel=kernel(),decision_calibration=clean)
 checks.append(ck('P08 calibrated decision reaches P04 model',model_fixture.get('decision_calibration',{}).get('available') is True and model_fixture['decision_calibration']['edge_state']==clean['edge_state']))
 checks.append(ck('raw P03 causal result remains separately auditable',model_fixture.get('decision_calibration',{}).get('raw_p03_causal_direction')==clean['raw_p03_causal_direction']))
 # Integration/source assertions.
 pipe=(N/'AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING/runtime/pipeline.py').read_text(encoding='utf-8-sig'); model=(N/'AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING/runtime/control_room_model.py').read_text(encoding='utf-8-sig'); launch=(REPO/'AlphaDesk.ps1').read_text(encoding='utf-8-sig')
 checks.append(ck('P08 decision state reaches P04 pipeline','calibrate_decision' in pipe and 'p08_decision_calibration.json' in pipe))
 checks.append(ck('P04 control model consumes P08 calibration','decision_calibration' in model))
 checks.append(ck('run Gold production routing unchanged','PRODUCTION_V3' in launch and 'Invoke-V2 $AlphaArgs' in launch))
 checks.append(ck('v3 decision status installed','v3-decision-status' in launch))
 checks.append(ck('V3 remains shadow and automatic promotion forbidden',load(N/'AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING/config/promotion_policy.json')['automatic_promotion_forbidden'] is True))
 checks.append(ck('trade execution authority remains NONE',load(P/'config/decision_calibration_policy.json')['trade_execution_authority']=='NONE'))
 # Static scientific hashes.
 import hashlib
 base=load(P/'baseline/PRE_P08_AUTHORITY_HASHES.json'); drift=[]
 for name,v in base['hashes'].items():
  f=REPO/v['path']; actual=hashlib.sha256(f.read_bytes()).hexdigest() if f.exists() else None
  if actual!=v['sha256']:drift.append(name)
 checks.append(ck('substantive Gold and upstream authority drift zero',not drift,drift))
 ok=all(x['status']=='PASS' for x in checks);out={'phase':'AD-V3-P08','version':'3.8.0-decision-science-calibration','acceptance_status':'PASS' if ok else 'FAIL_CLOSED','check_count':len(checks),'checks':checks,'historical_calibration_sample_state':'UNAVAILABLE','historical_episode_count_in_supplied_repository':0,'production_promotion_performed':False,'v3_state':'SHADOW_COMMISSIONING','trade_execution_authority':'NONE'};print(json.dumps(out,indent=2,ensure_ascii=False));return 0 if ok else 2
if __name__=='__main__':raise SystemExit(main())
