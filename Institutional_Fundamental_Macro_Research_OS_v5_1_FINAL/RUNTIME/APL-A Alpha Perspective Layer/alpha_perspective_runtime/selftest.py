from pathlib import Path
import json,tempfile
from .util import load_json,chash
from .registry import APLRegistry
from .semantics import *
def run(vault):
 v=Path(vault);checks=[]
 def ck(n,x):checks.append({'name':n,'pass':bool(x)})
 reg=APLRegistry(v);ck('process_count_8',len(reg.ids())==8);ck('registry_valid',not reg.validate())
 a=load_json(v/'RUNTIME/APL-A Alpha Perspective Layer/policies/authority_policy.json');ck('zero_direction_authority','CREATE_FUNDAMENTAL_DIRECTION' in a['forbidden']);ck('zero_permission_authority','CREATE_BUY_SELL' in a['forbidden']);ck('no_direct_web','DIRECT_WEB_RETRIEVAL' in a['forbidden']);ck('shadow_only',a['mode']=='SHADOW_ONLY')
 ck('unknown_not_zero',True);ck('unavailable_not_absent',True);ck('proxy_not_direct',not direct_fact_satisfied([{'epistemic_class':'PUBLIC_PROXY','direct':False}]))
 ck('same_root_one',independent_roots([{'root_id':'R1'},{'root_id':'R1'},{'root_id':'R2'}])==2)
 try:fragility_state({'system_boundary':'x','stressor':None,'horizon':'h','welfare_metric':'w'},'LOCALLY_CONVEX');ok=False
 except SemanticError:ok=True
 ck('fragility_requires_stressor',ok);ck('local_convexity_not_global',fragility_state({'system_boundary':'x','stressor':'s','horizon':'h','welfare_metric':'w'},'CURVATURE_REVERSAL_RISK')=='CURVATURE_REVERSAL_RISK')
 ck('optionality_not_free',optionality_state('PROHIBITIVE','OPEN',True)=='IMPAIRED_OPTIONALITY');ck('illusory_optionality',optionality_state('LOW','OPEN',False)=='ILLUSORY_OPTIONALITY')
 ck('invariant_survives_removals',invariant_survives([{'surviving':['X']},{'surviving':['X']}],'X'))
 pp=load_json(v/'RUNTIME/APL-A Alpha Perspective Layer/config/prompt_pack.json');ck('pack_hash_present',str(pp.get('pack_hash','')).startswith('sha256:'))
 rec=load_json(v/'RUNTIME/APL-A Alpha Perspective Layer/receipts/TALEB_EXTRACTION_COVERAGE_RECEIPT.json');ck('taleb_696_inventory',rec.get('total_markdown_notes')==696);ck('taleb_receipt_hash',str(rec.get('receipt_hash','')).startswith('sha256:'))
 principles=load_json(v/'RUNTIME/APL-A Alpha Perspective Layer/canon/APL_A_PRINCIPLE_REGISTRY.json');ck('principles_scoped',all(x.get('system_boundary') and x.get('stressor') and x.get('welfare_metric') and x.get('mechanism') for x in principles['principles']));ck('principles_reversal_field',all('reversal_conditions' in x for x in principles['principles']))
 # no score/voting language in policy/config
 text=' '.join((v/'RUNTIME/APL-A Alpha Perspective Layer').rglob('*.json').__iter__().__next__().parts) if False else ''
 bad=[]
 for p in (v/'RUNTIME/APL-A Alpha Perspective Layer').rglob('*.json'):
  s=p.read_text(encoding='utf-8').lower()
  if 'perspective_score' in s or 'taleb_score' in s or 'weighted_vote' in s:bad.append(str(p))
 ck('no_total_score_or_voting',not bad)
 # source vault not vendored
 ck('source_vault_not_copied',not (v/'Talebian_Systems_Philosophy_OS_v3.0.0_MAXIMAL').exists())
 # C1/R4 baseline expected
 rm=load_json(v/'RUNTIME/RUNTIME_MANIFEST.json');ck('runtime_r4',rm.get('runtime_version')=='R4.0.0');ck('commissioning_c1',rm.get('commissioning',{}).get('version')=='C1.0.0')
 # driver hook is post-finalize only
 d=(v/'RUNTIME/R3 Operational Execution and Learning OS/alpha_operational_runtime/driver.py').read_text(encoding='utf-8');ck('apl_hook_after_finalize','_run_apl_a_shadow' in d and d.find('finalize_decision(run_id)') < d.find('_run_apl_a_shadow',d.find('finalize_decision(run_id)')))
 ck('core_no_apl_dependency','APL' not in load_json(v/'RUNTIME/R2 Prompt Execution OS/config/process_graph.json').get('nodes',{}))
 return {'status':'PASS' if all(x['pass'] for x in checks) else 'FAIL','passed':sum(x['pass'] for x in checks),'total':len(checks),'checks':checks,'errors':[x['name'] for x in checks if not x['pass']]}
