#!/usr/bin/env python3
from pathlib import Path
import json,tempfile,sys,hashlib
PH=Path(__file__).resolve().parent.parent;PP=PH.parent
for p in (str(PH),str(PP)):
 if p not in sys.path:sys.path.insert(0,p)
from runtime.taxonomy import build_case
from runtime.patterns import aggregate
from runtime.hypotheses import build as build_hyp
from runtime.challengers import create as create_ch,ChallengerError
from runtime.experiments import create as create_exp,eligible_link
from runtime.operations import learn_from_links,status

def ok(name,cond,checks):checks.append({'name':name,'status':'PASS' if cond else 'FAIL'})
def main():
 checks=[];pol=json.loads((PH/'config/learning_policy.json').read_text());tax=json.loads((PH/'config/failure_taxonomy.json').read_text());cp=json.loads((PH/'config/challenger_policy.json').read_text());ep=json.loads((PH/'config/experiment_policy.json').read_text());links=json.loads((PH/'tests/fixtures/learning_outcomes.json').read_text())
 c=build_case(links[1],pol,'2026-08-15T00:00:00Z');fams={x['failure_family'] for x in c['suspected_failure_modes']}
 ok('learning_case_hash',str(c['learning_case_hash']).startswith('sha256:'),checks);ok('release_false_positive_detected','RELEASE_FALSE_POSITIVE' in fams,checks);ok('attribution_hypothesis_only',all(x['status']=='HYPOTHESIS_ONLY' for x in c['suspected_failure_modes']),checks);ok('authority_none',c['authority']['science_mutation']=='NONE' and c['authority']['broker']=='NONE',checks)
 # one development 12R cannot propose
 dcase=build_case(links[0],pol,'2026-08-15T00:00:00Z');p1=aggregate([dcase],pol);ok('single_dev_no_pattern_proposal',not any(x['proposal_eligible'] for x in p1),checks)
 cases=[build_case(x,pol,'2026-08-15T00:00:00Z') for x in links[1:]];pats=aggregate(cases,pol);rel=[x for x in pats if x['failure_family']=='RELEASE_FALSE_POSITIVE'];ok('recurring_release_pattern_exists',bool(rel),checks);ok('recurrence_gate_eligible',bool(rel and rel[0]['proposal_eligible']),checks);ok('recurrence_episodes_5',rel[0]['counts']['true_forward_independent_episodes']==5,checks);ok('recurrence_days_3',rel[0]['counts']['true_forward_trading_days']>=3,checks);ok('recurrence_regimes_2',rel[0]['counts']['true_forward_regimes']>=2,checks)
 h=build_hyp(rel[0],tax,'2026-08-15T01:00:00Z');ok('hypothesis_created',h and h['candidate_family']=='RELEASE_RULE_REVIEW',checks);ok('hypothesis_no_auto_apply',h['authority']['auto_apply'] is False,checks);ok('generation_episode_reuse_forbidden',h['validation_episode_reuse_forbidden'] is True,checks)
 spec={'question':'tighten independent confirmation requirement','parameter_family':'release_independent_support','auto_apply':False,'upstream_write':False,'permission_change':False,'broker_write':False};ch=create_ch(h,spec,cp,'2026-08-15T02:00:00Z');ok('challenger_shadow_only',ch['status']=='SHADOW_PROPOSAL_ONLY',checks);ok('challenger_authority_none',not ch['authority']['auto_apply'] and ch['authority']['broker']=='NONE',checks)
 for badtoken in ['target_price_to_pressure','auto_permission','future_data_fit','disable_independence','confirm_liquidity_from_price']:
  try:create_ch(h,{'note':badtoken},cp,'2026-08-15T02:00:00Z');blocked=False
  except ChallengerError:blocked=True
  ok('block_'+badtoken,blocked,checks)
 ex=create_exp(ch,ep,'2026-08-15T03:00:00Z');ok('experiment_excludes_generation',set(ex['excluded_generation_episode_keys'])==set(h['generation_episode_keys']),checks);ok('experiment_future_only',ex['validation_policy']['validation_must_be_post_experiment_seal'] is True,checks)
 post=dict(links[-1]);post['independent_episode_key']='NEW-EP';post['joined_at_utc']='2026-08-16T00:00:00Z';ok('postseal_new_episode_eligible',eligible_link(ex,post),checks);same=dict(post);same['independent_episode_key']=h['generation_episode_keys'][0];ok('generation_episode_not_eligible',not eligible_link(ex,same),checks);pre=dict(post);pre['joined_at_utc']='2026-08-14T00:00:00Z';ok('preseal_not_eligible',not eligible_link(ex,pre),checks)
 with tempfile.TemporaryDirectory() as td:
  r=learn_from_links(td,PH,links,'2026-08-15T04:00:00Z');s=status(td);ok('learning_cycle_cases',r['total_cases']==6,checks);ok('learning_hypothesis_created',len(r['new_hypotheses'])>=1,checks);ok('status_pass',s['status']=='PASS',checks);ok('queue_exists',len(r['queue']['items'])>0,checks);ok('no_upstream_write',s['authority']['auto_mutation'] is False,checks)
 # static controls
 ok('policy_single_case_false',pol['single_case_can_change_model'] is False,checks);ok('historical_gate_false',pol['historical_can_satisfy_tf_gate'] is False,checks);ok('challenger_upstream_write_false',cp['upstream_write'] is False,checks);ok('experiment_reuse_false',ep['reuse_generation_episodes_for_validation'] is False,checks);ok('experiment_auto_promote_false',ep['auto_promote_challenger'] is False,checks)
 for fn in ['P09_LEARNING_CASE','P09_RECURRING_PATTERN','P09_RESEARCH_HYPOTHESIS','P09_SHADOW_CHALLENGER','P09_CHALLENGER_EXPERIMENT']:
  ok('record_contract_'+fn,fn in ''.join(x.read_text(encoding='utf-8') for x in (PH/'runtime').glob('*.py')),checks)
 # phase boundary scan
 raw='\n'.join(x.read_text(encoding='utf-8',errors='ignore') for x in PH.rglob('*') if x.is_file() and x.name!='validate_phase09.py')
 ok('no_auto_permission_contract',pol['authority']['trade_permission']=='V1_INHERITED' and pol['auto_mutation'] is False,checks);ok('broker_none_declared',pol['authority']['broker']=='NONE',checks)
 fail=[x for x in checks if x['status']!='PASS'];out={'schema_version':'1.0.0','phase':'AD-V2-P09','status':'PASS' if not fail else 'FAIL','passed':len(checks)-len(fail),'failed':len(fail),'checks':checks};print(json.dumps(out,ensure_ascii=False,indent=2));return 0 if not fail else 1
if __name__=='__main__':raise SystemExit(main())
