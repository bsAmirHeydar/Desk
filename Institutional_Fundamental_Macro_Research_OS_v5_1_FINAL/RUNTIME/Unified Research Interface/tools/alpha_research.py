from pathlib import Path
import sys
HERE=Path(__file__).resolve();ROOT=HERE.parent.parent
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from alpha_interface_runtime.cli import main
if __name__=='__main__':raise SystemExit(main())
