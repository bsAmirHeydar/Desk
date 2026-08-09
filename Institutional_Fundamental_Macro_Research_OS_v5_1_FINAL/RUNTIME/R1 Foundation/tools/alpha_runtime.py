#!/usr/bin/env python3
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE))
from alpha_runtime.cli import main
if __name__=='__main__': raise SystemExit(main())
