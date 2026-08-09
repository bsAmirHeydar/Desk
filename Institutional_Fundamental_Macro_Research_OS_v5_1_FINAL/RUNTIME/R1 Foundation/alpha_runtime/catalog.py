from pathlib import Path
import sqlite3
from contextlib import contextmanager

class Catalog:
    def __init__(self,data_root,ddl_path,busy_timeout_ms=15000):
        self.data_root=Path(data_root); self.db=self.data_root/"catalog"/"catalog.sqlite3"; self.ddl=Path(ddl_path); self.busy=busy_timeout_ms
    @contextmanager
    def connect(self):
        self.db.parent.mkdir(parents=True,exist_ok=True)
        c=sqlite3.connect(self.db,timeout=self.busy/1000)
        try:
            c.execute("PRAGMA foreign_keys=ON")
            c.execute("PRAGMA journal_mode=WAL")
            c.execute(f"PRAGMA busy_timeout={int(self.busy)}")
            yield c
            c.commit()
        except Exception:
            c.rollback()
            raise
        finally:
            c.close()
    def init(self):
        with self.connect() as c: c.executescript(self.ddl.read_text(encoding="utf-8"))
    def checkpoint(self):
        with self.connect() as c:
            c.execute("PRAGMA wal_checkpoint(TRUNCATE)")
    def get_run(self,run_id):
        with self.connect() as c:
            c.row_factory=sqlite3.Row; r=c.execute("SELECT * FROM runs WHERE run_id=?",(run_id,)).fetchone(); return dict(r) if r else None
    def find_request(self,fp):
        with self.connect() as c:
            c.row_factory=sqlite3.Row; r=c.execute("SELECT * FROM runs WHERE request_fingerprint=? ORDER BY created_at_utc LIMIT 1",(fp,)).fetchone(); return dict(r) if r else None
    def upsert_artifact(self,ref):
        with self.connect() as c:
            c.execute("INSERT OR IGNORE INTO artifacts(artifact_hash,byte_length,media_type,object_relpath,created_at_utc) VALUES(?,?,?,?,?)",(ref['artifact_hash'],ref['byte_length'],ref['media_type'],ref['object_relpath'],ref['created_at_utc']))
    def register_run_artifact(self,run_id,ref,ref_relpath,immutable=0):
        with self.connect() as c:
            c.execute("INSERT INTO run_artifacts(run_id,logical_name,world,stage,artifact_hash,ref_relpath,immutable,created_at_utc) VALUES(?,?,?,?,?,?,?,?)",(run_id,ref['logical_name'],ref['world'],ref['stage'],ref['artifact_hash'],ref_relpath,int(immutable),ref['created_at_utc']))
    def list_artifacts(self,run_id,world=None):
        q="SELECT * FROM run_artifacts WHERE run_id=?"; args=[run_id]
        if world: q+=" AND world=?"; args.append(world)
        q+=" ORDER BY world,stage,logical_name"
        with self.connect() as c:
            c.row_factory=sqlite3.Row; return [dict(x) for x in c.execute(q,args).fetchall()]
