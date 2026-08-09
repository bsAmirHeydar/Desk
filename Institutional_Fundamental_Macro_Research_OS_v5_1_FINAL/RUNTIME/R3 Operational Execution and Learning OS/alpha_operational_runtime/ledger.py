from pathlib import Path
import json,os
from .util import now,uid,sha256_obj
class LedgerError(RuntimeError):pass
class D4Ledger:
    def __init__(self,rt):self.rt=rt;self.path=rt.data_root/'warehouse'/'d4_ledger.jsonl';self.path.parent.mkdir(parents=True,exist_ok=True);self.lock=rt.data_root/'locks'/'r3_d4_ledger.lock'
    def _lock(self):
        from alpha_runtime.locking import FileLock
        return FileLock(self.lock,30)
    def _rows(self):
        with self.rt.catalog.connect() as c:
            c.row_factory=__import__('sqlite3').Row;return [dict(x) for x in c.execute('SELECT * FROM r3_d4_ledger ORDER BY sequence').fetchall()]
    def _record(self,r):return {'record_type':r['record_type'],'record_id':r['record_id'],'created_at_utc':r['created_at_utc'],'previous_record_hash':r['previous_record_hash'],'record_hash':r['record_hash'],'payload':json.loads(r['payload_json'])}
    def rebuild_jsonl(self):
        rows=self._rows();tmp=self.path.with_suffix('.tmp')
        with open(tmp,'w',encoding='utf-8',newline='\n') as f:
            for r in rows:f.write(json.dumps(self._record(r),ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n')
            f.flush();os.fsync(f.fileno())
        os.replace(tmp,self.path);return len(rows)
    def append(self,record_type,payload,run_id=None,record_id=None):
        with self._lock():
            created=now();rid=record_id or uid('LEDGER');pj=json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(',',':'));ph=sha256_obj(payload)
            with self.rt.catalog.connect() as c:
                prevrow=c.execute('SELECT record_hash FROM r3_d4_ledger ORDER BY sequence DESC LIMIT 1').fetchone();prev=prevrow[0] if prevrow else 'GENESIS';basis={'record_type':record_type,'record_id':rid,'created_at_utc':created,'previous_record_hash':prev,'payload_hash':ph,'run_id':run_id};rh=sha256_obj(basis);c.execute('INSERT INTO r3_d4_ledger(record_id,record_type,record_hash,previous_record_hash,payload_hash,payload_json,run_id,created_at_utc) VALUES(?,?,?,?,?,?,?,?)',(rid,record_type,rh,prev,ph,pj,run_id,created))
            self.rebuild_jsonl();return {'record_type':record_type,'record_id':rid,'created_at_utc':created,'previous_record_hash':prev,'record_hash':rh,'payload':payload}
    def verify(self):
        with self._lock():
            rows=self._rows();prev='GENESIS';projected=[]
            for r in rows:
                try:payload=json.loads(r['payload_json'])
                except Exception:return False,'invalid payload JSON at '+r['record_id']
                ph=sha256_obj(payload)
                if ph!=r['payload_hash']:return False,'payload hash mismatch at '+r['record_id']
                if r['previous_record_hash']!=prev:return False,'previous hash mismatch at '+r['record_id']
                basis={'record_type':r['record_type'],'record_id':r['record_id'],'created_at_utc':r['created_at_utc'],'previous_record_hash':r['previous_record_hash'],'payload_hash':r['payload_hash'],'run_id':r['run_id']}
                if sha256_obj(basis)!=r['record_hash']:return False,'record hash mismatch at '+r['record_id']
                projected.append(json.dumps(self._record(r),ensure_ascii=False,sort_keys=True,separators=(',',':')));prev=r['record_hash']
            if self.path.exists():
                actual=[x.rstrip('\n') for x in self.path.read_text(encoding='utf-8').splitlines() if x.strip()]
                if actual!=projected:return False,'JSONL projection mismatch'
            return True,len(rows)
