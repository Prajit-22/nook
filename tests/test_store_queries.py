"""SQL-level tests for the D1 statements in store.py, executed against a
real in-memory SQLite via a shim that mimics the D1 binding API."""

import sqlite3

import store as storemod


class ShimResult:
    def __init__(self, value):
        self._value = value

    def to_py(self):
        return self._value


class ShimStatement:
    def __init__(self, conn, sql):
        self._conn = conn
        self._sql = sql
        self._params = ()

    def bind(self, *params):
        self._params = params
        return self

    async def first(self):
        cur = self._conn.execute(self._sql, self._params)
        row = cur.fetchone()
        return ShimResult(dict(row) if row else None)

    async def all(self):
        cur = self._conn.execute(self._sql, self._params)
        return ShimResult({"results": [dict(r) for r in cur.fetchall()]})

    async def run(self):
        self._conn.execute(self._sql, self._params)
        self._conn.commit()
        return ShimResult({})


class ShimDB:
    def __init__(self, conn):
        self._conn = conn

    def prepare(self, sql):
        return ShimStatement(self._conn, sql)


def make_store(tmp_path):
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    schema = open(str(tmp_path / ".." / "schema.sql")).read() if False else None
    import pathlib
    schema = (pathlib.Path(__file__).resolve().parent.parent / "schema.sql").read_text()
    conn.executescript(schema)
    return storemod.NookStore(ShimDB(conn), ai=None)


import pytest


@pytest.mark.asyncio
async def test_item_roundtrip_and_fts(tmp_path):
    store = make_store(tmp_path)
    item_id = await store.create_item(
        1, "link", "RAG post", "https://x.io/rag", "retrieval augmented generation",
        "about rag", "rag, llm", "hash1")
    assert item_id == 1
    found = await store.find_item_by_hash(1, "hash1")
    assert found["title"] == "RAG post"
    hits = await store.fts_search(1, "retrieval")
    assert hits and hits[0]["id"] == 1
    other = await store.fts_search(2, "retrieval")  # per-chat isolation
    assert other == []


@pytest.mark.asyncio
async def test_fts_search_sanitizes_weird_input(tmp_path):
    store = make_store(tmp_path)
    await store.create_item(1, "note", "n", "", "plain words here", "", "", "h")
    # characters that would break raw FTS5 syntax must not raise
    assert await store.fts_search(1, 'plain OR "words" NEAR (broken:') is not None


@pytest.mark.asyncio
async def test_unread_mark_and_delete(tmp_path):
    store = make_store(tmp_path)
    i1 = await store.create_item(1, "link", "a", "https://a.io", "alpha", "", "", "h1")
    i2 = await store.create_item(1, "link", "b", "https://b.io", "beta", "", "", "h2")
    assert [i["id"] for i in await store.unread_items(1)] == [i1, i2]
    await store.mark_read(1, [i1])
    assert [i["id"] for i in await store.unread_items(1)] == [i2]
    assert await store.delete_item(1, i2) is True
    assert await store.delete_item(1, i2) is False
    assert await store.fts_search(1, "beta") == []  # FTS row gone too


@pytest.mark.asyncio
async def test_subs_and_job_dedup(tmp_path):
    store = make_store(tmp_path)
    await store.subscribe(1)
    await store.subscribe(1)  # idempotent
    await store.subscribe(2)
    assert await store.subscribers() == [1, 2]
    await store.unsubscribe(1)
    assert await store.subscribers() == [2]
    await store.mark_jobs_sent(2, ["k1", "k2"])
    await store.mark_jobs_sent(2, ["k1"])  # idempotent
    assert await store.sent_job_keys(2) == {"k1", "k2"}
