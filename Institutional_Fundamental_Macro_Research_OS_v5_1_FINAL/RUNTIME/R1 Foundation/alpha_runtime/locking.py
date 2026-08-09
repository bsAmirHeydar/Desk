from pathlib import Path
import os, time

class FileLock:
    def __init__(self,path,timeout=15.0): self.path=Path(path); self.timeout=timeout; self.f=None
    def __enter__(self):
        self.path.parent.mkdir(parents=True,exist_ok=True)
        self.f=open(self.path,"a+b")
        deadline=time.time()+self.timeout
        while True:
            try:
                if os.name=="nt":
                    import msvcrt; self.f.seek(0); msvcrt.locking(self.f.fileno(),msvcrt.LK_NBLCK,1)
                else:
                    import fcntl; fcntl.flock(self.f.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
                break
            except (OSError,IOError):
                if time.time()>=deadline: raise TimeoutError(f"lock timeout: {self.path}")
                time.sleep(.05)
        return self
    def __exit__(self,*args):
        try:
            if self.f:
                if os.name=="nt":
                    import msvcrt; self.f.seek(0); msvcrt.locking(self.f.fileno(),msvcrt.LK_UNLCK,1)
                else:
                    import fcntl; fcntl.flock(self.f.fileno(),fcntl.LOCK_UN)
        finally:
            if self.f: self.f.close()
