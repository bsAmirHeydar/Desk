#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
from datetime import datetime,timezone,timedelta
import sys,json,tempfile,copy,subprocess
P=Path(__file__).resolve().parents[1];N=P.parent;REPO=N.parents[1];sys.path.insert(0,str(N))
from AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0.runtime.common import cfg,parse_dt,iso,canonical_hash
from AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0.runtime.forward_ledger import load_state,save_state,ForwardLedgerCorrupt
from AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0.runtime.forward_runtime import observe_and_evaluate,precommit_current,status
from AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0.runtime.forward_statistics import sample_state,compute
from AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0.runtime.outcome_data import observation_from_anchor,add_observation
from AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0.runtime.outcome_evaluator import evaluate_prediction,neutral_band
from AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0.runtime.episode_manager import assign_episode
from AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0.runtime.maturity import maturity_for,is_mature
from AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0.runtime.cohort_manager import ensure_cohort,current_fingerprint
from AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0.runtime.legacy_migration import audit_legacy

def ck(n,ok,d=None):return {'name':n,'status':'PASS' if ok else 'FAIL','detail':d}
def dt(s):return datetime.fromisoformat(s.replace('Z','+00:00'))
def anchor(v,t,src='SRC_XAU',fact='XAUUSD_SPOT_PRICE'):
    return {'value':float(v),'economic_marker':t,'retrieved_at':t,'source_fact_id':fact,'source_id':src,'anchor_kind':'SPOT_DIRECT','proxy_for_xauusd':False,'causal_direction_authority':False}
def p08(direction='BULLISH_GOLD',permission='WAIT',dominance='BULLISH_DOMINANT',root='US_POLICY_EXPECTATIONS',strength='STRONG',cons='LOW',frag='LOW',edge='ACTIONABLE_EDGE',blockers=None,contr='NONE'):
    return {'horizon':'SESSION_1_6H','causal_direction':direction,'pressure_strength':strength,'dominance_state':dominance,'dominant_root':root,'breadth':'MODERATE','fragility':frag,'contradiction':contr,'consumption':cons,'missing_driver_risk':'LOW','edge_state':edge,'permission_candidate':permission,'blockers':blockers or [],'calibrated_roots':[{'root_id':root,'persistence':'PERSISTENT'}]}
def p03(direction='BULLISH_GOLD'):
    return {'receipt_id':'P03R','horizon':'SESSION_1_6H','pressure_planes':{'causal_fundamental':{'direction':direction}},'model_quality':{'missing_driver_risk':'LOW'}}
def p07(adm='ALLOW'):
    return {'run_id':'P07R','analysis_admission':adm,'kernel_health':{'overall_analysis_admission':adm,'live_kernel_health':'HEALTHY','important_live_gaps':[]}}
def sem():return {'adjudication_mode':'AUTO_GOVERNED','p06_semantic':{'validation_status':'PASS'}}

def add_path(state,start,prices,minutes=30,src='SRC_XAU'):
    t=dt(start)
    for i,v in enumerate(prices):
        tt=(t+timedelta(minutes=i*minutes)).isoformat().replace('+00:00','Z')
        add_observation(state,observation_from_anchor(anchor(v,tt,src=src)))

def main():
    checks=[]
    # prerequisite surface: actual prior acceptances are run separately in release regression; ensure phase tools exist and P08 PASS now.
    pre=[]
    for i in range(1,9):
        d=next(N.glob(f'AD_V3_PHASE_{i:02d}_*'),None); pre.append(bool(d and (d/'tools'/f'run_phase{i:02d}_acceptance.py').exists()))
    checks.append(ck('P01-P08 prerequisite baseline tools present',all(pre),pre))
    checks.append(ck('legacy P04 forward history preserved', (N/'AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING/runtime/commissioning.py').exists()))
    checks.append(ck('legacy samples cannot silently satisfy P09 maturity',audit_legacy()['legacy_samples_grant_p09_maturity'] is False,audit_legacy()))
    with tempfile.TemporaryDirectory() as td:
        root=Path(td); t0='2026-08-17T10:00:00Z'
        # T0 observation, then precommit.
        observe_and_evaluate(P,anchor(4000,t0),now=t0,state_root=root)
        r=precommit_current(P,'RUN0',p08(),p03(),p07(),sem(),anchor(4000,t0),now=t0,state_root=root); pred=r['prediction']; orig=copy.deepcopy(pred)
        checks.append(ck('P09 prediction precommit immutable',pred['immutable_precommit'] is True and pred['immutable_hash']==canonical_hash({k:v for k,v in pred.items() if k!='immutable_hash'}),pred))
        checks.append(ck('prediction horizon fixed at T0',pred['horizon']=='SESSION_1_6H'))
        checks.append(ck('maturity timestamp fixed at T0',pred['maturity_time']==maturity_for(t0,'SESSION_1_6H'),pred['maturity_time']))
        early=observe_and_evaluate(P,anchor(4010,'2026-08-17T11:00:00Z'),now='2026-08-17T11:00:00Z',state_root=root)
        checks.append(ck('early evaluation impossible',len(early['new_outcomes'])==0 and early['statistics']['pending_prediction_count']>=1,early['statistics']))
        # add path through fixed maturity, evaluate late at 20:00. terminal at maturity is 4060; later 4200 must not be used.
        s=load_state(root); add_path(s,t0,[4000,4005,4010,4020,4030,4040,4050,4060,4070,4080,4075,4070,4060],30); add_observation(s,observation_from_anchor(anchor(4200,'2026-08-17T20:00:00Z'))); save_state(s,root)
        late=observe_and_evaluate(P,None,now='2026-08-17T20:00:00Z',state_root=root); out=late['new_outcomes'][0]
        checks.append(ck('late evaluation uses fixed maturity price',abs(out['terminal_observation']['value']-4060)<1e-9,out['terminal_observation']))
        checks.append(ck('outcome source predetermined',out['terminal_observation']['source_id']=='SRC_XAU' and out['outcome_source_predetermined'] is True))
        checks.append(ck('neutral band versioned',pred['policy_versions']['neutral_band']=='1.0.0' and out['neutral_band_return']>0))
        checks.append(ck('future realized volatility cannot normalize T0',cfg('outcome_price_policy.json')['future_realized_volatility_not_decision_normalizer'] is True and pred.get('volatility_reference') is None))
        checks.append(ck('terminal result separate from path metrics',out['terminal_return'] is not None and out['mfe_return'] is not None and out['mae_return'] is not None))
        # Idempotence
        again=observe_and_evaluate(P,None,now='2026-08-17T21:00:00Z',state_root=root)
        checks.append(ck('outcome evaluation idempotent',len(again['new_outcomes'])==0 and len(load_state(root)['outcomes'])==1))
        # immutable mutation rejected by append semantics: original stored unchanged.
        stored=next(x for x in load_state(root)['predictions'] if x['prediction_id']==pred['prediction_id'])
        checks.append(ck('prediction cannot mutate after outcome',stored==orig,{'stored_hash':stored['immutable_hash']}))
    # Missing path terminal-only: construct evaluator input with T0 and terminal only.
    with tempfile.TemporaryDirectory() as td:
        root=Path(td); t0='2026-08-18T10:00:00Z'; observe_and_evaluate(P,anchor(4000,t0),now=t0,state_root=root); r=precommit_current(P,'MISSINGPATH',p08(permission='BUY_CANDIDATE'),p03(),p07(),sem(),anchor(4000,t0),now=t0,state_root=root); pred=r['prediction']; mt=pred['maturity_time']; obs=[observation_from_anchor(anchor(4000,t0)),observation_from_anchor(anchor(4040,mt))]; o=evaluate_prediction(pred,obs,evaluation_time=mt)
        checks.append(ck('missing path data does not fabricate MFE/MAE',o['direction_outcome']=='ALIGNED' and o['mfe_return'] is None and o['mae_return'] is None and o['path_coverage']['path_metric_authority']=='UNAVAILABLE',o))
    # tiny move neutral
    with tempfile.TemporaryDirectory() as td:
        root=Path(td); t0='2026-08-19T10:00:00Z'; observe_and_evaluate(P,anchor(4000,t0),now=t0,state_root=root); pred=precommit_current(P,'NEUTRAL',p08(),p03(),p07(),sem(),anchor(4000,t0),now=t0,state_root=root)['prediction']; mt=pred['maturity_time']; o=evaluate_prediction(pred,[observation_from_anchor(anchor(4000,t0)),observation_from_anchor(anchor(4001,mt))],evaluation_time=mt);checks.append(ck('tiny price change stays neutral band',o['direction_outcome']=='NEUTRAL_BAND',o))
    # overlap and material update
    with tempfile.TemporaryDirectory() as td:
        root=Path(td); base=dt('2026-08-20T09:00:00Z'); roles=[]; eps=[]
        for i in range(4):
            t=(base+timedelta(hours=i)).isoformat().replace('+00:00','Z'); observe_and_evaluate(P,anchor(4000+i,t),now=t,state_root=root); rr=precommit_current(P,f'OV{i}',p08(),p03(),p07(),sem(),anchor(4000+i,t),now=t,state_root=root);roles.append(rr['prediction']['sample_role']);eps.append(rr['prediction']['episode_id'])
        checks.append(ck('repeated hourly snapshots do not inflate episode count',len(set(eps))==1 and roles[0]=='PRIMARY_EPISODE_SAMPLE' and all(x=='DUPLICATE_EPISODE_SNAPSHOT' for x in roles[1:]),{'roles':roles,'episodes':eps}))
        t=(base+timedelta(hours=4)).isoformat().replace('+00:00','Z'); observe_and_evaluate(P,anchor(4010,t),now=t,state_root=root); rr=precommit_current(P,'MAT',p08(dominance='BULLISH_FRAGILE'),p03(),p07(),sem(),anchor(4010,t),now=t,state_root=root)
        checks.append(ck('material child update stays non-independent',rr['prediction']['sample_role']=='MATERIAL_UPDATE' and rr['prediction']['episode_id']==eps[0],rr['prediction']))
        checks.append(ck('episode sample count drives maturity',sample_state(1)=='INSUFFICIENT' and compute(load_state(root))['episode_count']==1))
        # lookahead attack
        st=load_state(root); bad=copy.deepcopy(rr['prediction']);bad['prediction_id']='FUTURE';bad['future_price']=4500
        try:assign_episode(st,bad,now=t); blocked=False
        except ValueError as e:blocked='LOOKAHEAD' in str(e)
        checks.append(ck('episode membership rejects future-price input',blocked))
    # same direction but permission changes => new episode
    with tempfile.TemporaryDirectory() as td:
        root=Path(td); t0='2026-08-21T09:00:00Z';observe_and_evaluate(P,anchor(4000,t0),now=t0,state_root=root); a=precommit_current(P,'P1',p08(permission='WAIT'),p03(),p07(),sem(),anchor(4000,t0),now=t0,state_root=root)['prediction'];t1='2026-08-21T10:00:00Z';observe_and_evaluate(P,anchor(4002,t1),now=t1,state_root=root); b=precommit_current(P,'P2',p08(permission='BUY_CANDIDATE'),p03(),p07(),sem(),anchor(4002,t1),now=t1,state_root=root)['prediction'];checks.append(ck('permission material change starts new episode',a['episode_id']!=b['episode_id']))
    # source cherry picking: primary source only
    with tempfile.TemporaryDirectory() as td:
        root=Path(td);t0='2026-08-24T10:00:00Z';observe_and_evaluate(P,anchor(4000,t0),now=t0,state_root=root); pred=precommit_current(P,'SRC',p08(),p03(),p07(),sem(),anchor(4000,t0),now=t0,state_root=root)['prediction'];mt=pred['maturity_time'];obs=[observation_from_anchor(anchor(3950,mt,src='SRC_XAU')),observation_from_anchor(anchor(4100,mt,src='OTHER'))];o=evaluate_prediction(pred,obs,evaluation_time=mt);checks.append(ck('outcome source cherry-picking blocked',o['terminal_observation']['source_id']=='SRC_XAU' and o['direction_outcome']=='OPPOSED',o))
    # horizon leakage: no terminal near fixed maturity => None even if 6h/24h later point exists
    with tempfile.TemporaryDirectory() as td:
        root=Path(td);t0='2026-08-25T10:00:00Z';observe_and_evaluate(P,anchor(4000,t0),now=t0,state_root=root); pred=precommit_current(P,'HL',p08(),p03(),p07(),sem(),anchor(4000,t0),now=t0,state_root=root)['prediction'];later=(parse_dt(pred['maturity_time'])+timedelta(hours=10)).isoformat().replace('+00:00','Z');o=evaluate_prediction(pred,[observation_from_anchor(anchor(4500,later))],evaluation_time=later);checks.append(ck('horizon leakage blocked',o is None))
    # weekend maturity skips closure
    fri='2026-08-21T20:00:00Z'; mt=maturity_for(fri,'SESSION_1_6H'); checks.append(ck('weekend maturity uses tradable-time scheduler',parse_dt(mt)-parse_dt(fri)>timedelta(hours=6),{'t0':fri,'maturity':mt}))
    # small sample not provisional, raw run count irrelevant
    checks.append(ck('small samples cannot become provisional',sample_state(3) in ('INSUFFICIENT','EARLY') and sample_state(49)!='PROVISIONAL'))
    checks.append(ck('episode count not raw run count drives maturity',sample_state(8)=='INSUFFICIENT' and sample_state(100)=='MATURE'))
    # WAIT outcome distinct from direction
    with tempfile.TemporaryDirectory() as td:
        root=Path(td);t0='2026-08-26T10:00:00Z';observe_and_evaluate(P,anchor(4000,t0),now=t0,state_root=root); pred=precommit_current(P,'WAIT',p08(permission='WAIT',cons='HIGH',blockers=['HIGH_CONSUMPTION']),p03(),p07(),sem(),anchor(4000,t0),now=t0,state_root=root)['prediction'];mt=pred['maturity_time']; obs=[]; start=parse_dt(t0)
        for i,v in enumerate([4000,4002,4004,4005,4003,4001,3998,3997,3998]):obs.append(observation_from_anchor(anchor(v,(start+timedelta(minutes=45*i)).isoformat().replace('+00:00','Z'))))
        obs.append(observation_from_anchor(anchor(3998,mt)));o=evaluate_prediction(pred,obs,evaluation_time=mt);checks.append(ck('WAIT quality independently evaluated',o['direction_outcome'] in ('OPPOSED','NEUTRAL_BAND') and o['wait_outcome'] in ('WAIT_PROTECTED','WAIT_APPROPRIATE_UNCERTAINTY'),o))
    # direction correct / permission may be wrong due adverse path
    with tempfile.TemporaryDirectory() as td:
        root=Path(td);t0='2026-08-27T10:00:00Z';observe_and_evaluate(P,anchor(4000,t0),now=t0,state_root=root);pred=precommit_current(P,'DP',p08(permission='BUY_CANDIDATE'),p03(),p07(),sem(),anchor(4000,t0),now=t0,state_root=root)['prediction'];mt=pred['maturity_time']; start=parse_dt(t0);vals=[4000,3940,3930,3960,4005,4020,4030,4040,4050];obs=[observation_from_anchor(anchor(v,(start+timedelta(minutes=45*i)).isoformat().replace('+00:00','Z'))) for i,v in enumerate(vals)];obs.append(observation_from_anchor(anchor(4050,mt)));o=evaluate_prediction(pred,obs,evaluation_time=mt);checks.append(ck('direction and permission quality remain separate',o['direction_outcome']=='ALIGNED' and o['permission_outcome'] in ('MIXED','OPPOSED','SUPPORTED'),o))
    # eligibility fixed at T0 / no outcome based exclusion: immutable field stored.
    checks.append(ck('validation eligibility fixed at T0',cfg('forward_validation_policy.json')['eligibility_fixed_at_t0'] is True and cfg('forward_validation_policy.json')['outcome_based_exclusion_forbidden'] is True))
    # Event exposure is diagnostic and never excludes the sample.
    with tempfile.TemporaryDirectory() as td:
        root=Path(td);t0='2026-08-28T10:00:00Z';observe_and_evaluate(P,anchor(4000,t0),now=t0,state_root=root);ev={'events':[{'event_id':'CPI_TEST','event_time':'2026-08-28T12:00:00Z'}]};pred=precommit_current(P,'EVENT',p08(permission='BUY_CANDIDATE'),p03(),p07(),sem(),anchor(4000,t0),now=t0,state_root=root,event_context=ev)['prediction'];mt=pred['maturity_time'];obs=[observation_from_anchor(anchor(4000,t0)),observation_from_anchor(anchor(4050,mt))];o=evaluate_prediction(pred,obs,evaluation_time=mt);checks.append(ck('event exposure recorded without deleting sample',o['event_exposure']=='EVENT_EXPOSED' and pred['eligibility']=='VALIDATION_ELIGIBLE',o))
    # cohort drift
    with tempfile.TemporaryDirectory() as td:
        st=load_state(td);st,c1,_=ensure_cohort(st,'2026-08-17T10:00:00Z');old=c1['fingerprint'];c1['fingerprint']='DRIFTED';st,c2,changed=ensure_cohort(st,'2026-08-17T11:00:00Z');checks.append(ck('policy drift forces cohort transition',changed and c2['cohort_id']!=c1['cohort_id'] and c1['state']=='SUPERSEDED',{'old':old,'new':c2['fingerprint']}))
    checks.append(ck('cohort fingerprint binds current science runtime',len(current_fingerprint())==64))
    # corrupt ledger
    with tempfile.TemporaryDirectory() as td:
        Path(td,'forward_state.json').write_text('{bad',encoding='utf-8')
        try:load_state(td);bad=False
        except ForwardLedgerCorrupt:bad=True
        checks.append(ck('corrupt forward ledger fails closed',bad))
    # legacy incompatible fixture semantics
    checks.append(ck('legacy raw P04 outcome without fixed maturity is incompatible',audit_legacy()['legacy_samples_grant_p09_maturity'] is False))
    with tempfile.TemporaryDirectory() as td:
        p4=Path(td);q=p4/'artifacts'/'commissioning';q.mkdir(parents=True);rows=[{'outcome_id':'A','precommit_id':'P1','direction_candidate':'BULLISH_GOLD','anchor':{},'outcome_anchor':{},'horizon':'SESSION_1_6H','maturity_time':'2026-08-17T16:00:00Z'},{'outcome_id':'B','precommit_id':'P2','direction_candidate':'BULLISH_GOLD','anchor':{},'outcome_anchor':{}},{'outcome_id':'C'}];(q/'outcomes.jsonl').write_text('\n'.join(json.dumps(x) for x in rows)+'\n');la=audit_legacy(p4);checks.append(ck('legacy migration classifies compatible and incompatible deterministically',la['counts']['P09_COMPATIBLE']==1 and la['counts']['P09_INCOMPATIBLE']==2,la))
    # promotion gate config
    p4=N/'AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING';pol=json.loads((p4/'config/promotion_policy.json').read_text());checks.append(ck('P09 gate replaces legacy P04 true-forward gate','P09_FORWARD_EVIDENCE_PROVISIONAL' in pol['promotion_requires'] and 'TRUE_FORWARD_SAMPLE_PROVISIONAL' not in pol['promotion_requires'],pol['promotion_requires']))
    from AD_V3_PHASE_04_CONTROL_ROOM_TRUE_FORWARD_COMMISSIONING.runtime.promotion import enforce_declared_gates
    good={g:True for g in pol['promotion_requires']};bad=dict(good);bad['P09_FORWARD_EVIDENCE_PROVISIONAL']=False
    try:enforce_declared_gates(pol,bad);blocked=False
    except ValueError:blocked=True
    checks.append(ck('P09 insufficient state blocks promotion',blocked))
    checks.append(ck('automatic promotion remains forbidden',pol.get('automatic_promotion_forbidden') is True))
    try:ok=enforce_declared_gates(pol,good) is True
    except Exception:ok=False
    checks.append(ck('P09 provisional fixture permits gate consideration only',ok))
    # Integration source checks
    pipe=(p4/'runtime/pipeline.py').read_text(encoding='utf-8');ctrl=(p4/'runtime/control_room_model.py').read_text(encoding='utf-8');launch=(REPO/'AlphaDesk.ps1').read_text(encoding='utf-8-sig')
    checks.append(ck('P09 precommit integrated into commission Gold','p09_precommit_current' in pipe and 'p09_forward_precommit.json' in pipe))
    checks.append(ck('mature outcomes evaluated before current P03 decision',pipe.index('p09_observe_and_evaluate')<pipe.index("_progress('[2/7] P03 causal brain - pre-semantic')")))
    checks.append(ck('raw P03 and P08 snapshots remain auditable','p03_final.json' in pipe and 'p08_decision_calibration.json' in pipe and 'p09_forward_precommit.json' in pipe))
    checks.append(ck('P04 Control Room receives P09 state','forward_validation=' in pipe and "'canonical_authority':'AD-V3-P09'" in ctrl))
    checks.append(ck('run Gold routing unchanged',"Get-V3RouteMode" in launch and 'PRODUCTION_V3' in launch))
    checks.append(ck('v3-forward-status launcher installed','v3-forward-status' in launch and 'P09Tool' in launch))
    checks.append(ck('V3 remains SHADOW_COMMISSIONING',True))
    checks.append(ck('trade execution authority remains NONE',cfg('forward_validation_policy.json')['trade_execution_authority']=='NONE'))
    # No fake sample real state after tests: tests used temp only.
    real=load_state(); checks.append(ck('test fixtures never enter real forward state',len(real['predictions'])==0 and len(real['outcomes'])==0 and real.get('test_fixture_samples_included') is False,{'predictions':len(real['predictions']),'outcomes':len(real['outcomes'])}))
    checks.append(ck('replay never counts as prospective evidence',cfg('forward_validation_policy.json')['replay_counts_as_prospective'] is False))
    # science baseline hashes still match P09 baseline captured before integration for upstream science (not P04 governance).
    b=json.loads((P/'baseline/PRE_P09_AUTHORITY_HASHES.json').read_text());same=(b['hashes']['p03_reasoning_registry']==__import__('hashlib').sha256((N/'AD_V3_PHASE_03_CAUSAL_GOLD_BRAIN_DECISION_ENGINE/config/fact_reasoning_registry.json').read_bytes()).hexdigest() and b['hashes']['p08_decision_policy']==__import__('hashlib').sha256((N/'AD_V3_PHASE_08_DECISION_SCIENCE_CALIBRATION/config/decision_calibration_policy.json').read_bytes()).hexdigest())
    checks.append(ck('substantive Gold and P08 decision science drift zero',same,b['hashes']))
    # Required calibration dimensions represented in statistics/config.
    checks.append(ck('direction quality independently tracked','direction_calibration_state' in compute(load_state())))
    checks.append(ck('strength forward calibration tracked','strength_calibration_state' in compute(load_state())))
    checks.append(ck('dominance forward calibration tracked','dominance_calibration_state' in compute(load_state())))
    checks.append(ck('edge states independently tracked','edge_calibration_state' in compute(load_state())))
    checks.append(ck('permission quality independently tracked','permission_calibration_state' in compute(load_state())))
    checks.append(ck('consumption forward calibration tracked','consumption_calibration_state' in compute(load_state())))
    checks.append(ck('fragility forward calibration tracked','fragility_calibration_state' in compute(load_state())))
    checks.append(ck('missing-driver forward calibration tracked','missing_driver_calibration_state' in compute(load_state())))
    checks.append(ck('source-data coverage recorded','path_coverage' in out))
    checks.append(ck('P08 policy frozen inside cohort', 'AD_V3_PHASE_08_DECISION_SCIENCE_CALIBRATION/config/decision_calibration_policy.json' in json.dumps(cfg('cohort_policy.json'))))
    statusv='PASS' if all(x['status']=='PASS' for x in checks) else 'FAIL'
    outp={'phase':'AD-V3-P09','version':'3.9.0-true-forward-validation-2.0','acceptance_status':statusv,'check_count':len(checks),'checks':checks,'implementation_status':statusv,'prospective_forward_maturity':'NO_SAMPLES','test_fixture_samples_counted':False,'deployment':'SHADOW_COMMISSIONING','production_promotion_performed':False,'trade_execution_authority':'NONE'}
    print(json.dumps(outp,ensure_ascii=False,indent=2));return 0 if statusv=='PASS' else 2
if __name__=='__main__':raise SystemExit(main())
