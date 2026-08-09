# Prompt Registry and Pack Versioning

Every process has `prompt.md + manifest.json`. Prompt text, manifest, model capability profile and input artifact hashes are versioned. The Prompt Pack pins the exact collection used by a Run. A prompt edit therefore creates a new measurable research treatment rather than silently changing history.

Concrete provider/model names are not hard-coded. `model_profiles.json` defines capability intents; the host/R3 resolves them and records the binding.
