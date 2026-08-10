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
    return {'schema_version':'1.0.0','report_model_version':'2.0.0','interface_version':'UI2.0.0','header':{'subject':'NASDAQ100','original_request':'چرا نزدک ریخت و فشار چقدر مانده؟','as_of':'2026-08-10T10:00:00Z','horizon':'DAILY','research_classes':['CAUSAL_ATTRIBUTION'],'locale':'fa-IR'},'layer1':{'focus':{'label_fa':'اصلی‌ترین توضیح فعلی','answer_fa':'نرخ واقعی یکی از توضیح‌های اصلی است، اما علت قطعی هنوز مشخص نیست.'},'direction':'BEARISH','direction_fa':'نزولی','permission':'NO_TRADE','permission_fa':'فعلاً معامله نکن','force':'HIGH','force_fa':'بالا','consumption':'MODERATE','consumption_fa':'متوسط','remaining_pressure':'HIGH','remaining_pressure_fa':'بالا','persistence':'KEEP','persistence_fa':'ادامه‌دار','reversal_risk':'MODERATE','reversal_risk_fa':'متوسط','dominant_driver':'نرخ واقعی','what_matters_now_fa':'مهم‌ترین عامل فعلی نرخ واقعی است.','what_would_change_this_fa':'اگر نرخ واقعی برگردد تحلیل باید بازبینی شود.','next_review':'10:30 NY','next_review_fa':'10:30 NY'},'decision_strip':{'direction':'BEARISH','permission':'NO_TRADE'},'layer2':{'cards':cards,'drivers':{'primary_fa':'نرخ واقعی','secondary_fa':'انتظارات نرخ','opposing_fa':'اعتبار سالم'},'causal_chain':{'identified':False,'status':'CAUSAL_EFFECT_NOT_IDENTIFIED','status_fa':causal_status_text('CAUSAL_EFFECT_NOT_IDENTIFIED'),'steps':['نرخ مورد انتظار بالاتر','نرخ واقعی بالاتر','فشار روی سهام رشدی']},'pressure':{'force_fa':'بالا','consumption_fa':'متوسط','remaining_pressure_fa':'بالا','persistence_fa':'ادامه‌دار','reversal_fa':'متوسط'},'changes':{'items':[],'has_comparison':False,'empty_message_fa':'مقایسه معتبر با اجرای قبلی ثبت نشده است.'},'scenarios':[]},'analytical_cards':cards,'drivers':{},'pressure':{},'scenarios':[],'layer3':{'sections':sections},'method_health':{'status':'PASS','simple_summary_fa':'تحلیل از نظر روش تحقیق سالم است.','research_class':'CAUSAL_ATTRIBUTION','rigor_tier':'DEEP','hard_failure_count':0},'perspective':{'quiet':True,'material_findings_fa':[]},'evidence_explorer':{},'audit':{'run_id':'TEST','request_id':'REQ','direction_authority':{'request_compiler':'NONE','report_composer':'NONE','apl_a':'NONE'}},'ux':{'schema':'THREE_LAYER_V1'}}

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
    ck('interface_manifest',json.loads((v/'RUNTIME'/'Unified Research Interface'/'UNIFIED_INTERFACE_MANIFEST.json').read_text(encoding='utf-8'))['version']=='UI2.0.0')
    ck('apl_b_not_implemented',not any(p.is_dir() and 'APL-B' in p.name for p in (v/'RUNTIME').iterdir()))
    bad=[x for x in checks if not x['pass']]
    return {'schema_version':'1.0.0','status':'PASS' if not bad else 'FAIL','interface_version':'UI2.0.0','passed':len(checks)-len(bad),'total':len(checks),'checks':checks,'errors':[x['name'] for x in bad]}
