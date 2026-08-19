#!/usr/bin/env python3
from pathlib import Path
import subprocess,sys
P=Path(__file__).resolve().parents[1];raise SystemExit(subprocess.run([sys.executable,str(P/'tools/run_r03_acceptance.py')]).returncode)
