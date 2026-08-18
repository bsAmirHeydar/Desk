#!/usr/bin/env python3
from pathlib import Path
import sys
P=Path(__file__).resolve().parents[1]
raise SystemExit(__import__('subprocess').run([sys.executable,str(P/'tools/run_r02_acceptance.py')]).returncode)
