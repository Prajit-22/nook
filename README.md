# Nook

**Your reading nook on Telegram. Toss links at it all day; wake up to one digest - your reads summarized, plus fresh paid openings worth applying to.**

A Telegram bot you deploy to your own Cloudflare account as a pure-Python Worker. It fetches every link you send it, summarizes and tags it with Workers AI, answers questions over your saved links with sources, and sends a single morning digest: your unread reads + new paid job openings matched to your keywords, pulled live from public job boards at send time.

Runs entirely on Cloudflare's free tier. No server, no Docker, no API keys, no bill.

[![Deploy to Cloudflare](https://deploy.workers.cloudflare.com/button)](https://deploy.workers.cloudflare.com/?url=https://github.com/Prajit-22/nook)

## What it does

| You send | Nook |
| --- | --- |
| a link | fetches the page, extracts the text, writes a 2-3 sentence AI summary, tags it, saves it (`Saved #n`) |
| the same link twice | detects the duplicate (sha256) instead of saving again |
| a question in plain words | BM25 search (SQLite FTS5) over your saves, answers with cited sources |
| `/note <text>` | saves the thought, with a one-line summary |
| `/jobs` | fresh paid openings matching your keywords, right now |
| `/reads` | your unread pile, right now |
| `/list` / `/forget <id>` | manage your saves |
| `/stop` / `/start` | pause / resume the morning digest |
| nothing (cron) | at 08:00 IST, one digest: unread reads + fresh paid openings, deduped so you never see the same opening twice |

Every opening in a digest was **live on its source board at send time** and has **stated pay** - no stale listings, no unpaid noise. Sources today: RemoteOK and Remotive public APIs (both fetched fresh per digest). Keywords are yours to set in `wrangler.toml`.

## Architecture

```
Telegram webhook ──▶ entry.py ──▶ bot.py (orchestration)
                                      │
        ┌───────────────┬─────────────┼──────────────┐
        ▼               ▼             ▼              ▼
   store.py (D1)   Workers AI    jobs.py        digest.py
   items + FTS5    summaries,    RemoteOK +     plain-text
   subs + dedup    tags, answers Remotive       formatting

cron (08:00 IST) ─▶ bot.run_daily_digest ─▶ one message per subscriber
```

- **Pure Python Workers** - stdlib only, zero dependencies to bundle.
- **D1 (SQLite)** for saves, FTS5 for BM25 search, subscription list and job dedup.
- **Workers AI** (Llama 3.1 8B) for summaries, tags and answers - no LLM API key at all.
- Webhook calls are verified against a secret token; the webhook acks instantly and finishes AI work in the background, so Telegram never retries.
- All logic lives in pure modules (`bot.py`, `jobs.py`, `digest.py`, `extract.py`, `prompts.py`, `telegram_api.py`) covered by 58 unit tests; `entry.py` is the only file that touches the Workers runtime.

## Deploy your own

1. **Create a Telegram bot**: message [@BotFather](https://t.me/BotFather), `/newbot`, copy the token.
2. **Clone and configure**:

   ```bash
   git clone https://github.com/Prajit-22/nook && cd nook
   npx wrangler d1 create nook-db          # paste the database_id into wrangler.toml
   npx wrangler d1 execute nook-db --remote --file=schema.sql
   ```

3. **Set secrets**:

   ```bash
   npx wrangler secret put TELEGRAM_BOT_TOKEN        # from BotFather
   npx wrangler secret put TELEGRAM_WEBHOOK_SECRET   # any long random string
   ```

4. **Deploy and register the webhook**:

   ```bash
   npx wrangler deploy
   curl "https://api.telegram.org/bot<TOKEN>/setWebhook" \
     -d "url=https://nook.<your-subdomain>.workers.dev/webhook" \
     -d "secret_token=<your webhook secret>"
   ```

5. Optional: set `ALLOWED_CHAT_IDS` in `wrangler.toml` to your Telegram chat id (message [@userinfobot](https://t.me/userinfobot)) so only you can use it, and tune `JOB_KEYWORDS` to the openings you want.

## Tuning

| var | default | meaning |
| --- | --- | --- |
| `JOB_KEYWORDS` | backend, python, llm, ai, ... | digest keywords, matched against title + tags |
| `MAX_JOBS_IN_DIGEST` | 6 | openings per digest |
| `MAX_READS_IN_DIGEST` | 5 | reads per digest |
| `LLM_MODEL` | `@cf/meta/llama-3.1-8b-instruct-fast` | Workers AI chat model |
| `ALLOWED_CHAT_IDS` | empty (open) | comma-separated Telegram chat ids |

## Local development

```bash
uv run --with pytest --with pytest-asyncio python -m pytest tests/ -q
uv run pywrangler dev
```

## License

MIT
