CREATE TABLE IF NOT EXISTS web_codes (
    chat_id    INTEGER NOT NULL,
    code       TEXT    NOT NULL,
    created_at TEXT    NOT NULL,
    PRIMARY KEY (chat_id, code)
);
