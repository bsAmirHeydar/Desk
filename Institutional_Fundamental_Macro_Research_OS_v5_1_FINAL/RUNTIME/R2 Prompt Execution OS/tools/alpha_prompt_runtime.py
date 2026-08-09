#!/usr/bin/env python3
import sys
from pathlib import Path
HERE=Path(__file__).resolve(); R2=HERE.parent.parent
if str(R2) not in sys.path: sys.path.insert(0,str(R2))
from alpha_prompt_runtime.cli import main
if __name__=='__main__': raise SystemExit(main())
