from __future__ import annotations
import os,urllib.parse
from .base import BaseProvider,EntitlementMissing,SchemaDrift
from .http_util import get_json
from AD_V31_R04_INSTITUTIONAL_DATA_EDGE_OUTCOME_INFRASTRUCTURE.runtime.common import parse_dt,iso

class TwelveDataXAUUSD(BaseProvider):
    provider_id='TWELVEDATA_XAUUSD'
    def __init__(self,key=None,base=None):
        self.key=key or os.getenv('TWELVEDATA_API_KEY');self.base=base or os.getenv('TWELVEDATA_API_BASE','https://api.twelvedata.com')
    def capabilities(self):return {'instrument':'XAU/USD','scientific_series_id':'XAUUSD_SPOT_REFERENCE','historical':True,'intraday':True,'requires_env':['TWELVEDATA_API_KEY']}
    def fetch_historical(self,start,end,interval='1min'):
        if not self.key:raise EntitlementMissing('TWELVEDATA_API_KEY_MISSING')
        q=urllib.parse.urlencode({'symbol':'XAU/USD','interval':interval,'start_date':iso(parse_dt(start)),'end_date':iso(parse_dt(end)),'apikey':self.key,'timezone':'UTC','order':'ASC'})
        data,_,_=get_json(self.base.rstrip('/')+'/time_series?'+q,retries=1)
        if isinstance(data,dict) and data.get('status')=='error':raise EntitlementMissing('TWELVEDATA_ERROR:'+str(data.get('message')))
        rows=data.get('values') if isinstance(data,dict) else None
        if not isinstance(rows,list):raise SchemaDrift('TWELVEDATA_SCHEMA_DRIFT')
        return [self.normalize(x,interval) for x in rows]
    def normalize(self,x,interval):
        t=x.get('datetime');close=x.get('close')
        if not t or close is None:raise SchemaDrift('TWELVEDATA_BAR_INVALID')
        # Twelve Data datetime may be timezone-naive UTC because timezone=UTC requested.
        dt=parse_dt(t+'+00:00') if 'T' not in str(t) and '+' not in str(t) and not str(t).endswith('Z') else parse_dt(t)
        if not dt:raise SchemaDrift('TWELVEDATA_TIME_INVALID')
        try:v=float(close)
        except Exception:raise SchemaDrift('TWELVEDATA_VALUE_INVALID')
        if v<=0 or v>100000:raise SchemaDrift('TWELVEDATA_SANITY')
        return {'series_id':'XAUUSD_SPOT_REFERENCE','instrument':'XAUUSD','provider_id':self.provider_id,'economic_time':iso(dt),'market_time':iso(dt),'value':v,'unit':'USD_PER_OZ','quality':'PROVIDER_HISTORICAL','directness':'DIRECT_MARKET_REFERENCE','record_class':'HISTORICAL_REFERENCE','metadata':{'resolution':interval}}
