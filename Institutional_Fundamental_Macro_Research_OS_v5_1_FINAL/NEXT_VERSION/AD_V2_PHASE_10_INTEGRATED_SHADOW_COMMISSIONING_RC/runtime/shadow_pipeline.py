from __future__ import annotations
from pathlib import Path
from copy import deepcopy
import sys,json
from .common import hsh

class P10IntegrationError(ValueError): pass

def _import_stack(phase_parent):
 phase_parent=Path(phase_parent).resolve()
 if str(phase_parent) not in sys.path: sys.path.insert(0,str(phase_parent))
 from AD_V2_PHASE_02_DIRECTIONAL_PRESSURE_ENGINE.runtime.directional_pressure import build_from_roots
 from AD_V2_PHASE_03_PRICE_TRANSMISSION_ENGINE.runtime.price_transmission import build_transmission,_pressure_fingerprint
 from AD_V2_PHASE_04_LATENT_RELEASE_ENGINE.runtime.latent_release import build_latent_release
 from AD_V2_PHASE_05_GOLD_INTELLIGENCE_SPECIALIZATION.runtime.gold_intelligence import build_gold_intelligence
 from AD_V2_PHASE_06_RUN_MEMORY_UX_INTEGRATION.runtime.run_overlay import compose
 from AD_V2_PHASE_06_RUN_MEMORY_UX_INTEGRATION.runtime.v2_memory import find_previous,build_extension,persist
 from AD_V2_PHASE_06_RUN_MEMORY_UX_INTEGRATION.runtime.report_model_v2 import build as build_report
 from AD_V2_PHASE_06_RUN_MEMORY_UX_INTEGRATION.runtime.render_v2 import render_html
 return build_from_roots,build_transmission,_pressure_fingerprint,build_latent_release,build_gold_intelligence,compose,find_previous,build_extension,persist,build_report,render_html

def run(input_pack:dict,*,phase_parent,data_root,output_dir,persist_state=True):
 if not isinstance(input_pack,dict): raise P10IntegrationError('input pack required')
 for k in ['base_capsule','pressure_input','expected_signature','actual_response','gold_observations']:
  if k not in input_pack: raise P10IntegrationError('missing input '+k)
 build_p,build_t,pfp,build_l,build_g,compose,find_previous,build_extension,persist,build_report,render_html=_import_stack(phase_parent)
 base=deepcopy(input_pack['base_capsule']); pin=deepcopy(input_pack['pressure_input']); sig=deepcopy(input_pack['expected_signature']); actual=deepcopy(input_pack['actual_response']); obs=deepcopy(input_pack['gold_observations'])
 pressure=build_p(pin,history=input_pack.get('pressure_history'))
 if pressure.get('status')!='PASS': raise P10IntegrationError('P02 failed: '+json.dumps(pressure.get('integrity'),ensure_ascii=False))
 # Binding is mechanical only. Expected range/method/timestamps are not altered after actual response is supplied.
 sig['pressure_fingerprint']=pfp(pressure)
 transmission=build_t(pressure,sig,actual,divergence_history_count=int(input_pack.get('divergence_history_count',0)),missing_driver_candidates=input_pack.get('missing_driver_candidates'))
 if transmission.get('status')!='PASS': raise P10IntegrationError('P03 failed: '+json.dumps(transmission.get('integrity'),ensure_ascii=False))
 pre_gold=build_g(obs,as_of_utc=input_pack.get('gold_as_of_utc') or actual.get('window_end_utc'),active_horizon=pressure.get('active_horizon'),upstream_pressure=pressure,upstream_transmission=transmission,upstream_latent=None)
 if pre_gold.get('status')!='PASS': raise P10IntegrationError('P05 prepass failed')
 packet=((pre_gold.get('p04_adapter') or {}).get('evidence_packet')) or {'active_horizon':pressure.get('active_horizon'),'observations':[]}
 latent=build_l(pressure,transmission,packet,transmission_history=input_pack.get('transmission_history'),lifecycle_history=input_pack.get('lifecycle_history'))
 if latent.get('status')!='PASS': raise P10IntegrationError('P04 failed: '+json.dumps(latent.get('integrity'),ensure_ascii=False))
 gold=build_g(obs,as_of_utc=input_pack.get('gold_as_of_utc') or actual.get('window_end_utc'),active_horizon=pressure.get('active_horizon'),upstream_pressure=pressure,upstream_transmission=transmission,upstream_latent=latent)
 if gold.get('status')!='PASS': raise P10IntegrationError('P05 final failed')
 prev=find_previous(data_root,'XAUUSD',base.get('mode'),base.get('horizon')) if persist_state else None
 state=compose(base,pressure,transmission,latent,gold,previous=prev)
 ext=build_extension(state)
 receipt=None
 if persist_state: receipt=persist(data_root,ext)
 report=build_report(state,ext)
 out=Path(output_dir);out.mkdir(parents=True,exist_ok=True)
 report_path=out/(str(state.get('run_id'))+'_v2_report_model.json'); report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 html_path=render_html(report,out/(str(state.get('run_id'))+'_v2_explorer.html'))
 return {'schema_version':'1.0.0','phase':'AD-V2-P10','status':'PASS','run_id':state.get('run_id'),'p02':pressure,'p03':transmission,'p04':latent,'p05':gold,'p06':{'state':state,'capsule':receipt,'report_model':str(report_path),'explorer':str(html_path)},'integrity':{'status':'PASS','pressure_price_separation':True,'upstream_authorities_unchanged':True,'synthetic_or_manual_wrapper_is_not_true_forward_admission':True},'authority':{'trade_permission':'V1_INHERITED','broker':'NONE','mainline_override':False,'auto_promotion':False},'receipt_hash':hsh({'run_id':state.get('run_id'),'state_hash':state.get('canonical_v2_state_hash'),'capsule':receipt})}
