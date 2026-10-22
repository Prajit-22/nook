from extract import content_hash, extract_title, fallback_title, find_urls, html_to_text


def test_find_urls_strips_trailing_punctuation():
    text = "read https://example.com/a, then https://x.io/b)."
    assert find_urls(text) == ["https://example.com/a", "https://x.io/b"]


def test_find_urls_empty():
    assert find_urls("no links here") == []
    assert find_urls("") == []


def test_extract_title_prefers_og_title():
    page = '<html><head><meta property="og:title" content="OG &amp; Title"><title>Plain</title></head></html>'
    assert extract_title(page) == "OG & Title"


def test_extract_title_falls_back_to_title_tag():
    assert extract_title("<title>Hello World</title>") == "Hello World"
    assert extract_title("<p>no title</p>") == ""


def test_html_to_text_drops_scripts_and_nav():
    page = """
    <html><head><style>body{color:red}</style><script>evil()</script></head>
    <body><nav>menu junk</nav><article><p>Real content here.</p></body></html>
    """
    text = html_to_text(page)
    assert "Real content here." in text
    assert "evil()" not in text
    assert "menu junk" not in text
    assert "color:red" not in text


def test_html_to_text_unescapes_and_collapses():
    assert html_to_text("<p>a &amp; b</p><p>c</p>") == "a & b\nc"


def test_html_to_text_caps_length():
    assert len(html_to_text("<p>" + "x" * 20000 + "</p>")) <= 9000


def test_fallback_title_uses_domain():
    assert fallback_title("https://blog.example.com/post/1") == "blog.example.com"


def test_content_hash_stable_and_insensitive_to_case_ws():
    assert content_hash("Hello  World") == content_hash("hello world")
    assert content_hash("a") != content_hash("b")
