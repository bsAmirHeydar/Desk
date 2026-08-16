from __future__ import annotations
from pathlib import Path
from copy import deepcopy
from .common import SCHEMA_ID, SCHEMA_VERSION, PHASE, CONTRACT, hobj, now_utc, load_json, unknown

LAYER_ORDER = [
    ('timing','زمان‌بندی','Timing','زمان و رویدادهایی که می‌توانند رفتار طلا را تغییر دهند.'),
    ('fundamental','فاندامنتال','Fundamental','ریشه‌های اقتصادی و ساختاری که فشار اصلی طلا را می‌سازند.'),
    ('expectations_policy','انتظارات / سیاست / رژیم','Expectations / Policy / Regime','آنچه بازار از سیاست پولی، نرخ‌ها و آینده انتظار دارد.'),
    ('narrative_consumption','روایت / بازقیمت‌گذاری / مصرف','Narrative / Repricing / Consumption','اینکه داستان بازار چقدر تازه است و چه مقدار از اثر Driverها مصرف شده.'),
    ('positioning','پوزیشنینگ','Positioning','چیدمان قبلی بازیگران؛ Context است و به تنهایی Flow یا Direction نیست.'),
    ('flow','فلو واقعی','Actual Flow','شواهد معاملات، فشار تهاجمی، Depth و MBO در صورت دسترسی واقعی.'),
    ('funding','فاندینگ / Plumbing','Funding / Plumbing','فشارهای نقدینگی، Funding، Margin و Collateral که می‌توانند انتقال قیمت را مختل کنند.'),
    ('mechanics','مکانیک بازار / نقدشوندگی / نوسان','Mechanics / Liquidity / Volatility','ساختار بازار، Depth، Options، Expiry و شرایط نوسان/نقدشوندگی.'),
]

PERSIAN_STATE = {
    'NEGATIVE_TRANSMISSION':'انتقال منفی؛ قیمت فعلاً خلاف فشار اصلی حرکت می‌کند.',
    'COMPRESSION':'فشار وجود دارد اما هنوز به حرکت کامل قیمت تبدیل نشده.',
    'DELAYED':'انتقال فشار با تأخیر انجام می‌شود.',
    'ALIGNED':'قیمت با فشار اصلی هماهنگ است.',
    'UNDER_TRANSMISSION':'واکنش قیمت کمتر از انتظار مدل است.',
    'OVER_TRANSMISSION':'واکنش قیمت بیش از انتظار مدل است.',
    'NOT_READY':'هنوز شرایط رهاشدن حرکت اصلی آماده نیست.',
    'WATCH':'شرایط باید زیر نظر بماند؛ هنوز ورود نتیجه نمی‌شود.',
    'PRE_RELEASE':'زمینه‌ی رهاشدن بهتر شده، اما تریگر/Permission جداست.',
    'HIGH_READINESS':'آمادگی رهاشدن بالاست؛ این به تنهایی مجوز معامله نیست.',
}


def _val(obj, *path, default='UNKNOWN'):
    cur = obj
    for key in path:
        if not isinstance(cur, dict):
            return default
        cur = cur.get(key)
    return default if cur in (None,'',[],{}) else cur


def _fresh_state(obs):
    return _val(obs,'freshness','state')


def _source_config(repo):
    p = Path(repo)/'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL/NEXT_VERSION/AD_V2_PHASE_05_GOLD_INTELLIGENCE_SPECIALIZATION/config/gold_source_registry.json'
    if not p.exists(): return {}
    return {x.get('source_id'):x for x in load_json(p).get('sources',[]) if x.get('source_id')}


def _role_metrics(repo):
    p = Path(repo)/'Institutional_Fundamental_Macro_Research_OS_v5_1_FINAL/NEXT_VERSION/AD_V2_PHASE_05_GOLD_INTELLIGENCE_SPECIALIZATION/config/gold_evidence_role_registry.json'
    if not p.exists(): return {}
    return {x.get('metric_id'):x for x in load_json(p).get('metrics',[]) if x.get('metric_id')}


def _layer_for_obs(obs, meta):
    sid = str(obs.get('source_id') or '')
    mid = str(obs.get('metric_id') or '')
    roles = set(obs.get('roles') or meta.get('roles') or [])
    u = (sid+' '+mid+' '+' '.join(roles)).upper()
    if 'CFTC' in u or 'POSITIONING' in u or 'OPEN_INTEREST' in u or mid.endswith('_OI') or 'OI_' in u:
        return 'positioning'
    if 'MBO' in u or 'SIGNED_TRADE' in u or 'AGGRESS' in u or 'ORDER_FLOW' in u:
        return 'flow'
    if 'DEPTH' in u or 'LIQUIDITY' in u or 'OPTIONS' in u or 'VOLAT' in u or 'GAMMA' in u or 'EXPIR' in u:
        return 'mechanics'
    if 'REPO' in u or 'FUNDING' in u or 'DEALER_BALANCE' in u or 'FINANCING' in u or 'COLLATERAL' in u:
        return 'funding'
    if 'FEDWATCH' in u or 'POLICY_REPRICING' in u or 'UST2Y' in u or 'TIPS' in u or 'DXY' in u:
        return 'expectations_policy'
    if 'EVENT' in u or 'AUCTION' in u or 'MACRO' in u or 'BLS' in u:
        return 'timing'
    if 'ETF' in u or 'WGC' in u or 'PHYSICAL' in u or 'OFFICIAL' in u or 'STRUCTURAL' in u:
        return 'fundamental'
    return 'fundamental'


def _root_layer(root):
    s = (str(root.get('source_kind') or '')+' '+str(root.get('root_id') or '')+' '+str(root.get('label') or '')).upper()
    if 'EXPECTATION' in s or 'POLICY' in s or 'RATE' in s or 'USD' in s:
        return 'expectations_policy'
    if 'POSITION' in s:
        return 'positioning'
    if 'FUNDING' in s or 'COLLATERAL' in s or 'FINANC' in s:
        return 'funding'
    return 'fundamental'


def _coverage_state(items):
    if not items: return 'UNKNOWN'
    states = [_fresh_state(x) for x in items]
    if any(x in {'UNAVAILABLE','EXPIRED'} for x in states): return 'PARTIAL'
    if any(x == 'STALE' for x in states): return 'STALE'
    if all(x == 'FRESH' for x in states): return 'FRESH'
    return 'PARTIAL'


def _layer_objects(repo,p02,p03,p04,p05,input_pack):
    metas=_role_metrics(repo); layers={k:{
        'id':k,'title_fa':fa,'title_en':en,'description_fa':desc,'current_state':'UNKNOWN','current_signal':'UNKNOWN',
        'day_trading_relevance':'UNKNOWN','evidence':[],'contradictions':[],'freshness':'UNKNOWN','coverage':'UNKNOWN',
        'confidence':'UNKNOWN','missing_data':[],'changed_since_previous':[],'provenance':[],'decision_relevant':'UNKNOWN'
    } for k,fa,en,desc in LAYER_ORDER}
    roots = p02.get('causal_root_ledger') or []
    for r in roots:
        lid=_root_layer(r); item={'type':'CAUSAL_ROOT','root_id':r.get('root_id'),'label':r.get('label'),'polarity':r.get('polarity'),'source_kind':r.get('source_kind'),'mechanism':r.get('mechanism'),'freshness':_val(r,'freshness','state'),'confidence':r.get('confidence'),'independence_group':r.get('independence_group'),'observed_at_utc':r.get('observed_at_utc'),'owner':'AD-V2-P02'}
        layers[lid]['evidence'].append(item);layers[lid]['provenance'].append({'owner':'AD-V2-P02','field':'causal_root_ledger','root_id':r.get('root_id')})
        if r.get('polarity') and r.get('polarity') != _val(p02,'pressure_core','sign'):
            layers[lid]['contradictions'].append(item)
    obs = p05.get('admitted_observations') or []
    raw_obs = {x.get('observation_id'):x for x in ((input_pack or {}).get('gold_observations') or []) if x.get('observation_id')}
    for o in obs:
        meta=metas.get(o.get('metric_id'),{});lid=_layer_for_obs(o,meta); raw=raw_obs.get(o.get('observation_id'),{})
        item={'type':'OBSERVATION','observation_id':o.get('observation_id'),'metric_id':o.get('metric_id'),'source_id':o.get('source_id'),'roles':o.get('roles'),'status':o.get('status'),'freshness':_val(o,'freshness','state'),'age_seconds':_val(o,'freshness','age_seconds'),'provider_id':o.get('provider_id') or raw.get('provider_id'),'observed_at_utc':raw.get('observed_at_utc'),'state_code':raw.get('state_code'),'strength':raw.get('strength'),'confidence':raw.get('confidence'),'value':raw.get('value'),'provenance_ref':raw.get('provenance_ref'),'owner':'AD-V2-P05'}
        layers[lid]['evidence'].append(item);layers[lid]['provenance'].append({'owner':'AD-V2-P05','field':'admitted_observations','observation_id':o.get('observation_id')})
    # Timing includes governed event/reset and response-window state, never direction.
    layers['timing']['evidence'].append({'type':'RESPONSE_WINDOW','window':p03.get('response_window'),'expected_signature':p03.get('expected_signature_reference'),'owner':'AD-V2-P03'})
    for ev in ((p05.get('event_reset') or {}).get('events') or []): layers['timing']['evidence'].append({'type':'EVENT','event':ev,'owner':'AD-V2-P05'})
    # Narrative/consumption is an explicit canonical P02 field.
    layers['narrative_consumption']['evidence'].append({'type':'DRIVER_CONSUMPTION','value':p02.get('fundamental_driver_consumption'),'owner':'AD-V2-P02'})
    layers['narrative_consumption']['provenance'].append({'owner':'AD-V2-P02','field':'fundamental_driver_consumption'})
    # Mechanics gets event cap and P04 hypotheses as hypotheses, not facts.
    layers['mechanics']['evidence'].append({'type':'EVENT_RESET','value':p05.get('event_reset'),'owner':'AD-V2-P05'})
    layers['mechanics']['evidence'].append({'type':'LIQUIDITY_HYPOTHESES','value':p04.get('liquidity_hypotheses'),'owner':'AD-V2-P04','hypothesis_only':True})
    # Deterministic presentation coverage only; no market direction is synthesized.
    for lid,layer in layers.items():
        obs_items=[x for x in layer['evidence'] if x.get('type')=='OBSERVATION']
        root_items=[x for x in layer['evidence'] if x.get('type')=='CAUSAL_ROOT']
        layer['coverage']='AVAILABLE' if layer['evidence'] else 'UNKNOWN'
        layer['freshness']=_coverage_state(obs_items) if obs_items else ('FRESH' if root_items and all(x.get('freshness')=='FRESH' for x in root_items) else ('PARTIAL' if root_items else 'UNKNOWN'))
        layer['current_state']='ACTIVE' if layer['evidence'] else 'UNKNOWN'
        layer['confidence']='UNKNOWN'
        layer['decision_relevant']=True if lid in {'timing','fundamental','expectations_policy','flow','mechanics'} and layer['evidence'] else False
        layer['day_trading_relevance']={'timing':'VERY_HIGH','fundamental':'VERY_HIGH','expectations_policy':'VERY_HIGH','narrative_consumption':'HIGH','positioning':'CONTEXT','flow':'VERY_HIGH','funding':'CONDITIONAL_HIGH','mechanics':'HIGH'}[lid]
    # Special truth flags.
    flow_obs=[x for x in layers['flow']['evidence'] if x.get('type')=='OBSERVATION']
    true_flow=any(('SIGNED_TRADE' in str(x.get('metric_id')) or 'MBO' in str(x.get('metric_id')) or 'AGGRESS' in str(x.get('metric_id'))) and x.get('freshness')=='FRESH' for x in flow_obs)
    volume_only=any('VOLUME' in str(x.get('metric_id')) for x in (p05.get('admitted_observations') or [])) and not true_flow
    if not true_flow:
        layers['flow']['coverage']='PARTIAL' if flow_obs or volume_only else 'UNKNOWN'
        layers['flow']['missing_data'].append('TRUE_ORDER_FLOW_NOT_OBSERVED')
    layers['flow']['current_signal']='OBSERVED_TRUE_FLOW' if true_flow else 'NO_TRUE_FLOW_SIGNAL'
    if volume_only: layers['flow']['missing_data'].append('VOLUME_AVAILABLE_BUT_NOT_FLOW')
    return [layers[k] for k,_,_,_ in LAYER_ORDER]


def _data_health(repo,p05,layers):
    source_cfg=_source_config(repo); admitted=p05.get('admitted_observations') or []; by_source={}
    for o in admitted: by_source.setdefault(o.get('source_id'),[]).append(o)
    important=['XAUUSD_RUNTIME_FEED','GC_RUNTIME_FEED','DXY_RUNTIME_FEED','UST2Y_RUNTIME_FEED','UST10Y_TIPS_RUNTIME_FEED','SILVER_RUNTIME_FEED','CME_FEDWATCH','CFTC_COT','CME_VOLUME_OI','CME_MARKET_DEPTH','WGC_ETF','LBMA_TRADE_DATA','NYFED_REPO_RRP','GOLD_FINANCING_EVIDENCE']
    rows=[]
    for sid in important:
        cfg=source_cfg.get(sid,{}) ; obs=by_source.get(sid,[])
        freshness=_coverage_state(obs) if obs else 'UNKNOWN'
        availability='AVAILABLE' if obs else 'UNAVAILABLE_OR_NOT_CONNECTED'
        rows.append({'source_id':sid,'data_family':cfg.get('coverage','UNKNOWN'),'freshness':freshness,'expected_cadence':cfg.get('cadence','UNKNOWN'),'availability':availability,'coverage':'OBSERVED' if obs else 'UNKNOWN','confidence':'UNKNOWN','access_class':cfg.get('access','UNKNOWN'),'hard_boundary':cfg.get('hard_boundary'),'layer_can_use':bool(obs),'observations':len(obs)})
    flow=next(x for x in layers if x['id']=='flow')
    overall='PARTIAL' if flow['coverage']!='AVAILABLE' or p05.get('coverage_gaps') else ('FRESH' if any(r['freshness']=='FRESH' for r in rows) else 'UNKNOWN')
    return {'overall':overall,'sources':rows,'coverage_gaps':deepcopy(p05.get('coverage_gaps') or {}),'registered_source_is_not_assumed_available':True}


def _context(input_pack,p03,p05):
    target=((input_pack or {}).get('actual_response') or {}).get('target') or p03.get('target_response') or {}
    channels=((input_pack or {}).get('actual_response') or {}).get('channels') or ((p03.get('pathway_diagnostics') or {}).get('channels') or [])
    ch={x.get('channel_id'):x for x in channels if isinstance(x,dict)}
    raw=((input_pack or {}).get('gold_observations') or [])
    def metric(mid):
        for x in raw:
            if x.get('metric_id')==mid:return x
        return None
    items=[
      {'id':'XAUUSD','label':'XAUUSD','value':target.get('observed_response'),'unit':target.get('unit'),'status':target.get('data_quality') or 'UNKNOWN','note':'Observed response; not necessarily current spot price.'},
      {'id':'GC','label':'GC Futures','value':_val(ch.get('GC_PROXY',{}),'observed_direction'),'unit':'DIRECTION','status':'AVAILABLE' if ch.get('GC_PROXY') else 'UNKNOWN'},
      {'id':'DXY','label':'DXY','value':_val(ch.get('DXY',{}),'observed_direction'),'unit':'DIRECTION','status':'AVAILABLE' if ch.get('DXY') else 'UNKNOWN'},
      {'id':'US2Y','label':'US 2Y','value':_val(ch.get('US2Y',{}),'observed_direction'),'unit':'DIRECTION','status':'AVAILABLE' if ch.get('US2Y') else 'UNKNOWN'},
      {'id':'REAL_YIELD','label':'Real Yield','value':_val(ch.get('REAL10Y',{}),'observed_direction'),'unit':'DIRECTION','status':'AVAILABLE' if ch.get('REAL10Y') else 'UNKNOWN'},
      {'id':'SILVER','label':'Silver','value':(metric('SILVER_PRICE_RESPONSE') or {}).get('value'),'unit':'OBSERVED','status':'AVAILABLE' if metric('SILVER_PRICE_RESPONSE') else 'UNKNOWN'},
    ]
    return items


def _persian_interpretation(p02,p03,p04,execution):
    sign=_val(p02,'pressure_core','sign'); pclass=_val(p02,'pressure_core','class'); trans=_val(p03,'transmission_state','state'); maturity=_val(p04,'opposing_move_maturity','state'); readiness=_val(p04,'release_readiness','state'); perm=execution.get('permission') or 'UNKNOWN'
    direction={'BUY':'خرید','SELL':'فروش'}.get(sign,'نامشخص')
    trans_text=PERSIAN_STATE.get(trans,f'وضعیت انتقال فشار {trans} است.')
    return f'فشار اصلی فعلاً به سمت {direction} است ({pclass}). {trans_text} بلوغ حرکت مخالف {maturity} و آمادگی رهاشدن {readiness} است. Permission فعلی {perm} است و مستقل از Readiness باقی می‌ماند.'


def _what_matters(p02,p03,p04,p05,execution,data_health):
    rows=[]
    rows.append(f"Pressure: {_val(p02,'pressure_core','class')} | Trend: {_val(p02,'pressure_dynamics','trend')}")
    rows.append(f"Transmission: {_val(p03,'transmission_state','state')} | Residual: {_val(p03,'counterfactual_residual','magnitude_class')}")
    if _val(p03,'missing_driver_escalation','level') not in {'NONE','UNKNOWN'}: rows.append(f"Missing-driver escalation: {_val(p03,'missing_driver_escalation','level')}")
    rows.append(f"Release readiness: {_val(p04,'release_readiness','state')} | Permission: {execution.get('permission','UNKNOWN')}")
    if data_health.get('overall')!='FRESH': rows.append(f"Data health: {data_health.get('overall')}; gaps must remain explicit.")
    return rows[:5]


def _invalidations(p02,p03,p04):
    explicit=[]
    for r in p02.get('causal_root_ledger') or []:
        if r.get('polarity') and r.get('polarity') != _val(p02,'pressure_core','sign'):
            explicit.append({'type':'CURRENT_OPPOSING_ROOT','label':r.get('label'),'polarity':r.get('polarity'),'mechanism':r.get('mechanism'),'owner':'AD-V2-P02'})
    blockers=p04.get('research_blockers') or []
    for b in blockers: explicit.append({'type':'RESEARCH_BLOCKER','value':b,'owner':'AD-V2-P04'})
    if not explicit:
        return [{'type':'NO_GOVERNED_INVALIDATION_CONDITION','text_fa':'شرط ابطال صریح در داده‌ی upstream تعریف نشده؛ نیازمند شواهد بیشتر است.'}]
    return explicit


def _audit(p02,p03,p04,p05,layers,execution):
    flow=next(x for x in layers if x['id']=='flow')
    admitted=p05.get('admitted_observations') or []
    has_volume=any('VOLUME' in str(x.get('metric_id')) for x in admitted)
    has_true_flow=flow.get('current_signal')=='OBSERVED_TRUE_FLOW'
    return {
      'price_pressure_contamination_detected': bool((p02.get('integrity') or {}).get('target_price_contamination')),
      'volume_flow_substitution_detected': False,
      'oi_direction_substitution_detected': False,
      'missing_driver_escalation': _val(p03,'missing_driver_escalation','level'),
      'stale_critical_data': any(_fresh_state(x) in {'STALE','EXPIRED'} for x in admitted),
      'partial_flow_coverage': not has_true_flow,
      'volume_available_without_true_flow': bool(has_volume and not has_true_flow),
      'permission_source': execution.get('permission_source','UNKNOWN'),
      'science_owner_integrity': 'PASS' if p02.get('phase')=='AD-V2-P02' and p03.get('phase')=='AD-V2-P03' and p04.get('phase')=='AD-V2-P04' and p05.get('phase')=='AD-V2-P05' else 'FAIL',
      'checklist_fa':[
        'سه Driver اصلی Pressure چه هستند؟','کدام Driverها واقعاً مستقل‌اند؟','آیا Price طلا وارد محاسبه Pressure شده؟','کدام داده‌ها Fresh / Stale / Partial هستند؟','Positioning فقط Context است یا اشتباهاً Direction ساخته؟','آیا Volume با Flow اشتباه شده؟','چرا Transmission این State را گرفته؟','Unreleased Pressure بر چه شواهدی تکیه دارد؟','چه شواهد مستقلی Maturity را تأیید می‌کنند؟','چه چیزی می‌تواند Thesis را باطل کند؟'
      ]
    }


def _history(data_root,current):
    root=Path(data_root)/'alpha_desk_v2'/'control_room'/'runs'
    rows=[]
    if root.exists():
        for p in sorted(root.glob('*/control_room.json'),key=lambda x:x.stat().st_mtime,reverse=True)[:5]:
            try:
                o=load_json(p);ov=o.get('overview') or {};rows.append({'run_id':_val(o,'run','run_id'),'as_of':_val(o,'run','as_of'),'pressure':ov.get('directional_pressure'),'transmission':ov.get('price_transmission'),'maturity':ov.get('opposing_move_maturity'),'readiness':ov.get('release_readiness'),'permission':ov.get('trade_permission')})
            except Exception: pass
    rows.reverse(); rows.append({'run_id':current['run_id'],'as_of':current['as_of'],'pressure':current['pressure'],'transmission':current['transmission'],'maturity':current['maturity'],'readiness':current['readiness'],'permission':current['permission']})
    return rows[-6:]


def build_control_room(repo,p11_receipt,*,input_pack=None,data_root=None):
    p10=(p11_receipt or {}).get('p10_receipt') or {}
    if p10.get('status')!='PASS': raise ValueError('valid P10 receipt required')
    p02=deepcopy(p10.get('p02') or {});p03=deepcopy(p10.get('p03') or {});p04=deepcopy(p10.get('p04') or {});p05=deepcopy(p10.get('p05') or {});state=deepcopy(((p10.get('p06') or {}).get('state')) or {})
    execution=deepcopy(state.get('execution') or {})
    layers=_layer_objects(repo,p02,p03,p04,p05,input_pack or {})
    dh=_data_health(repo,p05,layers)
    changes=deepcopy((state.get('change_set') or {}).get('items') or [])
    pressure={'sign':_val(p02,'pressure_core','sign'),'class':_val(p02,'pressure_core','class'),'magnitude_class':_val(p02,'pressure_core','magnitude_class'),'signed_range':_val(p02,'pressure_core','signed_range'),'trend':_val(p02,'pressure_dynamics','trend'),'acceleration':_val(p02,'pressure_dynamics','acceleration'),'persistence':_val(p02,'persistence','value'),'freshness':_val(p02,'freshness_and_coverage','class'),'driver_consumption':_val(p02,'fundamental_driver_consumption','value'),'remaining_causal_pressure':_val(p02,'remaining_causal_pressure','value'),'contradiction_load':_val(p02,'contradiction_load','class'),'root_coverage':_val(p02,'freshness_and_coverage','root_coverage_weight'),'confidence':_val(p02,'pressure_confidence','class'),'drivers':deepcopy(p02.get('causal_root_ledger') or []),'owner':'AD-V2-P02','source_state_hash':hobj(p02)}
    transmission={'state':_val(p03,'transmission_state','state'),'efficiency':_val(p03,'transmission_efficiency','class'),'expected_signature':deepcopy(p03.get('expected_signature_reference')),'actual_response':deepcopy(p03.get('target_response')),'response_window':deepcopy(p03.get('response_window')),'counterfactual_residual':deepcopy(p03.get('counterfactual_residual')),'pathway_diagnostics':deepcopy(p03.get('pathway_diagnostics')),'missing_driver_escalation':deepcopy(p03.get('missing_driver_escalation')),'model_disagreement':deepcopy(p03.get('model_disagreement')),'confidence':_val(p03,'transmission_confidence','class'),'owner':'AD-V2-P03','source_state_hash':hobj(p03)}
    release={'unreleased_pressure':deepcopy(p04.get('unreleased_pressure')) if p04.get('unreleased_pressure') is not None else 'UNKNOWN','latent_causal_reserve':deepcopy(p04.get('latent_causal_reserve')) if p04.get('latent_causal_reserve') is not None else 'UNKNOWN','opposing_move_maturity':deepcopy(p04.get('opposing_move_maturity')) if p04.get('opposing_move_maturity') is not None else 'UNKNOWN','transmission_inflection':deepcopy(p04.get('transmission_inflection')) if p04.get('transmission_inflection') is not None else 'UNKNOWN','release_readiness':deepcopy(p04.get('release_readiness')) if p04.get('release_readiness') is not None else 'UNKNOWN','lifecycle':deepcopy(p04.get('release_lifecycle')) if p04.get('release_lifecycle') is not None else 'UNKNOWN','event_reset':deepcopy(p05.get('event_reset')) if p05.get('event_reset') is not None else 'UNKNOWN','liquidity_hypotheses':deepcopy(p04.get('liquidity_hypotheses')) if p04.get('liquidity_hypotheses') is not None else 'UNKNOWN','research_blockers':deepcopy(p04.get('research_blockers')) if p04.get('research_blockers') is not None else [],'owner':'AD-V2-P04','source_state_hash':hobj(p04)}
    current={'run_id':state.get('run_id') or p10.get('run_id'),'as_of':state.get('as_of') or p04.get('as_of_utc'),'pressure':pressure['class'],'transmission':transmission['state'],'maturity':_val(p04,'opposing_move_maturity','state'),'readiness':_val(p04,'release_readiness','state'),'permission':execution.get('permission','UNKNOWN')}
    hist=_history(data_root,current) if data_root else [current]
    overview={'directional_pressure':pressure['class'],'pressure_sign':pressure['sign'],'pressure_magnitude_class':pressure['magnitude_class'],'pressure_trend':pressure['trend'],'persistence':pressure['persistence'],'driver_consumption':pressure['driver_consumption'],'remaining_causal_pressure':pressure['remaining_causal_pressure'],'price_transmission':transmission['state'],'unreleased_pressure':_val(p04,'unreleased_pressure','class'),'opposing_move_maturity':current['maturity'],'release_readiness':current['readiness'],'technical_trigger':'UNKNOWN','trade_permission':execution.get('permission','UNKNOWN'),'data_health':dh['overall'],'last_run_time':current['as_of'],'lifecycle':_val(p04,'release_lifecycle','state'),'what_matters_now':_what_matters(p02,p03,p04,p05,execution,dh),'current_interpretation':_persian_interpretation(p02,p03,p04,execution),'changed_since_previous_run':changes,'invalidation_conditions':_invalidations(p02,p03,p04),'market_context':_context(input_pack or {},p03,p05)}
    obj={'schema_id':SCHEMA_ID,'schema_version':SCHEMA_VERSION,'contract':CONTRACT,'output_contract_version':'1.0.0','renderer_version':'1.0.0','generated_at':now_utc(),'identity':{'product':'ALPHA DESK V2','desk':'GOLD CONTROL ROOM','subject':'XAUUSD','gold_only':True,'language':'fa-IR','direction':'rtl'},'run':{'run_id':current['run_id'],'as_of':current['as_of'],'horizon':state.get('horizon') or p02.get('active_horizon'),'mode':state.get('mode') or p11_receipt.get('mode'),'p11_mode':p11_receipt.get('mode'),'p10_receipt_hash':p10.get('receipt_hash'),'canonical_v2_state_hash':state.get('canonical_v2_state_hash')},'authority':{'v1':'AUTHORITATIVE','v2':'SHADOW','presentation_science_authority':'NONE','trade_permission':execution.get('permission','UNKNOWN'),'permission_source':execution.get('permission_source','UNKNOWN'),'v2_override_allowed':False,'broker':'NONE','auto_promotion':False},'overview':overview,'pressure':pressure,'transmission':transmission,'release':release,'layers':layers,'events':{'event_reset':deepcopy(p05.get('event_reset')),'response_window':deepcopy(p03.get('response_window')),'expected_signature':deepcopy(p03.get('expected_signature_reference')),'next_major_event':'UNKNOWN'},'memory':{'changes':changes,'timeline':hist,'portable_memory':deepcopy(state.get('portable_memory'))},'audit':_audit(p02,p03,p04,p05,layers,execution),'data_health':dh,'provenance':{'upstream_state_hashes':{'p02':hobj(p02),'p03':hobj(p03),'p04':hobj(p04),'p05':hobj(p05),'p06':state.get('canonical_v2_state_hash') or hobj(state)},'owners':{'pressure':'AD-V2-P02','transmission':'AD-V2-P03','release':'AD-V2-P04','gold':'AD-V2-P05','memory':'AD-V2-P06','permission':'V1_BASE_CAPSULE'},'presentation_only':True}}
    content=deepcopy(obj);content.pop('generated_at',None);obj['canonical_content_hash']=hobj(content)
    return obj
