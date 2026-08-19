from __future__ import annotations

def _edge_rank(e):return {'NO_EDGE':0,'LOW_EDGE':1,'CONDITIONAL_EDGE':2,'ACTIONABLE_EDGE':3}.get(e,0)
def evaluate(p08,fragility,unknown,scenario_packet,nonlinearity):
    pre_perm=p08.get('permission_candidate') or ((p08.get('permission') or {}).get('research_action_candidate')) or 'WAIT';pre_edge=p08.get('edge_state','NO_EDGE');overall=(fragility or {}).get('overall');dims=(fragility or {}).get('dimensions') or {};env=(unknown or {}).get('unknown_envelope');epi=(unknown or {}).get('epistemic_shock');sc=scenario_packet.get('scenarios') or [];opposing=any(x.get('relation_to_canonical_direction')=='OPPOSES' for x in sc);triggered_event=any(x.get('scenario_class')=='SCHEDULED_EVENT_DISCONTINUITY' and x.get('status')=='TRIGGERED' for x in sc)
    overlay='NO_CHANGE';reasons=[];post_perm=pre_perm;post_edge=pre_edge
    if pre_perm=='WAIT':overlay='NO_CHANGE';reasons.append('UPSTREAM_WAIT_PRESERVED')
    elif env=='CRITICAL' or overall=='CRITICALLY_FRAGILE' or epi or (triggered_event and nonlinearity.get('state')=='DISCONTINUOUS_EVENT'):
        overlay='FORCE_WAIT';post_perm='WAIT';post_edge='LOW_EDGE' if _edge_rank(pre_edge)>1 else pre_edge;reasons += [x for x,o in [('UNKNOWN_ENVELOPE_CRITICAL',env=='CRITICAL'),('CRITICAL_SYSTEM_FRAGILITY',overall=='CRITICALLY_FRAGILE'),('EPISTEMIC_SHOCK',bool(epi)),('TRIGGERED_DISCONTINUITY',triggered_event)] if o]
    elif (dims.get('MODEL_FRAGILITY')=='HIGH' and opposing) or dims.get('DATA_FRAGILITY') in ('HIGH','CRITICAL') or env=='WIDE' or dims.get('NARRATIVE_FRAGILITY')=='HIGH' or dims.get('EVENT_FRAGILITY')=='HIGH':
        overlay='CAP_TO_CONDITIONAL';post_perm='WAIT';post_edge='CONDITIONAL_EDGE' if _edge_rank(pre_edge)>2 else pre_edge;reasons.append('MATERIAL_PERSPECTIVE_FRAGILITY')
    # monotonic invariants
    if _edge_rank(post_edge)>_edge_rank(pre_edge):raise RuntimeError('R03_EDGE_UPGRADE_FORBIDDEN')
    if pre_perm=='WAIT' and post_perm!='WAIT':raise RuntimeError('R03_PERMISSION_UPGRADE_FORBIDDEN')
    return {'overlay':overlay,'pre_overlay_permission':pre_perm,'post_overlay_permission':post_perm,'pre_overlay_edge':pre_edge,'post_overlay_edge':post_edge,'reasons':reasons,'authority_upgraded':False,'direction_authority':False,'edge_upgrade_forbidden':True,'permission_upgrade_forbidden':True}
