#!/usr/bin/env python3
import json,pathlib
P=pathlib.Path(__file__).resolve().parents[1]
out={p.name:json.loads(p.read_text()) for p in sorted((P/'config').glob('*.json'))};print(json.dumps(out,ensure_ascii=False,indent=2))
