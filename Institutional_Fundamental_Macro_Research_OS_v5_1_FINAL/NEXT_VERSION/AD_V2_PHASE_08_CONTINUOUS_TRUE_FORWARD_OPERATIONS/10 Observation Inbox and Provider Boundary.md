# Observation inbox

External processes may write observation JSON/JSONL files to the configured P08 inbox. The cycle imports the inbox only **after** its commitment-freeze phase.

Processed files are moved to a processed area only after successful append-only ingestion. Invalid files are retained for operator inspection and are never silently discarded.

P08 does not embed provider credentials and does not make network requests.
