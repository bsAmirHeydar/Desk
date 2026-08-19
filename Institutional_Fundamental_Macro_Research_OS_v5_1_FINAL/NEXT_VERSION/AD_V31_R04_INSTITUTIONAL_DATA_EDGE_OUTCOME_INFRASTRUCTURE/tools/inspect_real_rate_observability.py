from __future__ import annotations
import json,sys
from pathlib import Path
HERE=Path(__file__).resolve();NEXT=HERE.parents[2]
if str(NEXT) not in sys.path:sys.path.insert(0,str(NEXT))
from AD_V31_R04_INSTITUTIONAL_DATA_EDGE_OUTCOME_INFRASTRUCTURE.runtime.data_edge_runtime import status
s=status();print(json.dumps({'official_daily':s['official_real_yield'],'intraday_proxy':s['intraday_real_rate_proxy'],'rule':'official daily is never relabeled live'},indent=2))
