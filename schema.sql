-- nook schema (D1 / SQLite). Apply once after `wrangler d1 create`:
--   npx wrangler d1 execute nook-db --remote --file=schema.sql

-- One row per saved thing (a link or a plain-text note).
CREATE TABLE IF NOT EXISTS items (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id      INTEGER NOT NULL,
    kind         TEXT    NOT NULL,              -- 'link' | 'note'
    title        TEXT    NOT NULL,
    url          TEXT    NOT NULL DEFAULT '',
    content      TEXT    NOT NULL,              -- extracted page text / note body
    summary      TEXT    NOT NULL DEFAULT '',   -- 2-3 sentence Workers AI summary
    tags         TEXT    NOT NULL DEFAULT '',   -- comma-separated, lowercase
    content_hash TEXT    NOT NULL UNIQUE,       -- sha256; dedupes repeat saves
    read         INTEGER NOT NULL DEFAULT 0,    -- 1 once it has been in a reads digest
    created_at   TEXT    NOT NULL
);

-- Keyword search over saved items: SQLite FTS5 gives us BM25 for free.
-- item_id rides along UNINDEXED so MATCH results map straight back to items.
CREATE VIRTUAL TABLE IF NOT EXISTS items_fts USING fts5(
    item_id UNINDEXED,
    title,
    summary,
    content
);

CREATE INDEX IF NOT EXISTS idx_items_chat ON items(chat_id, id);

-- Chat ids that get the daily digest (via /start).
CREATE TABLE IF NOT EXISTS subs (
    chat_id    INTEGER PRIMARY KEY,
    created_at TEXT    NOT NULL
);

-- Dedup for the job digest: which opening was already sent to which chat.
CREATE TABLE IF NOT EXISTS jobs_sent (
    chat_id  INTEGER NOT NULL,
    job_key  TEXT    NOT NULL,
    sent_at  TEXT    NOT NULL,
    PRIMARY KEY (chat_id, job_key)
);
