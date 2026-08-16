from pathlib import Path
import hashlib,json,os
from datetime import datetime,timezone

def now():return datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
def hobj(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),default=str).encode()).hexdigest()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def data_root(repo):
 v=os.environ.get('ALPHALAB_DATA_ROOT')
 return Path(v).resolve() if v else (Path(repo).resolve().parent/'AlphaLab_Data')
