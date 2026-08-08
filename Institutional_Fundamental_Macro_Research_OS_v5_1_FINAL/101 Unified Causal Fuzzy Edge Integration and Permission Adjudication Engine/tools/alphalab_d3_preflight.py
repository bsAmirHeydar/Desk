#!/usr/bin/env python3
from pathlib import Path
import argparse,json,subprocess,sys
p=argparse.ArgumentParser();p.add_argument('--vault-root',required=True);p.add_argument('--mode',choices=['runtime','deployment'],default='runtime');a=p.parse_args();r=Path(a.vault_root);e=[];checks=[]
try:m=json.loads((r/'CURRENT_PRODUCTION_MANIFEST.json').read_text())
except Exception as x:m={};e.append('MANIFEST_PARSE '+str(x))
if m.get('current_stack')!='V19.0.0':e.append('CURRENT_STACK_NOT_V19')
if m.get('fact_constitution_version')!='1.1.0':e.append('FACT_CONSTITUTION_DRIFT')
if m.get('decision_authority',{}).get('direction')!='FUNDAMENTAL_ONLY':e.append('DIRECTION_AUTHORITY_DRIFT')
d3=m.get('d3_unified_edge') or {}
if d3.get('authority_mode')!='ENFORCED_CAUSAL_MODULATION':e.append('D3_NOT_ENFORCED_CAUSAL_MODULATION')
if d3.get('direction_flip_allowed') is not False:e.append('D3_DIRECTION_FLIP_NOT_FORBIDDEN')
if d3.get('new_permission_from_pre_d3_no_trade_v19') is not False:e.append('D3_NEW_PERMISSION_GUARD_MISSING')
if (m.get('d2_market_sciences') or {}).get('authority_mode')!='CANONICAL_SHADOW':e.append('D2_SOURCE_AUTHORITY_DRIFT')
if (m.get('d2_market_sciences') or {}).get('direct_permission_effect')!='NONE':e.append('D2_DIRECT_PERMISSION_DRIFT')
for req in m.get('required_runtime_contracts',[]):
    if not (r/req).exists():e.append('MISSING_RUNTIME_CONTRACT '+req)
cmds=[
 ('manifest_sync',[r/'94 Institutional Evidence Calibration Portfolio and Model Risk Production Engine/tools/alphalab_manifest_sync.py','--vault-root',r,'--check']),
 ('d3_coverage',[r/'101 Unified Causal Fuzzy Edge Integration and Permission Adjudication Engine/tools/alphalab_d3_coverage_audit.py','--vault-root',r]),
 ('d2_regression',[r/'100 Six-Market D2 Fact Books and Production Shadow Engine/tools/alphalab_d2_preflight.py','--vault-root',r,'--mode',a.mode]),
 ('d1_regression',[r/'95 Fact Constitution and Institutional Evidence Fabric/tools/alphalab_d1_preflight.py','--vault-root',r,'--mode',a.mode]),
 ('v16_regression',[r/'94 Institutional Evidence Calibration Portfolio and Model Risk Production Engine/tools/alphalab_preflight.py','--vault-root',r,'--mode',a.mode])]
for name,args in cmds:
    q=subprocess.run([sys.executable,*map(str,args)],capture_output=True,text=True);checks.append({'name':name,'pass':q.returncode==0})
    if q.returncode:e.append(name+'_FAIL '+(q.stdout+q.stderr)[-1400:])
print(json.dumps({'status':'PASS' if not e else 'FAIL','mode':a.mode,'checks':checks,'errors':e},indent=2));sys.exit(0 if not e else 2)
