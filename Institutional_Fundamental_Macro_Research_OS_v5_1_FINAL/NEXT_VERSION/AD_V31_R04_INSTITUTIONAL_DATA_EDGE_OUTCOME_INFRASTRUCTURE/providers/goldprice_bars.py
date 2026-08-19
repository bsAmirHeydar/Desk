from __future__ import annotations
import os,urllib.parse
from .base import BaseProvider,EntitlementMissing,SchemaDrift
from .http_util import get_json
from AD_V31_R04_INSTITUTIONAL_DATA_EDGE_OUTCOME_INFRASTRUCTURE.runtime.common import parse_dt,iso

class GoldPriceDevBars(BaseProvider):
    provider_id='GOLDPRICEDEV_XAU_BARS'
    def __init__(self,key=None,base=None):
        self.key=key or os.getenv('GOLDPRICEDEV_API_KEY');self.base=base or os.getenv('GOLDPRICEDEV_API_BASE','https://api.goldprice.dev')
    def capabilities(self):return {'instrument':'XAUUSD','scientific_series_id':'XAUUSD_SPOT_REFERENCE','historical':True,'intraday':True,'requires_env':['GOLDPRICEDEV_API_KEY']}
    def _headers(self):
        if not self.key:raise EntitlementMissing('GOLDPRICEDEV_API_KEY_MISSING')
        return {'Accept':'application/json','Authorization':f'Bearer {self.key}','X-API-Key':self.key,'User-Agent':'AlphaDesk-R04/1.0'}
    def fetch_historical(self,start,end,interval='1m'):
        q=urllib.parse.urlencode({'symbol':'XAU-USD-SPOT','interval':interval,'start':iso(parse_dt(start)),'end':iso(parse_dt(end))})
        data,_,_=get_json(self.base.rstrip('/')+'/v1/bars?'+q,headers=self._headers(),retries=1)
        rows=data.get('data') if isinstance(data,dict) else None
        if rows is None and isinstance(data,dict): rows=data.get('bars') or data.get('values')
        if not isinstance(rows,list):raise SchemaDrift('GOLDPRICEDEV_BARS_SCHEMA_DRIFT')
        return [self.normalize(x,interval) for x in rows]
    def normalize(self,x,interval):
        t=x.get('timestamp') or x.get('time') or x.get('datetime'); close=x.get('close') or x.get('price')
        if parse_dt(t) is None or not isinstance(close,(int,float,str)):raise SchemaDrift('GOLDPRICEDEV_BAR_INVALID')
        try:v=float(close)
        except Exception:raise SchemaDrift('GOLDPRICEDEV_BAR_VALUE_INVALID')
        if v<=0 or v>100000:raise SchemaDrift('GOLDPRICEDEV_BAR_SANITY')
        return {'series_id':'XAUUSD_SPOT_REFERENCE','instrument':'XAUUSD','provider_id':self.provider_id,'economic_time':iso(parse_dt(t)),'market_time':iso(parse_dt(t)),'value':v,'unit':'USD_PER_OZ','quality':'PROVIDER_HISTORICAL','directness':'PROXY_REFERENCE','record_class':'HISTORICAL_REFERENCE','metadata':{'resolution':interval}}
