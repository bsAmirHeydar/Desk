from pathlib import Path
import os,json,shlex,subprocess,time,urllib.request,urllib.error,hashlib
from .util import now,sha256_obj,dump_json,load_json,uid

class HostError(RuntimeError):
    def __init__(self,msg,category='PERMANENT_ERROR'): super().__init__(msg); self.category=category

def _command_from_env(name):
    v=os.environ.get(name)
    if not v: raise HostError('host command env not set: '+name,'CONFIGURATION')
    return shlex.split(v,posix=(os.name!='nt'))
class _Base:
    def _receipt(self,payload,out,raw,started,t0,attempt,adapter):
        hr=out.get('host_receipt',{}) if isinstance(out,dict) else {}
        return {'schema_version':'1.0.0','invocation_id':payload.get('invocation_id') or payload.get('operation_id'),'adapter':adapter,'provider':hr.get('provider'),'model':hr.get('model'),'model_version':hr.get('model_version'),'request_id':hr.get('request_id'),'temperature':hr.get('temperature'),'seed':hr.get('seed'),'reasoning_profile':payload.get('model_profile'),'tool_profile':hr.get('tool_profile'),'started_at_utc':started,'completed_at_utc':now(),'latency_ms':round((time.monotonic()-t0)*1000,3),'input_tokens':hr.get('input_tokens'),'output_tokens':hr.get('output_tokens'),'request_hash':sha256_obj(payload),'response_hash':'sha256:'+hashlib.sha256(raw).hexdigest(),'attempt':attempt,'metadata':{}}
    def retrieve(self,request):
        payload=dict(request); payload.setdefault('operation','EVIDENCE_RETRIEVAL'); payload.setdefault('operation_id',uid('RET_OP'))
        out,_=self.request(payload,1)
        if out.get('status') not in (None,'OK','PRESENT','UNAVAILABLE'): raise HostError('retrieval host status: '+str(out.get('status')),'PERMANENT_ERROR')
        return out.get('snapshots',[]) or []
class CommandHost(_Base):
    def __init__(self,binding,data_root): self.b=binding; self.data_root=Path(data_root)
    def request(self,payload,attempt=1):
        started=now();t0=time.monotonic();d=self.data_root/'tmp'/'r3_host';d.mkdir(parents=True,exist_ok=True);oid=payload.get('invocation_id') or payload.get('operation_id') or uid('OP');req=d/(oid+'.request.json');rsp=d/(oid+'.response.json');dump_json(req,payload)
        cmd=_command_from_env(self.b['command_env'])+[str(req),str(rsp)]
        try:q=subprocess.run(cmd,capture_output=True,text=True,timeout=int(self.b.get('timeout_seconds',1200)),env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
        except subprocess.TimeoutExpired as e: raise HostError('host timeout','TRANSIENT_ERROR') from e
        if q.returncode!=0: raise HostError('host command failed: '+(q.stderr or q.stdout)[-2000:],'TRANSIENT_ERROR')
        if not rsp.exists(): raise HostError('host response file missing','PERMANENT_ERROR')
        try:out=load_json(rsp);raw=rsp.read_bytes()
        except Exception as e: raise HostError('host response invalid JSON','PERMANENT_ERROR') from e
        rec=self._receipt(payload,out,raw,started,t0,attempt,'COMMAND');rec['metadata']={'stderr_tail':q.stderr[-500:] if q.stderr else ''};return out,rec
    def invoke(self,invocation,attempt=1):return self.request(invocation,attempt)
class HttpHost(_Base):
    def __init__(self,binding,data_root): self.b=binding
    def request(self,payload,attempt=1):
        endpoint=os.environ.get(self.b['endpoint_env'])
        if not endpoint: raise HostError('host endpoint env not set','CONFIGURATION')
        token=os.environ.get(self.b.get('token_env','')) if self.b.get('token_env') else None; body=json.dumps(payload,ensure_ascii=False).encode('utf-8');hdr={'Content-Type':'application/json'}
        if token:hdr['Authorization']='Bearer '+token
        started=now();t0=time.monotonic();req=urllib.request.Request(endpoint,data=body,headers=hdr,method='POST')
        try:
            with urllib.request.urlopen(req,timeout=int(self.b.get('timeout_seconds',1200))) as r:raw=r.read()
        except (urllib.error.URLError,TimeoutError) as e:raise HostError('HTTP host error: '+str(e),'TRANSIENT_ERROR') from e
        try:out=json.loads(raw.decode('utf-8'))
        except Exception as e:raise HostError('HTTP host returned invalid JSON','PERMANENT_ERROR') from e
        return out,self._receipt(payload,out,raw,started,t0,attempt,'HTTP_JSON')
    def invoke(self,invocation,attempt=1):return self.request(invocation,attempt)
class FixtureHost(_Base):
    def __init__(self,binding,data_root,fixture=None):self.b=binding;self.fixture=fixture
    def request(self,payload,attempt=1):
        if not callable(self.fixture):raise HostError('fixture host has no fixture callback','CONFIGURATION')
        out=self.fixture(payload);raw=json.dumps(out,sort_keys=True,separators=(',',':')).encode();t0=time.monotonic();t=now();rec=self._receipt(payload,out,raw,t,t0,attempt,'FIXTURE');rec.update({'provider':'FIXTURE','model':'DETERMINISTIC','model_version':'1','temperature':0.0,'seed':0,'latency_ms':0.0});return out,rec
    def invoke(self,invocation,attempt=1):return self.request(invocation,attempt)
def make_host(binding,data_root,fixture=None,production=True):
    if production and binding.get('test_only'):raise HostError('test-only host forbidden for production','AUTHORITY')
    a=binding['adapter']
    if a=='COMMAND':return CommandHost(binding,data_root)
    if a=='HTTP_JSON':return HttpHost(binding,data_root)
    if a=='FIXTURE':return FixtureHost(binding,data_root,fixture)
    raise HostError('unsupported host adapter: '+a,'CONFIGURATION')
