#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,pathlib,subprocess,sys,tempfile
from _v12_common import load_json,all_errors,link_report

def run(cmd):
 p=subprocess.run(cmd,capture_output=True,text=True)
 try: data=json.loads(p.stdout) if p.stdout.strip() else {'status':'FAIL','errors':['no JSON output']}
 except Exception: data={'status':'FAIL','errors':[p.stdout,p.stderr]}
 data['returncode']=p.returncode
 return data

ap=argparse.ArgumentParser(description='Run the complete offline Alpha Lab V12 validation suite.')
ap.add_argument('--vault-root',required=True); ap.add_argument('--patch-root',required=True); ap.add_argument('--baseline-link-report',required=True); ap.add_argument('--output',required=True)
a=ap.parse_args(); root=pathlib.Path(a.vault_root); patch=pathlib.Path(a.patch_root); module=root/'90 Market Narrative Intelligence Engine'; checks={};
valid=sorted((module/'examples').glob('example_*.json')); invalid=sorted((module/'examples').glob('invalid_*.json'))
ve=[]
for p in valid:
 e=all_errors(load_json(p),p.name=='example_multi_market_daily.json')
 if e: ve.append({'file':p.name,'errors':e})
checks['valid_examples']={'status':'PASS' if not ve else 'FAIL','errors':ve,'count':len(valid)}
# Each negative fixture must be rejected by the aggregate semantic validator.
miss=[]
for p in invalid:
 if not all_errors(load_json(p)): miss.append(p.name)
checks['invalid_fixtures_rejected']={'status':'PASS' if not miss else 'FAIL','errors':[f'fixture unexpectedly passed: {x}' for x in miss],'count':len(invalid)}
bench=list((module/'benchmarks').glob('B*.json')); be=[]
for p in bench:
 d=load_json(p)
 for k in ['benchmark_id','frozen_cutoff_utc','allowed_evidence','prohibited_future_information','expected_state','required_rival_models','confidence_caps','pass_criteria']:
  if k not in d: be.append(f'{p.name} missing {k}')
checks['benchmarks']={'status':'PASS' if len(bench)>=30 and not be else 'FAIL','errors':be+([] if len(bench)>=30 else ['fewer than 30 benchmarks']),'count':len(bench)}
py=sys.executable
checks['v11_regression']=run([py,str(module/'tools/validate_v11_regression_preservation.py'),'--vault-root',str(root)])
checks['vault_integrity']=run([py,str(module/'tools/validate_vault_links_frontmatter_and_precedence.py'),'--vault-root',str(root),'--baseline-link-report',a.baseline_link_report,'--patch-manifest',str(patch/'PATCH_MANIFEST.json')])
checks['patch_manifest']=run([py,str(module/'tools/validate_patch_manifest.py'),'--patch-root',str(patch)])
# Daily prompt content gate.
prompt=module/'41 Alpha Lab V12 Daily Fundamental and Narrative Analysis Prompt.md'; pe=[]
if not prompt.is_file(): pe.append('daily prompt missing')
else:
 t=prompt.read_text(encoding='utf-8',errors='replace')
 for token in ['Phase A','Phase B','Phase C','Phase D','Phase E','Phase F','Executive Market Map','Market Attention Map','Competing Narrative Matrix','Machine-Readable V12 State Record']:
  if token not in t: pe.append(f'daily prompt missing {token}')
checks['daily_prompt']={'status':'PASS' if not pe else 'FAIL','errors':pe}
status='PASS' if all(v.get('status')=='PASS' and v.get('returncode',0)==0 for v in checks.values()) else 'FAIL'
out={'status':status,'checks':checks,'certification_boundary':['internal architecture and deterministic QA only','no empirical attention-share certification','no proprietary adoption or flow claims']}
pathlib.Path(a.output).write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8'); print(json.dumps(out,indent=2)); raise SystemExit(0 if status=='PASS' else 1)
