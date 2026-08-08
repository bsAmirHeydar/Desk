#!/usr/bin/env python3
import argparse,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--output',required=True);a=p.parse_args()
x=json.loads(Path(a.input).read_text(encoding='utf-8'))
required=['version','instrument','analysis_cutoff_utc','fundamental_direction','pre_d3_research_edge','pre_d3_permission','integration_vectors']
missing=[k for k in required if k not in x]
if missing: raise SystemExit('MISSING_REQUIRED: '+','.join(missing))
if x.get('version') not in {'1.0.0','1.1.0'}: raise SystemExit('BAD_VERSION')
pre=x['pre_d3_permission']; direction=x['fundamental_direction']; vectors=x.get('integration_vectors') or []
severity={'UNKNOWN':0,'NONE':1,'SUPPORT':2,'FRICTION':3,'DELAY':4,'TRANSMISSION_BREAK':5,'EXECUTION_BLOCK':6}
mat={'CONTEXTUAL':0,'SUPPORTING':1,'MATERIAL':2,'DECISION_CRITICAL':3}
direct_grades={'DIRECT_IDENTIFIED','OFFICIAL_OR_EXCHANGE','DERIVED_WITH_LINEAGE'}
# Group by root; preserve every material channel. Independence count is per root, never per descendant.
groups={}
for i,v in enumerate(vectors):
    rid=str(v.get('root_id') or '').strip()
    if not rid: raise SystemExit('EMPTY_ROOT_ID')
    vv=dict(v);vv.setdefault('channel_id',str(v.get('channel_id') or f'{rid}:C{i+1}'))
    groups.setdefault(rid,[]).append(vv)
root_map=[];contested=[]
for rid,vs in sorted(groups.items()):
    material=[v for v in vs if mat.get(v.get('materiality'),0)>=2]
    supportive=[v for v in material if v.get('alignment_to_fundamental')=='SUPPORTIVE' and v.get('obstruction_class') in {'NONE','SUPPORT'}]
    opposing=[v for v in material if v.get('alignment_to_fundamental') in {'OPPOSING','MIXED'} or v.get('obstruction_class') in {'FRICTION','DELAY','TRANSMISSION_BREAK','EXECUTION_BLOCK','UNKNOWN'}]
    if supportive and opposing:net='CONTESTED';contested.append(rid)
    elif any(v.get('obstruction_class') in {'FRICTION','DELAY','TRANSMISSION_BREAK','EXECUTION_BLOCK'} for v in material):net='OBSTRUCTIVE'
    elif supportive:net='SUPPORTIVE'
    elif any(v.get('obstruction_class')=='UNKNOWN' for v in material):net='UNKNOWN'
    else:net='NON_DIRECTIONAL'
    root_map.append({'root_id':rid,'independent_root_count':1,'net_root_state':net,'channels':vs,'material_channel_count':len(material),'supportive_channel_ids':[v['channel_id'] for v in supportive],'opposing_or_obstructive_channel_ids':[v['channel_id'] for v in opposing]})
roots=[r['root_id'] for r in root_map]
applied=[];rejected=[];caps=list(x.get('base_confidence_caps') or [])
quality='MAINTAINED';final_perm=pre;validity='KEEP_BASE';rev='LOW';asym='NEUTRAL';promotion='NONE'
def setq(q):
    global quality
    rank={'AMPLIFIED':0,'CONFIRMED':1,'MAINTAINED':2,'FRAGILE':3,'CONSTRAINED':4,'DELAYED':5,'SUPPRESSED':6,'CAPACITY_BLOCKED':7,'INSUFFICIENT_EVIDENCE':8}
    if rank[q]>rank[quality]:quality=q
def cap(c):
    if c not in caps:caps.append(c)
# Cognitive context can constrain but never create/flip.
cc=x.get('cognitive_context') or {}
if cc.get('cognitive_state') in {'CONTESTED','MODEL_DISAGREEMENT','INSUFFICIENT_EVIDENCE'} and pre!='NO_TRADE':
    final_perm='NO_TRADE';setq('INSUFFICIENT_EVIDENCE');validity='IMMEDIATE_REVIEW';applied.append({'rule':'V21_COGNITIVE_FAIL_CLOSED','state':cc.get('cognitive_state')})
# Pre-D3 inactive decisions cannot be positively promoted by Module 101.
if pre=='NO_TRADE':
    final_perm='NO_TRADE';applied.append({'rule':'NO_NEW_PERMISSION_FROM_PRE_D3_NO_TRADE'})
# Work on every channel for obstruction semantics; roots are used for independence counts.
allv=[v for r in root_map for v in r['channels']]
critical_unknown=[v for v in allv if v.get('decision_critical_unknown') is True or (v.get('obstruction_class')=='UNKNOWN' and v.get('materiality')=='DECISION_CRITICAL')]
if critical_unknown:
    final_perm='NO_TRADE';setq('INSUFFICIENT_EVIDENCE');validity='IMMEDIATE_REVIEW';applied.append({'rule':'DECISION_CRITICAL_D3_UNKNOWN','roots':sorted({v['root_id'] for v in critical_unknown})})
cap_false=x.get('capacity_sufficient_for_intended_execution') is False;cap_scope=x.get('capacity_scope_matched')
exec_blocks=[v for v in allv if v.get('obstruction_class')=='EXECUTION_BLOCK' and mat.get(v.get('materiality'),0)>=2]
if cap_false or exec_blocks:
    final_perm='NO_TRADE';setq('CAPACITY_BLOCKED');validity='IMMEDIATE_REVIEW';cap('CAPACITY_UNCERTAINTY');applied.append({'rule':'EXECUTION_CAPACITY_BLOCK','roots':sorted({v['root_id'] for v in exec_blocks})})
elif cap_scope is False:
    cap('CAPACITY_UNCERTAINTY');setq('CONSTRAINED');validity='SHORTEN_MODERATE';applied.append({'rule':'CAPACITY_SCOPE_MISMATCH_CAP'})
delays=[v for v in allv if v.get('obstruction_class')=='DELAY' and mat.get(v.get('materiality'),0)>=2]
if delays and quality not in {'INSUFFICIENT_EVIDENCE','CAPACITY_BLOCKED'}:
    final_perm='NO_TRADE';setq('DELAYED');validity='UNTIL_MECHANICAL_EVENT';cap('MECHANICAL_DISTORTION');applied.append({'rule':'MATERIAL_MECHANICAL_DELAY','roots':sorted({v['root_id'] for v in delays})})
breaks=[v for v in allv if v.get('obstruction_class')=='TRANSMISSION_BREAK' and mat.get(v.get('materiality'),0)>=2]
if breaks and quality not in {'INSUFFICIENT_EVIDENCE','CAPACITY_BLOCKED'}:
    final_perm='NO_TRADE';setq('SUPPRESSED');validity='IMMEDIATE_REVIEW';applied.append({'rule':'MATERIAL_TRANSMISSION_BREAK','roots':sorted({v['root_id'] for v in breaks})})
    for v in breaks:
        if v.get('science')=='ACTUAL_FLOW':cap('FLOW_OPPOSITION')
        if v.get('science')=='FUNDING_PLUMBING':cap('FUNDING_RESTRICTION')
fric=[v for v in allv if v.get('obstruction_class')=='FRICTION' and mat.get(v.get('materiality'),0)>=2]
if fric and quality not in {'INSUFFICIENT_EVIDENCE','CAPACITY_BLOCKED','DELAYED','SUPPRESSED'}:
    setq('CONSTRAINED');validity='SHORTEN_MODERATE';applied.append({'rule':'MATERIAL_D3_FRICTION','roots':sorted({v['root_id'] for v in fric})})
    for v in fric:
        if v.get('science')=='POSITIONING_OWNERSHIP':cap('CROWDING_FRAGILITY')
        elif v.get('science')=='ACTUAL_FLOW':cap('FLOW_OPPOSITION')
        elif v.get('science')=='FUNDING_PLUMBING':cap('FUNDING_RESTRICTION')
        elif v.get('science')=='INSTITUTIONAL_MECHANICS':cap('MECHANICAL_DISTORTION')
        elif v.get('science')=='MARKET_CAPACITY':cap('CAPACITY_UNCERTAINTY')
# A material same-root support/opposition conflict remains visible and cannot count as clean support.
if contested and quality not in {'INSUFFICIENT_EVIDENCE','CAPACITY_BLOCKED','DELAYED','SUPPRESSED'}:
    setq('CONSTRAINED');cap('CONTESTED_ROOT_CHANNELS');applied.append({'rule':'MULTI_CHANNEL_ROOT_CONTEST','roots':sorted(contested)})
# Positioning fragility semantic overlay.
for v in allv:
    if v.get('science')=='POSITIONING_OWNERSHIP':
        frag=str(v.get('fragility_state','UNKNOWN'));crowd=str(v.get('crowding_state','UNKNOWN'))
        if crowd=='VERY_CROWDED' and frag in {'HIGH','EXTREME'}:
            rev='EXTREME' if frag=='EXTREME' else 'HIGH';asym='POOR' if frag=='EXTREME' else 'DEGRADED';cap('CROWDING_FRAGILITY')
            if quality in {'MAINTAINED','CONFIRMED','AMPLIFIED'}:setq('FRAGILE')
            if validity=='KEEP_BASE':validity='SHORTEN_SEVERE' if frag=='EXTREME' else 'SHORTEN_MODERATE'
            applied.append({'rule':'CROWDING_FRAGILITY','root':v['root_id']})
    if v.get('science')=='ACTUAL_FLOW' and v.get('alignment_to_fundamental')=='OPPOSING' and str(v.get('persistence','UNKNOWN')) in {'ACCELERATING','PERSISTENT'}:
        rev='HIGH' if rev!='EXTREME' else rev;asym='DEGRADED' if asym!='POOR' else asym;cap('FLOW_OPPOSITION')
        if quality in {'MAINTAINED','CONFIRMED','AMPLIFIED'}:setq('FRAGILE')
        applied.append({'rule':'PERSISTENT_OPPOSING_FLOW_FRAGILITY','root':v['root_id']})
# Clean support is evaluated per independent root, not descendant count.
clean_support=[]
for rm in root_map:
    if rm['net_root_state']!='SUPPORTIVE':continue
    eligible=[v for v in rm['channels'] if v.get('alignment_to_fundamental')=='SUPPORTIVE' and v.get('obstruction_class') in {'NONE','SUPPORT'} and mat.get(v.get('materiality'),0)>=2 and v.get('evidence_grade') in direct_grades]
    if eligible:clean_support.append(rm['root_id'])
if pre!='NO_TRADE' and quality=='MAINTAINED':
    if len(clean_support)>=2:
        quality='AMPLIFIED';asym='FAVORABLE' if asym=='NEUTRAL' else asym;applied.append({'rule':'MULTI_ROOT_DIRECT_SUPPORT','roots':clean_support})
    elif len(clean_support)==1:
        quality='CONFIRMED';applied.append({'rule':'DIRECT_SUPPORT_CONFIRMATION','roots':clean_support})
elif pre=='NO_TRADE' and clean_support:
    promotion='HIGH' if len(clean_support)>=2 else 'MEDIUM';rejected.append({'rule':'SUPPORTIVE_D2_CANNOT_CREATE_PERMISSION','roots':clean_support})
if pre=='NO_TRADE' and final_perm!='NO_TRADE':raise SystemExit('SAFETY_NEW_PERMISSION_CREATED')
if pre in {'BUY','SELL'} and final_perm not in {pre,'NO_TRADE'}:raise SystemExit('SAFETY_DIRECTION_FLIP')
out={'version':'1.1.0','instrument':x['instrument'],'analysis_cutoff_utc':x['analysis_cutoff_utc'],'fundamental_direction':direction,'final_direction':direction,'pre_d3_research_edge':x['pre_d3_research_edge'],'pre_d3_permission':pre,'final_permission':final_perm,'d3_edge_quality':quality,'reversal_hazard':rev,'asymmetry_state':asym,'confidence_caps':sorted(caps),'validity_action':validity,'applied_rules':applied,'rejected_rules':rejected,'deduplicated_root_ids':roots,'deduplicated_root_count':len(roots),'root_channel_map':root_map,'contested_root_ids':sorted(contested),'support_independent_root_count':len(clean_support),'promotion_readiness':promotion,'cognitive_context_received':bool(cc),'direction_flip_forbidden':True,'new_permission_creation_forbidden_v19':True,'rule':'Fundamental Direction immutable; D3 is causal modulation. V21 deduplicates independence while preserving multi-channel root effects.'}
Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf-8');print(json.dumps(out,ensure_ascii=False))
