PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;

CREATE TABLE IF NOT EXISTS runtime_metadata (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS episodes (
    episode_id TEXT PRIMARY KEY,
    research_program_id TEXT NOT NULL,
    episode_type TEXT NOT NULL,
    subject TEXT,
    created_at_utc TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS runs (
    run_id TEXT PRIMARY KEY,
    episode_id TEXT,
    research_program_id TEXT NOT NULL,
    run_scope TEXT NOT NULL,
    subject TEXT NOT NULL,
    run_mode TEXT NOT NULL,
    analysis_cutoff_utc TEXT NOT NULL,
    state TEXT NOT NULL,
    request_fingerprint TEXT NOT NULL,
    run_fingerprint TEXT,
    run_relpath TEXT NOT NULL,
    vault_stack TEXT NOT NULL,
    runtime_version TEXT NOT NULL,
    manifest_revision INTEGER NOT NULL,
    decision_seal_hash TEXT,
    run_close_seal_hash TEXT,
    created_at_utc TEXT NOT NULL,
    updated_at_utc TEXT NOT NULL,
    FOREIGN KEY(episode_id) REFERENCES episodes(episode_id)
);
CREATE INDEX IF NOT EXISTS idx_runs_cutoff ON runs(analysis_cutoff_utc);
CREATE INDEX IF NOT EXISTS idx_runs_subject ON runs(subject, run_mode);
CREATE INDEX IF NOT EXISTS idx_runs_request_fp ON runs(request_fingerprint);

CREATE TABLE IF NOT EXISTS artifacts (
    artifact_hash TEXT PRIMARY KEY,
    byte_length INTEGER NOT NULL,
    media_type TEXT NOT NULL,
    object_relpath TEXT NOT NULL,
    created_at_utc TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS run_artifacts (
    run_id TEXT NOT NULL,
    logical_name TEXT NOT NULL,
    world TEXT NOT NULL,
    stage TEXT NOT NULL,
    artifact_hash TEXT NOT NULL,
    ref_relpath TEXT NOT NULL,
    immutable INTEGER NOT NULL DEFAULT 0,
    created_at_utc TEXT NOT NULL,
    PRIMARY KEY(run_id, logical_name),
    FOREIGN KEY(run_id) REFERENCES runs(run_id),
    FOREIGN KEY(artifact_hash) REFERENCES artifacts(artifact_hash)
);
CREATE INDEX IF NOT EXISTS idx_run_artifacts_world ON run_artifacts(run_id, world, stage);

CREATE TABLE IF NOT EXISTS run_events (
    run_id TEXT NOT NULL,
    sequence INTEGER NOT NULL,
    event_type TEXT NOT NULL,
    from_state TEXT,
    to_state TEXT,
    occurred_at_utc TEXT NOT NULL,
    details_json TEXT NOT NULL,
    PRIMARY KEY(run_id, sequence),
    FOREIGN KEY(run_id) REFERENCES runs(run_id)
);

CREATE TABLE IF NOT EXISTS seals (
    run_id TEXT NOT NULL,
    seal_type TEXT NOT NULL,
    seal_hash TEXT NOT NULL,
    artifact_hash TEXT NOT NULL,
    created_at_utc TEXT NOT NULL,
    PRIMARY KEY(run_id, seal_type),
    FOREIGN KEY(run_id) REFERENCES runs(run_id)
);

CREATE TABLE IF NOT EXISTS replay_links (
    source_run_id TEXT NOT NULL,
    replay_run_id TEXT NOT NULL,
    replay_mode TEXT NOT NULL,
    visibility_parity INTEGER,
    created_at_utc TEXT NOT NULL,
    PRIMARY KEY(source_run_id, replay_run_id),
    FOREIGN KEY(source_run_id) REFERENCES runs(run_id),
    FOREIGN KEY(replay_run_id) REFERENCES runs(run_id)
);
