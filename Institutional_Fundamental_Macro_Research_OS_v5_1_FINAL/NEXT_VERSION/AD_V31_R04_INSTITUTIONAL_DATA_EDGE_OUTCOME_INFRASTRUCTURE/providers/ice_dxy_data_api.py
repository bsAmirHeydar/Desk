from __future__ import annotations
import os,urllib.parse
from .base import BaseProvider,EntitlementMissing,SchemaDrift
from .http_util import get_json
from AD_V31_R04_INSTITUTIONAL_DATA_EDGE_OUTCOME_INFRASTRUCTURE.runtime.common import parse_dt,iso
class ICEDXYDataAPI(BaseProvider):
    provider_id='ICE_DXY_DATA_API'
    def __init__(self):
        self.url=os.getenv('ICE_DXY_DATA_API_URL');self.token=os.getenv('ICE_DXY_DATA_API_TOKEN')
    def capabilities(self):return {'instrument':'ICE_US_DOLLAR_INDEX','scientific_series_id':'ICE_DXY_DIRECT','direct':True,'historical':True,'realtime':True,'requires_env':['ICE_DXY_DATA_API_URL','ICE_DXY_DATA_API_TOKEN']}
    def _check(self):
        if not self.url or not self.token:raise EntitlementMissing('ICE_DXY_DATA_API_ENTITLEMENT_MISSING')
    def fetch_historical(self,start,end,interval='1min'):
        self._check();q=urllib.parse.urlencode({'symbol':'DXY','start':iso(parse_dt(start)),'end':iso(parse_dt(end)),'interval':interval});data,_,_=get_json(self.url+('&' if '?' in self.url else '?')+q,headers={'Authorization':'Bearer '+self.token,'Accept':'application/json'},retries=1)
        rows=data.get('data') if isinstance(data,dict) else None
        if not isinstance(rows,list):raise SchemaDrift('ICE_DXY_API_SCHEMA_DRIFT')
        out=[]
        for x in rows:
            t=x.get('timestamp') or x.get('time');v=x.get('value') or x.get('close')
            dt=parse_dt(t)
            try:v=float(v)
            except Exception:raise SchemaDrift('ICE_DXY_API_VALUE_INVALID')
            if not dt or not (50<=v<=200):raise SchemaDrift('ICE_DXY_API_SANITY')
            out.append({'series_id':'ICE_DXY_DIRECT','instrument':'DXY','provider_id':self.provider_id,'economic_time':iso(dt),'market_time':iso(dt),'value':v,'unit':'INDEX_POINTS','quality':'DIRECT_PROVIDER','directness':'DIRECT','record_class':'HISTORICAL_REFERENCE','metadata':{'resolution':interval}})
        return out
