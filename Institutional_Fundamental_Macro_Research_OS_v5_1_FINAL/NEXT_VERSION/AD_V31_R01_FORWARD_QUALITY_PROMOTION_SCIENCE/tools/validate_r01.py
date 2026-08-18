#!/usr/bin/env python3
import json,pathlib,sys
P=pathlib.Path(__file__).resolve().parents[1];N=P.parent;sys.path.insert(0,str(N))
from AD_V31_R01_FORWARD_QUALITY_PROMOTION_SCIENCE.runtime.qualification_freeze import verify_manifest
from AD_V3_PHASE_12_FINAL_CERTIFICATION_PRODUCTION_FREEZE.runtime.gates import GATE_IDS

def ck(n,o,d=None):return {'name':n,'status':'PASS' if o else 'FAIL','detail':d}
def main():
 c=[];pol=json.loads((P/'config/forward_quality_policy.json').read_text());cov=json.loads((P/'config/coverage_policy.json').read_text());bench=json.loads((P/'config/benchmark_policy.json').read_text());fr=verify_manifest()
 c.append(ck('R01 policy freeze valid',fr['status']=='PASS',fr.get('drift')));c.append(ck('no single magic score',pol.get('no_single_magic_score') is True));c.append(ck('threshold optimizer forbidden',pol.get('threshold_optimizer_forbidden') is True));c.append(ck('benchmark change requires new cohort',bench.get('benchmark_change_requires_new_qualification_cohort') is True));c.append(ck('primary qualification horizon SESSION_1_6H',pol.get('primary_horizon')=='SESSION_1_6H'));c.append(ck('coverage includes bull bear event volatility root',all(k in cov['hard_requirements'] for k in ['min_bullish_episodes','min_bearish_episodes','min_event_exposed_episodes','min_volatility_regimes','max_dominant_root_share'])));c.append(ck('P12 includes separate forward gates',all(x in GATE_IDS for x in ['P09_SAMPLE_MATURITY_GATE','R01_FORWARD_QUALITY_GATE','R01_COVERAGE_GATE','R01_CRITICAL_SUBGROUP_GATE'])));c.append(ck('legacy maturity-only gate retired','P09_FORWARD_EVIDENCE_PROVISIONAL' not in GATE_IDS))
 ok=all(x['status']=='PASS' for x in c);print(json.dumps({'phase':'AD-V3.1-R01','version':'3.1.1-forward-quality','status':'PASS' if ok else 'FAIL_CLOSED','check_count':len(c),'checks':c},ensure_ascii=False,indent=2));return 0 if ok else 2
if __name__=='__main__':raise SystemExit(main())
