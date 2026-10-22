"""Thin adapter over the Cloudflare bindings (D1 + Workers AI).

Deliberately boring: every prompt lives in prompts.py, every orchestration
decision in bot.py. This file only translates Python calls into binding
calls and converts Pyodide JsProxy results back into plain Python via _py.
"""

from typing import Dict, List, Optional

DEFAULT_LLM_MODEL = "@cf/meta/llama-3.1-8b-instruct"


def _py(value):
    """Convert a Pyodide JsProxy into a native Python object when needed.
    Plain Python objects (as in tests/demo) pass straight through."""
    if hasattr(value, "to_py"):
        return value.to_py()
    return value


class NookStore:
    def __init__(self, db, ai, llm_model=None):
        self._db = db
        self._ai = ai
        self._llm_model = llm_model or DEFAULT_LLM_MODEL

    # ---- Workers AI ------------------------------------------------------

    async def chat(self, messages: List[Dict[str, str]]) -> str:
        resp = _py(await self._ai.run(self._llm_model, {"messages": messages}))
        return resp.get("response", "")

    # ---- items -----------------------------------------------------------

    async def find_item_by_hash(self, chat_id: int, digest: str) -> Optional[Dict]:
        row = _py(
            await self._db.prepare(
                "SELECT id, title FROM items WHERE chat_id = ? AND content_hash = ?"
            )
            .bind(chat_id, digest)
            .first()
        )
        return dict(row) if row else None

    async def create_item(self, chat_id, kind, title, url, content, summary, tags, digest) -> int:
        row = _py(
            await self._db.prepare(
                "INSERT INTO items (chat_id, kind, title, url, content, summary, tags, content_hash,"
                " created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now')) RETURNING id"
            )
            .bind(chat_id, kind, title, url, content, summary, tags, digest)
            .first()
        )
        item_id = int(row["id"])
        await self._db.prepare(
            "INSERT INTO items_fts (item_id, title, summary, content) VALUES (?, ?, ?, ?)"
        ).bind(item_id, title, summary, content[:6000]).run()
        return item_id

    async def list_items(self, chat_id: int, limit: int = 10) -> List[Dict]:
        rows = _py(
            await self._db.prepare(
                "SELECT id, title, url, summary, tags, read FROM items"
                " WHERE chat_id = ? ORDER BY id DESC LIMIT ?"
            )
            .bind(chat_id, limit)
            .all()
        )
        return [dict(r) for r in (rows.get("results") if isinstance(rows, dict) else rows) or []]

    async def unread_items(self, chat_id: int) -> List[Dict]:
        rows = _py(
            await self._db.prepare(
                "SELECT id, title, url, summary, tags FROM items"
                " WHERE chat_id = ? AND read = 0 ORDER BY id ASC"
            )
            .bind(chat_id)
            .all()
        )
        return [dict(r) for r in (rows.get("results") if isinstance(rows, dict) else rows) or []]

    async def mark_read(self, chat_id: int, item_ids) -> None:
        for item_id in item_ids:
            await self._db.prepare(
                "UPDATE items SET read = 1 WHERE chat_id = ? AND id = ?"
            ).bind(chat_id, int(item_id)).run()

    async def delete_item(self, chat_id: int, item_id: int) -> bool:
        existing = _py(
            await self._db.prepare("SELECT id FROM items WHERE chat_id = ? AND id = ?")
            .bind(chat_id, item_id)
            .first()
        )
        if not existing:
            return False
        await self._db.prepare("DELETE FROM items_fts WHERE item_id = ?").bind(item_id).run()
        await self._db.prepare("DELETE FROM items WHERE id = ?").bind(item_id).run()
        return True

    async def fts_search(self, chat_id: int, match_query: str, limit: int = 5) -> List[Dict]:
        """BM25 keyword search via SQLite FTS5. The query is sanitized to a
        plain AND of words so user text can never break FTS5 syntax."""
        words = [w for w in "".join(
            ch if ch.isalnum() else " " for ch in match_query
        ).split() if len(w) > 2]
        if not words:
            return []
        query = " ".join(f'"{w}"' for w in words[:8])
        rows = _py(
            await self._db.prepare(
                "SELECT i.id, i.title, i.url, i.summary, i.content FROM items_fts f"
                " JOIN items i ON i.id = f.item_id"
                " WHERE items_fts MATCH ? AND i.chat_id = ?"
                " ORDER BY bm25(items_fts) LIMIT ?"
            )
            .bind(query, chat_id, limit)
            .all()
        )
        return [dict(r) for r in (rows.get("results") if isinstance(rows, dict) else rows) or []]

    # ---- digest subscriptions --------------------------------------------

    async def subscribe(self, chat_id: int) -> None:
        await self._db.prepare(
            "INSERT INTO subs (chat_id, created_at) VALUES (?, datetime('now'))"
            " ON CONFLICT(chat_id) DO NOTHING"
        ).bind(chat_id).run()

    async def unsubscribe(self, chat_id: int) -> None:
        await self._db.prepare("DELETE FROM subs WHERE chat_id = ?").bind(chat_id).run()

    async def subscribers(self) -> List[int]:
        rows = _py(await self._db.prepare("SELECT chat_id FROM subs").all())
        result = rows.get("results") if isinstance(rows, dict) else rows
        return [int(r["chat_id"]) for r in result or []]

    # ---- job digest dedup --------------------------------------------------

    async def sent_job_keys(self, chat_id: int) -> set:
        rows = _py(
            await self._db.prepare("SELECT job_key FROM jobs_sent WHERE chat_id = ?")
            .bind(chat_id)
            .all()
        )
        result = rows.get("results") if isinstance(rows, dict) else rows
        return {r["job_key"] for r in result or []}

    async def mark_jobs_sent(self, chat_id: int, keys) -> None:
        for key in keys:
            await self._db.prepare(
                "INSERT INTO jobs_sent (chat_id, job_key, sent_at) VALUES (?, ?, datetime('now'))"
                " ON CONFLICT DO NOTHING"
            ).bind(chat_id, key).run()
