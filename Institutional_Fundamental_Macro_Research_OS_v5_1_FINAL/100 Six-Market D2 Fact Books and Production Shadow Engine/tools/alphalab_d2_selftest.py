#!/usr/bin/env python3
from pathlib import Path
import json,subprocess,sys,tempfile
HERE=Path(__file__).resolve().parent;MOD=HERE.parent;V=MOD.parent;checks=[]
def chk(name,ok,detail=''):checks.append((name,bool(ok),str(detail)))
def run(args):
 q=subprocess.run([sys.executable,*map(str,args)],capture_output=True,text=True,timeout=45)
 return q.returncode,q.stdout+q.stderr
m=json.loads((V/'CURRENT_PRODUCTION_MANIFEST.json').read_text());
chk('stack_v18_to_v21',m.get('current_stack') in {'V18.0.0','V19.0.0','V20.0.0','V21.0.0','V21.1.0','V21.2.0','V21.3.0'},m.get('current_stack'))
chk('fact_constitution_1_1',m.get('fact_constitution_version')=='1.1.0',m.get('fact_constitution_version'))
chk('fundamental_only_direction',m.get('decision_authority',{}).get('direction')=='FUNDAMENTAL_ONLY',m.get('decision_authority'))
d2=m.get('d2_market_sciences') or {};chk('d2_canonical_shadow',d2.get('authority_mode')=='CANONICAL_SHADOW',d2);chk('d2_zero_direct_permission_effect', (d2.get('final_permission_effect')=='NONE' if m.get('current_stack')=='V18.0.0' else d2.get('direct_permission_effect')=='NONE'), d2);chk('d3_promotion_state_valid',d2.get('d3_promotion_state') in {'NOT_PROMOTED','PROMOTED_VIA_MODULE_101_ONLY'},d2)
ca=m.get('canonical_authorities') or {}
for k in ['positioning_ownership','actual_flow','funding_plumbing','institutional_mechanics_capacity','d2_six_market_router']:chk('authority_'+k,k in ca and (V/ca[k]).exists(),ca.get(k))
# policies encode critical non-equivalences
p96=json.loads((V/'96 Positioning Ownership and Crowding Science/config/positioning_policy.json').read_text());chk('positioning_flow_distinct','FLOW' in p96['canonical_distinctions'] and p96['rules']['open_interest_not_directional_flow'],p96)
p97=json.loads((V/'97 Actual Flow and Transaction Pressure Science/config/flow_policy.json').read_text());chk('volume_not_net_flow',p97['rules']['volume_not_net_flow'],p97);chk('aum_not_auto_flow',p97['rules']['aum_change_not_flow_without_decomposition'],p97);chk('expected_hedge_not_realized',p97['rules']['expected_hedge_not_realized_flow'],p97)
p98=json.loads((V/'98 Funding Plumbing Collateral and Balance Sheet Capacity Science/config/funding_plumbing_policy.json').read_text());chk('liquidity_decomposed',len(p98['components'])>=6 and p98['rules']['single_liquidity_scalar_forbidden_without_decomposition'],p98);chk('basis_not_spot_direction',p98['rules']['basis_not_spot_direction'],p98)
p99=json.loads((V/'99 Institutional Mechanics and Market Capacity Science/config/mechanics_capacity_policy.json').read_text());chk('mechanics_not_realized_flow',p99['rules']['mechanical_event_not_realized_flow'],p99);chk('capacity_scoped',p99['rules']['capacity_must_be_venue_size_horizon_state_specific'],p99);chk('mechanics_not_direction',p99['rules']['mechanics_not_fundamental_direction'],p99)
# 6x5 coverage and source registry
rc,o=run([HERE/'alphalab_d2_coverage_audit.py','--vault-root',V]);z=json.loads(o);chk('six_by_five_d2_coverage',rc==0 and z.get('cells')==30,o)
rc,o=run([HERE/'alphalab_d2_source_audit.py','--vault-root',V]);z=json.loads(o);chk('source_registry_audited',rc==0 and z.get('rule')=='REGISTRATION_DOES_NOT_IMPLY_LIVE_AVAILABILITY',o)
rc,o=run([HERE/'alphalab_observability_audit.py','--vault-root',V]);z=json.loads(o);chk('observability_16x6_audited',rc==0 and z.get('families')==16 and z.get('cells')==96,o)
# six market books
books={'XAUUSD':20,'NASDAQ100':21,'SP500':22,'DJIA':23,'EURUSD':24,'USDJPY':25};chk('six_market_books',all((MOD/f'{n:02d} {mk} D2 Fact Book.md').exists() for mk,n in books.items()),books)
# D1 registry transition remains no decision authority
reg=json.loads((V/'95 Fact Constitution and Institutional Evidence Fabric/config/fact_family_registry.json').read_text());d2f=[x for x in reg['families'] if x.get('d2_role')=='CANONICAL_SHADOW_STATE'];chk('five_d2_families_canonical_shadow',len(d2f)==5 and all(x.get('new_decision_authority') is False for x in d2f),d2f)
cov=json.loads((V/'95 Fact Constitution and Institutional Evidence Fabric/config/six_market_fact_coverage.json').read_text());chk('d1_six_by_ten_preserved',sum(len(x) for x in cov['coverage'].values())==60,cov.get('version'))
# simple state validators
with tempfile.TemporaryDirectory() as td0:
 td=Path(td0)
 samples=[
  ('p.json',V/'96 Positioning Ownership and Crowding Science/tools/alphalab_positioning_validate.py',{'instrument':'NASDAQ100','as_of_utc':'2026-08-08T00:00:00Z','authority_mode':'CANONICAL_SHADOW','coverage_state':'PARTIAL_PUBLIC','crowding_state':'BALANCED','fragility_state':'MODERATE','evidence_ids':[],'permission_effect_v18':'NONE'}),
  ('f.json',V/'97 Actual Flow and Transaction Pressure Science/tools/alphalab_flow_validate.py',{'instrument':'NASDAQ100','as_of_utc':'2026-08-08T00:00:00Z','authority_mode':'CANONICAL_SHADOW','coverage_state':'PARTIAL_PUBLIC','persistence':'UNKNOWN','absorption':'UNKNOWN','evidence_ids':[],'permission_effect_v18':'NONE'}),
  ('u.json',V/'98 Funding Plumbing Collateral and Balance Sheet Capacity Science/tools/alphalab_funding_validate.py',{'instrument':'NASDAQ100','as_of_utc':'2026-08-08T00:00:00Z','authority_mode':'CANONICAL_SHADOW','coverage_state':'PARTIAL_PUBLIC','stress_state':'NORMAL','evidence_ids':[],'permission_effect_v18':'NONE'}),
  ('c.json',V/'99 Institutional Mechanics and Market Capacity Science/tools/alphalab_mechanics_capacity_validate.py',{'instrument':'NASDAQ100','as_of_utc':'2026-08-08T00:00:00Z','authority_mode':'CANONICAL_SHADOW','coverage_state':'PARTIAL_PUBLIC','capacity_grade':'NORMAL','stress_capacity_grade':'LOW','evidence_ids':[],'permission_effect_v18':'NONE'})]
 for fn,tool,obj in samples:
  q=td/fn;q.write_text(json.dumps(obj));rc,o=run([tool,'--state',q]);chk('validator_'+fn,rc==0,o)
 pack={'version':'1.0.0','authority_mode':'CANONICAL_SHADOW','instrument':'NASDAQ100','analysis_cutoff_utc':'2026-08-08T00:00:00Z','positioning':{},'actual_flow':{},'funding_plumbing':{},'institutional_mechanics':{},'market_capacity':{},'cross_science_independent_roots':0,'missing_or_licensed_required':[],'d2_permission_effect':'NONE','d3_promotion_state':'PROMOTED_VIA_MODULE_101_ONLY' if m.get('current_stack') in {'V19.0.0','V20.0.0','V21.0.0','V21.1.0','V21.2.0','V21.3.0'} else 'NOT_PROMOTED'}
 q=td/'pack.json';q.write_text(json.dumps(pack));rc,o=run([HERE/'alphalab_d2_validate_pack.py','--pack',q]);chk('d2_pack_validator',rc==0,o)
 bad=dict(pack);bad['d2_permission_effect']='BUY';q.write_text(json.dumps(bad));rc,o=run([HERE/'alphalab_d2_validate_pack.py','--pack',q]);chk('premature_permission_rejected',rc!=0 and 'PREMATURE_D2_PERMISSION' in o,o)
# V21.3 observability receipt behavioral tests: baseline materiality is mandatory; runtime materiality is flexible but receipted.
with tempfile.TemporaryDirectory() as td1:
 td=Path(td1); horizon='SESSION_1_6H'; inst='NASDAQ100'
 mp=json.loads((MOD/'config/six_market_observability_map.json').read_text()); cells=mp['markets'][inst]
 items=[]
 for fid,c in cells.items():
  if c['materiality']=='NOT_MATERIAL' or horizon not in c.get('active_horizons',[]): continue
  items.append({'family_id':fid,'baseline_materiality':c['materiality'],'runtime_materiality':c['materiality'],'materiality_reason':'baseline retained for self-test','coverage_state':'UNDETERMINED','evidence_class':'NONE','freshness_state':'UNDETERMINED','access_state':'UNDETERMINED','admitted_source_ids':[],'current_state_eligible':False,'known_private_gap':bool(c.get('known_private_gap')),'reason':'self-test explicit unknown; no silent gap'})
 receipt={'version':'1.0.0','instrument':inst,'analysis_cutoff_utc':'2026-08-08T12:00:00Z','active_horizon':horizon,'items':items,'critical_gaps':[],'silent_gap_count':0,'permission_authority':'NONE_NEW'}
 q=td/'obs.json'; q.write_text(json.dumps(receipt));rc,o=run([HERE/'alphalab_observability_validate.py','--vault-root',V,'--receipt',q]);chk('observability_receipt_full_unknown_pass',rc==0,o)
 bad=json.loads(json.dumps(receipt)); bad['items']=bad['items'][1:]; q.write_text(json.dumps(bad));rc,o=run([HERE/'alphalab_observability_validate.py','--vault-root',V,'--receipt',q]);chk('observability_missing_material_family_rejected',rc!=0 and 'MISSING_BASELINE_MATERIAL_FAMILY_' in o,o)
 flex=json.loads(json.dumps(receipt)); flex['items'][0]['runtime_materiality']='NOT_MATERIAL';flex['items'][0]['coverage_state']='NOT_MATERIAL';flex['items'][0]['materiality_reason']='run-specific causal routing established this family is not material at the decision cutoff';q.write_text(json.dumps(flex));rc,o=run([HERE/'alphalab_observability_validate.py','--vault-root',V,'--receipt',q]);chk('observability_contextual_materiality_flexible',rc==0,o)
 no_reason=json.loads(json.dumps(flex)); no_reason['items'][0]['materiality_reason']='';q.write_text(json.dumps(no_reason));rc,o=run([HERE/'alphalab_observability_validate.py','--vault-root',V,'--receipt',q]);chk('observability_materiality_change_requires_reason',rc!=0 and ('RUNTIME_MATERIALITY_CHANGE_WITHOUT_REASON' in o or 'SCHEMA:' in o),o)
 pack11={'version':'1.1.0','authority_mode':'CANONICAL_SHADOW','instrument':inst,'analysis_cutoff_utc':'2026-08-08T12:00:00Z','positioning':{},'actual_flow':{},'funding_plumbing':{},'institutional_mechanics':{},'market_capacity':{},'cross_science_independent_roots':0,'missing_or_licensed_required':[],'d2_permission_effect':'NONE','d3_promotion_state':'PROMOTED_VIA_MODULE_101_ONLY','observability_receipt':receipt}
 q.write_text(json.dumps(pack11));rc,o=run([HERE/'alphalab_d2_validate_pack.py','--pack',q,'--vault-root',V]);chk('d2_pack_v11_observability_integrated',rc==0,o)

# Regression self-tests and deployment/runtime preflights are executed independently by VERIFY_PATCH.py.
passed=sum(ok for _,ok,_ in checks);failed=[{'name':n,'detail':d[-1500:]} for n,ok,d in checks if not ok]
print(json.dumps({'status':'PASS' if not failed else 'FAIL','passed':passed,'total':len(checks),'failed':failed},indent=2));sys.exit(0 if not failed else 2)
