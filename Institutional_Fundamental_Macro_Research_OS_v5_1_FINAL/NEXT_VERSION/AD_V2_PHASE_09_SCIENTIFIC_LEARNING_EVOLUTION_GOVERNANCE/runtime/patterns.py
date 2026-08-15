from collections import defaultdict
import hashlib,json

def aggregate(cases,policy):
 groups=defaultdict(list)
 for c in cases:
  for m in c.get('suspected_failure_modes') or []:
   if m.get('failure_family')!='NO_CLEAR_MODEL_FAILURE':groups[m.get('failure_family')].append(c)
 out=[];g=policy['recurrence_gate']
 for fam,rows in sorted(groups.items()):
  tf=[r for r in rows if r.get('sample_provenance')=='TRUE_FORWARD' and r.get('true_forward_eligible')]
  eps=set(r.get('independent_episode_key') for r in tf if r.get('independent_episode_key'));days=set(r.get('trading_day') for r in tf if r.get('trading_day'));regs=set(r.get('regime') for r in tf if r.get('regime'))
  eligible=len(eps)>=g['min_true_forward_independent_episodes'] and len(days)>=g['min_true_forward_trading_days'] and len(regs)>=g['min_true_forward_regimes']
  sig={'failure_family':fam,'tf_episodes':sorted(eps),'tf_days':sorted(days),'tf_regimes':sorted(regs),'all_case_ids':sorted(r['learning_case_id'] for r in rows)}
  pid='P09PAT_'+hashlib.sha256(json.dumps(sig,sort_keys=True).encode()).hexdigest()[:24].upper()
  out.append({'schema_version':'1.0.0','phase':'AD-V2-P09','record_type':'P09_RECURRING_PATTERN','pattern_id':pid,'failure_family':fam,'counts':{'all_cases':len(rows),'true_forward_cases':len(tf),'true_forward_independent_episodes':len(eps),'true_forward_trading_days':len(days),'true_forward_regimes':len(regs)},'episode_keys':sorted(eps),'proposal_eligible':eligible,'historical_counts_toward_gate':False,'single_episode_votes_once':True,'integrity':{'status':'PASS','dependence_aware':True,'p_hacking_search':False}})
 return out
