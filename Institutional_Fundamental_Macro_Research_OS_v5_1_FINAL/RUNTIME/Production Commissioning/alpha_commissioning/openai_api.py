import json, os, time, urllib.request, urllib.error, socket

class OpenAIAPIError(RuntimeError):
    def __init__(self,msg,category='PERMANENT_ERROR',status=None):
        super().__init__(msg);self.category=category;self.status=status

class OpenAIResponsesClient:
    def __init__(self,api_key=None,base='https://api.openai.com/v1',timeout=3600,max_attempts=3):
        self.api_key=api_key or os.environ.get('OPENAI_API_KEY')
        if not self.api_key:raise OpenAIAPIError('OPENAI_API_KEY is not set','CONFIGURATION')
        self.base=base.rstrip('/');self.timeout=int(timeout);self.max_attempts=int(max_attempts)
    def _request(self,method,path,payload=None):
        body=None if payload is None else json.dumps(payload,ensure_ascii=False,separators=(',',':')).encode('utf-8')
        headers={'Authorization':'Bearer '+self.api_key,'Content-Type':'application/json','User-Agent':'AlphaLab-C1/1.0'}
        last=None
        for attempt in range(1,self.max_attempts+1):
            req=urllib.request.Request(self.base+path,data=body,headers=headers,method=method)
            try:
                with urllib.request.urlopen(req,timeout=self.timeout) as r:raw=r.read();status=getattr(r,'status',200)
                return json.loads(raw.decode('utf-8')),status
            except urllib.error.HTTPError as e:
                raw=e.read().decode('utf-8','replace')
                retry=e.code in (408,409,429,500,502,503,504)
                last=OpenAIAPIError('OpenAI HTTP %s: %s'%(e.code,raw[-4000:]),'TRANSIENT_ERROR' if retry else 'PERMANENT_ERROR',e.code)
                if not retry or attempt>=self.max_attempts:raise last
            except (urllib.error.URLError,TimeoutError,socket.timeout,ConnectionError) as e:
                last=OpenAIAPIError('OpenAI network error: '+str(e),'TRANSIENT_ERROR')
                if attempt>=self.max_attempts:raise last
            time.sleep(min(2**(attempt-1),8))
        raise last or OpenAIAPIError('unknown OpenAI request failure')
    def create(self,payload):return self._request('POST','/responses',payload)[0]

def output_text(resp):
    parts=[]
    for item in resp.get('output') or []:
        if item.get('type')!='message':continue
        for c in item.get('content') or []:
            if c.get('type') in ('output_text','text') and isinstance(c.get('text'),str):parts.append(c['text'])
    if not parts and isinstance(resp.get('output_text'),str):parts.append(resp['output_text'])
    return ''.join(parts).strip()

def web_sources(resp):
    out=[]
    for item in resp.get('output') or []:
        if item.get('type')=='web_search_call':
            action=item.get('action') or {}
            for s in action.get('sources') or []:
                if isinstance(s,dict) and s.get('url'):out.append(s)
        if item.get('type')=='message':
            for c in item.get('content') or []:
                for a in c.get('annotations') or []:
                    if isinstance(a,dict) and a.get('url'):out.append({'url':a.get('url'),'title':a.get('title')})
    ded=[];seen=set()
    for s in out:
        u=s.get('url')
        if u and u not in seen:seen.add(u);ded.append(s)
    return ded
