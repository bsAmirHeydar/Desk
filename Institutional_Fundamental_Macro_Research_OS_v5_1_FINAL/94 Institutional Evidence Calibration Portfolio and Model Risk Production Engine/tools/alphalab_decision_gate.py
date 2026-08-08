#!/usr/bin/env python3
import argparse,json
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('--input',required=True); p.add_argument('--output',required=True); a=p.parse_args()
s=json.loads(Path(a.input).read_text(encoding='utf-8'))
dir=s['fundamental_direction']; force=s['fundamental_force_state']; nar=s['narrative_clearance']; ev=s['evidence_clearance']; tim=s['timing_clearance']
up=dir in {'STRONG_BULLISH','BULLISH','MILD_BULLISH'}; dn=dir in {'STRONG_BEARISH','BEARISH','MILD_BEARISH'}; caps=[]
if ev=='BLOCK': core='INSUFFICIENT_EVIDENCE'
elif force=='FRAGMENTED' or dir=='FRAGMENTED': core='EVENT_OR_FRAGMENTED'
elif force!='ACTIVE' or not (up or dn): core='BIAS_ONLY' if (up or dn) else 'NO_EDGE'
elif nar in {'ALIGNED_DOMINANT','ALIGNED_EMERGING'}:
    core='ACTIVE_CANDIDATE_BULL' if up else 'ACTIVE_CANDIDATE_BEAR'
    if nar=='ALIGNED_EMERGING': caps.append('NARRATIVE_EMERGING')
elif nar=='NEUTRAL': core='CONDITIONAL_CANDIDATE_BULL' if up else 'CONDITIONAL_CANDIDATE_BEAR'
elif nar=='CONFLICTED': core='EVENT_OR_FRAGMENTED' if s.get('narrative_conflict_decision_critical',False) else ('CONDITIONAL_CANDIDATE_BULL' if up else 'CONDITIONAL_CANDIDATE_BEAR')
elif nar=='OPPOSING': core='BIAS_ONLY'
else: core='CONDITIONAL_CANDIDATE_BULL' if up else ('CONDITIONAL_CANDIDATE_BEAR' if dn else 'NO_EDGE')
if ev=='HOLD' and core.startswith('ACTIVE_'): core='CONDITIONAL_CANDIDATE_BULL' if up else 'CONDITIONAL_CANDIDATE_BEAR'
if ev=='CLEAR_WITH_CONFIDENCE_CAP': caps.append('EVIDENCE_SECONDARY_UNCERTAINTY')
if core=='INSUFFICIENT_EVIDENCE': edge='INSUFFICIENT_EVIDENCE'
elif core=='EVENT_OR_FRAGMENTED': edge='EVENT_OR_FRAGMENTED'
elif core.startswith('ACTIVE_'):
    if tim in {'CLEAR','CLEAR_WITH_CONSTRAINTS'}: edge='EDGE_ACTIVE'
    elif tim=='UNDETERMINED_MATERIAL': edge='INSUFFICIENT_EVIDENCE'
    elif tim=='VETO': edge='EVENT_OR_FRAGMENTED' if s.get('timing_veto_class')=='EVENT_FRAGMENTATION' else 'EDGE_CONDITIONAL'
    else: edge='EDGE_CONDITIONAL'
elif core.startswith('CONDITIONAL_'): edge='EDGE_CONDITIONAL'
elif core=='BIAS_ONLY': edge='BIAS_ONLY'
else: edge='NO_EDGE'
if tim=='CLEAR_WITH_CONSTRAINTS': caps.append('TIMING_CONSTRAINT')
perm='BUY' if edge=='EDGE_ACTIVE' and up else ('SELL' if edge=='EDGE_ACTIVE' and dn else 'NO_TRADE')
out={'fundamental_direction':dir,'core_edge_candidate':core,'research_edge':edge,'permission_before_operational_and_portfolio':perm,'confidence_caps':caps,'rule':'Fundamental creates direction; Narrative and Timing only clear/constrain.'}
Path(a.output).write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8'); print(json.dumps(out))
