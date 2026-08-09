#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys
p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--hypothesis-ids',nargs='*',default=[]);p.add_argument('--pre-permission');p.add_argument('--d4-ledger');a=p.parse_args();x=json.loads(Path(a.input).read_text(encoding='utf-8'));e=[];sc=x.get('scenarios') or [];ids=[s.get('scenario_id') for s in sc];idset=set(ids);hids=set(a.hypothesis_ids)
if not (1<=len(sc)<=6):e.append('scenario count must be 1..6 materially distinct paths')
if len(ids)!=len(idset):e.append('duplicate scenario ids')
if len(sc)==1 and not x.get('single_scenario_justification'):e.append('single scenario requires justification')
prim=[s for s in sc if s.get('plausibility_band')=='PRIMARY']
if x.get('tree_state')=='PRIMARY_SCENARIO_IDENTIFIED' and len(prim)!=1:e.append('PRIMARY_SCENARIO_IDENTIFIED requires exactly one PRIMARY')
for s in sc:
 if hids:
  for h in s.get('source_hypothesis_ids') or []:
   if h not in hids:e.append(f"{s.get('scenario_id')}: unknown hypothesis {h}")
 for t in s.get('transition_paths') or []:
  if t.get('to_scenario_id') not in idset:e.append(f"{s.get('scenario_id')}: transition target missing {t.get('to_scenario_id')}")
 if a.pre_permission=='BUY' and s.get('permission_implication')=='SUPPORT_EXISTING' and s.get('direction') not in {'BULLISH','STRONGLY_BULLISH'}:e.append(f"{s.get('scenario_id')}: bearish/nonbullish path cannot SUPPORT_EXISTING BUY")
 if a.pre_permission=='SELL' and s.get('permission_implication')=='SUPPORT_EXISTING' and s.get('direction') not in {'BEARISH','STRONGLY_BEARISH'}:e.append(f"{s.get('scenario_id')}: bullish/nonbearish path cannot SUPPORT_EXISTING SELL")
 if a.pre_permission=='NO_TRADE' and s.get('permission_implication')=='SUPPORT_EXISTING':e.append(f"{s.get('scenario_id')}: NO_TRADE has no existing directional permission to support")
mode=x.get('probability_mode');probs=[s.get('calibrated_probability') for s in sc if s.get('calibrated_probability') is not None]
if mode=='QUALITATIVE' and probs:e.append('qualitative scenarios cannot contain numeric probabilities')
if mode=='CALIBRATED':
 cid=x.get('calibration_record_id')
 if not cid:e.append('calibrated mode requires calibration_record_id')
 if not x.get('calibration_reference_class_id'):e.append('calibrated mode requires calibration_reference_class_id')
 if len(probs)!=len(sc):e.append('calibrated mode requires probability for every scenario')
 elif abs(sum(map(float,probs))-1)>0.01:e.append('calibrated probabilities must sum to 1')
 if not a.d4_ledger:e.append('calibrated mode requires D4 ledger for referential validation')
 else:
  found=False
  q=Path(a.d4_ledger)
  if q.exists():
   for line in q.read_text(encoding='utf-8').splitlines():
    if not line.strip():continue
    try:o=json.loads(line)
    except:continue
    pay=o.get('payload') or {}
    if o.get('record_id')==cid or pay.get('calibration_id')==cid:found=True;break
  if not found:e.append('calibration_record_id not found in D4 ledger')
print(json.dumps({'status':'PASS' if not e else 'FAIL','scenario_count':len(sc),'errors':e},indent=2));sys.exit(0 if not e else 2)
