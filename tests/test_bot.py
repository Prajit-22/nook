"""End-to-end orchestration tests with fakes for store, send, fetch."""

import bot as botmod
from telegram_api import parse_update


class FakeStore:
    def __init__(self):
        self.items = {}
        self.next_id = 1
        self.subs = set()
        self.sent_keys = set()
        self.ai_calls = []

    async def chat(self, messages):
        self.ai_calls.append(messages)
        return "fake ai answer."

    async def find_item_by_hash(self, chat_id, digest):
        for it in self.items.values():
            if it["chat_id"] == chat_id and it["content_hash"] == digest:
                return it
        return None

    async def create_item(self, chat_id, kind, title, url, content, summary, tags, digest):
        item_id = self.next_id
        self.next_id += 1
        self.items[item_id] = dict(id=item_id, chat_id=chat_id, kind=kind, title=title,
                                   url=url, content=content, summary=summary, tags=tags,
                                   content_hash=digest, read=0)
        return item_id

    async def list_items(self, chat_id, limit=10):
        mine = [i for i in self.items.values() if i["chat_id"] == chat_id]
        return sorted(mine, key=lambda i: -i["id"])[:limit]

    async def unread_items(self, chat_id):
        return [i for i in self.items.values() if i["chat_id"] == chat_id and not i["read"]]

    async def mark_read(self, chat_id, ids):
        for i in ids:
            if i in self.items:
                self.items[i]["read"] = 1

    async def delete_item(self, chat_id, item_id):
        if item_id in self.items and self.items[item_id]["chat_id"] == chat_id:
            del self.items[item_id]
            return True
        return False

    async def fts_search(self, chat_id, query, limit=5):
        words = {"".join(ch for ch in w if ch.isalnum()) for w in query.lower().split()}
        words.discard("")
        hits = [i for i in self.items.values()
                if i["chat_id"] == chat_id and words & set((i["title"] + " " + i["content"]).lower().split())]
        return hits[:limit]

    async def subscribe(self, chat_id):
        self.subs.add(chat_id)

    async def unsubscribe(self, chat_id):
        self.subs.discard(chat_id)

    async def subscribers(self):
        return sorted(self.subs)

    async def sent_job_keys(self, chat_id):
        return set(self.sent_keys)

    async def mark_jobs_sent(self, chat_id, keys):
        self.sent_keys.update(keys)


PAGE = """<html><head><title>Great RAG Post</title></head>
<body><article><p>Retrieval augmented generation explained well.</p></article></body></html>"""

FEED = [
    {"key": "r:1", "title": "Backend Intern", "company": "Acme",
     "url": "https://jobs.io/1", "salary": "$20k-$30k/yr", "tags": ["python", "backend"],
     "date": "2026-10-22"},
]


def make_bot(store, sent, page=PAGE, feed=FEED, **kwargs):
    async def fetch_page(url):
        return page

    async def fetch_jobs_feed():
        return feed

    async def send(chat_id, text):
        sent.append((chat_id, text))

    kwargs.setdefault("job_keywords", "python,backend,intern")
    return botmod.Nook(store=store, send=send, fetch_page=fetch_page,
                       fetch_jobs_feed=fetch_jobs_feed, **kwargs)


def update(chat_id, text):
    return parse_update({"message": {"chat": {"id": chat_id}, "text": text}})


import pytest


@pytest.mark.asyncio
async def test_save_link_summarizes_and_stores():
    store, sent = FakeStore(), []
    nook = make_bot(store, sent)
    await nook.handle_update(update(1, "check this https://x.io/rag"))
    assert store.items[1]["title"] == "Great RAG Post"
    assert "fake ai answer." in store.items[1]["summary"]
    assert "Saved #1: Great RAG Post" in sent[-1][1]


@pytest.mark.asyncio
async def test_save_link_dedupes_by_url():
    store, sent = FakeStore(), []
    nook = make_bot(store, sent)
    await nook.handle_update(update(1, "https://x.io/rag"))
    await nook.handle_update(update(1, "https://x.io/rag"))
    assert len(store.items) == 1
    assert "Already in your nook as #1" in sent[-1][1]


@pytest.mark.asyncio
async def test_save_link_fetch_failure_saves_bare_link():
    store, sent = FakeStore(), []
    nook = make_bot(store, sent, page=None)
    await nook.handle_update(update(1, "https://down.example.com/x"))
    assert store.items[1]["title"] == "down.example.com"
    assert "Could not fetch" in sent[-1][1]


@pytest.mark.asyncio
async def test_note_command():
    store, sent = FakeStore(), []
    nook = make_bot(store, sent)
    await nook.handle_update(update(1, "/note remember the milk"))
    assert store.items[1]["kind"] == "note"
    assert "Saved #1" in sent[-1][1]
    await nook.handle_update(update(1, "/note"))
    assert "Nothing to save" in sent[-1][1]


@pytest.mark.asyncio
async def test_plain_text_is_a_question_over_the_nook():
    store, sent = FakeStore(), []
    nook = make_bot(store, sent)
    await nook.handle_update(update(1, "https://x.io/rag"))
    await nook.handle_update(update(1, "what is retrieval?"))
    assert "Sources:" in sent[-1][1] and "#1" in sent[-1][1]


@pytest.mark.asyncio
async def test_question_with_no_hits():
    store, sent = FakeStore(), []
    nook = make_bot(store, sent)
    await nook.handle_update(update(1, "totally unrelated zzz"))
    assert "could not find anything" in sent[-1][1]


@pytest.mark.asyncio
async def test_start_subscribes_and_stop_unsubscribes():
    store, sent = FakeStore(), []
    nook = make_bot(store, sent)
    await nook.handle_update(update(9, "/start"))
    assert 9 in store.subs
    await nook.handle_update(update(9, "/stop"))
    assert 9 not in store.subs


@pytest.mark.asyncio
async def test_forget():
    store, sent = FakeStore(), []
    nook = make_bot(store, sent)
    await nook.handle_update(update(1, "https://x.io/rag"))
    await nook.handle_update(update(1, "/forget 1"))
    assert store.items == {}
    await nook.handle_update(update(1, "/forget 99"))
    assert "No #99" in sent[-1][1]


@pytest.mark.asyncio
async def test_jobs_digest_sends_once_then_quiet():
    store, sent = FakeStore(), []
    nook = make_bot(store, sent)
    await nook.handle_update(update(1, "/jobs"))
    assert "Backend Intern @ Acme" in sent[-1][1]
    await nook.handle_update(update(1, "/jobs"))
    assert "No fresh paid openings" in sent[-1][1]  # deduped via jobs_sent


@pytest.mark.asyncio
async def test_reads_digest_marks_read():
    store, sent = FakeStore(), []
    nook = make_bot(store, sent)
    await nook.handle_update(update(1, "https://x.io/rag"))
    await nook.handle_update(update(1, "/reads"))
    assert "IN YOUR NOOK" in sent[-1][1]
    assert store.items[1]["read"] == 1
    await nook.handle_update(update(1, "/reads"))
    assert "Nothing unread" in sent[-1][1]


@pytest.mark.asyncio
async def test_daily_digest_combines_and_marks():
    store, sent = FakeStore(), []
    nook = make_bot(store, sent)
    await nook.handle_update(update(1, "/start"))
    await nook.handle_update(update(1, "https://x.io/rag"))
    sent.clear()
    await nook.run_daily_digest(await store.subscribers())
    combined = sent[0][1]
    assert "Nook letter, sealed and delivered" in combined
    assert "IN YOUR NOOK" in combined and "FRESH OPENINGS" in combined
    assert store.items[1]["read"] == 1 and "r:1" in store.sent_keys


@pytest.mark.asyncio
async def test_allowlist_blocks_strangers():
    store, sent = FakeStore(), []
    nook = make_bot(store, sent, allowed_chat_ids={1})
    await nook.handle_update(update(999, "https://x.io/rag"))
    assert "private" in sent[-1][1]
    assert store.items == {}


@pytest.mark.asyncio
async def test_unknown_command_and_help():
    store, sent = FakeStore(), []
    nook = make_bot(store, sent)
    await nook.handle_update(update(1, "/frobulate"))
    assert "Unknown command" in sent[-1][1]
    await nook.handle_update(update(1, "/help"))
    assert "/note" in sent[-1][1]
