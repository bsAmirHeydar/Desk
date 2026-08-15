#!/usr/bin/env python3
from __future__ import annotations
from copy import deepcopy

PHASE='AD-V2-P06'; VERSION='0.6.0'

def build(state,extension=None):
    s=state.get('science_v2') or {}; p=s.get('pressure') or {}; t=s.get('transmission') or {}; l=s.get('latent_release') or {}; g=s.get('gold_intelligence') or {}; ch=state.get('change_set') or {}
    pressure={'class':(p.get('pressure_core') or {}).get('class'),'sign':(p.get('pressure_core') or {}).get('sign'),'range':(p.get('pressure_core') or {}).get('signed_range'),'trend':(p.get('pressure_dynamics') or {}).get('trend'),'acceleration':(p.get('pressure_dynamics') or {}).get('acceleration'),'remaining':p.get('remaining_causal_pressure'),'persistence':p.get('persistence'),'consumption':p.get('fundamental_driver_consumption'),'confidence':p.get('pressure_confidence'),'contradiction':p.get('contradiction_load')}
    transmission={'state':(t.get('transmission_state') or {}).get('state'),'efficiency':t.get('transmission_efficiency'),'residual':t.get('counterfactual_residual'),'pathway':t.get('pathway_state'),'missing_driver':t.get('missing_driver_escalation'),'confidence':t.get('transmission_confidence'),'response_window':t.get('response_window')}
    latent={'unreleased':l.get('unreleased_pressure'),'maturity':l.get('opposing_move_maturity'),'reserve':l.get('latent_causal_reserve'),'inflection':l.get('transmission_inflection'),'readiness':l.get('release_readiness'),'lifecycle':l.get('release_lifecycle'),'hypotheses':l.get('liquidity_hypotheses'),'blockers':l.get('research_blockers'),'confidence':l.get('confidence')}
    gold={'coverage':g.get('observability_coverage'),'coverage_gaps':g.get('coverage_gaps'),'event_reset':g.get('event_reset'),'missing_driver_search':g.get('missing_driver_search'),'admitted_observations':g.get('admitted_observations')}
    return {'schema_version':'1.0.0','phase':PHASE,'report_model_version':'0.6.0','subject':state.get('subject'),'run_id':state.get('run_id'),'as_of':state.get('as_of'),'horizon':state.get('horizon'),'mode':state.get('mode'),
      'command_center':{'pressure':pressure,'transmission':transmission,'latent_release':latent,'permission':state.get('execution'),'gold':{'event_cap':(g.get('event_reset') or {}).get('release_readiness_cap_recommended'),'missing_driver_required':(g.get('missing_driver_search') or {}).get('required')}},
      'pressure':pressure,'transmission':transmission,'latent_release':latent,'gold_evidence':gold,'execution':deepcopy(state.get('execution')),'changes':deepcopy(ch),'portable_memory':deepcopy(state.get('portable_memory')),'quality':{'status':(extension or {}).get('quality_status'),'capsule_extension_hash':(extension or {}).get('capsule_extension_hash')},
      'ux':{'rtl':True,'primary_language':'fa-IR','pressure_price_separated':True,'release_readiness_is_permission':False,'presentation_authority_only':True}}
