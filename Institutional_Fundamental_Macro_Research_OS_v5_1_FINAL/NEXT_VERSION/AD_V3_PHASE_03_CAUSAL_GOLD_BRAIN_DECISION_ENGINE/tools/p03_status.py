from pathlib import Path
import json
P=Path(__file__).resolve().parents[1]
print(json.dumps({'phase':'AD-V3-P03','installed':P.exists(),'deployment':'SHADOW_ONLY','production_direction_authority':False,'production_trade_permission_authority':False},indent=2))
