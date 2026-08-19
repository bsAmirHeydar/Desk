from __future__ import annotations
class ProviderError(RuntimeError):pass
class SchemaDrift(ProviderError):pass
class EntitlementMissing(ProviderError):pass
class RateLimited(ProviderError):pass
class BaseProvider:
    provider_id='BASE'
    def capabilities(self):raise NotImplementedError
    def health(self):return {'provider_id':self.provider_id,'state':'UNKNOWN'}
    def fetch_current(self):raise NotImplementedError
    def fetch_historical(self,start,end,interval='1min'):raise NotImplementedError
    def lineage(self):return {'provider_id':self.provider_id}
