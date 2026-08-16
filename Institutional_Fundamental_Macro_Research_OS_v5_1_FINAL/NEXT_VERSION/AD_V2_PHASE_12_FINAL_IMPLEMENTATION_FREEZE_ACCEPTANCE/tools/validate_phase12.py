#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE));from runtime.freeze import verify,load,v1_binding
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo-root',required=True);a=ap.parse_args();repo=Path(a.repo_root).resolve();f=verify(repo,BASE);checks=[]
 def ck(n,o,d=None):checks.append({'name':n,'status':'PASS' if o else 'FAIL','detail':d})
 ck('freeze_registry',f['status']=='PASS',f.get('failed_count'));auth=load(BASE/'config/final_authority_manifest.json');post=load(BASE/'config/post_p12_policy.json');ck('v1_authoritative',auth.get('v1_production_authoritative') is True);ck('v2_shadow',auth.get('v2_implementation')=='FROZEN_RC1_SHADOW');ck('permission_inherited',auth.get('trade_permission')=='V1_INHERITED');ck('no_broker',auth.get('broker')=='NONE');ck('no_auto_promotion',auth.get('auto_promotion') is False);ck('fixed_roadmap_closed',post.get('fixed_roadmap_closed') is True and post.get('default_next_phase') is None);ck('frontdoor_present',(repo/'AlphaDesk.ps1').is_file());
 try:ck('v1_authority_surface_git_frozen',v1_binding(repo).get('status')=='PASS' and v1_binding(repo).get('bridge_mode')=='DIRECT_V1_RUNTIME_SURFACE')
 except Exception as e:ck('v1_authority_surface_git_frozen',False,str(e))
 ck('normal_run_contract',(repo/'ALPHA_DESK_V2_RUN.md').is_file())
 # Must freeze exactly 12 phase manifests P00-P11
 ids={x['surface_id'] for x in load(BASE/'config/final_freeze_registry.json')['surfaces']};ck('p00_p11_manifests',all(f'P{i:02d}_MANIFEST' in ids for i in range(12)))
 fail=[x for x in checks if x['status']!='PASS'];print(json.dumps({'schema_version':'1.0.0','phase':'AD-V2-P12','status':'PASS' if not fail else 'FAIL','passed':len(checks)-len(fail),'failed':len(fail),'checks':checks},ensure_ascii=False,indent=2));return 0 if not fail else 2
if __name__=='__main__':raise SystemExit(main())
