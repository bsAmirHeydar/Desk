from pathlib import Path
import json
from .compiler import compile_request
from .render import explorer_html
from .simple_language import to_fa,causal_status_text

def _fixture():
    cards=[];sections={}
    ids=[('timing','زمان و موقعیت بازار'),('fundamental','وضعیت بنیادی'),('expectations','انتظارات، سیاست و شرایط کلی'),('narrative','روایت و ذهن بازار'),('positioning','موقعیت معامله‌گران'),('flow','جریان واقعی خرید و فروش'),('funding','نقدینگی و تأمین مالی'),('mechanics','ساختار و رفتار بازار')]
    for sid,title in ids:
        deep={'section_id':sid,'title_fa':title,'simple_result_fa':'نتیجه ساده و قابل فهم.','observations_fa':['یک مشاهده'],'why_it_matters_fa':['چون روی بازار اثر دارد.'],'support_fa':['شاهد تأییدکننده'],'opposition_fa':['شاهد مخالف'],'unknowns_fa':['یک مورد هنوز نامشخص است.'],'mechanism_fa':['مکانیزم محتمل'],'relation_to_direction_fa':'تأیید می‌کند','horizon_fa':'روزانه','invalidation_fa':['اگر شرایط عوض شود.'],'evidence_refs':[],'technical_detail':{'state':'UNKNOWN'}}
        sections[sid]=deep
        cards.append({'section_id':sid,'id':title,'title_fa':title,'state':'UNKNOWN','state_fa':'نامشخص','stance':'UNKNOWN','relation_fa':'نامشخص','summary_fa':'خلاصه ساده.','important_point_fa':'مهم‌ترین نکته.','detail':{},'deep_dive':deep})
    return {'schema_version':'1.0.0','report_model_version':'2.0.0','interface_version':'UI2.1.0','header':{'subject':'NASDAQ100','original_request':'چرا نزدک ریخت و فشار چقدر مانده؟','as_of':'2026-08-10T10:00:00Z','horizon':'DAILY','research_classes':['CAUSAL_ATTRIBUTION'],'locale':'fa-IR'},'layer1':{'focus':{'label_fa':'اصلی‌ترین توضیح فعلی','answer_fa':'نرخ واقعی یکی از توضیح‌های اصلی است، اما علت قطعی هنوز مشخص نیست.'},'direction':'BEARISH','direction_fa':'نزولی','permission':'NO_TRADE','permission_fa':'فعلاً معامله نکن','force':'HIGH','force_fa':'بالا','consumption':'MODERATE','consumption_fa':'متوسط','remaining_pressure':'HIGH','remaining_pressure_fa':'بالا','persistence':'KEEP','persistence_fa':'ادامه‌دار','reversal_risk':'MODERATE','reversal_risk_fa':'متوسط','dominant_driver':'نرخ واقعی','what_matters_now_fa':'مهم‌ترین عامل فعلی نرخ واقعی است.','what_would_change_this_fa':'اگر نرخ واقعی برگردد تحلیل باید بازبینی شود.','next_review':'10:30 NY','next_review_fa':'10:30 NY'},'decision_strip':{'direction':'BEARISH','permission':'NO_TRADE'},'layer2':{'cards':cards,'drivers':{'primary_fa':'نرخ واقعی','secondary_fa':'انتظارات نرخ','opposing_fa':'اعتبار سالم'},'causal_chain':{'identified':False,'status':'CAUSAL_EFFECT_NOT_IDENTIFIED','status_fa':causal_status_text('CAUSAL_EFFECT_NOT_IDENTIFIED'),'steps':['نرخ مورد انتظار بالاتر','نرخ واقعی بالاتر','فشار روی سهام رشدی']},'pressure':{'force_fa':'بالا','consumption_fa':'متوسط','remaining_pressure_fa':'بالا','persistence_fa':'ادامه‌دار','reversal_fa':'متوسط'},'changes':{'items':[],'has_comparison':False,'empty_message_fa':'مقایسه معتبر با اجرای قبلی ثبت نشده است.'},'scenarios':[]},'analytical_cards':cards,'drivers':{},'pressure':{},'scenarios':[],'layer3':{'sections':sections},'method_health':{'status':'PASS','simple_summary_fa':'تحلیل از نظر روش تحقیق سالم است.','research_class':'CAUSAL_ATTRIBUTION','rigor_tier':'DEEP','hard_failure_count':0},'perspective':{'quiet':True,'material_findings_fa':[]},'evidence_explorer':{},'audit':{'run_id':'TEST','request_id':'REQ','direction_authority':{'request_compiler':'NONE','report_composer':'NONE','apl_a':'NONE'}},'ux':{'schema':'THREE_LAYER_V1'}}

def run(vault_root):
    v=Path(vault_root).resolve();checks=[]
    def ck(n,b,d=None):checks.append({'name':n,'pass':bool(b),'detail':d})
    tests=[({'subject':'NASDAQ100','request_text':"What caused today's Nasdaq decline?",'mode':'LIVE'},'CAUSAL_ATTRIBUTION'),({'subject':'NASDAQ100','request_text':'Why did Nasdaq fall today?','mode':'LIVE'},'CAUSAL_ATTRIBUTION'),({'subject':'XAUUSD','request_text':'چرا طلا بعد از CPI حرکت کرد؟','mode':'LIVE'},'CAUSAL_ATTRIBUTION'),({'subject':'EURUSD','request_text':'آیا حرکت فعلی ادامه دارد و چقدر فشار باقی مانده؟','mode':'LIVE'},'PERSISTENCE_REVERSAL')]
    outs=[]
    for req,exp in tests:
        c=compile_request(v,req);outs.append(c);ck('route_'+exp,c['primary_research_class']==exp,(c['primary_research_class'],c['research_classes']))
    ck('paraphrase_stability',outs[0]['primary_research_class']==outs[1]['primary_research_class']=='CAUSAL_ATTRIBUTION')
    ck('persian_locale',outs[2]['locale']=='fa-IR')
    ck('compiler_zero_authority',all(x['authority']['direction']=='NONE' for x in outs))
    ck('unknown_not_neutral',to_fa('UNKNOWN')=='نامشخص' and to_fa('UNKNOWN')!=to_fa('NEUTRAL'))
    ck('causal_not_overstated','علت قطعی هنوز شناسایی نشده' in causal_status_text('CAUSAL_EFFECT_NOT_IDENTIFIED'))
    model=_fixture();h=explorer_html(model)
    ck('three_layers','L1' in h and 'L2' in h and 'L3' in h and 'deep-dialog' in h)
    ck('l1_request_aware','اصلی‌ترین توضیح فعلی' in h and 'فشار چقدر مانده' in h)
    ck('l2_eight_sections',all(x in h for x in ['وضعیت بنیادی','روایت و ذهن بازار','موقعیت معامله‌گران','جریان واقعی خرید و فروش','نقدینگی و تأمین مالی','ساختار و رفتار بازار']))
    ck('l3_section_specific','data-deep="fundamental"' in h and 'data-deep="flow"' in h and 'technical_detail' in h)
    ck('rtl','lang="fa" dir="rtl"' in h)
    ck('accessibility','aria-haspopup="dialog"' in h and 'aria-label="بستن تحلیل عمیق"' in h and 'prefers-reduced-motion' in h)
    ck('apl_separate','APL-A فقط ناظر است' in h and model['layer1']['direction']=='BEARISH')
    ck('no_fake_probability','67%' not in h)
    ck('interface_manifest',json.loads((v/'RUNTIME'/'Unified Research Interface'/'UNIFIED_INTERFACE_MANIFEST.json').read_text(encoding='utf-8'))['version']=='UI2.1.0')
    run_policy=json.loads((v/'RUNTIME'/'Unified Research Interface'/'config'/'run_command_policy.json').read_text(encoding='utf-8'))
    ck('one_command_run',run_policy['command']=='run <subject>' and run_policy['defaults']['mode']=='LIVE' and run_policy['defaults']['depth']=='DEEP')
    ck('chat_run_no_local_api_requirement',run_policy['openai_api_key_required_for_chat'] is False and run_policy['environment_certification_required_for_chat'] is False)
    ck('root_run_contract',(v.parent/'RUN.md').is_file() and 'run NASDAQ100' in (v.parent/'RUN.md').read_text(encoding='utf-8'))
    ck('apl_b_not_implemented',not any(p.is_dir() and 'APL-B' in p.name for p in (v/'RUNTIME').iterdir()))
    from .quality import pre_run, report_fidelity, set_gate
    from .memory import _secret_scan, detect_changes, verify_capsule, persist, status as memory_status
    import tempfile,shutil
    qreg=json.loads((v/'RUNTIME'/'Unified Research Interface'/'config'/'run_quality_registry.json').read_text(encoding='utf-8'))
    ck('run2_gate_registry',qreg['gate_set_version']=='RUN2.0.0' and len(qreg['gates'])>=20)
    ck('run2_no_quality_score',qreg['policy']=='MULTIDIMENSIONAL_NO_SINGLE_SCORE')
    pr=pre_run(v,compile_request(v,{'subject':'NASDAQ100','request_text':'تحلیل کامل امروز','mode':'LIVE','depth':'DEEP'}));ck('run2_pre_run_gate',pr['status']=='PASS')
    ck('run2_secret_guard',bool(_secret_scan({'OPENAI_API_KEY':'secret'})) and not _secret_scan({'market':'NASDAQ100'}))
    ck('run2_change_detection',detect_changes({'run_id':'A','direction':'BULLISH','permission':'BUY','force_lifecycle':{},'unknowns':[]},{'run_id':'B','direction':'BEARISH','permission':'NO_TRADE','force_lifecycle':{},'unknowns':['x']})['has_comparison'])
    ms=json.loads((v/'RUNTIME'/'Unified Research Interface'/'config'/'run_memory_policy.json').read_text(encoding='utf-8'));ck('run2_chat_truth',ms['chat_native']['mutate_uploaded_vault_in_place'] is False and ms['chat_native']['portable_capsule_required'] is True)
    ck('run2_capsule_schema',(v/'RUNTIME'/'Unified Research Interface'/'schemas'/'AlphaLab_Run_Capsule.schema.json').is_file())
    ck('run2_quality_schema',(v/'RUNTIME'/'Unified Research Interface'/'schemas'/'AlphaLab_Run_Quality_Receipt.schema.json').is_file())
    # Persistence/capsule immutability and integrity are tested without touching real AlphaLab_Data.
    td=Path(tempfile.mkdtemp(prefix='alphalab_run2_'))
    try:
        q={'schema_version':'1.0.0','gate_set_version':'RUN2.0.0','run_id':'RUN_TEST','status':'PASS','scientific_process_status':'PASS','market_state_resolution':'UNKNOWN','gates':[{'gate_id':'PERSISTENCE','status':'PENDING','severity':'HARD','detail':None}],'hard_failures':[],'warnings':[]}
        cap={'schema_version':'1.0.0','capsule_version':'RUN2.0.0','run_id':'RUN_TEST','request_id':'REQ_TEST','subject':'NASDAQ100','mode':'LIVE','as_of':'2026-08-10T10:00:00Z','horizon':'DAILY_OPEN_TO_CLOSE','primary_research_class':'DIRECTIONAL_FORECAST','direction':'UNKNOWN','permission':'NO_TRADE','force_lifecycle':{'direction':'UNKNOWN','force':'UNKNOWN','consumption':'UNKNOWN','remaining_pressure':'UNKNOWN','persistence':'UNKNOWN','reversal':'UNKNOWN'},'unknowns':['state unresolved'],'run_quality_receipt':q,'quality_status':'PASS','canonical_result_hash':'sha256:'+'1'*64,'reproducibility_state':'EVIDENCE_SNAPSHOT_REPRODUCIBLE','created_at':'2026-08-10T10:00:00Z'}
        sealed,pr=persist(td,cap);ck('run2_capsule_atomic_persist',pr['status']=='PASS' and Path(pr['path']).is_file());ck('run2_capsule_verify',verify_capsule(pr['path'])['status']=='PASS');ck('run2_unknown_can_be_quality_pass',sealed['quality_status']=='PASS' and sealed['direction']=='UNKNOWN')
        try:persist(td,cap);dup=False
        except RuntimeError:dup=True
        ck('run2_capsule_duplicate_rejected',dup)
        tam=json.loads(Path(pr['path']).read_text(encoding='utf-8'));tam['direction']='BEARISH';tp=td/'tampered.json';tp.write_text(json.dumps(tam),encoding='utf-8');ck('run2_capsule_tamper_detected',verify_capsule(tp)['status']=='FAIL')
        ck('run2_memory_status',memory_status(td)['status']=='PASS' and memory_status(td)['runs']==1)
    finally:shutil.rmtree(td,ignore_errors=True)
    future=compile_request(v,{'subject':'NASDAQ100','request_text':'historical','mode':'HISTORICAL','as_of':'2099-01-01T00:00:00Z'});ck('run2_future_historical_blocked',pre_run(v,future)['status']=='BLOCKED')
    badmodel=_fixture();badmodel['layer1']['direction']='BULLISH';can={'decision':{'final_direction':'BEARISH','permission':'NO_TRADE'},'science':{'force_lifecycle':{}}};ck('run2_report_mismatch_detected',report_fidelity(can,badmodel)['status']=='FAIL')
    bad=[x for x in checks if not x['pass']]
    return {'schema_version':'1.0.0','status':'PASS' if not bad else 'FAIL','interface_version':'UI2.1.0','passed':len(checks)-len(bad),'total':len(checks),'checks':checks,'errors':[x['name'] for x in bad]}
