from __future__ import annotations
from .common import cfg,label,term,uniq,sha_obj,safe_url

MATERIAL=[('causal_direction','جهت'),('pressure_strength','قدرت فشار'),('dominance_state','غلبه'),('dominant_root','ریشه غالب'),('dominance_robustness','پایداری غلبه'),('model_sensitivity','حساسیت مدل'),('permission_candidate','مجوز پژوهشی'),('edge_state','Edge'),('consumption','مصرف'),('fragility','شکنندگی'),('contradiction','تناقض')]

def _permission(d):
 return d.get('permission_candidate') or ((d.get('permission') or {}).get('research_action_candidate')) or 'WAIT'
def _direction(d):return d.get('causal_direction') or d.get('raw_p03_causal_direction') or 'UNKNOWN'
def _root_label(x):return label(x,'root') if x else 'ریشه غالب مشخص نشده'
def _top_constraint(d):
 b=list(d.get('blockers') or d.get('permission_blockers') or [])
 if b:return b[0]
 if d.get('consumption') in ('HIGH','CONSUMED','EXHAUSTED'):return 'HIGH_CONSUMPTION'
 if d.get('fragility')=='HIGH':return 'HIGH_FRAGILITY'
 return None

def _headline(d,blocked=False):
 direction=_direction(d);perm=_permission(d);root=_root_label(d.get('dominant_root'));constraint=_top_constraint(d)
 if blocked:return 'تحلیل جهت‌دار فعلاً مجاز نیست؛ داده‌ی حیاتی کافی برای تصمیم پژوهشی وجود ندارد.'
 if direction in ('UNKNOWN','MIXED'):
  base='شواهد فعلی برای یک جهت علّی روشن در طلا کافی نیست.' if direction=='UNKNOWN' else 'ریشه‌های علّی اصلی طلا در تعارض‌اند و برتری پایدار یک‌طرفه اثبات نشده است.'
 elif 'BULLISH' in direction:
  base=f'فشار علّی طلا صعودی است و «{root}» مهم‌ترین ریشه‌ی فعلی است.'
 elif 'BEARISH' in direction:
  base=f'فشار علّی طلا نزولی است و «{root}» مهم‌ترین ریشه‌ی فعلی است.'
 else: base='وضعیت علّی طلا نیاز به شواهد روشن‌تر دارد.'
 if perm in ('WAIT','WAIT_CANDIDATE'):base+=' با وجود thesis فعلی، مجوز اقدام پژوهشی هنوز WAIT است.'
 elif 'BUY' in perm:base+=' مجوز پژوهشی فعلی در سمت خرید قرار دارد.'
 elif 'SELL' in perm:base+=' مجوز پژوهشی فعلی در سمت فروش قرار دارد.'
 if constraint:base+=f' محدودیت اصلی: {label(constraint)}.'
 return base

def _summary(d,trans,events):
 parts=[f"قدرت فشار: {label(d.get('pressure_strength'))}؛ غلبه: {label(d.get('dominance_state'))}؛ پهنا: {label(d.get('breadth'))}."]
 parts.append(f"مصرف: {label(d.get('consumption'))}؛ شکنندگی: {label(d.get('fragility'))}؛ Edge: {label(d.get('edge_state'))}.")
 if trans:parts.append(f"رفتار قیمت/Transmission: {label(trans.get('state') or trans.get('transmission_state') or 'UNKNOWN')}. این بخش جهت بنیادی را بازنویسی نمی‌کند.")
 if events:parts.append(f"نزدیک‌ترین رویداد ثبت‌شده: {events[0].get('label') or events[0].get('event') or events[0].get('name')}.")
 return parts

def _comparison(cur,prev):
 if not prev:return {'available':False,'items':[],'message':'Run موفق قابل‌مقایسه‌ی قبلی وجود ندارد.'}
 cd=cur.get('decision_calibration') or {};pd=prev.get('decision_calibration') or {};items=[]
 for k,fa in MATERIAL:
  a=cd.get(k);b=pd.get(k)
  if a!=b:items.append({'field':k,'label':fa,'from':b,'to':a,'from_human':_root_label(b) if k=='dominant_root' else label(b),'to_human':_root_label(a) if k=='dominant_root' else label(a),'classification':'MATERIAL' if k in {'causal_direction','dominance_state','dominant_root','permission_candidate'} else 'IMPORTANT'})
 ck=((cur.get('data_kernel') or {}).get('kernel_health') or {}).get('overall_analysis_admission');pk=((prev.get('data_kernel') or {}).get('kernel_health') or {}).get('overall_analysis_admission')
 if ck!=pk:items.append({'field':'analysis_admission','label':'سلامت/Admission داده','from':pk,'to':ck,'from_human':label(pk),'to_human':label(ck),'classification':'IMPORTANT'})
 cs=((cur.get('semantic') or {}).get('bundle') or {}).get('adjudication_mode');ps=((prev.get('semantic') or {}).get('bundle') or {}).get('adjudication_mode')
 if cs!=ps:items.append({'field':'semantic_mode','label':'حالت معنایی','from':ps,'to':cs,'from_human':label(ps),'to_human':label(cs),'classification':'IMPORTANT'})
 return {'available':True,'items':items,'message':'تغییر معناداری در state اصلی ثبت نشده است.' if not items else None,'compared_to_run_id':(prev.get('run') or {}).get('run_id')}

def _evidence(cri):
 idx=cri.get('evidence_index') or {};rows=[]
 for o in idx.get('observations') or []:
  m=o.get('metadata') or {};p07=m.get('p07_kernel') or {};url=safe_url(o.get('provenance_ref'))
  rows.append({'fact_id':o.get('fact_id'),'observation_id':o.get('observation_id'),'value':o.get('value'),'value_type':o.get('value_type'),'unit':o.get('unit'),'source_id':o.get('source_id'),'source_url':url,'directness':o.get('directness'),'epistemic_state':o.get('epistemic_state'),'reference_period':o.get('reference_period'),'event_time':o.get('event_time'),'published_at':o.get('published_at'),'retrieved_at':o.get('retrieved_at'),'freshness_state':p07.get('freshness_state'),'operational_tier':p07.get('operational_tier'),'source_action':p07.get('source_action'),'cache_reused':p07.get('cache_reused'),'warnings':o.get('warnings') or []})
 return rows

def _roots(cri,evidence):
 d=cri.get('decision_calibration') or {};p3=cri.get('causal_state') or {};cf=((p3.get('pressure_planes') or {}).get('causal_fundamental') or {});raw={x.get('root_id'):x for x in cf.get('root_states') or []};evmap={x['fact_id']:x for x in evidence};dominant=d.get('dominant_root');support=set(d.get('supporting_roots') or []);opp=set(d.get('opposing_roots') or []);out=[]
 for r in d.get('calibrated_roots') or []:
  rid=r.get('root_id');rr=raw.get(rid,{})
  role='PRIMARY_DOMINANT' if rid==dominant else ('SECONDARY_SUPPORT' if rid in support else ('OFFSET' if rid in opp else 'BACKGROUND'))
  facts=[]
  for fid in r.get('evidence_fact_ids') or []:
   if fid in evmap:facts.append(evmap[fid])
   else:facts.append({'fact_id':fid,'observation_id':None,'value':None,'source_id':None,'freshness_state':'UNAVAILABLE','operational_tier':None})
  out.append({'root_id':rid,'label':_root_label(rid),'role':role,'direction':r.get('direction') or rr.get('direction'),'background_bias':r.get('background_bias') or rr.get('background_bias'),'causal_importance':r.get('causal_importance'),'importance_basis':r.get('importance_basis'),'magnitude':r.get('magnitude'),'magnitude_temporal_role':r.get('magnitude_temporal_role'),'root_health':r.get('root_health') or {},'root_health_state':((r.get('root_health') or {}).get('state')),'freshness':r.get('freshness'),'evidence_quality':r.get('evidence_quality'),'independence':r.get('independence'),'persistence':r.get('persistence'),'semantic_unknown_count':r.get('semantic_unknown_count',0),'empirical_information_state':r.get('empirical_information_state'),'evidence_fact_ids':r.get('evidence_fact_ids') or [],'facts':facts})
 role_rank={'PRIMARY_DOMINANT':0,'SECONDARY_SUPPORT':1,'OFFSET':2,'BACKGROUND':3};return sorted(out,key=lambda x:(role_rank.get(x['role'],9),x['label']))

def _events(cri):
 pred=((cri.get('forward_validation') or {}).get('prediction') or {});ev=((pred.get('event_context') or {}).get('events') or []);out=[]
 for x in ev:
  if not isinstance(x,dict):continue
  out.append({'event':x.get('event') or x.get('name') or x.get('label') or 'Event','label':x.get('label') or x.get('event') or x.get('name') or 'رویداد','time':x.get('time') or x.get('event_time') or x.get('scheduled_at'),'t_minus':x.get('t_minus'),'materiality':x.get('materiality') or 'CONTEXT','affected_roots':x.get('affected_roots') or [],'status':x.get('status') or 'UPCOMING'})
 return out

def _watch(d,kernel,trans,events,forward):
 out=[]
 if events:out.append({'kind':'EVENT','title':'رویداد بعدی','text':events[0].get('label'),'detail':events[0].get('time')})
 for fid in ((kernel.get('kernel_health') or {}).get('important_live_gaps') or [])[:2]:out.append({'kind':'DATA','title':'داده‌ی حیاتی','text':f'به‌روزرسانی/رفع شکاف {fid}','detail':'این شکاف می‌تواند Edge یا Permission را محدود کند.'})
 if trans and (trans.get('state') or 'UNKNOWN') not in ('ALIGNED','CONFIRMING'):out.append({'kind':'PRICE','title':'رفتار قیمت','text':'بررسی کنید آیا قیمت شروع به انتقال فشار علّی می‌کند یا همچنان مقاومت دارد.','detail':'Price Transmission جهت بنیادی را بازنویسی نمی‌کند.'})
 if (forward.get('prediction') or {}).get('maturity_time'):out.append({'kind':'FORWARD','title':'Forward checkpoint','text':'بلوغ prediction جاری','detail':(forward.get('prediction') or {}).get('maturity_time')})
 if d.get('missing_driver_risk') in ('HIGH','ELEVATED'):out.append({'kind':'RISK','title':'عامل گمشده','text':'رفتار فعلی بازار با evidence مشاهده‌شده کاملاً توضیح داده نمی‌شود.','detail':'عامل جدید اختراع نمی‌شود؛ فقط ریسک توضیح‌ناپذیری بالا گزارش می‌شود.'})
 return out[:6]

def _gap_impact(fid):
 f=str(fid)
 if 'DXY' in f or 'DOLLAR' in f or 'USD' in f:return 'روی USD confirmation و در نتیجه Edge/Permission اثر می‌گذارد.'
 if 'REAL_YIELD' in f or 'NOMINAL_YIELD' in f:return 'روی ریشه‌ی نرخ/بازده واقعی و قدرت تصمیم session اثر می‌گذارد.'
 if 'DEALER' in f or 'OPTIONS' in f:return 'روی مکانیک/شکنندگی و تبیین حرکت کوتاه‌مدت اثر می‌گذارد.'
 if 'LONDON' in f or 'OTC' in f:return 'روی مشاهده‌ی فلو OTC اثر می‌گذارد و ممکن است missing-driver risk را بالا نگه دارد.'
 return 'اثر آن به ریشه‌ی مربوطه و کیفیت تصمیم محدود می‌شود؛ جهت از روی شکاف داده ساخته نمی‌شود.'

def build_view_model(cri,previous_input=None,fixture=False):
 run=cri.get('run') or {};d=cri.get('decision_calibration') or {};kernel=cri.get('data_kernel') or {};kh=kernel.get('kernel_health') or {};semantic=cri.get('semantic') or {};bundle=semantic.get('bundle') or {};semrec=semantic.get('validation_receipt') or {};p3=cri.get('causal_state') or {};trans=p3.get('price_transmission') or {};fwd=cri.get('forward_validation') or {};stats=fwd.get('statistics') or {};cohort=fwd.get('active_cohort') or {};evidence=_evidence(cri);roots=_roots(cri,evidence);events=_events(cri);blocked=(kh.get('overall_analysis_admission') in ('BLOCK','BLOCKED') or d.get('permission_candidate')=='NO_AUTHORITY')
 perm='NO_AUTHORITY' if blocked else _permission(d);direction=_direction(d)
 gaps=[]
 for fid in uniq(list(kh.get('important_live_gaps') or [])+list(kernel.get('known_provider_gap_facts') or [])+list(kernel.get('known_private_gap_facts') or [])+list(kernel.get('known_paid_gap_facts') or []))[:12]:gaps.append({'fact_id':fid,'impact':_gap_impact(fid)})
 semmeta=bundle.get('p06_semantic') or {}
 vm={'record_type':'AD_V3_P11_CONTROL_ROOM_VIEW_MODEL','schema_version':'1.0.0','report_version':'3.11.0-final-control-room','fixture':bool(fixture),'run':run,'authority':{'deployment_state':(cri.get('promotion') or {}).get('state','SHADOW_COMMISSIONING'),'authority_mode':run.get('authority_mode'),'trade_execution_authority':'NONE','badge':'TEST FIXTURE — NOT LIVE' if fixture else ('PRODUCTION V3' if (cri.get('promotion') or {}).get('state')=='PRODUCTION_V3' else 'V3 SHADOW COMMISSIONING')},'executive':{'direction':direction,'direction_human':label(direction),'pressure_strength':d.get('pressure_strength','UNKNOWN'),'pressure_strength_human':label(d.get('pressure_strength')),'dominance':d.get('dominance_state','UNKNOWN'),'dominance_human':label(d.get('dominance_state')),'dominance_robustness':d.get('dominance_robustness','NOT_APPLICABLE'),'model_sensitivity':d.get('model_sensitivity','NOT_APPLICABLE'),'dominant_root':d.get('dominant_root'),'dominant_root_human':_root_label(d.get('dominant_root')),'dominant_root_magnitude':d.get('dominant_root_magnitude','UNKNOWN'),'dominant_root_health_state':((d.get('dominant_root_health') or {}).get('state') or 'UNKNOWN'),'dominant_root_importance':d.get('dominant_root_importance','UNKNOWN'),'breadth':d.get('breadth','UNKNOWN'),'fragility':d.get('fragility','UNKNOWN'),'contradiction':d.get('contradiction','UNKNOWN'),'consumption':d.get('consumption','UNKNOWN'),'edge':d.get('edge_state','NO_EDGE'),'permission':perm,'permission_human':label(perm),'headline':_headline(d,blocked),'summary':_summary(d,trans,events),'blockers':d.get('blockers') or [],'fragility_reasons':d.get('fragility_reasons') or [],'missing_driver_risk':d.get('missing_driver_risk'),'analysis_blocked':blocked},'what_changed':_comparison(cri,previous_input),'drivers':[x for x in roots if x['role']!='BACKGROUND'][:(cfg('presentation_policy.json') or {}).get('max_prominent_drivers',5)],'pressure_planes':p3.get('pressure_planes') or {},'price_transmission':trans,'lifecycle':p3.get('lifecycle') or {},'watch_next':_watch(d,kernel,trans,events,fwd),'invalidation':d.get('invalidation_conditions') or [],'events':events,'roots':roots,'data_health':{'analysis_admission':kh.get('overall_analysis_admission') or kernel.get('analysis_admission'),'live_kernel_health':kh.get('live_kernel_health'),'live_kernel_total':kh.get('live_kernel_total',0),'live_kernel_fresh':kh.get('live_kernel_fresh',0),'context_health':kh.get('context_health'),'context_total':kh.get('context_total',0),'context_valid':kh.get('context_valid',0),'escalation_health':kh.get('escalation_health'),'freshness_counts':kh.get('freshness_state_counts') or {},'cache_reuse':(kernel.get('performance') or {}).get('context_reused',0),'network_requests':(kernel.get('performance') or {}).get('network_requests',0),'acquisition_ms':(kernel.get('performance') or {}).get('total_p07_ms'),'gaps':gaps},'semantic_health':{'mode':bundle.get('adjudication_mode'),'validation_status':semrec.get('status') or semmeta.get('validation_status'),'requests':semrec.get('request_count') or semrec.get('requested_count') or ((semantic.get('packet') or {}).get('item_count')) or 0,'validated':semrec.get('validated_count') or semmeta.get('validated_count',0),'unknown':semrec.get('unknown_count') or semmeta.get('unknown_count',0),'rejected':semrec.get('rejected_count') or semmeta.get('rejected_count',0),'fallback':semrec.get('fallback_count') or semmeta.get('fallback_count',0),'model_host_state':semmeta.get('model_host_state')},'forward':{'cohort_id':cohort.get('cohort_id') or stats.get('active_cohort'),'cohort_state':cohort.get('state'),'prediction_count':stats.get('raw_prediction_count',0),'episode_count':stats.get('episode_count',0),'mature_episode_count':stats.get('mature_episode_count',0),'pending_count':stats.get('pending_prediction_count',0),'mature_unevaluated_count':stats.get('mature_unevaluated_count',0),'evidence_state':stats.get('forward_evidence_state','NO_SAMPLES'),'qualification':cri.get('forward_qualification') or {},'direction_state':stats.get('direction_calibration_state','INSUFFICIENT'),'strength_state':stats.get('strength_calibration_state','INSUFFICIENT'),'dominance_state':stats.get('dominance_calibration_state','INSUFFICIENT'),'edge_state':stats.get('edge_calibration_state','INSUFFICIENT'),'permission_state':stats.get('permission_calibration_state','INSUFFICIENT'),'wait_state':stats.get('wait_calibration_state','INSUFFICIENT'),'consumption_state':stats.get('consumption_calibration_state','INSUFFICIENT'),'fragility_state':stats.get('fragility_calibration_state','INSUFFICIENT'),'missing_driver_state':stats.get('missing_driver_calibration_state','INSUFFICIENT'),'prediction':fwd.get('prediction'),'new_outcomes':fwd.get('new_outcomes') or [],'legacy':((fwd.get('evaluation_before_current_run') or {}).get('legacy') or {})},'evidence':evidence,'audit':{'run_id':run.get('run_id'),'decision_time':run.get('decision_time'),'horizon':run.get('horizon'),'runtime_version':run.get('runtime_version'),'promotion_state':(cri.get('promotion') or {}).get('state'),'authority_mode':run.get('authority_mode'),'lineage':cri.get('lineage') or {},'warnings':cri.get('warnings') or [],'input_sha256':sha_obj(cri),'seal_status':'PENDING_P10_SEAL','stage_timings':cri.get('stage_timings') or []},'comparison_state':{'causal_direction':direction,'pressure_strength':d.get('pressure_strength'),'dominance_state':d.get('dominance_state'),'dominance_robustness':d.get('dominance_robustness'),'model_sensitivity':d.get('model_sensitivity'),'dominant_root':d.get('dominant_root'),'permission_candidate':perm,'edge_state':d.get('edge_state'),'consumption':d.get('consumption'),'fragility':d.get('fragility'),'contradiction':d.get('contradiction'),'analysis_admission':kh.get('overall_analysis_admission'),'semantic_mode':bundle.get('adjudication_mode')}}
 return vm
