from pathlib import Path
import sys
HERE=Path(__file__).resolve();C1=HERE.parent.parent
if str(C1) not in sys.path:sys.path.insert(0,str(C1))
from alpha_commissioning.openai_host import main
if __name__=='__main__':raise SystemExit(main())
