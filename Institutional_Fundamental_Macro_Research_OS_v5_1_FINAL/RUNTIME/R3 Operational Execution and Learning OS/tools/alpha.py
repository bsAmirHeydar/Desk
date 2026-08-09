from pathlib import Path
import sys
HERE=Path(__file__).resolve();R3=HERE.parent.parent
if str(R3) not in sys.path:sys.path.insert(0,str(R3))
from alpha_operational_runtime.cli import main
if __name__=='__main__':raise SystemExit(main())
