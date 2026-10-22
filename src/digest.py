"""Plain-text formatting for the two digest halves (reads + jobs) and the
bot's static copy. Telegram auto-links bare URLs, so no markup needed."""


def format_reads_section(unread_items, limit=5) -> str:
    if not unread_items:
        return ""
    lines = [f"IN YOUR NOOK - {len(unread_items)} unread"]
    for item in unread_items[:limit]:
        title = item.get("title") or item.get("url") or "untitled"
        summary = (item.get("summary") or "").strip()
        first_line = summary.split("\n")[0][:160]
        lines.append(f"\n#{item['id']} {title}")
        if first_line:
            lines.append(first_line)
        if item.get("url"):
            lines.append(item["url"])
    if len(unread_items) > limit:
        lines.append(f"\n...and {len(unread_items) - limit} more. /reads for the rest.")
    return "\n".join(lines)


def format_jobs_section(jobs) -> str:
    if not jobs:
        return ""
    lines = ["FRESH OPENINGS (paid, live at send time)"]
    for job in jobs:
        title = job.get("title", "")
        company = job.get("company", "")
        salary = job.get("salary", "")
        header = f"\n{title}"
        if company:
            header += f" @ {company}"
        if salary:
            header += f" - {salary}"
        lines.append(header)
        lines.append(job["url"])
    return "\n".join(lines)


def format_digest(unread_items, jobs, reads_limit=5) -> str:
    parts = ["Good morning - your daily Nook digest, sealed and delivered:"]
    reads = format_reads_section(unread_items, limit=reads_limit)
    jobs_text = format_jobs_section(jobs)
    if reads:
        parts.append(reads)
    if jobs_text:
        parts.append(jobs_text)
    if not reads and not jobs_text:
        parts.append("Nothing new in your nook and no fresh matching openings today. /jobs to re-check on demand.")
    return "\n\n".join(parts)


WELCOME = (
    "Nook here - your reading corner on Telegram, kept by a magpie. Toss links into your nook "
    "all day and I will fetch, summarize and tag every one. Each morning I deliver one sealed "
    "letter: your unread reads, plus fresh paid openings that match you.\n\n"
    "- Send any link to save it\n"
    "- Ask a question in plain words to search your nook\n"
    "- /note <text> saves a thought instead\n"
    "- /jobs for fresh openings now, /reads for your unread nook\n"
    "- /list recent saves, /forget <id> to delete one\n"
    "- /stop pauses the morning digest\n\n"
    "You are subscribed to the daily digest."
)

HELP = (
    "Send a link: I fetch the page, summarize and tag it.\n"
    "Ask anything in plain words: I answer from your saved links, with sources.\n\n"
    "/note <text> - save a thought\n"
    "/jobs - fresh paid openings now\n"
    "/reads - your unread nook now\n"
    "/list - last 10 saves\n"
    "/forget <id> - delete a save\n"
    "/stop - pause the morning digest\n"
    "/start - resume it"
)

NO_MATCH_ANSWER = (
    "I could not find anything about that in your nook. "
    "Save a few links first, or try different words."
)
