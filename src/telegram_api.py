"""Pure helpers for the Telegram Bot API: update parsing, outbound payload
building, webhook-secret verification and message splitting.

No Workers imports here - entry.py does the actual network calls, so every
function in this module is unit-testable off the edge.
"""

import hmac

TELEGRAM_API = "https://api.telegram.org"
MAX_MESSAGE_LEN = 4096


def api_url(token: str, method: str) -> str:
    return f"{TELEGRAM_API}/bot{token}/{method}"


def verify_secret(provided: str, expected: str) -> bool:
    """Telegram signs webhook calls with the secret we registered in
    setWebhook (X-Telegram-Bot-Api-Secret-Token). Reject everything else."""
    if not expected:
        return False
    return hmac.compare_digest(str(provided or ""), str(expected))


class Update:
    """The slice of a Telegram update we care about."""

    def __init__(self, chat_id: int, text: str):
        self.chat_id = chat_id
        self.text = text.strip()

    def __repr__(self):  # pragma: no cover - debugging aid
        return f"Update(chat_id={self.chat_id}, text={self.text!r})"


def parse_update(body: dict):
    """Extract a text message from a webhook payload, or None for anything
    we do not handle (stickers, photos, channel posts, ...)."""
    if not isinstance(body, dict):
        return None
    message = body.get("message")
    if not isinstance(message, dict):
        return None
    chat = message.get("chat") or {}
    chat_id = chat.get("id")
    text = message.get("text") or message.get("caption") or ""
    if chat_id is None or not text.strip():
        return None
    try:
        chat_id = int(chat_id)
    except (TypeError, ValueError):
        return None
    return Update(chat_id=chat_id, text=text)


def build_send_payload(chat_id: int, text: str) -> dict:
    """Plain text only: URLs in the body still auto-link in Telegram, and we
    never have to worry about Markdown-escaping user content."""
    return {"chat_id": chat_id, "text": text}


def split_message(text: str, limit: int = MAX_MESSAGE_LEN):
    """Split an over-long reply on paragraph, then line, then word
    boundaries so no chunk ever exceeds Telegram's 4096-char cap."""
    if len(text) <= limit:
        return [text]
    chunks = []
    remaining = text
    while len(remaining) > limit:
        window = remaining[:limit]
        cut = max(window.rfind("\n\n"), window.rfind("\n"), window.rfind(" "))
        if cut < limit // 2:  # no decent boundary; hard-cut
            cut = limit
        chunks.append(remaining[:cut].rstrip())
        remaining = remaining[cut:].lstrip()
    if remaining:
        chunks.append(remaining)
    return chunks


def command_of(text: str):
    """'/jobs extra words' -> ('jobs', 'extra words'). Handles /cmd@BotName."""
    if not text.startswith("/"):
        return None, text
    head, _, rest = text.partition(" ")
    cmd = head[1:].split("@")[0].lower()
    return cmd, rest.strip()
