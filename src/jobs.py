"""Job-board sources for the daily digest: URL builders, response parsers,
keyword filtering and ranking. Pure functions - entry.py does the fetching.

Sources are public JSON APIs, fetched at send time, so every opening in a
digest was live on the source moments before it was sent. Only openings
with stated pay make it into a digest (paid_only=True is the default).
"""

REMOTEOK_URL = "https://remoteok.com/api"
REMOTIVE_URL = "https://remotive.com/api/remote-jobs?limit=300"

DEFAULT_KEYWORDS = (
    "backend,python,llm,ai,genai,machine learning,full stack,"
    "forward deployed,intern,junior,fresher,entry level"
)

# Terms that mark an opening as early-career; ranked above the rest.
EARLY_CAREER_TERMS = (
    "intern", "internship", "junior", "entry level", "entry-level",
    "fresher", "new grad", "graduate", "working student",
)


def _clean(text) -> str:
    import re

    return re.sub(r"<[^>]+>", " ", str(text or "")).strip()


def parse_remoteok(data):
    """RemoteOK's API returns a list whose first element is legal metadata,
    not a job. Salary comes as salary_min/salary_max (0 when unstated)."""
    jobs = []
    if not isinstance(data, list):
        return jobs
    for raw in data[1:]:
        if not isinstance(raw, dict) or not raw.get("position"):
            continue
        lo = raw.get("salary_min") or 0
        hi = raw.get("salary_max") or 0
        try:
            lo, hi = int(lo or 0), int(hi or 0)
        except (TypeError, ValueError):
            lo, hi = 0, 0
        salary = ""
        if lo or hi:
            salary = f"${lo // 1000}k-${hi // 1000}k/yr" if hi else f"${lo // 1000}k+/yr"
        jobs.append({
            "source": "remoteok",
            "key": f"remoteok:{raw.get('id') or raw.get('url')}",
            "title": _clean(raw.get("position")),
            "company": _clean(raw.get("company")),
            "url": raw.get("url") or "",
            "salary": salary,
            "tags": [str(t).lower() for t in (raw.get("tags") or [])],
            "date": str(raw.get("date") or ""),
        })
    return jobs


def parse_remotive(data):
    """Remotive returns {'jobs': [...]}; salary is a free-text field that is
    empty when the employer did not publish pay."""
    jobs = []
    if not isinstance(data, dict):
        return jobs
    for raw in data.get("jobs") or []:
        if not isinstance(raw, dict) or not raw.get("title"):
            continue
        jobs.append({
            "source": "remotive",
            "key": f"remotive:{raw.get('id') or raw.get('url')}",
            "title": _clean(raw.get("title")),
            "company": _clean(raw.get("company_name")),
            "url": raw.get("url") or "",
            "salary": _clean(raw.get("salary")),
            "tags": [str(t).lower() for t in (raw.get("tags") or [])]
                    + [str(raw.get("category") or "").lower()],
            "date": str(raw.get("publication_date") or ""),
        })
    return jobs


def parse_keywords(raw: str):
    return [part.strip().lower() for part in (raw or "").split(",") if part.strip()]


def matches(job: dict, keywords) -> bool:
    haystack = " ".join([job.get("title", ""), job.get("company", ""), " ".join(job.get("tags", []))]).lower()
    return any(kw in haystack for kw in keywords)


def is_early_career(job: dict) -> bool:
    haystack = f"{job.get('title', '')} {' '.join(job.get('tags', []))}".lower()
    return any(term in haystack for term in EARLY_CAREER_TERMS)


# Title words that mark a role as not fresher-relevant.
SENIOR_WORDS = frozenset(
    "senior sr staff principal lead head director vp manager architect "
    "chief distinguished iii iv".split()
)
SENIOR_PHRASES = ("vice president", "sde 3", "sde iii")

_VOWELS = set("aeiou")


def _token_gibberish(token: str) -> bool:
    """A long token with no vowels or a 5+ consonant run is keyboard mash,
    not a word ('lkjlkgxcv', 'scvsdv'). Short acronyms (SQL, HR) pass."""
    t = "".join(ch for ch in token.lower() if ch.isalpha())
    if len(t) < 5:
        return False
    if not _VOWELS.intersection(t):
        return True
    run = 0
    for ch in t:
        run = run + 1 if ch not in _VOWELS and ch != "y" else 0
        if run >= 5:
            return True
    return False


def is_plausible(job: dict) -> bool:
    """Reject listings whose title or company looks like keyboard mash."""
    for field in ("title", "company"):
        for token in str(job.get(field, "")).split():
            if _token_gibberish(token):
                return False
    return True


def is_fresher_relevant(job: dict) -> bool:
    """A role is fresher-relevant unless its title marks it senior-only."""
    import re

    words = re.findall(r"[a-z0-9]+", str(job.get("title", "")).lower())
    if SENIOR_WORDS.intersection(words):
        return False
    joined = " ".join(words)
    return not any(phrase in joined for phrase in SENIOR_PHRASES)


def select_jobs(jobs, keywords, paid_only=True, limit=6, exclude_keys=frozenset()):
    """Filter to paid, keyword-matching, unsent openings; early-career first,
    newest next; dedup by (title, company) so cross-posted roles appear once."""
    out = []
    seen_pairs = set()
    for job in jobs:
        if not job.get("title") or not job.get("url"):
            continue
        if job.get("key") in exclude_keys:
            continue
        if paid_only and not job.get("salary"):
            continue
        if not is_plausible(job) or not is_fresher_relevant(job):
            continue
        if keywords and not matches(job, keywords):
            continue
        pair = (job["title"].lower(), job.get("company", "").lower())
        if pair in seen_pairs:
            continue
        seen_pairs.add(pair)
        out.append(job)
    out.sort(key=lambda j: (not is_early_career(j), j.get("date", "")), reverse=False)
    # newest first within each early-career bucket: stable sort by date desc,
    # then stable sort by early-career flag
    out.sort(key=lambda j: j.get("date", ""), reverse=True)
    out.sort(key=lambda j: not is_early_career(j))
    return out[:limit]
