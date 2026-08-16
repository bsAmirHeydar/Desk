#!/usr/bin/env python3
from pathlib import Path
import json,sys
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE));from runtime.cluster import compile_cluster
print(json.dumps(compile_cluster(BASE),ensure_ascii=False,indent=2))
