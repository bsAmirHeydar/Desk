#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys,tempfile
BASE=Path(__file__).resolve().parents[1];PARENT=BASE.parent;sys.path.insert(0,str(BASE));from runtime.shadow_pipeline import run
PASS=0;FAIL=0;checks=[]
def chk(n,c,d=None):
 global PASS,FAIL
 if c:PASS+=1;checks.append({'name':n,'status':'PASS'})
 else:FAIL+=1;checks.append({'name':n,'status':'FAIL','detail':d})
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo-root',required=True);ap.add_argument('--json-out');a=ap.parse_args();repo=Path(a.repo_root).resolve();pack=json.loads((BASE/'tests/fixtures/integrated_gold_shadow_input.json').read_text())
 for n in range(10):
  m=list(PARENT.glob(f'AD_V2_PHASE_{n:02d}_*/DEVELOPMENT_MANIFEST.json'));chk(f'phase_{n:02d}_manifest',len(m)==1,[str(x) for x in m])
 pol=json.loads((BASE/'config/release_candidate_policy.json').read_text());chk('mainline_override_false',pol['mainline_override'] is False);chk('permission_creation_false',pol['positive_permission_creation'] is False);chk('broker_none',pol['broker_authority']=='NONE');chk('auto_promotion_false',pol['auto_promotion'] is False);chk('auto_tuning_false',pol['auto_tuning'] is False)
 with tempfile.TemporaryDirectory(prefix='p10_val_') as td:
  td=Path(td);o=run(pack,phase_parent=PARENT,data_root=td/'data',output_dir=td/'out',persist_state=True);chk('integrated_run_pass',o.get('status')=='PASS',o);state=((o.get('p06') or {}).get('state') or {});chk('pressure_owner_preserved',((state.get('authority') or {}).get('pressure'))=='AD-V2-P02');chk('transmission_owner_preserved',((state.get('authority') or {}).get('transmission'))=='AD-V2-P03');chk('latent_owner_preserved',((state.get('authority') or {}).get('latent_release'))=='AD-V2-P04');chk('gold_owner_preserved',((state.get('authority') or {}).get('gold_specialization'))=='AD-V2-P05');chk('permission_inherited',((state.get('execution') or {}).get('permission_source'))=='V1_BASE_CAPSULE' and ((state.get('execution') or {}).get('v2_override_allowed')) is False);chk('broker_none_runtime',((state.get('execution') or {}).get('broker_authority'))=='NONE');chk('capsule_persisted',Path(((o.get('p06') or {}).get('capsule') or {}).get('path','')).is_file());chk('explorer_rendered',Path(((o.get('p06') or {}).get('explorer',''))).is_file());chk('synthetic_not_tf',not (td/'data/alpha_desk_v2/p07_validation/commitments/index.jsonl').exists())
 # price contamination attack: change only actual target response; P02 output must remain identical
 p2a=o['p02'];pack2=json.loads(json.dumps(pack));pack2['actual_response']['target']['observed_response']=0.8
 with tempfile.TemporaryDirectory(prefix='p10_val2_') as td2:
  q=run(pack2,phase_parent=PARENT,data_root=Path(td2)/'d',output_dir=Path(td2)/'o',persist_state=False);chk('price_does_not_mutate_p02',p2a.get('pressure_core')==q['p02'].get('pressure_core') and p2a.get('pressure_dynamics')==q['p02'].get('pressure_dynamics'))
 out={'schema_version':'1.0.0','phase':'AD-V2-P10','status':'PASS' if FAIL==0 else 'FAIL','passed':PASS,'failed':FAIL,'checks':checks,'deployment':'V2_RC_SHADOW_ONLY'}
 if a.json_out:Path(a.json_out).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({'phase':'AD-V2-P10','status':out['status'],'passed':PASS,'failed':FAIL},indent=2));return 0 if FAIL==0 else 1
if __name__=='__main__':raise SystemExit(main())
