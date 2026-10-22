from prompts import clean_summary, clean_tags, answer_messages, summarize_messages


def test_clean_tags_normalizes():
    assert clean_tags("RAG, Python,  Hiring, rag, #design.") == "rag, python, hiring, design"


def test_clean_tags_caps_at_six():
    assert len(clean_tags("a,b,c,d,e,f,g,h").split(", ")) == 6


def test_clean_tags_garbage_is_empty():
    assert clean_tags("") == ""
    assert clean_tags("###") == ""


def test_clean_summary_strips_preamble():
    assert clean_summary("Here's a summary: the thing works.") == "the thing works."
    assert clean_summary("Plain answer.") == "Plain answer."


def test_answer_messages_numbers_sources():
    msgs = answer_messages("what is rag?", [
        {"title": "A", "summary": "s1", "content": "c1"},
        {"title": "B", "summary": "", "content": "c2"},
    ])
    assert "[1] A" in msgs[1]["content"] and "[2] B" in msgs[1]["content"]
    assert "what is rag?" in msgs[1]["content"]


def test_summarize_messages_include_title_and_cap():
    msgs = summarize_messages("T", "x" * 9000)
    assert "T" in msgs[1]["content"]
    assert len(msgs[1]["content"]) < 7000
