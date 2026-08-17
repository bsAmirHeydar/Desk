from __future__ import annotations
import json,pathlib,sys
P=pathlib.Path(__file__).resolve().parents[1];N=P.parent

def main():
 required=[P/'runtime/presenter.py',P/'runtime/renderer.py',P/'schemas/control_room_view_model.schema.json',P/'schemas/report_receipt.schema.json',P/'config/label_registry.json',N/'AD_V3_PHASE_10_UNIFIED_RUNTIME_ONE_RUN/runtime/control_room_input.py']
 errors=[str(x) for x in required if not x.exists()]
 out={'status':'PASS' if not errors else 'FAIL','errors':errors,'canonical_renderer':'AD-V3-P11','input_contract':'ControlRoomInputV3','network_required':False,'trade_execution_authority':'NONE'};print(json.dumps(out,ensure_ascii=False,indent=2));return 0 if not errors else 2
if __name__=='__main__':raise SystemExit(main())
