"""Cloudflare Python Worker entry point.

This module is the ONLY one that touches the Workers runtime (js.fetch, the
workers SDK, Pyodide FFI). It wires the pure/testable modules together:

    Telegram webhook -> parse_update -> Nook -> NookStore -> D1/Workers AI
    cron -> Nook.run_daily_digest
    GET / -> landing page (web.py)

Run locally with `uv run pywrangler dev`; deploy with `uv run pywrangler
deploy`. Unit tests do not import this file (there is no Workers runtime in
CI) - they cover every module it wires up.
"""

import json

from js import Object, fetch
from pyodide.ffi import to_js
from workers import Response, WorkerEntrypoint

import jobs as joblib
from bot import Nook
from store import NookStore
from telegram_api import api_url, build_send_payload, parse_update, split_message, verify_secret
from web import LANDING_HTML, NOT_FOUND_HTML, SERVER_ERROR_HTML

USER_AGENT = "nook-bot/0.1 (+https://github.com/Prajit-22/nook)"
FETCH_HEADERS = {"User-Agent": USER_AGENT, "Accept": "text/html,application/json"}


def _js(value):
    """Deep-convert a Python dict/list into real JS objects for the FFI."""
    return to_js(value, dict_converter=Object.fromEntries)


class Default(WorkerEntrypoint):
    async def fetch(self, request):
        try:
            return await self._route(request)
        except Exception:
            return Response(
                SERVER_ERROR_HTML,
                status=500,
                headers={"content-type": "text/html; charset=utf-8"},
            )

    async def _route(self, request):
        after_host = request.url.split("://", 1)[-1]
        path = "/" + after_host.split("/", 1)[1] if "/" in after_host else "/"
        path = path.split("?")[0].rstrip("/") or "/"
        if request.method == "GET":
            if path == "/health":
                return Response("ok", headers={"cache-control": "no-store"})
            if path == "/":
                return Response(
                    LANDING_HTML,
                    headers={
                        "content-type": "text/html; charset=utf-8",
                        "cache-control": "public, max-age=300",
                        "x-content-type-options": "nosniff",
                        "referrer-policy": "strict-origin-when-cross-origin",
                    },
                )
            return self._not_found()
        if request.method != "POST" or not path.endswith("/webhook"):
            return self._not_found()

        provided = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
        if not verify_secret(provided, self.env.TELEGRAM_WEBHOOK_SECRET):
            return Response("forbidden", status=403)

        try:
            body = await request.json()
            if hasattr(body, "to_py"):
                body = body.to_py()
        except Exception:
            return Response("ok")  # never make Telegram retry unparseable JSON
        update = parse_update(body) if isinstance(body, dict) else None
        if update is None:
            return Response("ok")

        # Ack immediately (Telegram retries slow webhooks); the AI work
        # finishes in the background and replies go out via sendMessage.
        self.ctx.waitUntil(self._guarded(update))
        return Response("ok")

    def _not_found(self):
        return Response(
            NOT_FOUND_HTML,
            status=404,
            headers={"content-type": "text/html; charset=utf-8"},
        )

    async def scheduled(self, event):
        store = self._store()
        bot = self._bot(store)
        await bot.run_daily_digest(await store.subscribers())

    # ---- wiring ------------------------------------------------------------

    def _store(self):
        return NookStore(self.env.DB, self.env.AI, llm_model=self.env.LLM_MODEL)

    def _bot(self, store):
        allowed = {
            int(part.strip())
            for part in (self.env.ALLOWED_CHAT_IDS or "").split(",")
            if part.strip().lstrip("-").isdigit()
        }
        return Nook(
            store=store,
            send=self._send,
            fetch_page=self._fetch_page,
            fetch_jobs_feed=self._fetch_jobs_feed,
            allowed_chat_ids=allowed or None,
            job_keywords=self.env.JOB_KEYWORDS,
            max_jobs=int(self.env.MAX_JOBS_IN_DIGEST or "6"),
            max_reads=int(self.env.MAX_READS_IN_DIGEST or "5"),
        )

    async def _guarded(self, update):
        """waitUntil failures are otherwise silent - log and tell the user
        their message did not land instead of leaving them hanging."""
        try:
            await self._bot(self._store()).handle_update(update)
        except Exception as exc:
            print("handle_update failed: %r" % (exc,))
            try:
                await self._send(update.chat_id, "Something went wrong on my end - please try again.")
            except Exception:
                pass

    # ---- outbound network ---------------------------------------------------

    async def _post_telegram(self, method, payload):
        resp = await fetch(
            api_url(self.env.TELEGRAM_BOT_TOKEN, method),
            _js({"method": "POST", "headers": {"content-type": "application/json"},
                 "body": json.dumps(payload)}),
        )
        return (await resp.json()).to_py()

    async def _send(self, chat_id, text):
        for part in split_message(text):
            await self._post_telegram("sendMessage", build_send_payload(chat_id, part))

    async def _fetch_page(self, url):
        try:
            resp = await fetch(url, _js({"headers": FETCH_HEADERS, "redirect": "follow"}))
            if getattr(resp, "status", 200) >= 400:
                return None
            return await resp.text()
        except Exception as exc:
            print("fetch_page failed for %s: %r" % (url, exc))
            return None

    async def _fetch_json(self, url):
        resp = await fetch(url, _js({"headers": FETCH_HEADERS}))
        return (await resp.json()).to_py()

    async def _fetch_jobs_feed(self):
        """Live pull from every source; a source being down never blocks the
        digest - it just contributes nothing this run."""
        jobs = []
        for url, parser in (
            (joblib.REMOTEOK_URL, joblib.parse_remoteok),
            (joblib.REMOTIVE_URL, joblib.parse_remotive),
        ):
            try:
                jobs.extend(parser(await self._fetch_json(url)))
            except Exception as exc:
                print("job source failed %s: %r" % (url, exc))
        return jobs
