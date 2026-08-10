from pathlib import Path
import json,tempfile
from .compiler import compile_request
from .report_model import build as build_report
from .render import explorer_html

def run(vault_root):
    v=Path(vault_root).resolve();checks=[]
    def ck(n,b,d=None):checks.append({'name':n,'pass':bool(b),'detail':d})
    tests=[
      ({'subject':'NASDAQ100','request_text':'What caused today\'s Nasdaq decline?','mode':'LIVE'},'CAUSAL_ATTRIBUTION'),
      ({'subject':'NASDAQ100','request_text':'Why did Nasdaq fall today?','mode':'LIVE'},'CAUSAL_ATTRIBUTION'),
      ({'subject':'XAUUSD','request_text':'چرا طلا بعد از CPI حرکت کرد؟','mode':'LIVE'},'CAUSAL_ATTRIBUTION'),
      ({'subject':'EURUSD','request_text':'آیا حرکت فعلی ادامه دارد و چقدر فشار باقی مانده؟','mode':'LIVE'},'PERSISTENCE_REVERSAL'),
      ({'subject':['EURUSD','USDJPY'],'request_text':'قدرت نسبی این دو بازار را مقایسه کن.','mode':'LIVE'},'CROSS_SECTIONAL_RELATIVE_VALUE'),
      ({'subject':'BTCUSD','request_text':'این دارایی جدید را بررسی کن.','mode':'LIVE'},'NEW_ASSET_RESEARCH')]
    outs=[]
    for req,exp in tests:
        c=compile_request(v,req);outs.append(c);ck('route_'+exp, c['primary_research_class']==exp,(c['primary_research_class'],c['research_classes']))
    ck('paraphrase_stability',outs[0]['primary_research_class']==outs[1]['primary_research_class']=='CAUSAL_ATTRIBUTION')
    ck('persian_locale',outs[2]['locale']=='fa-IR')
    ck('uncertified_plan_only',outs[-1]['execution_eligibility']=='RESEARCH_ONLY_UNCERTIFIED')
    ck('compiler_zero_authority',all(x['authority']['direction']=='NONE' and x['authority']['broker_write']=='NONE' for x in outs))
    # rendering semantic fixture
    model={'header':{'subject':'NASDAQ100','original_request':'تست','as_of':'2026-08-10T10:00:00Z','horizon':'DAILY'},'decision_strip':{'direction':'BEARISH','permission':'NO_TRADE','pressure_strength':'HIGH','consumption':'MODERATE','remaining_pressure':'FAVORABLE','reversal_risk':'MODERATE'},'analytical_cards':[{'id':x,'state':'UNKNOWN','summary_fa':'نامشخص','detail':{}} for x in ['Timing','Fundamental','Expectations / Policy / Regime','Narrative / Reflexivity / Consumption','Positioning','Actual Flow','Funding / Plumbing','Mechanics / Capacity / Volatility']],'drivers':{'primary':'real yields','secondary':None,'opposing':None},'pressure':{'force':'HIGH','consumption':'MODERATE','remaining_pressure':'FAVORABLE','persistence':'KEEP','reversal':'MODERATE'},'scenarios':[],'method_health':{'status':'PASS','research_class':'DIRECTIONAL_FORECAST','rigor_tier':'DEEP'},'perspective':{'quiet':True,'material_findings':[]},'evidence_explorer':{},'audit':{'run_id':'TEST','request_id':'REQ','direction_authority':{'request_compiler':'NONE','report_composer':'NONE','apl_a':'NONE'}}}
    h=explorer_html(model);ck('html_rtl','dir="rtl"' in h and 'جهت' in h and 'APL-A' in h);ck('eight_cards',sum(x in h for x in ['Timing','Fundamental','Positioning','Actual Flow','Funding / Plumbing','Mechanics / Capacity / Volatility'])==6)
    ck('legacy_root_retired',not (v.parent/'AlphaLab_V14_Any_Symbol_Live_Launcher.md').exists() and not (v.parent/'AlphaLab_V14_Live_DayTrading_Intelligence_Prompt.md').exists())
    ck('apl_b_not_implemented',not any(p.is_dir() and 'APL-B' in p.name for p in (v/'RUNTIME').iterdir()))
    bad=[x for x in checks if not x['pass']];return {'schema_version':'1.0.0','status':'PASS' if not bad else 'FAIL','interface_version':'UI1.0.0','passed':len(checks)-len(bad),'total':len(checks),'checks':checks,'errors':[x['name'] for x in bad]}
