from pathlib import Path
from datetime import datetime, timezone
import json,hashlib,time,uuid,sys
TEXT_EXT={'.md','.json','.yaml','.yml','.txt','.csv','.py','.sql','.ps1','.cmd'}
def now():return datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00','Z')
def uid(p):return p+'_'+uuid.uuid4().hex[:20].upper()
def load_json(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def canonical_bytes(p):
 p=Path(p);b=p.read_bytes()
 if p.suffix.lower() not in TEXT_EXT:return b
 try:s=b.decode('utf-8-sig')
 except UnicodeDecodeError:return b
 return s.replace('\r\n','\n').replace('\r','\n').encode('utf-8')
def chash(p):return 'sha256:'+hashlib.sha256(canonical_bytes(p)).hexdigest()
def shaobj(x):return 'sha256:'+hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def add_paths(v):
 v=Path(v)
 for rel in ('RUNTIME/R1 Foundation','RUNTIME/R2 Prompt Execution OS','RUNTIME/R3 Operational Execution and Learning OS','RUNTIME/APL-A Alpha Perspective Layer'):
  p=str(v/rel)
  if p not in sys.path:sys.path.insert(0,p)
