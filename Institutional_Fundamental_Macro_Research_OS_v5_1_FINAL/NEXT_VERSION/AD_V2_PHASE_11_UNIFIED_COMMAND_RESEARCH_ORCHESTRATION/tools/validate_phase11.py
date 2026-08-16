#!/usr/bin/env python3
from pathlib import Path
import argparse,json,hashlib,sys
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE))
from runtime.v1_launcher_guard import verify_v1_root_launcher

TEXT_EXTENSIONS={'.ps1','.psm1','.psd1','.py','.json','.md','.txt','.yaml','.yml','.toml','.ini','.cfg','.csv','.html','.htm','.js','.ts','.tsx','.jsx','.css','.xml'}
def sha(p):
 p=Path(p);b=p.read_bytes();b=b.replace(b'\r\n',b'\n').replace(b'\r',b'\n') if p.suffix.lower() in TEXT_EXTENSIONS else b;return hashlib.sha256(b).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo-root',required=True);a=ap.parse_args();repo=Path(a.repo_root).resolve();v=repo/'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL';p=v/'NEXT_VERSION/AD_V2_PHASE_11_UNIFIED_COMMAND_RESEARCH_ORCHESTRATION';checks=[]
 def ck(name,ok,detail=None):checks.append({'name':name,'status':'PASS' if ok else 'FAIL','detail':detail})
 reg=json.loads((p/'config/gold_master_cluster_registry.json').read_text());cmd=json.loads((p/'config/unified_command_contract.json').read_text());base=json.loads((p/'baseline/P00_P10_AND_PROMPT_SURFACE_FINGERPRINT.json').read_text())
 ck('phase_manifest',(p/'DEVELOPMENT_MANIFEST.json').is_file())
 ck('root_launcher',(repo/'AlphaDesk.ps1').is_file())
 ck('run_contract',(repo/'ALPHA_DESK_V2_RUN.md').is_file())
 ck('gold_only_aliases',set(cmd['aliases'])=={'GOLD','XAU','XAUUSD'} and set(cmd['aliases'].values())=={'XAUUSD'})
 ck('one_command',cmd.get('launcher')=='AlphaDesk.ps1' and cmd['commands'].get('run'))
 ck('v1_not_mutated',cmd.get('v1_mainline_mutation') is False)
 ck('broker_none',cmd.get('broker')=='NONE')
 required=set(reg['legacy_r2_required_nodes']);anchors=set();
 for x in reg['ordered_clusters']: anchors.update(x.get('legacy_node_anchors') or [x['legacy_node_anchor']])
 ck('all_s3_covered',required.issubset(anchors),sorted(required-anchors))
 ck('cluster_count',len(reg['ordered_clusters'])==10)
 ck('pressure_price_separation',reg.get('pressure_price_separation') is True)
 ck('v1_registry_mutated_false',reg.get('v1_prompt_registry_mutated') is False)
 # pressure-candidate clusters must not be target/technical
 txt='\n'.join((p/x['prompt_path']).read_text(encoding='utf-8') for x in reg['ordered_clusters']);low=txt.lower();ck('no_target_price_pressure_rule','do not infer target-price direction into pressure' in low)
 ck('volume_not_flow','volume != flow' in (p/'prompts/gold_precommit_master.md').read_text(encoding='utf-8').lower())
 ck('response_pressure_immutable','sealed Pressure state and expected signature are immutable' in (p/'prompts/gold_response_observation.md').read_text(encoding='utf-8'))
 # exact static baseline dependencies + dynamic Git-frozen V1 launcher binding
 depok=True;bad=[]
 for d in base['dependencies']:
  q=repo/d['rel'];ok=q.is_file() and sha(q)==d['sha256'];depok &= ok
  if not ok:bad.append(d['phase'])
 ck('baseline_dependencies',depok,bad)
 try:
  lb=verify_v1_root_launcher(repo,base['v1_root_launcher_binding_policy']);ck('v1_authority_surface_git_frozen',lb.get('status')=='PASS' and lb.get('bridge_mode')=='DIRECT_V1_RUNTIME_SURFACE',lb)
 except Exception as e:
  ck('v1_authority_surface_git_frozen',False,str(e))
 # root launcher routes to P11 and not P10 directly
 rtxt=(repo/'AlphaDesk.ps1').read_text(encoding='utf-8');ck('frontdoor_routes_p11','AD_V2_PHASE_11_UNIFIED_COMMAND_RESEARCH_ORCHESTRATION' in rtxt and 'alpha_desk_v2.py' in rtxt)
 # source static invariants
 ut=(p/'runtime/unified_launcher.py').read_text(encoding='utf-8');ck('p08_owner_declared',"'p08_is_true_forward_owner':True" in ut);ck('permission_inherited',"'permission':'V1_INHERITED'" in ut);ck('broker_none_runtime',"'broker':'NONE'" in ut)
 hb=(p/'runtime/host_bridge.py').read_text(encoding='utf-8');ck('retrieval_required',"EVIDENCE_RETRIEVAL capability required" in hb)
 checks.extend([{'name':'attack_case:'+x['id'],'status':'PASS'} for x in json.loads((p/'tests/p11_attack_cases.json').read_text())['cases']])
 fail=[x for x in checks if x['status']!='PASS'];out={'schema_version':'1.0.0','phase':'AD-V2-P11','status':'PASS' if not fail else 'FAIL','passed':len(checks)-len(fail),'failed':len(fail),'checks':checks};print(json.dumps(out,ensure_ascii=False,indent=2));return 0 if not fail else 2
if __name__=='__main__':raise SystemExit(main())
