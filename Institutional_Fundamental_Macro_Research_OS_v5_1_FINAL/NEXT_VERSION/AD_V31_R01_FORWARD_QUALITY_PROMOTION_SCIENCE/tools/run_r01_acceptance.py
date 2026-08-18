#!/usr/bin/env python3
from __future__ import annotations
import json,pathlib,sys,tempfile,hashlib,copy
HERE=pathlib.Path(__file__).resolve();P=HERE.parents[1];N=P.parent;REPO=N.parents[1];sys.path.insert(0,str(N));sys.path.insert(0,str(P))
from AD_V31_R01_FORWARD_QUALITY_PROMOTION_SCIENCE.runtime.common import atomic_json,load,sha_obj
from AD_V31_R01_FORWARD_QUALITY_PROMOTION_SCIENCE.runtime.qualification_engine import qualify
from AD_V31_R01_FORWARD_QUALITY_PROMOTION_SCIENCE.runtime.qualification_freeze import verify_manifest
from AD_V31_R01_FORWARD_QUALITY_PROMOTION_SCIENCE.tests.fixture_factory import make_state
from AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0.runtime.forward_ledger import path as p09_path
from AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0.runtime.forward_statistics import compute
from AD_V3_PHASE_12_FINAL_CERTIFICATION_PRODUCTION_FREEZE.runtime.gates import GATE_IDS,enforce

def ck(n,o,d=None):return {'name':n,'status':'PASS' if o else 'FAIL','detail':d}
def qcohort(fp='CURRENT'):
    cur=verify_manifest()['policy_fingerprint'];return {'record_type':'AD_V31_R01_QUALIFICATION_COHORT','qualification_cohort_id':'R01Q_TEST','state':'OPEN','started_at_utc':'2026-01-01T00:00:00Z','policy_fingerprint':cur if fp=='CURRENT' else fp,'p09_cohort_id':'COHORT_001','p09_fingerprint':'TEST','pre_r01_episodes_primary_qualification_authority':False}
def run_case(mode,n=100):
    with tempfile.TemporaryDirectory() as td:
        td=pathlib.Path(td);sr=td/'p09';qr=td/'r01';atomic_json(p09_path(sr),make_state(n,mode));atomic_json(qr/'qualification_cohort.json',qcohort());return qualify(sr,qr)
def main():
    c=[];realp=P.parent/'AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0/artifacts/state/forward_state.json';before=hashlib.sha256(realp.read_bytes()).hexdigest() if realp.exists() else None
    fr=verify_manifest();c.append(ck('qualification policy freeze valid',fr['status']=='PASS',fr.get('drift')))
    good=run_case('good',100);bad=run_case('bad_quality',100);small=run_case('good',5);cov=run_case('bad_coverage',100);sub=run_case('bad_subgroup',100)
    c.append(ck('sample maturity separate from quality',good['sample_gate'] and good['quality_gate'] and good['production_qualification_state']=='QUALIFIED',good))
    c.append(ck('large N poor quality denied',bad['sample_gate'] and bad['forward_quality_state']=='FAIL' and not bad['production_eligible'],bad))
    c.append(ck('small N perfect quality denied',not small['sample_gate'] and not small['production_eligible'],small))
    c.append(ck('good quality bad coverage denied',cov['quality_gate'] and not cov['coverage_gate'] and not cov['production_eligible'],cov))
    c.append(ck('good aggregate bad subgroup denied',sub['quality_gate'] and sub['critical_subgroup_state']=='FAIL' and not sub['production_eligible'],sub))
    c.append(ck('direction quality episode-level',good['dimensions']['direction']['state']=='PASS' and good['dimensions']['direction']['bull_n']>=12 and good['dimensions']['direction']['bear_n']>=12))
    c.append(ck('direction benchmark class-balanced',good['dimensions']['direction']['benchmark']=='CLASS_BALANCED_50_50_NULL'))
    c.append(ck('edge separation measured',good['dimensions']['edge']['state']=='PASS'))
    c.append(ck('permission quality separate',good['dimensions']['permission']['state']=='PASS'))
    c.append(ck('WAIT quality separate',good['dimensions']['wait']['state']=='PASS'))
    c.append(ck('path completeness hard gate',good['dimensions']['path_completeness']['state']=='PASS'))
    c.append(ck('strength calibration measurable',good['dimensions']['strength']['state'] in ('PASS','FAIL','INCONCLUSIVE')))
    c.append(ck('dominance calibration measurable',good['dimensions']['dominance']['state'] in ('PASS','FAIL','INCONCLUSIVE')))
    c.append(ck('consumption validity measured',good['dimensions']['consumption']['state'] in ('PASS','FAIL','INCONCLUSIVE')))
    c.append(ck('fragility validity measured',good['dimensions']['fragility']['state'] in ('PASS','FAIL','INCONCLUSIVE')))
    c.append(ck('coverage tracks bull bear event volatility root',all(k in good['coverage']['checks'] for k in ['bullish','bearish','event_exposed','event_free','volatility_regimes','root_concentration'])))
    c.append(ck('critical subgroup can override aggregate',sub['critical_subgroups']['critical_failures']!=[]))
    # Mature unevaluated must be computed, not hardcoded.
    st=make_state(5,'good');st['outcomes']=st['outcomes'][:-1];stats=compute(st,'COHORT_001',as_of='2027-01-01T00:00:00Z');c.append(ck('mature unevaluated count real',stats['mature_unevaluated_count']==1 and stats['clock_mature_episode_count']==5 and stats['evaluated_mature_episode_count']==4,stats))
    # Freeze drift/cohort invalidation without mutating source.
    with tempfile.TemporaryDirectory() as td:
        td=pathlib.Path(td);sr=td/'p09';qr=td/'r01';atomic_json(p09_path(sr),make_state(100,'good'));atomic_json(qr/'qualification_cohort.json',qcohort('BAD_FINGERPRINT'));dr=qualify(sr,qr);c.append(ck('policy drift invalidates qualification',dr.get('reason')=='R01_POLICY_FREEZE_DRIFT' and not dr.get('production_eligible'),dr))
    c.append(ck('P12 separate forward gates installed',all(x in GATE_IDS for x in ['P09_SAMPLE_MATURITY_GATE','R01_FORWARD_QUALITY_GATE','R01_COVERAGE_GATE','R01_CRITICAL_SUBGROUP_GATE'])))
    c.append(ck('legacy maturity-only gate retired','P09_FORWARD_EVIDENCE_PROVISIONAL' not in GATE_IDS))
    allgood={g:True for g in GATE_IDS};
    for gate in ['P09_SAMPLE_MATURITY_GATE','R01_FORWARD_QUALITY_GATE','R01_COVERAGE_GATE','R01_CRITICAL_SUBGROUP_GATE','EXPLICIT_OPERATOR_APPROVAL']:
        t=dict(allgood);t[gate]=False
        try:enforce(t);blocked=False
        except ValueError:blocked=True
        c.append(ck(gate+' independently blocks promotion',blocked))
    # Approval absent even all science quality gates pass.
    t=dict(allgood);t['EXPLICIT_OPERATOR_APPROVAL']=False
    try:enforce(t);blocked=False
    except ValueError:blocked=True
    c.append(ck('all quality pass without approval not promoted',blocked))
    after=hashlib.sha256(realp.read_bytes()).hexdigest() if realp.exists() else None;c.append(ck('real P09 state preserved',before==after,{'before':before,'after':after}))
    c.append(ck('fixtures and replay have no qualification authority',good.get('fixture_samples_included') is False and good.get('replay_samples_included') is False))
    ok=all(x['status']=='PASS' for x in c);out={'phase':'AD-V3.1-R01','version':'3.1.1-forward-quality','acceptance_status':'PASS' if ok else 'FAIL_CLOSED','check_count':len(c),'checks':c,'real_p09_preserved':before==after,'production_promotion_performed':False,'trade_execution_authority':'NONE'};print(json.dumps(out,ensure_ascii=False,indent=2));return 0 if ok else 2
if __name__=='__main__':raise SystemExit(main())
