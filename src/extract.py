"""URL detection, HTML-to-text and title extraction - stdlib only."""

import hashlib
import html
import re

URL_RE = re.compile(r"https?://[^\s<>\]\)\}\"']+", re.IGNORECASE)
MAX_CONTENT_CHARS = 9000

_TAG_RE = re.compile(r"<[^>]+>")
_BLOCK_CLOSE_RE = re.compile(
    r"</(p|div|li|h[1-6]|article|section|tr|blockquote)>|<br[^>]*>", re.IGNORECASE
)
_TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)
_OG_TITLE_RE = re.compile(
    r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\'](.*?)["\']', re.IGNORECASE | re.DOTALL
)
_BLOCK_RE = re.compile(
    r"<(script|style|noscript|svg|head|header|footer|nav)[^>]*>.*?</\1>",
    re.IGNORECASE | re.DOTALL,
)


def find_urls(text: str):
    """All http(s) URLs in a message, trailing punctuation stripped."""
    urls = []
    for match in URL_RE.finditer(text or ""):
        urls.append(match.group(0).rstrip(".,;:!?)>]"))
    return urls


def extract_title(page_html: str) -> str:
    og = _OG_TITLE_RE.search(page_html or "")
    if og:
        return html.unescape(og.group(1)).strip()[:200]
    title = _TITLE_RE.search(page_html or "")
    if title:
        return html.unescape(_TAG_RE.sub("", title.group(1))).strip()[:200]
    return ""


def html_to_text(page_html: str) -> str:
    """Crude but dependable readable-text extraction: drop non-content
    blocks, strip tags, unescape entities, collapse whitespace, cap length."""
    text = _BLOCK_RE.sub(" ", page_html or "")
    text = _BLOCK_CLOSE_RE.sub("\n", text)
    text = _TAG_RE.sub(" ", text)
    text = html.unescape(text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    lines = [line.strip() for line in text.splitlines()]
    text = "\n".join(line for line in lines if line)
    return text[:MAX_CONTENT_CHARS].strip()


def content_hash(text: str) -> str:
    normalized = " ".join(text.split()).lower()
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def fallback_title(url: str) -> str:
    """When a page yields no title, use a readable bit of the URL."""
    no_scheme = re.sub(r"^https?://", "", url)
    return no_scheme.split("/")[0] or url
