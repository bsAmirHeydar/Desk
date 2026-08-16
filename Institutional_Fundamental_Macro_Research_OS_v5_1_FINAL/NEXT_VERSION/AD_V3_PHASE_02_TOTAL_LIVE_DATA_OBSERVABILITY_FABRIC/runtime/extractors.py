from __future__ import annotations
import csv, io, json, re, html, xml.etree.ElementTree as ET
from datetime import datetime, timezone
from .common import iso, stable_id

_TAG=re.compile(r'<[^>]+>')
_WS=re.compile(r'\s+')

def html_to_text(b: bytes) -> str:
    s=b.decode('utf-8','replace')
    s=re.sub(r'(?is)<script.*?</script>|<style.*?</style>',' ',s)
    s=_TAG.sub(' ',s)
    return _WS.sub(' ',html.unescape(s)).strip()

def evidence_snippet(text: str, terms: list[str], radius=280) -> tuple[str|None,str|None]:
    low=text.casefold()
    candidates=sorted({t.strip() for t in terms if len(t.strip())>=3},key=len,reverse=True)
    for t in candidates:
        i=low.find(t.casefold())
        if i>=0:
            a=max(0,i-radius); z=min(len(text),i+len(t)+radius)
            return text[a:z].strip(),t
    return (text[:min(len(text),700)].strip() if text else None), None

def generic_observation(fact: dict, source: dict, body: bytes, retrieved_at: str, raw_hash: str, content_type='') -> dict:
    is_text=('text' in (content_type or '').lower()) or source.get('format') in ('html','csv','json','xml')
    if not is_text:
        # A fetched PDF/XLS proves source availability, not semantic observation of the requested fact.
        return _obs(fact,source,'PUBLIC_PROXY','RAW_SNAPSHOT',{'byte_length':len(body)},retrieved_at,raw_hash,warnings=['SEMANTIC_VALUE_NOT_PARSED_FROM_BINARY','RAW_SOURCE_AVAILABLE_ONLY'])
    text=html_to_text(body) if source.get('format')=='html' else body.decode('utf-8','replace')
    snippet, matched=evidence_snippet(text,fact.get('discovery_terms',[]))
    cad=(source.get('cadence') or '').upper()
    state=('OBSERVED_DELAYED' if matched and cad in ('WEEKLY','MONTHLY','QUARTERLY','ANNUAL','IRREGULAR') else ('OBSERVED_CURRENT' if matched else 'PUBLIC_PROXY'))
    warnings=[] if matched else ['DISCOVERY_TERM_NOT_FOUND_SOURCE_SNAPSHOT_RETAINED']
    return _obs(fact,source,state,'TEXT_EVIDENCE',{'excerpt':snippet,'matched_term':matched},retrieved_at,raw_hash,warnings=warnings)

def raw_public_pdf_proxy_observation(fact,source,body,retrieved_at,raw_hash):
    return _obs(fact,source,'PUBLIC_PROXY','RAW_SNAPSHOT',{'byte_length':len(body),'format':'pdf'},retrieved_at,raw_hash,warnings=['OFFICIAL_PDF_FETCHED_SEMANTIC_EXTRACTION_NOT_CERTIFIED','DO_NOT_TREAT_PROXY_AS_DIRECT_FACT'])

def treasury_xml_values(body: bytes) -> tuple[dict,str|None]:
    root=ET.fromstring(body)
    entries=[]
    for e in root.iter():
        if e.tag.endswith('entry'):
            row={}
            for x in e.iter():
                tag=x.tag.split('}')[-1]
                if x.text and x.text.strip(): row[tag]=x.text.strip()
            entries.append(row)
    if not entries: return {},None
    def dateval(r):
        for k in ('NEW_DATE','INDEX_DATE','QUOTE_DATE','Date','date'):
            if k in r: return r[k]
        return ''
    row=sorted(entries,key=dateval)[-1]
    return row,dateval(row) or None

def treasury_observation(fact,source,body,retrieved_at,raw_hash,real=False):
    row,ref=treasury_xml_values(body)
    aliases={
      'UST_2Y_NOMINAL_YIELD':['BC_2YEAR'], 'UST_5Y_NOMINAL_YIELD':['BC_5YEAR'], 'UST_10Y_NOMINAL_YIELD':['BC_10YEAR'], 'UST_30Y_NOMINAL_YIELD':['BC_30YEAR'],
      'UST_5Y_REAL_YIELD':['TC_5YEAR','BC_5YEAR'], 'UST_10Y_REAL_YIELD':['TC_10YEAR','BC_10YEAR'], 'UST_30Y_REAL_YIELD':['TC_30YEAR','BC_30YEAR']
    }
    value=None; field=None
    for a in aliases.get(fact['fact_id'],[]):
        if row.get(a) not in (None,''):
            try: value=float(row[a]); field=a; break
            except: pass
    if value is None:
        return _obs(fact,source,'PARSE_FAILED','NONE',None,retrieved_at,raw_hash,reference_period=ref,warnings=['TREASURY_FIELD_NOT_FOUND'])
    return _obs(fact,source,'OBSERVED_CURRENT','NUMBER',value,retrieved_at,raw_hash,reference_period=ref,unit='percent',metadata={'upstream_field':field})

def nyfed_sofr_observation(fact,source,body,retrieved_at,raw_hash):
    try: d=json.loads(body.decode('utf-8'))
    except Exception:
        return _obs(fact,source,'PARSE_FAILED','NONE',None,retrieved_at,raw_hash,warnings=['INVALID_JSON'])
    rows=[]
    if isinstance(d,dict):
        for k in ('refRates','rates','data'):
            if isinstance(d.get(k),list): rows=d[k]; break
        if not rows and isinstance(d.get('refRates'),dict): rows=list(d['refRates'].values())
    elif isinstance(d,list): rows=d
    if not rows: return _obs(fact,source,'PARSE_FAILED','NONE',None,retrieved_at,raw_hash,warnings=['NO_RATE_ROWS'])
    r=rows[0]
    val=None
    for k in ('percentRate','rate','ratePercent','rate_pct'):
        if k in r:
            try: val=float(r[k]); break
            except: pass
    ref=next((str(r.get(k)) for k in ('effectiveDate','date','businessDate') if r.get(k)),None)
    if val is None: return _obs(fact,source,'PARSE_FAILED','NONE',None,retrieved_at,raw_hash,reference_period=ref,warnings=['SOFR_RATE_FIELD_NOT_FOUND'])
    return _obs(fact,source,'OBSERVED_DELAYED','NUMBER',val,retrieved_at,raw_hash,reference_period=ref,unit='percent',metadata={'row':r})

def fed_h10_observation(fact,source,body,retrieved_at,raw_hash):
    text=html_to_text(body)
    labels={'FED_BROAD_DOLLAR':'BROAD','FED_AFE_DOLLAR':'Advanced Foreign Economies','FED_EME_DOLLAR':'Emerging Market Economies'}
    label=labels.get(fact['fact_id'],'')
    idx=text.casefold().find(label.casefold()) if label else -1
    if idx<0:
        return generic_observation(fact,source,body,retrieved_at,raw_hash,'text/html')
    chunk=text[idx:idx+700]
    nums=re.findall(r'(?<!\d)(\d{2,3}\.\d{2,6})(?!\d)',chunk)
    if not nums: return _obs(fact,source,'PARSE_FAILED','NONE',None,retrieved_at,raw_hash,warnings=['H10_VALUE_NOT_FOUND'])
    return _obs(fact,source,'OBSERVED_DELAYED','NUMBER',float(nums[-1]),retrieved_at,raw_hash,unit='index',metadata={'excerpt':chunk})

def fed_h10_daily_index_observation(fact,source,body,retrieved_at,raw_hash):
    text=html_to_text(body)
    # Dedicated H.10 daily index pages contain chronological Date | Rate rows.
    pairs=re.findall(r'(?i)\b(\d{1,2}-[A-Z]{3}-\d{2,4})\s+(ND|\d{2,3}\.\d{2,8})\b',text)
    numeric=[]
    for ds,vs in pairs:
        if vs.upper()=='ND': continue
        try: numeric.append((ds,float(vs)))
        except: pass
    if not numeric:
        return _obs(fact,source,'PARSE_FAILED','NONE',None,retrieved_at,raw_hash,warnings=['H10_DAILY_DATE_RATE_NOT_FOUND'])
    ref,val=numeric[-1]
    return _obs(fact,source,'OBSERVED_DELAYED','NUMBER',val,retrieved_at,raw_hash,reference_period=ref,unit='index',metadata={'rows_parsed':len(numeric),'dedicated_daily_index':True})

_BLS_FACT_SERIES={
 'US_CPI':'CUSR0000SA0','US_CORE_CPI':'CUSR0000SA0L1E','US_PPI':'WPSFD4',
 'US_PAYROLLS':'CES0000000001','US_UNEMPLOYMENT':'LNS14000000','US_WAGES':'CES0500000003','US_JOLTS':'JTS000000000000000JOL'
}
_BLS_UNITS={
 'US_CPI':'index','US_CORE_CPI':'index','US_PPI':'index','US_PAYROLLS':'thousands_persons',
 'US_UNEMPLOYMENT':'percent','US_WAGES':'usd_per_hour','US_JOLTS':'thousands_positions'
}

def bls_api_observation(fact,source,body,retrieved_at,raw_hash):
    try: d=json.loads(body.decode('utf-8'))
    except Exception:
        return _obs(fact,source,'PARSE_FAILED','NONE',None,retrieved_at,raw_hash,warnings=['BLS_INVALID_JSON'])
    if str(d.get('status','')).upper() not in ('REQUEST_SUCCEEDED',''):
        return _obs(fact,source,'PARSE_FAILED','NONE',None,retrieved_at,raw_hash,warnings=['BLS_REQUEST_STATUS:'+str(d.get('status'))])
    wanted=_BLS_FACT_SERIES.get(fact['fact_id'])
    rows=(d.get('Results') or {}).get('series') or []
    series=next((x for x in rows if x.get('seriesID')==wanted),None)
    if not series: return _obs(fact,source,'PARSE_FAILED','NONE',None,retrieved_at,raw_hash,warnings=['BLS_SERIES_NOT_FOUND:'+str(wanted)])
    vals=[]
    for r in series.get('data') or []:
        period=str(r.get('period') or '')
        if not re.fullmatch(r'M(0[1-9]|1[0-2])',period): continue
        try: value=float(str(r.get('value')).replace(',',''))
        except: continue
        year=str(r.get('year') or '')
        ref=(year+'-'+period[1:]) if year else None
        vals.append((ref,value,r))
    if not vals: return _obs(fact,source,'PARSE_FAILED','NONE',None,retrieved_at,raw_hash,warnings=['BLS_NO_MONTHLY_VALUES'])
    # API returns newest first, but use sortable YYYY-MM defensively.
    ref,val,row=sorted(vals,key=lambda x:x[0] or '')[-1]
    return _obs(fact,source,'OBSERVED_DELAYED','NUMBER',val,retrieved_at,raw_hash,reference_period=ref,unit=_BLS_UNITS.get(fact['fact_id']),metadata={'series_id':wanted,'period_name':row.get('periodName'),'latest_flag':row.get('latest')})

def fred_csv_observation(fact,source,body,retrieved_at,raw_hash):
    text=body.decode('utf-8','replace')
    rows=list(csv.DictReader(io.StringIO(text)))
    if not rows: return _obs(fact,source,'PARSE_FAILED','NONE',None,retrieved_at,raw_hash,warnings=['FRED_CSV_NO_ROWS'])
    series=source.get('series_id') or fact.get('metadata',{}).get('series_id') or 'RSAFS'
    candidates=[]
    for r in rows:
        raw=r.get(series)
        if raw in (None,'','.'): continue
        try: value=float(str(raw).replace(',',''))
        except: continue
        ref=r.get('observation_date') or r.get('DATE') or r.get('date')
        candidates.append((ref,value))
    if not candidates: return _obs(fact,source,'PARSE_FAILED','NONE',None,retrieved_at,raw_hash,warnings=['FRED_CSV_VALUE_NOT_FOUND'])
    ref,val=sorted(candidates,key=lambda x:x[0] or '')[-1]
    return _obs(fact,source,'PUBLIC_PROXY','NUMBER',val,retrieved_at,raw_hash,reference_period=ref,unit='million_usd_sa',metadata={'series_id':series,'originating_agency':source.get('originating_agency'),'proxy_reason':'OFFICIAL_FED_REPUBLISHER_OF_CENSUS_SERIES'},warnings=['PUBLIC_PROXY_NOT_DIRECT_CENSUS_API'])


def census_retail_sales_observation(fact,source,body,retrieved_at,raw_hash):
    text=html_to_text(body)
    # Current Census sales release wording: sales for July 2026 ... were $763.6 billion, down 0.6 percent ... previous month, but up 5.0 percent ... July 2025.
    m=re.search(r'(?is)sales\s+for\s+([A-Za-z]+)\s+(20\d{2}).{0,900}?\$\s*([0-9]+(?:\.[0-9]+)?)\s+billion.{0,450}?\b(up|down)\s+([0-9]+(?:\.[0-9]+)?)\s+percent.{0,450}?previous\s+month.{0,450}?\b(?:but\s+)?(up|down)\s+([0-9]+(?:\.[0-9]+)?)\s+percent',text)
    if not m:
        return _obs(fact,source,'PARSE_FAILED','NONE',None,retrieved_at,raw_hash,warnings=['CENSUS_RETAIL_CURRENT_RELEASE_FIELDS_NOT_FOUND'])
    month,year,level,mom_dir,mom,yoy_dir,yoy=m.groups()
    mom=float(mom)*(-1.0 if mom_dir.lower()=='down' else 1.0)
    yoy=float(yoy)*(-1.0 if yoy_dir.lower()=='down' else 1.0)
    value={'level_billion_usd':float(level),'mom_percent':mom,'yoy_percent':yoy}
    pub=None
    dm=re.search(r'(?i)(?:FOR\s+RELEASE[^,]*,\s*)?(?:MONDAY|TUESDAY|WEDNESDAY|THURSDAY|FRIDAY|SATURDAY|SUNDAY)?[,]?\s*([A-Z][A-Z]+\s+\d{1,2},\s+20\d{2})',text)
    if dm: pub=dm.group(1).title()
    ref=f'{month.title()} {year}'
    return _obs(fact,source,'OBSERVED_DELAYED','OBJECT',value,retrieved_at,raw_hash,reference_period=ref,published_at=pub,unit='sales_level_and_percent_changes',metadata={'official_census_release':True,'survey':'Advance Monthly Retail Trade Survey'})

def fed_h10_inr_observation(fact,source,body,retrieved_at,raw_hash):
    text=html_to_text(body)
    pairs=re.findall(r'(?i)\b(\d{1,2}-[A-Z]{3}-\d{2,4})\s+(ND|\d{1,3}\.\d{2,8})\b',text)
    numeric=[]
    for ds,vs in pairs:
        if vs.upper()=='ND': continue
        try: numeric.append((ds,float(vs)))
        except Exception: pass
    if not numeric:
        return _obs(fact,source,'PARSE_FAILED','NONE',None,retrieved_at,raw_hash,warnings=['FED_H10_INR_DATE_RATE_NOT_FOUND'])
    ref,usd_inr=numeric[-1]
    return _obs(fact,source,'PUBLIC_PROXY','OBJECT',{'usd_inr':usd_inr,'affordability_proxy_only':True},retrieved_at,raw_hash,reference_period=ref,unit='INR_per_USD',metadata={'official_federal_reserve_h10':True,'rates_are_inr_per_usd':True},warnings=['USDINR_ALONE_IS_NOT_COMPLETE_LOCAL_GOLD_AFFORDABILITY','LOCAL_PREMIUM_DUTY_GST_AND_RETAIL_MARKUP_NOT_INCLUDED'])

def pib_gold_duty_observation(fact,source,body,retrieved_at,raw_hash):
    text=html_to_text(body)
    low=text.casefold()
    current=('extensions of concessional customs duty regimes for gold and silver dore bars' in low or 'concessional customs duty regimes for gold and silver dore' in low)
    if not current:
        return _obs(fact,source,'PARSE_FAILED','NONE',None,retrieved_at,raw_hash,warnings=['PIB_CURRENT_GOLD_DUTY_POLICY_SIGNAL_NOT_FOUND'])
    baseline=source.get('baseline_customs_duty_percent')
    value={
      'concessional_regime_extended':True,
      'exact_current_legal_rate_confirmed':False,
      'historical_policy_baseline_percent':baseline
    }
    return _obs(fact,source,'PUBLIC_PROXY','OBJECT',value,retrieved_at,raw_hash,reference_period='2026-27 Union Budget',published_at='2026-02-01',unit='policy_state',metadata={'current_source_is_official_government_communication':True,'baseline_source_url':source.get('baseline_source_url'),'baseline_source_date':source.get('baseline_source_date')},warnings=['OFFICIAL_POLICY_COMMUNICATION_NOT_CBIC_LEGAL_TARIFF_TABLE','HISTORICAL_6_PERCENT_BASELINE_NOT_ASSERTED_AS_FRESH_LEGAL_RATE'])

def rbi_inr_observation(fact,source,body,retrieved_at,raw_hash):
    text=html_to_text(body)
    m=re.search(r'(?i)INR\s*/\s*1\s*USD\s*[:|]?\s*([0-9]{1,3}(?:\.[0-9]+)?)',text)
    if not m: return _obs(fact,source,'PARSE_FAILED','NONE',None,retrieved_at,raw_hash,warnings=['RBI_USDINR_NOT_FOUND'])
    usd_inr=float(m.group(1))
    return _obs(fact,source,'PUBLIC_PROXY','OBJECT',{'usd_inr':usd_inr,'affordability_proxy_only':True},retrieved_at,raw_hash,unit='INR_per_USD',metadata={'official_rbi_rate_surface':True},warnings=['USDINR_ALONE_IS_NOT_COMPLETE_LOCAL_GOLD_AFFORDABILITY'])

def wgc_sge_withdrawals_observation(fact,source,body,retrieved_at,raw_hash):
    text=html_to_text(body)
    # WGC wording: "SGE withdrawals ... fell 8% m/m to 80t in July".
    patterns=[
      r'(?i)(?:SGE|Shanghai Gold Exchange)[^\.]{0,220}?withdrawals[^\.]{0,220}?(?:to|totalled|totaled)\s+([0-9]+(?:\.[0-9]+)?)\s*t\b',
      r'(?i)withdrawals[^\.]{0,220}?(?:SGE|Shanghai Gold Exchange)[^\.]{0,220}?([0-9]+(?:\.[0-9]+)?)\s*t\b'
    ]
    val=None
    for pat in patterns:
        m=re.search(pat,text)
        if m:
            try: val=float(m.group(1)); break
            except: pass
    month=None
    mm=re.search(r'(?i)\b(January|February|March|April|May|June|July|August|September|October|November|December)\b',text)
    if mm: month=mm.group(1)
    if val is None:
        return generic_observation(fact,source,body,retrieved_at,raw_hash,'text/html')
    return _obs(fact,source,'PUBLIC_PROXY','NUMBER',val,retrieved_at,raw_hash,reference_period=month,unit='tonnes',metadata={'underlying_source':'Shanghai Gold Exchange','reporting_source':'World Gold Council'},warnings=['INDUSTRY_PROXY_CITING_PRIMARY_SGE'])

def _clean_num(v):
    if v is None: return None
    s=str(v).strip().replace(',','').replace("'",'')
    if s in ('','-','--','----','N/A','NA'): return None
    s=re.sub(r'[A-Za-z]+$','',s).strip()
    try:return float(s)
    except:return None

def _quote_rows(d):
    if isinstance(d,list): return d
    if isinstance(d,dict):
        for k in ('quotes','data','quoteData','results'):
            if isinstance(d.get(k),list): return d[k]
            if isinstance(d.get(k),dict):
                inner=d[k]
                for kk in ('quotes','data','results'):
                    if isinstance(inner.get(kk),list): return inner[kk]
    return []

def _qfield(q,*names):
    for n in names:
        if q.get(n) not in (None,''): return q.get(n)
    return None

def cme_gold_quotes_observation(fact,source,body,retrieved_at,raw_hash):
    try:d=json.loads(body.decode('utf-8'))
    except Exception:return _obs(fact,source,'PARSE_FAILED','NONE',None,retrieved_at,raw_hash,warnings=['CME_GOLD_QUOTES_INVALID_JSON'])
    rows=_quote_rows(d)
    parsed=[]
    for q in rows:
        contract=_qfield(q,'expirationDate','month','contractMonth','expirationMonth','quoteCode','productCode')
        last=_clean_num(_qfield(q,'last','lastPrice','lastTradePrice'))
        settle=_clean_num(_qfield(q,'priorSettle','settle','settlement','settlementPrice'))
        volume=_clean_num(_qfield(q,'volume','totalVolume'))
        oi=_clean_num(_qfield(q,'openInterest','open_interest','oi'))
        if contract or last is not None or settle is not None:
            parsed.append({'contract':str(contract) if contract is not None else None,'last':last,'settlement':settle,'volume':volume,'open_interest':oi})
    if not parsed:return _obs(fact,source,'PARSE_FAILED','NONE',None,retrieved_at,raw_hash,warnings=['CME_GOLD_QUOTES_NO_ROWS'])
    fid=fact['fact_id']
    if fid=='GC_FUTURES_PRICE':
        ranked=sorted(parsed,key=lambda x:(x.get('volume') or -1),reverse=True)
        q=ranked[0]; val=q.get('last') if q.get('last') is not None else q.get('settlement')
        if val is None:return _obs(fact,source,'PARSE_FAILED','NONE',None,retrieved_at,raw_hash,warnings=['CME_GOLD_PRICE_NOT_FOUND'])
        return _obs(fact,source,'OBSERVED_DELAYED','NUMBER',val,retrieved_at,raw_hash,unit='usd_per_troy_ounce',metadata={'selected_contract':q,'contracts_seen':len(parsed),'public_delayed_web_endpoint':True})
    if fid=='GC_OPEN_INTEREST':
        vals=[x['open_interest'] for x in parsed if isinstance(x.get('open_interest'),(int,float))]
        if not vals:return _obs(fact,source,'PARSE_FAILED','NONE',None,retrieved_at,raw_hash,warnings=['CME_GOLD_OI_NOT_FOUND'])
        return _obs(fact,source,'OBSERVED_DELAYED','NUMBER',sum(vals),retrieved_at,raw_hash,unit='contracts',metadata={'contracts_seen':len(parsed),'aggregation':'sum_contract_open_interest'})
    if fid=='GC_VOLUME':
        vals=[x['volume'] for x in parsed if isinstance(x.get('volume'),(int,float))]
        if not vals:return _obs(fact,source,'PARSE_FAILED','NONE',None,retrieved_at,raw_hash,warnings=['CME_GOLD_VOLUME_NOT_FOUND'])
        return _obs(fact,source,'OBSERVED_DELAYED','NUMBER',sum(vals),retrieved_at,raw_hash,unit='contracts',metadata={'contracts_seen':len(parsed),'aggregation':'sum_contract_volume'})
    if fid=='GC_CURVE_TERM_STRUCTURE':
        curve=[x for x in parsed if x.get('last') is not None or x.get('settlement') is not None]
        if len(curve)<2:return _obs(fact,source,'PARSE_FAILED','NONE',None,retrieved_at,raw_hash,warnings=['CME_GOLD_CURVE_INSUFFICIENT_ROWS'])
        return _obs(fact,source,'OBSERVED_DELAYED','OBJECT',{'contracts':curve[:18]},retrieved_at,raw_hash,metadata={'public_delayed_web_endpoint':True},warnings=['CURVE_STATE_ONLY_NOT_CAUSAL_DIRECTION'])
    return generic_observation(fact,source,body,retrieved_at,raw_hash,'application/json')

def cme_fedfunds_quotes_observation(fact,source,body,retrieved_at,raw_hash):
    try:d=json.loads(body.decode('utf-8'))
    except Exception:return _obs(fact,source,'PARSE_FAILED','NONE',None,retrieved_at,raw_hash,warnings=['CME_FEDFUNDS_QUOTES_INVALID_JSON'])
    rows=_quote_rows(d); curve=[]
    for q in rows:
        contract=_qfield(q,'expirationDate','month','contractMonth','expirationMonth','quoteCode')
        px=_clean_num(_qfield(q,'last','lastPrice','priorSettle','settle','settlement'))
        if px is None: continue
        curve.append({'contract':str(contract) if contract is not None else None,'price':px,'implied_average_rate':100.0-px})
    if not curve:return _obs(fact,source,'PARSE_FAILED','NONE',None,retrieved_at,raw_hash,warnings=['CME_FEDFUNDS_NO_QUOTES'])
    return _obs(fact,source,'OBSERVED_DELAYED','OBJECT',{'fed_funds_futures_curve':curve[:18]},retrieved_at,raw_hash,unit='percent_implied_average_rate',metadata={'instrument':'30-Day Federal Funds Futures','method':'100-futures_price','public_delayed_web_endpoint':True},warnings=['FUTURES_CURVE_IS_NOT_FEDWATCH_PROBABILITY_TREE','NO_FAKE_MEETING_PROBABILITIES'])

# CFTC f_disagg.txt uses the official 191-field layout documented by CFTC.
_CFTC_IDX={
 'open_interest':7,'prod_long':8,'prod_short':9,'swap_long':10,'swap_short':11,'swap_spread':12,
 'mm_long':13,'mm_short':14,'mm_spread':15,'other_long':16,'other_short':17,'other_spread':18,
 'total_long':19,'total_short':20,'nonrep_long':21,'nonrep_short':22
}

def _num(s):
    try:return int(str(s).strip())
    except:
        try:return float(str(s).strip())
        except:return None

def cftc_gold_row(body:bytes):
    s=body.decode('utf-8','replace')
    for row in csv.reader(io.StringIO(s)):
        if row and 'GOLD' in row[0].upper() and ('COMMODITY EXCHANGE' in row[0].upper() or 'COMEX' in row[0].upper()):
            return row
    return None

def cftc_observation(fact,source,body,retrieved_at,raw_hash):
    row=cftc_gold_row(body)
    if not row: return _obs(fact,source,'PARSE_FAILED','NONE',None,retrieved_at,raw_hash,warnings=['GOLD_ROW_NOT_FOUND'])
    ref=row[2] if len(row)>2 else None
    fid=fact['fact_id']
    mapping={
      'CFTC_PRODUCER_MERCHANT':{'long':_CFTC_IDX['prod_long'],'short':_CFTC_IDX['prod_short']},
      'CFTC_SWAP_DEALER':{'long':_CFTC_IDX['swap_long'],'short':_CFTC_IDX['swap_short'],'spread':_CFTC_IDX['swap_spread']},
      'CFTC_MANAGED_MONEY':{'long':_CFTC_IDX['mm_long'],'short':_CFTC_IDX['mm_short'],'spread':_CFTC_IDX['mm_spread']},
      'CFTC_OTHER_REPORTABLES':{'long':_CFTC_IDX['other_long'],'short':_CFTC_IDX['other_short'],'spread':_CFTC_IDX['other_spread']},
      'CFTC_NONREPORTABLE':{'long':_CFTC_IDX['nonrep_long'],'short':_CFTC_IDX['nonrep_short']},
      'CFTC_GOLD_TOTAL_POSITIONING':{'open_interest':_CFTC_IDX['open_interest'],'reportable_long':_CFTC_IDX['total_long'],'reportable_short':_CFTC_IDX['total_short']}
    }
    if fid=='GC_OPEN_INTEREST':
        v=_num(row[_CFTC_IDX['open_interest']]) if len(row)>_CFTC_IDX['open_interest'] else None
        if v is None:return _obs(fact,source,'PARSE_FAILED','NONE',None,retrieved_at,raw_hash,reference_period=ref,warnings=['CFTC_OPEN_INTEREST_NOT_PARSED'])
        return _obs(fact,source,'OBSERVED_DELAYED','NUMBER',v,retrieved_at,raw_hash,reference_period=ref,unit='contracts',metadata={'market':row[0],'weekly_cftc_fallback':True},warnings=['CFTC_OI_IS_WEEKLY_DELAYED_NOT_LIVE'])
    if fid=='GC_VOLUME':
        return generic_observation(fact,source,body,retrieved_at,raw_hash,'text/csv')
    if fid not in mapping: return generic_observation(fact,source,body,retrieved_at,raw_hash,'text/csv')
    val={k:_num(row[i]) if i<len(row) else None for k,i in mapping[fid].items()}
    if all(v is None for v in val.values()): return _obs(fact,source,'PARSE_FAILED','NONE',None,retrieved_at,raw_hash,reference_period=ref,warnings=['CFTC_FIELDS_NOT_PARSED'])
    if 'long' in val and 'short' in val and val['long'] is not None and val['short'] is not None: val['net']=val['long']-val['short']
    return _obs(fact,source,'OBSERVED_DELAYED','OBJECT',val,retrieved_at,raw_hash,reference_period=ref,unit='contracts',metadata={'market':row[0]})

def _obs(fact,source,state,value_type,value,retrieved_at,raw_hash,reference_period=None,event_time=None,published_at=None,unit=None,metadata=None,warnings=None):
    seed={'fact_id':fact['fact_id'],'source_id':source['source_id'],'reference_period':reference_period,'retrieved_at':retrieved_at,'raw_sha256':raw_hash,'value':value}
    return {
      'record_type':'AD_V3_P02_FACT_OBSERVATION','observation_id':stable_id('P02OBS',seed),'phase':'AD-V3-P02','subject':'XAUUSD','fact_id':fact['fact_id'],
      'source_id':source['source_id'],'epistemic_state':state,'value_type':value_type,'value':value,'unit':unit,
      'reference_period':reference_period,'event_time':event_time,'published_at':published_at,'first_seen_at':retrieved_at,'retrieved_at':retrieved_at,
      'revision_number':0,'supersedes_observation_id':None,'directness':('PROXY' if state=='PUBLIC_PROXY' else 'DIRECT'),'provenance_ref':source.get('machine_endpoint') or source.get('canonical_url'),
      'raw_sha256':raw_hash,'metadata':metadata or {},'warnings':warnings or []
    }
