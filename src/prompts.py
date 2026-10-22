"""All LLM prompts in one place (message lists for Workers AI chat models)."""

SUMMARIZE_SYSTEM = (
    "You summarize saved web pages for a personal read-it-later library. "
    "Write a tight 2-3 sentence summary: what it is, the key takeaway. "
    "No preamble, no 'This article', no quotes around the output."
)

TAGS_SYSTEM = (
    "You tag saved web pages for a personal library. "
    "Reply with 3-6 lowercase tags, comma-separated, nothing else. "
    "Short concrete topics (e.g. rag, python, hiring, design), no sentences."
)

ANSWER_SYSTEM = (
    "You answer questions using only the user's saved links and notes, "
    "provided as numbered sources. Answer in 2-4 sentences and cite the "
    "sources you used like [1], [2]. If the sources do not cover the "
    "question, say so plainly instead of guessing."
)


def summarize_messages(title: str, text: str):
    return [
        {"role": "system", "content": SUMMARIZE_SYSTEM},
        {"role": "user", "content": f"Title: {title}\n\n{text[:6000]}"},
    ]


def tags_messages(title: str, text: str):
    return [
        {"role": "system", "content": TAGS_SYSTEM},
        {"role": "user", "content": f"Title: {title}\n\n{text[:3000]}"},
    ]


def answer_messages(question: str, sources):
    numbered = "\n\n".join(
        f"[{i + 1}] {s['title']}\n{s['summary'] or s['content'][:800]}"
        for i, s in enumerate(sources)
    )
    return [
        {"role": "system", "content": ANSWER_SYSTEM},
        {"role": "user", "content": f"Sources:\n{numbered}\n\nQuestion: {question}"},
    ]


def clean_tags(raw: str) -> str:
    """Normalize model tag output: lowercase, strip junk, dedupe, cap at 6."""
    seen = []
    for part in (raw or "").replace("\n", ",").split(","):
        tag = part.strip().lower().strip("#. ")
        tag = "".join(ch for ch in tag if ch.isalnum() or ch in " -")
        if tag and tag not in seen:
            seen.append(tag)
    return ", ".join(seen[:6])


def clean_summary(raw: str) -> str:
    import re as _re

    cleaned = (raw or "").strip().strip('"')
    return _re.sub(
        r"^(here(?:'s| is)(?: a)?[^\n:]*:\s*)+", "", cleaned, flags=_re.IGNORECASE
    ).strip()
