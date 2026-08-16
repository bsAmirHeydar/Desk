from __future__ import annotations
import gzip, os, time, urllib.request, urllib.error
from dataclasses import dataclass
from .common import sha256_bytes, iso

@dataclass
class FetchResult:
    source_id: str
    url: str
    status: str
    http_status: int | None
    content_type: str | None
    body: bytes | None
    error: str | None
    retrieved_at: str
    sha256: str | None
    elapsed_ms: int

class PublicHttpClient:
    def __init__(self, policy: dict):
        self.timeout=int(policy.get('default_timeout_seconds',18))
        self.retries=int(policy.get('default_retries',2))
        self.backoff=list(policy.get('retry_backoff_seconds',[1,3]))
        self.max_bytes=int(policy.get('max_response_bytes',12_000_000))
        self.user_agent=policy.get('user_agent','AlphaDesk-V3-P02/1.0')
    def fetch(self, source_id: str, url: str, method='GET', data: bytes|None=None, headers: dict|None=None) -> FetchResult:
        started=time.monotonic(); last=None
        hs={'User-Agent':self.user_agent,'Accept':'*/*','Accept-Encoding':'gzip'}
        hs.update(headers or {})
        for attempt in range(self.retries+1):
            try:
                req=urllib.request.Request(url,data=data,headers=hs,method=method)
                with urllib.request.urlopen(req,timeout=self.timeout) as r:
                    raw=r.read(self.max_bytes+1)
                    if len(raw)>self.max_bytes: raise ValueError('response exceeds max_response_bytes')
                    enc=(r.headers.get('Content-Encoding') or '').lower()
                    if enc=='gzip': raw=gzip.decompress(raw)
                    return FetchResult(source_id,url,'SUCCESS',getattr(r,'status',200),r.headers.get('Content-Type'),raw,None,iso(),sha256_bytes(raw),int((time.monotonic()-started)*1000))
            except Exception as e:
                last=e
                if attempt < self.retries:
                    time.sleep(self.backoff[min(attempt,len(self.backoff)-1)])
        return FetchResult(source_id,url,'FETCH_FAILED',None,None,None,repr(last),iso(),None,int((time.monotonic()-started)*1000))
