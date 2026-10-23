"""Orchestration: what the bot does with each Telegram update, and what the
daily cron digest sends. Pure Python around injected async callables
(store, send, fetch_page, fetch_jobs_feed) so the whole flow is testable.
"""

import digest as dg
import extract
import jobs as joblib
import prompts


class Nook:
    def __init__(self, store, send, fetch_page, fetch_jobs_feed,
                 allowed_chat_ids=None, job_keywords=None,
                 max_jobs=6, max_reads=5, bot_name="Nook"):
        self._store = store
        self._send = send
        self._fetch_page = fetch_page      # async url -> html str or None
        self._fetch_jobs_feed = fetch_jobs_feed  # async () -> list[job dict]
        self._allowed = allowed_chat_ids
        self._keywords = joblib.parse_keywords(
            job_keywords if job_keywords is not None else joblib.DEFAULT_KEYWORDS
        )
        self._max_jobs = max_jobs
        self._max_reads = max_reads
        self._bot_name = bot_name

    async def handle_update(self, update) -> None:
        chat_id = update.chat_id
        text = update.text
        if self._allowed is not None and chat_id not in self._allowed:
            await self._send(chat_id, "This bot is private to its owner.")
            return

        cmd, rest = self._split_command(text)
        if cmd == "start":
            await self._store.subscribe(chat_id)
            if rest.lower() == "webkey":
                # Deep link from the web sign-in page: hand over a key directly.
                await self._web_code(chat_id)
            else:
                await self._send(chat_id, dg.WELCOME,
                                 url_button=("Open Nook", dg.APP_URL + "/app"))
        elif cmd in ("help", "commands"):
            await self._send(chat_id, dg.HELP)
        elif cmd == "stop":
            await self._store.unsubscribe(chat_id)
            await self._send(chat_id, "Daily digest paused. /start to resume; your saves stay put.")
        elif cmd == "note":
            await self._save_note(chat_id, rest)
        elif cmd in ("jobs", "job"):
            await self._send(chat_id, "Checking the boards...")
            await self.send_jobs_digest(chat_id)
        elif cmd in ("reads", "read"):
            await self.send_reads_digest(chat_id)
        elif cmd == "readall":
            unread = await self._store.unread_items(chat_id)
            await self._store.mark_read(chat_id, [i["id"] for i in unread])
            await self._send(chat_id, f"Marked {len(unread)} item(s) as read.")
        elif cmd == "list":
            await self._list(chat_id)
        elif cmd == "forget":
            await self._forget(chat_id, rest)
        elif cmd == "web":
            await self._web_code(update.chat_id)
        elif cmd == "ask":
            await self._answer(chat_id, rest)
        elif cmd is not None:
            await self._send(chat_id, "Unknown command. /help lists what I understand.")
        else:
            urls = extract.find_urls(text)
            if urls:
                await self._save_link(chat_id, urls[0], note=text)
            else:
                await self._answer(chat_id, text)

    # ---- commands ----------------------------------------------------------

    @staticmethod
    def _split_command(text: str):
        from telegram_api import command_of

        return command_of(text)

    async def _save_note(self, chat_id: int, note: str) -> None:
        if not note:
            await self._send(chat_id, "Nothing to save - try /note followed by your thought.")
            return
        digest = extract.content_hash("note:" + note)
        existing = await self._store.find_item_by_hash(chat_id, digest)
        if existing:
            await self._send(chat_id, f"Already in your nook as #{existing['id']}.")
            return
        summary = prompts.clean_summary(await self._store.chat(prompts.summarize_messages("note", note)))
        item_id = await self._store.create_item(
            chat_id, "note", note[:80], "", note, summary, "", digest
        )
        await self._send(chat_id, f"Saved #{item_id}. {summary}")

    async def _save_link(self, chat_id: int, url: str, note: str = "") -> None:
        digest = extract.content_hash("link:" + url)
        existing = await self._store.find_item_by_hash(chat_id, digest)
        if existing:
            await self._send(chat_id, f"Already in your nook as #{existing['id']} ({existing['title']}).")
            return
        page_html = await self._fetch_page(url)
        if not page_html:
            await self._send(chat_id, f"Could not fetch that page - saved the bare link instead.\n{url}")
            await self._store.create_item(chat_id, "link", extract.fallback_title(url), url, url, "", "", digest)
            return
        title = extract.extract_title(page_html) or extract.fallback_title(url)
        content = extract.html_to_text(page_html)
        if not content:
            await self._store.create_item(chat_id, "link", title, url, url, "", "", digest)
            await self._send(chat_id, f"Saved #{title} - the page had no readable text, kept the link.")
            return
        summary = prompts.clean_summary(await self._store.chat(prompts.summarize_messages(title, content)))
        tags = prompts.clean_tags(await self._store.chat(prompts.tags_messages(title, content)))
        item_id = await self._store.create_item(chat_id, "link", title, url, content, summary, tags, digest)
        tag_line = f"\n[{tags}]" if tags else ""
        await self._send(chat_id, f"Saved #{item_id}: {title}\n{summary}{tag_line}")

    async def _answer(self, chat_id: int, question: str) -> None:
        if not question.strip():
            await self._send(chat_id, "Ask me something about your saved links.")
            return
        sources = await self._store.fts_search(chat_id, question)
        if not sources:
            await self._send(chat_id, dg.NO_MATCH_ANSWER)
            return
        answer = (await self._store.chat(prompts.answer_messages(question, sources))).strip()
        titles = "\n".join(f"[{i + 1}] #{s['id']} {s['title']}" for i, s in enumerate(sources))
        await self._send(chat_id, f"{answer}\n\nSources:\n{titles}")

    async def _list(self, chat_id: int) -> None:
        items = await self._store.list_items(chat_id, limit=10)
        if not items:
            await self._send(chat_id, "Your nook is empty. Send me a link.")
            return
        lines = ["Latest in your nook:"]
        for item in items:
            mark = "" if item.get("read") else " (unread)"
            lines.append(f"#{item['id']} {item['title']}{mark}")
        lines.append("\n/forget <id> to remove one, /reads for summaries.")
        await self._send(chat_id, "\n".join(lines))

    async def _forget(self, chat_id: int, arg: str) -> None:
        try:
            item_id = int(arg.strip().lstrip("#"))
        except ValueError:
            await self._send(chat_id, "Which one? Try /forget 3 (ids from /list).")
            return
        if await self._store.delete_item(chat_id, item_id):
            await self._send(chat_id, f"Forgot #{item_id}.")
        else:
            await self._send(chat_id, f"No #{item_id} in your nook.")

    # ---- digests (on-demand and cron) -------------------------------------

    async def _web_code(self, chat_id: int) -> None:
        import secrets
        # No 0/O, 1/I/L - every code reads the same in any font.
        alphabet = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"
        code = "".join(secrets.choice(alphabet) for _ in range(6))
        await self._store.create_web_code(chat_id, code)
        link = dg.APP_URL + "/app?key=" + code
        await self._send(
            chat_id,
            "One tap and you are in - the button below signs you in on this device.\n"
            "On a laptop, open " + dg.APP_URL + "/app and type " + code + ".\n"
            "Good for ten minutes, one use - ask again with /web for a fresh one.",
            url_button=("Open Nook", link),
        )

    async def send_reads_digest(self, chat_id: int, mark_read=True) -> None:
        unread = await self._store.unread_items(chat_id)
        if not unread:
            await self._send(chat_id, "Nothing unread in your nook. Send me a link.")
            return
        await self._send(chat_id, dg.format_reads_section(unread, limit=self._max_reads))
        if mark_read:
            await self._store.mark_read(chat_id, [i["id"] for i in unread])

    async def send_jobs_digest(self, chat_id: int) -> None:
        feed = await self._fetch_jobs_feed()
        seen = await self._store.sent_job_keys(chat_id)
        picked = joblib.select_jobs(
            feed, self._keywords, paid_only=True,
            limit=self._max_jobs, exclude_keys=seen,
        )
        if not picked:
            await self._send(chat_id, "No fresh paid openings matching your keywords right now.")
            return
        await self._send(chat_id, dg.format_jobs_section(picked))
        await self._store.mark_jobs_sent(chat_id, [j["key"] for j in picked])

    async def run_daily_digest(self, chat_ids) -> None:
        """Cron entry: one combined message per subscriber."""
        feed = await self._fetch_jobs_feed()
        for chat_id in chat_ids:
            try:
                unread = await self._store.unread_items(chat_id)
                seen = await self._store.sent_job_keys(chat_id)
                picked = joblib.select_jobs(
                    feed, self._keywords, paid_only=True,
                    limit=self._max_jobs, exclude_keys=seen,
                )
                await self._send(chat_id, dg.format_digest(unread, picked, reads_limit=self._max_reads))
                if unread:
                    await self._store.mark_read(chat_id, [i["id"] for i in unread])
                if picked:
                    await self._store.mark_jobs_sent(chat_id, [j["key"] for j in picked])
            except Exception as exc:  # one bad chat must not kill the batch
                print("daily digest failed for %s: %r" % (chat_id, exc))
