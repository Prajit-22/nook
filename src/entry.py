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
from webapp import (
    APP_HTML, LOGIN_HTML, MANIFEST, SERVICE_WORKER, SESSION_COOKIE,
    session_from_headers, sign_session,
)

USER_AGENT = "nook-bot/0.1 (+https://github.com/Prajit-22/nook)"
FETCH_HEADERS = {"User-Agent": USER_AGENT, "Accept": "text/html,application/json"}


def _js(value):
    """Deep-convert a Python dict/list into real JS objects for the FFI."""
    return to_js(value, dict_converter=Object.fromEntries)


class Default(WorkerEntrypoint):
    async def fetch(self, request):
        try:
            return await self._route(request)
        except Exception as exc:
            print("route failed: %r" % (exc,))
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
            if path == "/app/manifest.webmanifest":
                return Response(json.dumps(MANIFEST), headers={
                    "content-type": "application/manifest+json", "cache-control": "no-store"})
            if path == "/app/sw.js":
                return Response(SERVICE_WORKER, headers={
                    "content-type": "application/javascript", "cache-control": "no-store"})
            if path in ("/app", "/share"):
                chat_id = self._session_chat(request)
                if chat_id is None:
                    return self._html(LOGIN_HTML)
                if path == "/share":
                    qs = request.url.split("?", 1)[1] if "?" in request.url else ""
                    return Response.redirect("/app?" + qs, 302)
                return self._html(APP_HTML, cache="no-store")
            if path == "/api/reads":
                return await self._api(request, self._api_reads)
            if path == "/api/ask":
                return await self._api(request, self._api_ask)
            if path == "/api/digest":
                return await self._api(request, self._api_digest)
            if path == "/api/jobs":
                return await self._api(request, self._api_jobs)
            return self._not_found()
        if path == "/app/login" and request.method == "POST":
            return await self._login(request)
        if path == "/api/save" and request.method == "POST":
            return await self._api_save(request)
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

    # ---- web app -----------------------------------------------------------

    def _html(self, body, cache=None):
        headers = {"content-type": "text/html; charset=utf-8",
                   "x-content-type-options": "nosniff"}
        headers["cache-control"] = cache or "no-store"
        return Response(body, headers=headers)

    def _session_chat(self, request):
        return session_from_headers(
            request.headers.get("cookie") or "", self.env.TELEGRAM_WEBHOOK_SECRET)

    async def _login(self, request):
        try:
            body = await request.json()
            if hasattr(body, "to_py"):
                body = body.to_py()
        except Exception:
            body = {}
        code = str(body.get("code", "")).strip().upper() if isinstance(body, dict) else ""
        if not code:
            return Response("bad code", status=400)
        chat_id = await self._store().consume_web_code(code)
        if chat_id is None:
            return Response("bad code", status=403)
        token = sign_session(chat_id, self.env.TELEGRAM_WEBHOOK_SECRET)
        return Response("ok", headers={
            "set-cookie": "%s=%s; Path=/; Max-Age=%d; HttpOnly; Secure; SameSite=Lax"
            % (SESSION_COOKIE, token, 30 * 24 * 3600)})

    async def _api(self, request, handler):
        chat_id = self._session_chat(request)
        if chat_id is None:
            return Response('{"error":"sign in first"}', status=401,
                            headers={"content-type": "application/json"})
        try:
            payload = await handler(chat_id, request)
        except Exception as exc:
            print("api failed: %r" % (exc,))
            return Response('{"error":"dropped it"}', status=500,
                            headers={"content-type": "application/json"})
        return Response(json.dumps(payload), headers={
            "content-type": "application/json", "cache-control": "no-store"})

    async def _api_reads(self, chat_id, request):
        return await self._store().list_items(chat_id, limit=100)

    async def _api_ask(self, chat_id, request):
        from urllib.parse import urlparse, parse_qs
        q = parse_qs(urlparse(request.url).query).get("q", [""])[0].strip()
        if not q:
            return {"answer": "Ask me something first."}
        store = self._store()
        results = await store.fts_search(chat_id, q, limit=4)
        if not results:
            return {"answer": "Nothing in your nook matches that yet. Save a few links first."}
        context = "\n\n".join(
            "#%d %s (%s)\n%s" % (r["id"], r["title"], r["url"], (r["summary"] or r["content"][:500]))
            for r in results)
        answer = await store.chat([
            {"role": "system", "content":
             "You are Nook, a magpie keeping the user's reading pile. Answer only from the "
             "clippings below, cite them as #id, two short paragraphs max."},
            {"role": "user", "content": "Clippings:\n" + context + "\n\nQuestion: " + q},
        ])
        return {"answer": answer, "sources": [{"id": r["id"], "title": r["title"], "url": r["url"]} for r in results]}

    async def _fresh_jobs(self, chat_id):
        store = self._store()
        feed = await self._fetch_jobs_feed()
        seen = await store.sent_job_keys(chat_id)
        return joblib.select_jobs(
            feed, self.env.JOB_KEYWORDS, paid_only=True,
            limit=int(self.env.MAX_JOBS_IN_DIGEST or "6"), exclude_keys=seen)

    async def _api_jobs(self, chat_id, request):
        return await self._fresh_jobs(chat_id)

    async def _api_digest(self, chat_id, request):
        store = self._store()
        return {"reads": await store.unread_items(chat_id),
                "jobs": await self._fresh_jobs(chat_id)}

    async def _api_save(self, request):
        chat_id = self._session_chat(request)
        if chat_id is None:
            return Response('{"error":"sign in first"}', status=401,
                            headers={"content-type": "application/json"})
        try:
            body = await request.json()
            if hasattr(body, "to_py"):
                body = body.to_py()
        except Exception:
            body = {}
        url = str(body.get("url", "")).strip() if isinstance(body, dict) else ""
        if not url.startswith(("http://", "https://")):
            return Response('{"error":"that is not a link"}', status=400,
                            headers={"content-type": "application/json"})

        async def silent_save():
            async def noop(*a, **k):
                return None
            bot = self._bot(self._store())
            bot._send = noop
            await bot._save_link(chat_id, url)
        self.ctx.waitUntil(silent_save())
        return Response('{"ok":true}', status=202,
                        headers={"content-type": "application/json"})

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
