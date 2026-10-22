from digest import format_digest, format_jobs_section, format_reads_section


def item(i, read=0):
    return {"id": i, "title": f"Post {i}", "url": f"https://x.io/{i}",
            "summary": f"Summary of post {i}.", "tags": "a, b", "read": read}


def job(i, salary="$20k-$40k/yr"):
    return {"key": f"k{i}", "title": f"Intern {i}", "company": "Acme",
            "url": f"https://jobs.io/{i}", "salary": salary}


def test_reads_section_lists_unread_with_links():
    out = format_reads_section([item(1), item(2)])
    assert "IN YOUR NOOK - 2 unread" in out
    assert "#1 Post 1" in out and "https://x.io/2" in out


def test_reads_section_empty_is_empty_string():
    assert format_reads_section([]) == ""


def test_reads_section_overflow_note():
    out = format_reads_section([item(i) for i in range(1, 9)], limit=5)
    assert "3 more" in out


def test_jobs_section_includes_pay_and_link():
    out = format_jobs_section([job(1)])
    assert "Intern 1 @ Acme - $20k-$40k/yr" in out
    assert "https://jobs.io/1" in out


def test_jobs_section_empty_is_empty_string():
    assert format_jobs_section([]) == ""


def test_full_digest_combines_sections():
    out = format_digest([item(1)], [job(1)])
    assert "daily Nook digest" in out
    assert "IN YOUR NOOK" in out and "FRESH OPENINGS" in out


def test_full_digest_empty_state_message():
    out = format_digest([], [])
    assert "Nothing new" in out and "/jobs" in out
