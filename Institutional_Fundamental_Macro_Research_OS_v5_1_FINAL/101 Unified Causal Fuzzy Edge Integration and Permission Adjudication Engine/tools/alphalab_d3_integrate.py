#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path

p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--output',required=True);a=p.parse_args()
x=json.loads(Path(a.input).read_text(encoding='utf-8'))
required=['version','instrument','analysis_cutoff_utc','fundamental_direction','pre_d3_research_edge','pre_d3_permission','integration_vectors']
missing=[k for k in required if k not in x]
if missing: raise SystemExit('MISSING_REQUIRED: '+','.join(missing))
if x.get('version')!='1.0.0': raise SystemExit('BAD_VERSION')
pre=x['pre_d3_permission']; direction=x['fundamental_direction']; vectors=x.get('integration_vectors') or []

# Deduplicate by causal root for load-bearing classification. Keep the most severe observation per root.
severity={'UNKNOWN':0,'NONE':1,'SUPPORT':2,'FRICTION':3,'DELAY':4,'TRANSMISSION_BREAK':5,'EXECUTION_BLOCK':6}
mat={'CONTEXTUAL':0,'SUPPORTING':1,'MATERIAL':2,'DECISION_CRITICAL':3}
by_root={}
for v in vectors:
    rid=str(v.get('root_id') or '').strip()
    if not rid: raise SystemExit('EMPTY_ROOT_ID')
    key=(severity.get(v.get('obstruction_class'),0),mat.get(v.get('materiality'),0))
    old=by_root.get(rid)
    if old is None or key>(severity.get(old.get('obstruction_class'),0),mat.get(old.get('materiality'),0)):
        by_root[rid]=v
roots=sorted(by_root)
unique=list(by_root.values())

applied=[];rejected=[];caps=list(x.get('base_confidence_caps') or [])
quality='MAINTAINED';final_perm=pre;validity='KEEP_BASE';rev='LOW';asym='NEUTRAL';promotion='NONE'

def setq(q):
    global quality
    rank={'AMPLIFIED':0,'CONFIRMED':1,'MAINTAINED':2,'FRAGILE':3,'CONSTRAINED':4,'DELAYED':5,'SUPPRESSED':6,'CAPACITY_BLOCKED':7,'INSUFFICIENT_EVIDENCE':8}
    if rank[q]>rank[quality]:quality=q

def cap(c):
    if c not in caps:caps.append(c)

# Pre-D3 inactive decisions cannot be promoted in V19.
if pre=='NO_TRADE':
    final_perm='NO_TRADE'; quality='MAINTAINED'; applied.append({'rule':'V19_NO_NEW_PERMISSION_FROM_PRE_D3_NO_TRADE'})

# Decision-critical unknown always blocks.
critical_unknown=[v for v in unique if v.get('decision_critical_unknown') is True or (v.get('obstruction_class')=='UNKNOWN' and v.get('materiality')=='DECISION_CRITICAL')]
if critical_unknown:
    final_perm='NO_TRADE';setq('INSUFFICIENT_EVIDENCE');validity='IMMEDIATE_REVIEW';applied.append({'rule':'DECISION_CRITICAL_D3_UNKNOWN','roots':[v['root_id'] for v in critical_unknown]})

# Explicit capacity block has execution precedence.
cap_false=x.get('capacity_sufficient_for_intended_execution') is False
cap_scope=x.get('capacity_scope_matched')
exec_blocks=[v for v in unique if v.get('obstruction_class')=='EXECUTION_BLOCK' and v.get('materiality') in {'MATERIAL','DECISION_CRITICAL'}]
if cap_false or exec_blocks:
    final_perm='NO_TRADE';setq('CAPACITY_BLOCKED');validity='IMMEDIATE_REVIEW';cap('CAPACITY_UNCERTAINTY');applied.append({'rule':'EXECUTION_CAPACITY_BLOCK','roots':[v['root_id'] for v in exec_blocks]})
elif cap_scope is False:
    cap('CAPACITY_UNCERTAINTY');setq('CONSTRAINED');validity='SHORTEN_MODERATE';applied.append({'rule':'CAPACITY_SCOPE_MISMATCH_CAP'})

# Decision-critical mechanics delay current entry without changing thesis direction.
delays=[v for v in unique if v.get('obstruction_class')=='DELAY' and v.get('materiality') in {'MATERIAL','DECISION_CRITICAL'}]
if delays and quality not in {'INSUFFICIENT_EVIDENCE','CAPACITY_BLOCKED'}:
    final_perm='NO_TRADE';setq('DELAYED');validity='UNTIL_MECHANICAL_EVENT';cap('MECHANICAL_DISTORTION');applied.append({'rule':'MATERIAL_MECHANICAL_DELAY','roots':[v['root_id'] for v in delays]})

# A transmission break suppresses otherwise active exposure. It cannot flip direction.
breaks=[v for v in unique if v.get('obstruction_class')=='TRANSMISSION_BREAK' and v.get('materiality') in {'MATERIAL','DECISION_CRITICAL'}]
if breaks and quality not in {'INSUFFICIENT_EVIDENCE','CAPACITY_BLOCKED'}:
    final_perm='NO_TRADE';setq('SUPPRESSED');validity='IMMEDIATE_REVIEW';applied.append({'rule':'MATERIAL_TRANSMISSION_BREAK','roots':[v['root_id'] for v in breaks]})
    for v in breaks:
        if v.get('science')=='ACTUAL_FLOW':cap('FLOW_OPPOSITION')
        if v.get('science')=='FUNDING_PLUMBING':cap('FUNDING_RESTRICTION')

# Frictions constrain but do not automatically kill an active edge.
fric=[v for v in unique if v.get('obstruction_class')=='FRICTION' and v.get('materiality') in {'MATERIAL','DECISION_CRITICAL'}]
if fric and quality not in {'INSUFFICIENT_EVIDENCE','CAPACITY_BLOCKED','DELAYED','SUPPRESSED'}:
    setq('CONSTRAINED');validity='SHORTEN_MODERATE';applied.append({'rule':'MATERIAL_D3_FRICTION','roots':[v['root_id'] for v in fric]})
    for v in fric:
        if v.get('science')=='POSITIONING_OWNERSHIP':cap('CROWDING_FRAGILITY')
        elif v.get('science')=='ACTUAL_FLOW':cap('FLOW_OPPOSITION')
        elif v.get('science')=='FUNDING_PLUMBING':cap('FUNDING_RESTRICTION')
        elif v.get('science')=='INSTITUTIONAL_MECHANICS':cap('MECHANICAL_DISTORTION')
        elif v.get('science')=='MARKET_CAPACITY':cap('CAPACITY_UNCERTAINTY')

# Positioning fragility conventions via optional semantic fields.
pos=[v for v in unique if v.get('science')=='POSITIONING_OWNERSHIP']
for v in pos:
    frag=str(v.get('fragility_state','UNKNOWN'))
    crowd=str(v.get('crowding_state','UNKNOWN'))
    if crowd=='VERY_CROWDED' and frag in {'HIGH','EXTREME'}:
        rev='EXTREME' if frag=='EXTREME' else 'HIGH';asym='POOR' if frag=='EXTREME' else 'DEGRADED';cap('CROWDING_FRAGILITY')
        if quality in {'MAINTAINED','CONFIRMED','AMPLIFIED'}:setq('FRAGILE')
        if validity=='KEEP_BASE':validity='SHORTEN_SEVERE' if frag=='EXTREME' else 'SHORTEN_MODERATE'
        applied.append({'rule':'CROWDING_FRAGILITY','root':v['root_id']})

# Opposing/decelerating flow raises reversal hazard even if not strong enough for transmission break.
for v in unique:
    if v.get('science')=='ACTUAL_FLOW' and v.get('alignment_to_fundamental')=='OPPOSING':
        pers=str(v.get('persistence','UNKNOWN'))
        if pers in {'ACCELERATING','PERSISTENT'}:
            rev='HIGH' if rev!='EXTREME' else rev;asym='DEGRADED' if asym!='POOR' else asym;cap('FLOW_OPPOSITION')
            if quality in {'MAINTAINED','CONFIRMED','AMPLIFIED'}:setq('FRAGILE')
            applied.append({'rule':'PERSISTENT_OPPOSING_FLOW_FRAGILITY','root':v['root_id']})

# Support is descriptive/confirmatory and cannot override blocks.
support=[v for v in unique if v.get('alignment_to_fundamental')=='SUPPORTIVE' and v.get('obstruction_class') in {'NONE','SUPPORT'} and v.get('materiality') in {'MATERIAL','DECISION_CRITICAL'}]
direct=[v for v in support if v.get('evidence_grade') in {'DIRECT_IDENTIFIED','OFFICIAL_OR_EXCHANGE','DERIVED_WITH_LINEAGE'}]
if pre!='NO_TRADE' and quality=='MAINTAINED':
    if len({v['root_id'] for v in direct})>=2:
        quality='AMPLIFIED';asym='FAVORABLE' if asym=='NEUTRAL' else asym;applied.append({'rule':'MULTI_ROOT_DIRECT_SUPPORT','roots':sorted({v['root_id'] for v in direct})})
    elif direct:
        quality='CONFIRMED';applied.append({'rule':'DIRECT_SUPPORT_CONFIRMATION','roots':sorted({v['root_id'] for v in direct})})
elif pre=='NO_TRADE' and direct:
    promotion='HIGH' if len({v['root_id'] for v in direct})>=2 else 'MEDIUM'
    rejected.append({'rule':'SUPPORTIVE_D2_WOULD_NOT_CREATE_PERMISSION_IN_V19','roots':sorted({v['root_id'] for v in direct})})

# Final safety: never invert and never create from NO_TRADE.
if pre=='NO_TRADE' and final_perm!='NO_TRADE': raise SystemExit('SAFETY_NEW_PERMISSION_CREATED')
if pre in {'BUY','SELL'} and final_perm not in {pre,'NO_TRADE'}: raise SystemExit('SAFETY_DIRECTION_FLIP')

out={
 'version':'1.0.0','instrument':x['instrument'],'analysis_cutoff_utc':x['analysis_cutoff_utc'],'fundamental_direction':direction,'final_direction':direction,
 'pre_d3_research_edge':x['pre_d3_research_edge'],'pre_d3_permission':pre,'final_permission':final_perm,'d3_edge_quality':quality,
 'reversal_hazard':rev,'asymmetry_state':asym,'confidence_caps':sorted(caps),'validity_action':validity,'applied_rules':applied,'rejected_rules':rejected,
 'deduplicated_root_ids':roots,'deduplicated_root_count':len(roots),'promotion_readiness':promotion,
 'direction_flip_forbidden':True,'new_permission_creation_forbidden_v19':True,
 'rule':'Fundamental Direction immutable; D3 is causal modulation, not voting.'
}
Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(out,ensure_ascii=False))
