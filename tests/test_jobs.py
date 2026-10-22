from jobs import (
    DEFAULT_KEYWORDS, is_early_career, matches, parse_keywords,
    parse_remoteok, parse_remotive, select_jobs,
)

REMOTEOK_PAYLOAD = [
    {"legal": "metadata block, not a job"},
    {"id": 1, "position": "Backend Engineer Intern", "company": "Acme",
     "url": "https://remoteok.com/1", "salary_min": 20000, "salary_max": 40000,
     "tags": ["python", "backend", "intern"], "date": "2026-10-22T00:00:00+00:00"},
    {"id": 2, "position": "Staff Distributed Systems Engineer", "company": "BigCo",
     "url": "https://remoteok.com/2", "salary_min": 200000, "salary_max": 300000,
     "tags": ["golang", "distributed"], "date": "2026-10-21T00:00:00+00:00"},
    {"id": 3, "position": "Python Developer", "company": "NoPay",
     "url": "https://remoteok.com/3", "salary_min": 0, "salary_max": 0,
     "tags": ["python"], "date": "2026-10-22T00:00:00+00:00"},
]

REMOTIVE_PAYLOAD = {"jobs": [
    {"id": 10, "title": "Junior AI Engineer", "company_name": "LLMCorp",
     "url": "https://remotive.com/10", "salary": "$30k-$50k",
     "category": "Software Development", "tags": ["llm", "python"],
     "publication_date": "2026-10-22T10:00:00"},
    {"id": 11, "title": "Designer", "company_name": "Studio",
     "url": "https://remotive.com/11", "salary": "",
     "category": "Design", "tags": [], "publication_date": "2026-10-22T11:00:00"},
]}


def test_parse_remoteok_skips_metadata_block():
    jobs = parse_remoteok(REMOTEOK_PAYLOAD)
    assert [j["title"] for j in jobs] == [
        "Backend Engineer Intern", "Staff Distributed Systems Engineer", "Python Developer"]


def test_parse_remoteok_salary_formatting():
    jobs = parse_remoteok(REMOTEOK_PAYLOAD)
    assert jobs[0]["salary"] == "$20k-$40k/yr"
    assert jobs[2]["salary"] == ""  # unpaid stays empty


def test_parse_remoteok_bad_payload():
    assert parse_remoteok({"not": "a list"}) == []
    assert parse_remoteok([]) == []


def test_parse_remotive():
    jobs = parse_remotive(REMOTIVE_PAYLOAD)
    assert jobs[0]["company"] == "LLMCorp"
    assert jobs[1]["salary"] == ""
    assert "software development" in jobs[0]["tags"]


def test_parse_remotive_bad_payload():
    assert parse_remotive([]) == []
    assert parse_remotive({}) == []


def test_keywords_and_matching():
    kws = parse_keywords(DEFAULT_KEYWORDS)
    intern = parse_remoteok(REMOTEOK_PAYLOAD)[0]
    staff = parse_remoteok(REMOTEOK_PAYLOAD)[1]
    assert matches(intern, kws)
    assert not matches(staff, kws)


def test_is_early_career():
    intern = parse_remoteok(REMOTEOK_PAYLOAD)[0]
    staff = parse_remoteok(REMOTEOK_PAYLOAD)[1]
    assert is_early_career(intern)
    assert not is_early_career(staff)


def test_select_jobs_paid_only_keyword_filtered_early_first():
    feed = parse_remoteok(REMOTEOK_PAYLOAD) + parse_remotive(REMOTIVE_PAYLOAD)
    picked = select_jobs(feed, parse_keywords(DEFAULT_KEYWORDS), paid_only=True)
    titles = [j["title"] for j in picked]
    assert "Python Developer" not in titles   # no pay -> excluded
    assert "Designer" not in titles           # no pay + no keyword -> excluded
    assert "Staff Distributed Systems Engineer" not in titles  # no keyword
    assert titles[0] in ("Backend Engineer Intern", "Junior AI Engineer")
    assert is_early_career(picked[0])


def test_select_jobs_excludes_already_sent_and_dedupes():
    feed = parse_remoteok(REMOTEOK_PAYLOAD) + parse_remotive(REMOTIVE_PAYLOAD)
    picked = select_jobs(feed, parse_keywords(DEFAULT_KEYWORDS),
                         exclude_keys={"remoteok:1"})
    assert all(j["key"] != "remoteok:1" for j in picked)
    dup = feed + [dict(feed[0], key="other-key")]  # same title+company, new key
    titles = [j["title"] for j in select_jobs(dup, parse_keywords(DEFAULT_KEYWORDS))]
    assert titles.count("Backend Engineer Intern") == 1


def test_select_jobs_limit():
    many = [dict(parse_remoteok(REMOTEOK_PAYLOAD)[0], key=f"k{i}", title=f"Intern {i}")
            for i in range(20)]
    assert len(select_jobs(many, parse_keywords("intern"), limit=6)) == 6
