#!/usr/bin/env python3
import argparse,json,pathlib,re
ap=argparse.ArgumentParser(description='Validate preservation of V11 and V10.4 state controls.')
ap.add_argument('--vault-root',required=True); a=ap.parse_args(); r=pathlib.Path(a.vault_root); e=[]
required=[
'89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/00 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine MOC.md',
'89 Fundamental Force Consumption Persistence and Asymmetry Calibration Engine/v11_fundamental_state.schema.json',
'88 Hybrid Daily Session Event Fundamental State Engine/14 Hybrid Fundamental State Schema.md',
'87 Alpha Lab Asset-Specific Persian PDF Analysis Prompts/11 Daily Fundamental Context Engine.md']
for x in required:
 if not (r/x).is_file(): e.append(f'missing {x}')
schema=r/'88 Hybrid Daily Session Event Fundamental State Engine/14 Hybrid Fundamental State Schema.md'
if schema.is_file():
 t=schema.read_text(encoding='utf-8',errors='replace')
 enums=re.findall(r'^  - ([A-Z0-9_]+)$',t,re.M)
 expected={'DAILY_BASELINE','END_OF_DAY_STATE','STATE_DECAY_UPDATE','CAUSAL_LEADER_CHANGE','NO_MATERIAL_DIRECTION_CHANGE','EVENT_T_PLUS_5','EVENT_T_PLUS_15','EVENT_T_PLUS_60'}
 if not expected.issubset(set(enums)): e.append('V10.4 record-type controls missing')
 if 'V11 backward-compatible extension' not in t: e.append('V11 backward compatibility section missing')
print(json.dumps({'status':'PASS' if not e else 'FAIL','errors':e},indent=2)); raise SystemExit(0 if not e else 1)
