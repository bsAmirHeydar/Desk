from pathlib import Path
from .util import load_json,uid,norm

CLASSES=['DESCRIPTIVE_STATE_ESTIMATION','EVENT_ANALYSIS','CAUSAL_ATTRIBUTION','DIRECTIONAL_FORECAST','PERSISTENCE_REVERSAL','NARRATIVE_ATTENTION','REGIME_ANALYSIS','STRUCTURAL_LONG_HORIZON_THESIS','CROSS_SECTIONAL_RELATIVE_VALUE','EXPOSURE_RISK_ANALYSIS','MODEL_VALIDATION','ANOMALY_FAILURE_INVESTIGATION','NEW_ASSET_RESEARCH']
PATTERNS=[
 ('ANOMALY_FAILURE_INVESTIGATION',['why was','wrong','failure','mistake','اشتباه','خطا','چرا غلط','چرا اشتباه']),
 ('CROSS_SECTIONAL_RELATIVE_VALUE',['compare','relative','versus',' vs ','مقایسه','نسبی','در برابر']),
 ('CAUSAL_ATTRIBUTION',['why ','what drove','what caused','cause','causal','چرا','علت','عامل حرکت','باعث']),
 ('EVENT_ANALYSIS',['cpi','nfp','fomc','ecb','fed meeting','event','release','after ','بعد از','پس از','خبر','جلسه']),
 ('NARRATIVE_ATTENTION',['narrative','attention','market care','what matters','روایت','توجه بازار','بازار به چی','بازار به چه']),
 ('REGIME_ANALYSIS',['regime','رژیم','فاز بازار']),
 ('STRUCTURAL_LONG_HORIZON_THESIS',['structural','long term','long-term','بلندمدت','ساختاری','چرخه‌ای']),
 ('EXPOSURE_RISK_ANALYSIS',['exposure','tail risk','fragility','risk concentration','ریسک','شکنندگی','اکسپوژر']),
 ('MODEL_VALIDATION',['validate model','model validation','اعتبار مدل','مدل را بررسی']),
 ('PERSISTENCE_REVERSAL',['continue','persistence','remaining pressure','remain','reversal','will it last','ادامه','ماندگار','باقی مانده','باقی مونده','فشار باقی','چقدر مونده','چقدر مانده','مونده','مانده','برگشت','ریورسال']),
 ('DIRECTIONAL_FORECAST',['direction','bullish','bearish','buy','sell','جهت','صعودی','نزولی','خرید','فروش']),
 ('DESCRIPTIVE_STATE_ESTIMATION',['state','status','analyze','analyse','current','today','وضعیت','بررسی','تحلیل','امروز'])]
HORIZONS=[
 ('MICRO_0_15M',['0-15','15m','۱۵ دقیقه','پانزده دقیقه']),('SHORT_15_60M',['15-60','1h','hour','ساعتی','یک ساعت']),('SESSION_1_6H',['session','جلسه معاملاتی','سشن']),('MULTI_DAY_2_10D',['multi-day','next days','چند روز','هفته جاری']),('SWING_2_8W',['swing','سوئینگ','چند هفته']),('STRUCTURAL',['structural','long term','بلندمدت','ساختاری'])]

def _subjects(v,raw):
    cfg=load_json(Path(v)/'RUNTIME'/'R3 Operational Execution and Learning OS'/'config'/'launcher_profiles.json');aliases={k.upper():val for k,val in cfg['aliases'].items()};prod=set(cfg['production_instruments'])
    vals=raw if isinstance(raw,list) else [x.strip() for x in str(raw).split(',') if x.strip()]
    out=[]
    for x in vals:
        u=str(x).strip().upper();canon=aliases.get(u);status='CERTIFIED_RUNTIME_SUBJECT' if canon in prod else ('RESEARCH_SUPPORTED_UNCERTIFIED' if u else 'UNKNOWN_SUBJECT')
        out.append({'input':x,'canonical':canon or u,'status':status})
    return out

def compile_request(vault_root,request):
    v=Path(vault_root).resolve();req=dict(request);req.setdefault('schema_version','1.0.0');rid=req.get('request_id') or uid('REQ');req['request_id']=rid
    original_text=str(req.get('request_text') or '').strip();n=norm(original_text);subs=_subjects(v,req.get('subject'));reasons=[]
    explicit=req.get('research_class');classes=[]
    if explicit:
        e=str(explicit).upper().replace('-','_').replace(' ','_')
        if e not in CLASSES:raise RuntimeError('unknown research_class: '+e)
        classes=[e];reasons.append('explicit research_class')
    for cls,keys in PATTERNS:
        if any(norm(k) in n for k in keys) and cls not in classes:classes.append(cls);reasons.append('semantic cue -> '+cls)
    if any(x['status']=='RESEARCH_SUPPORTED_UNCERTIFIED' for x in subs):
        if 'NEW_ASSET_RESEARCH' not in classes:classes.insert(0,'NEW_ASSET_RESEARCH')
        reasons.append('subject outside certified runtime -> NEW_ASSET_RESEARCH')
    if not classes:classes=['DESCRIPTIVE_STATE_ESTIMATION'];reasons.append('safe low-assumption fallback')
    priority=['ANOMALY_FAILURE_INVESTIGATION','CROSS_SECTIONAL_RELATIVE_VALUE','CAUSAL_ATTRIBUTION','EVENT_ANALYSIS','MODEL_VALIDATION','NEW_ASSET_RESEARCH','EXPOSURE_RISK_ANALYSIS','REGIME_ANALYSIS','STRUCTURAL_LONG_HORIZON_THESIS','PERSISTENCE_REVERSAL','DIRECTIONAL_FORECAST','NARRATIVE_ATTENTION','DESCRIPTIVE_STATE_ESTIMATION']
    primary=min(classes,key=lambda c:priority.index(c) if c in priority else 999)
    mode=str(req.get('mode') or 'LIVE').upper();asof=req.get('historical_cutoff') or req.get('as_of')
    rmode={'LIVE':'LIVE','SHADOW':'SHADOW_LIVE','HISTORICAL':'HISTORICAL_REPLAY','WALK_FORWARD':'RESEARCH_REPLAY','REPLAY':'RESEARCH_REPLAY'}.get(mode)
    if mode=='DEEP_RESEARCH':rmode='HISTORICAL_REPLAY' if asof and str(asof).upper()!='NOW' else 'LIVE'
    if rmode is None:raise RuntimeError('unsupported interface mode: '+mode)
    if rmode in ('HISTORICAL_REPLAY','RESEARCH_REPLAY') and not asof:raise RuntimeError(mode+' requires as_of/historical_cutoff')
    horizon=req.get('horizon') or None
    if not horizon:
        for h,keys in HORIZONS:
            if any(norm(k) in n for k in keys):horizon=h;break
    horizon=horizon or 'DAILY_OPEN_TO_CLOSE'
    depth=str(req.get('depth') or 'AUTO').upper()
    if depth=='AUTO' and any(k in n for k in ['عمیق','مفصل','کامل','deep','detailed','complete']):depth='DEEP';reasons.append('explicit depth language')
    profile=str(req.get('output_profile') or 'EXPLORER').upper();locale=req.get('locale') or ('fa-IR' if any('\u0600'<=ch<='\u06ff' for ch in original_text) else 'en-US')
    all_cert=all(x['status']=='CERTIFIED_RUNTIME_SUBJECT' for x in subs)
    elig='CERTIFIED_RUNTIME' if all_cert else ('RESEARCH_ONLY_UNCERTIFIED' if any(x['status']=='RESEARCH_SUPPORTED_UNCERTIFIED' for x in subs) else 'UNKNOWN_SUBJECT')
    tags=list(req.get('intent_tags') or []);tags += ['research_class:'+primary,'interface_request:'+rid,'interface:UI1.0.0']+[('secondary_intent:'+c) for c in classes if c!=primary]
    if len(subs)>1:tags.append('multi-intent-subjects')
    return {'schema_version':'1.0.0','request_id':rid,'original_request':req,'resolved_subjects':subs,'primary_research_class':primary,'research_classes':classes,'mode':mode,'r3_run_mode':rmode,'analysis_cutoff':asof or 'NOW','active_horizon':horizon,'depth':depth,'output_profile':profile,'locale':locale,'intent_tags':tags,'execution_eligibility':elig,'universe_scope':req.get('universe_scope') or ('MULTI_MARKET' if len(subs)>1 else 'SINGLE'),'compiler_rationale':reasons,'authority':{'direction':'NONE','permission':'NONE','broker_write':'NONE'}}
