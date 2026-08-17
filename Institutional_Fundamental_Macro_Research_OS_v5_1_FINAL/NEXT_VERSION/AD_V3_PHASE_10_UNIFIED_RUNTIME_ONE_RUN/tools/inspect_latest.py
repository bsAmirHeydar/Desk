from __future__ import annotations
import json,pathlib
PH=pathlib.Path(__file__).resolve().parents[1]
def ld(p):return json.loads(p.read_text(encoding='utf-8-sig')) if p.exists() else None
print(json.dumps({'last_attempt':ld(PH/'artifacts/latest/last_attempt.json'),'last_success':ld(PH/'artifacts/latest/last_success.json')},indent=2,ensure_ascii=False))
