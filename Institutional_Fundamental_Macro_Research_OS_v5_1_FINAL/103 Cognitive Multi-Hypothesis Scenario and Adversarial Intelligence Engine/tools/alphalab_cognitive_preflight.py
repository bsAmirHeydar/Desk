#!/usr/bin/env python3
from pathlib import Path
import argparse,json,subprocess,sys
p=argparse.ArgumentParser();p.add_argument('--vault-root',required=True);p.add_argument('--mode',choices=['runtime','deployment'],default='runtime');a=p.parse_args();r=Path(a.vault_root);e=[];checks=[]
try:m=json.loads((r/'CURRENT_PRODUCTION_MANIFEST.json').read_text(encoding='utf-8'))
except Exception as x:m={};e.append('MANIFEST_PARSE '+str(x))
if m.get('current_stack')!='V21.2.0':e.append('CURRENT_STACK_NOT_V21_2')
if m.get('fact_constitution_version')!='1.1.0':e.append('FACT_CONSTITUTION_DRIFT')
if m.get('decision_authority',{}).get('direction')!='FUNDAMENTAL_ONLY':e.append('DIRECTION_AUTHORITY_DRIFT')
ch=m.get('cognitive_hardening') or {}
if ch.get('authority_mode')!='ENFORCED_COGNITIVE_HARDENING':e.append('COGNITIVE_HARDENING_NOT_ENFORCED')
if ch.get('semantic_integrity_mode')!='ENFORCED_LAST_MILE':e.append('SEMANTIC_LAST_MILE_NOT_ENFORCED')
if ch.get('direction_flip_allowed') is not False:e.append('COGNITIVE_DIRECTION_FLIP_GUARD_DRIFT')
if ch.get('positive_permission_creation') is not False:e.append('COGNITIVE_POSITIVE_PERMISSION_GUARD_DRIFT')
if ch.get('outside_strategy_edge_permission_effect')!='NONE':e.append('OUTSIDE_STRATEGY_PERMISSION_DRIFT')
if ch.get('market_price_direction_authority') is not False:e.append('PRICE_DIRECTION_AUTHORITY_DRIFT')
if ch.get('scenario_probability_mode')!='QUALITATIVE_UNLESS_D4_CALIBRATED':e.append('SCENARIO_PROBABILITY_POLICY_DRIFT')
if ch.get('final_trigger_contract')!='STRUCTURED_TRIGGER_PREDICATE':e.append('FINAL_TRIGGER_CONTRACT_DRIFT')
if (m.get('d3_unified_edge') or {}).get('authority_mode')!='ENFORCED_CAUSAL_MODULATION':e.append('D3_AUTHORITY_DRIFT')
d4=m.get('d4_forward_validation') or {}
if d4.get('authority_mode')!='GOVERNANCE_ENFORCED' or d4.get('version')!='1.2.0':e.append('D4_AUTHORITY_OR_VERSION_DRIFT')
for req in m.get('required_runtime_contracts') or []:
 if not (r/req).exists():e.append('MISSING_RUNTIME_CONTRACT '+req)
cmds=[
 ('manifest_sync',[r/'94 Institutional Evidence Calibration Portfolio and Model Risk Production Engine/tools/alphalab_manifest_sync.py','--vault-root',r,'--check']),
 ('base_production_preflight',[r/'94 Institutional Evidence Calibration Portfolio and Model Risk Production Engine/tools/alphalab_preflight.py','--vault-root',r,'--mode',a.mode]),
 ('d4_selftest',[r/'102 Forward Validation Calibration Promotion and Scientific Governance Engine/tools/alphalab_d4_selftest.py']),
 ('cognitive_selftest',[r/'103 Cognitive Multi-Hypothesis Scenario and Adversarial Intelligence Engine/tools/alphalab_cognitive_selftest.py']),
 ('cognitive_schema_audit',[r/'103 Cognitive Multi-Hypothesis Scenario and Adversarial Intelligence Engine/tools/alphalab_cognitive_schema_audit.py','--vault-root',r]),
 ('cognitive_coverage',[r/'103 Cognitive Multi-Hypothesis Scenario and Adversarial Intelligence Engine/tools/alphalab_cognitive_coverage_audit.py','--vault-root',r])]
for name,args in cmds:
 q=subprocess.run([sys.executable,*map(str,args)],capture_output=True,text=True);checks.append({'name':name,'pass':q.returncode==0})
 if q.returncode:e.append(name+'_FAIL '+(q.stdout+q.stderr)[-3000:])
print(json.dumps({'status':'PASS' if not e else 'FAIL','mode':a.mode,'checks':checks,'errors':e},indent=2,ensure_ascii=False));sys.exit(0 if not e else 2)
