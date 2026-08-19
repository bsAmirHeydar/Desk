from __future__ import annotations
from pathlib import Path
from .common import PHASE,load_json,iso
from .provider_registry import capabilities,access_counts
from .provider_health import assess
from .pit_store import put,verify
from collections import Counter
from .outcome_recovery import default_store

def ingest_anchor(anchor,state_root=None,record_class='LIVE_CAPTURED'):
    if not anchor or not isinstance(anchor.get('value'),(int,float)):return {'stored':False,'reason':'NO_NUMERIC_ANCHOR'}
    series=anchor.get('scientific_series_id')
    if not series:return {'stored':False,'reason':'NO_SCIENTIFIC_SERIES_ID'}
    rec={'series_id':series,'instrument':anchor.get('instrument_key'),'fact_id':anchor.get('source_fact_id'),'provider_id':anchor.get('source_id') or 'UNKNOWN','economic_time':anchor.get('economic_marker') or anchor.get('event_time') or anchor.get('published_at') or anchor.get('retrieved_at'),'fetch_time':anchor.get('retrieved_at'),'value':float(anchor['value']),'unit':anchor.get('unit') or 'PRICE','quality':anchor.get('quality') or 'OBSERVED','directness':'PROXY' if anchor.get('proxy_for_xauusd') else 'DIRECT','record_class':record_class,'raw_reference':anchor.get('raw_reference'),'metadata':{'anchor_kind':anchor.get('anchor_kind'),'outcome_only':True}}
    if not rec['economic_time']:return {'stored':False,'reason':'NO_ECONOMIC_TIME'}
    row,created=put(default_store(state_root),rec);return {'stored':True,'created':created,'record_checksum':row['record_checksum']}

def status(state_root=None):
    caps=capabilities();access=access_counts();pit=verify(default_store(state_root));gaps=load_json(PHASE/'config/data_gap_registry.json',{}) or {}
    dxy=next((p for p in caps if p['provider_id']=='ICE_DXY_DATA_API'),None)
    dxy_public=next((p for p in caps if p['provider_id']=='ICE_DXY_DELAYED_PUBLIC'),None)
    gp=next((p for p in caps if p['provider_id']=='GOLDPRICEDEV_XAU_BARS'),None)
    td=next((p for p in caps if p['provider_id']=='TWELVEDATA_XAUUSD'),None)
    src=load_json(PHASE.parent/'AD_V3_PHASE_02_TOTAL_LIVE_DATA_OBSERVABILITY_FABRIC/config/source_contract_registry.json',{}) or {}; cc=Counter(x.get('collector_type') for x in src.get('sources',[])); structured=sum(v for k,v in cc.items() if k not in ('GENERIC_HTML','GAP_ONLY'))
    return {'record_type':'AD_V31_R04_DATA_EDGE_STATUS','version':'3.1.4-institutional-data-edge','implementation_status':'PASS','provider_counts_by_access_class':access,'provider_count':len(caps),'configured_provider_count':sum(1 for x in caps if x.get('configured')),'authorized_provider_count':sum(1 for x in caps if x.get('authorized_for_use')),'direct_dxy':{'state':'DIRECT_CONFIGURED' if dxy and dxy.get('authorized_for_use') else ('DIRECT_DELAYED_IMPLEMENTED_NOT_LIVE_VERIFIED' if dxy_public else 'PROVIDER_GAP'),'provider':'ICE_DXY_DATA_API' if dxy and dxy.get('authorized_for_use') else 'ICE_DXY_DELAYED_PUBLIC'},'usd_proxy':{'state':'AVAILABLE_SEPARATE_IDENTITY'},'intraday_real_rate_proxy':{'state':'UNAVAILABLE_COMPONENT_GAP','identity':'INTRADAY_REAL_RATE_PROXY','official_real_yield':False},'official_real_yield':{'state':'OFFICIAL_DAILY_CONTEXT'},'outcome_providers':{'goldprice_dev':'CONFIGURED' if gp and gp.get('authorized_for_use') else 'NOT_CONFIGURED','twelve_data':'CONFIGURED' if td and td.get('authorized_for_use') else 'NOT_CONFIGURED','pit_local':'HEALTHY' if pit['status']=='PASS' else 'DEGRADED'},'pit_store':pit,'source_architecture':{'structured_source_contracts':structured,'generic_html_source_contracts':cc.get('GENERIC_HTML',0),'gap_only_source_contracts':cc.get('GAP_ONLY',0),'r04_typed_adapters':4},'capabilities':{'gc_price_volume_oi':'PUBLIC_DELAYED_EXISTING','market_depth':'PAID_GAP','aggressor_flow':'PAID_GAP','options_iv_skew':'PARTIAL_PUBLIC_CONTEXT','dealer_gamma':'PAID_GAP','efp_lease_forward':'PAID_GAP','london_otc':'PRIVATE_GAP','private_flow':'PRIVATE_GAP'},'critical_provider_gaps':[x['gap_id'] for x in gaps.get('gaps',[]) if x.get('priority')=='CRITICAL' and x.get('state')!='RESOLVED'],'failover_active':False,'V3_state':'SHADOW_COMMISSIONING','promotion_performed':False,'trade_execution_authority':'NONE','as_of':iso()}
