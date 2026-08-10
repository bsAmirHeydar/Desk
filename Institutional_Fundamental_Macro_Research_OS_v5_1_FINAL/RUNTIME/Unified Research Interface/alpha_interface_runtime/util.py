from pathlib import Path
import json,hashlib,uuid,datetime,re

def load_json(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds').replace('+00:00','Z')
def uid(prefix):return prefix+'_'+uuid.uuid4().hex[:16].upper()
def sha_obj(x):return 'sha256:'+hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')).hexdigest()
def text(x):
    if x is None:return ''
    if isinstance(x,str):return x
    return json.dumps(x,ensure_ascii=False,sort_keys=True)
def norm(s):
    s=str(s or '').strip().lower();s=s.replace('ي','ی').replace('ك','ک');return re.sub(r'\\s+',' ',s)
def first(obj,*keys,default=None):
    if not isinstance(obj,dict):return default
    for k in keys:
        if k in obj and obj[k] not in (None,'',[]):return obj[k]
    return default
