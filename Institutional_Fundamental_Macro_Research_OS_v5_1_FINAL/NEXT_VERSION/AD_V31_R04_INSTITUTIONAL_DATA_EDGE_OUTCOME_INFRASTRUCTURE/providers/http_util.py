from __future__ import annotations
import json,urllib.request,urllib.parse,urllib.error,time

def get_json(url,headers=None,timeout=12,retries=1):
    last=None
    for i in range(retries+1):
        try:
            req=urllib.request.Request(url,headers=headers or {'Accept':'application/json','User-Agent':'AlphaDesk-R04/1.0'})
            with urllib.request.urlopen(req,timeout=timeout) as r:
                if getattr(r,'status',200)==429:raise RuntimeError('RATE_LIMITED')
                body=r.read().decode('utf-8','replace')
                try:return json.loads(body),dict(r.headers),getattr(r,'status',200)
                except Exception as e:raise RuntimeError('SCHEMA_DRIFT_NON_JSON') from e
        except Exception as e:
            last=e
            if i<retries:time.sleep(min(1.0*(i+1),2.0))
    raise last
