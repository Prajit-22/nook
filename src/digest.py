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
        lines.append(f"\n...and {len(unread_items) - limit} more on the pile. /reads for the rest.")
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
    parts = ["Good morning. Your Nook letter, sealed and delivered:"]
    reads = format_reads_section(unread_items, limit=reads_limit)
    jobs_text = format_jobs_section(jobs)
    if reads:
        parts.append(reads)
    if jobs_text:
        parts.append(jobs_text)
    if not reads and not jobs_text:
        parts.append("The pile is empty and no matching openings came in overnight. /jobs to re-check on demand.")
    parts.append("- your magpie")
    return "\n\n".join(parts)


WELCOME = (
    "Nook here. A reading corner on Telegram, kept by a magpie.\n\n"
    "Toss links at me all day - I fetch each page, write a two-sentence summary, "
    "tag it, and file it. Every morning at 08:00 you get one sealed letter: your "
    "unread reads, plus fresh paid openings matched to you.\n\n"
    "How it works:\n"
    "- Send any link to save it\n"
    "- Ask a question in plain words to search your nook, with sources\n"
    "- /note <text> saves a thought instead\n"
    "- /jobs fresh openings now, /reads your unread pile now\n"
    "- /list recent saves, /forget <id> removes one\n"
    "- /stop pauses the morning letter, /start resumes it\n\n"
    "You are subscribed to the daily letter."
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
