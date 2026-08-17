from __future__ import annotations

def build_hypotheses(causal,root_paths):
    direction=causal.get('direction'); roots=causal.get('root_states',[])
    support=[r for r in roots if r.get('direction')==direction] if direction in ('BULLISH_GOLD','BEARISH_GOLD') else []
    rivals=[r for r in roots if r.get('direction') in ('BULLISH_GOLD','BEARISH_GOLD') and r.get('direction')!=direction]
    primary={'direction':direction,'supporting_roots':[r['root_id'] for r in support],'expected_signatures':{r['root_id']:root_paths.get('paths',{}).get(r['root_id'],{}) for r in support}}
    return {'primary':primary,'rivals':[{'root_id':r['root_id'],'direction':r['direction']} for r in rivals],'minimum_sufficient_explanation_roots':[r['root_id'] for r in support[:3]],'forced_story_forbidden':True}
