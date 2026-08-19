from __future__ import annotations
import os,re,json,urllib.request
from .base import BaseProvider,EntitlementMissing,SchemaDrift
from AD_V31_R04_INSTITUTIONAL_DATA_EDGE_OUTCOME_INFRASTRUCTURE.runtime.common import parse_dt,iso

class ICEDXYDelayedPublic(BaseProvider):
    provider_id='ICE_DXY_DELAYED_PUBLIC'
    canonical_url='https://www.ice.com/products/194/US-Dollar-Index-Futures/data'
    def capabilities(self):return {'instrument':'ICE_US_DOLLAR_INDEX','scientific_series_id':'ICE_DXY_DIRECT','direct':True,'realtime':False,'delayed':True,'historical':False}
    @staticmethod
    def normalize_fixture(obj):
        # Strict normalized fixture contract; public-page live parser remains deployment-verified, not fabricated.
        if not isinstance(obj,dict):raise SchemaDrift('ICE_DXY_SCHEMA_DRIFT')
        value=obj.get('value');t=obj.get('economic_time') or obj.get('timestamp')
        if t is None or value is None:raise SchemaDrift('ICE_DXY_REQUIRED_FIELDS_MISSING')
        dt=parse_dt(t)
        try:v=float(value)
        except Exception:raise SchemaDrift('ICE_DXY_VALUE_INVALID')
        if not dt or not (50.0 <= v <= 200.0):raise SchemaDrift('ICE_DXY_SANITY')
        return {'series_id':'ICE_DXY_DIRECT','instrument':'DXY','provider_id':'ICE_DXY_DELAYED_PUBLIC','economic_time':iso(dt),'market_time':iso(dt),'value':v,'unit':'INDEX_POINTS','quality':'DIRECT_DELAYED','directness':'DIRECT','record_class':'LIVE_CAPTURED','metadata':{'delayed':True}}
    def fetch_current(self):
        # We intentionally do not guess undocumented HTML selectors. Deployment can supply a verified adapter endpoint.
        raise EntitlementMissing('ICE_PUBLIC_DELAYED_TYPED_PARSER_REQUIRES_DEPLOYMENT_VERIFICATION')
