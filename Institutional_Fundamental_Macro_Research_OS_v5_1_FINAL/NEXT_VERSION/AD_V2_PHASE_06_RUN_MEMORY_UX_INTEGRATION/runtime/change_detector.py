#!/usr/bin/env python3
from __future__ import annotations
from copy import deepcopy
import json, hashlib

PHASE='AD-V2-P06'
VERSION='0.6.0'

def _get(obj,path):
    cur=obj
    for part in str(path).split('.'):
        if not isinstance(cur,dict): return None
        cur=cur.get(part)
    return cur

def _stable(x):
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),default=str).encode()).hexdigest()

def default_registry():
    return [
      ('pressure_class','P02','science_v2.pressure.pressure_core.class','PRESSURE'),
      ('pressure_sign','P02','science_v2.pressure.pressure_core.sign','PRESSURE'),
      ('pressure_trend','P02','science_v2.pressure.pressure_dynamics.trend','PRESSURE'),
      ('pressure_acceleration','P02','science_v2.pressure.pressure_dynamics.acceleration','PRESSURE'),
      ('remaining_causal_pressure','P02','science_v2.pressure.remaining_causal_pressure.value','PRESSURE'),
      ('transmission_state','P03','science_v2.transmission.transmission_state.state','TRANSMISSION'),
      ('transmission_efficiency','P03','science_v2.transmission.transmission_efficiency.class','TRANSMISSION'),
      ('residual_state','P03','science_v2.transmission.counterfactual_residual.state','TRANSMISSION'),
      ('residual_magnitude','P03','science_v2.transmission.counterfactual_residual.magnitude_class','TRANSMISSION'),
      ('missing_driver_escalation','P03','science_v2.transmission.missing_driver_escalation.level','TRANSMISSION'),
      ('unreleased_pressure','P04','science_v2.latent_release.unreleased_pressure.class','LATENT'),
      ('opposing_move_maturity','P04','science_v2.latent_release.opposing_move_maturity.state','LATENT'),
      ('latent_reserve','P04','science_v2.latent_release.latent_causal_reserve.class','LATENT'),
      ('transmission_inflection','P04','science_v2.latent_release.transmission_inflection.state','LATENT'),
      ('release_readiness','P04','science_v2.latent_release.release_readiness.state','LATENT'),
      ('release_lifecycle','P04','science_v2.latent_release.release_lifecycle.state','LATENT'),
      ('event_readiness_cap','P05','science_v2.gold_intelligence.event_reset.release_readiness_cap_recommended','GOLD'),
      ('gold_missing_driver_search','P05','science_v2.gold_intelligence.missing_driver_search.required','GOLD'),
      ('trade_permission','V1','execution.permission','EXECUTION')
    ]

def detect(previous,current,registry=None):
    if not previous:
        return {'schema_version':'1.0.0','phase':PHASE,'status':'PASS','has_comparison':False,'comparison_run_id':None,'material_change':False,'items':[],'domain_summary':{},'pressure_changed':False,'price_only_change_cannot_set_pressure_changed':True}
    items=[]; domains={}
    for fid,owner,path,domain in (registry or default_registry()):
        a=_get(previous,path); b=_get(current,path)
        if a!=b:
            item={'field':fid,'owner':owner,'domain':domain,'from':deepcopy(a),'to':deepcopy(b),'path':path}
            items.append(item); domains[domain]=domains.get(domain,0)+1
    # research blockers are semantically material as a set
    a=_get(previous,'science_v2.latent_release.research_blockers') or []
    b=_get(current,'science_v2.latent_release.research_blockers') or []
    if _stable(a)!=_stable(b):
        items.append({'field':'research_blockers','owner':'P04','domain':'LATENT','from':deepcopy(a),'to':deepcopy(b),'path':'science_v2.latent_release.research_blockers'}); domains['LATENT']=domains.get('LATENT',0)+1
    pressure_changed=any(x['domain']=='PRESSURE' for x in items)
    return {'schema_version':'1.0.0','phase':PHASE,'status':'PASS','has_comparison':True,'comparison_run_id':previous.get('run_id'),'material_change':bool(items),'items':items,'domain_summary':domains,'pressure_changed':pressure_changed,'price_only_change_cannot_set_pressure_changed':True}
