from __future__ import annotations
import json,sys
from pathlib import Path
HERE=Path(__file__).resolve();NEXT=HERE.parents[2]
if str(NEXT) not in sys.path:sys.path.insert(0,str(NEXT))
from AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0.runtime.forward_runtime import status as p09_status
from AD_V31_R04_INSTITUTIONAL_DATA_EDGE_OUTCOME_INFRASTRUCTURE.runtime.data_edge_runtime import status as r04_status
p=p09_status(NEXT/'AD_V3_PHASE_09_TRUE_FORWARD_VALIDATION_2_0');s=p.get('statistics') or {};print(json.dumps({'record_type':'AD_V31_R04_OUTCOME_INFRASTRUCTURE_STATUS','predictions':s.get('raw_prediction_count',0),'mature':s.get('clock_mature_episode_count',0),'evaluated':s.get('evaluated_mature_episode_count',0),'historically_recovered':s.get('historically_recovered_count',0),'mature_unevaluated':s.get('mature_unevaluated_count',0),'path_full':s.get('path_full_count',0),'path_partial':s.get('path_partial_count',0),'path_unavailable':s.get('path_unavailable_count',0),'store_health':r04_status().get('pit_store')},indent=2))
