import time
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from webapp import sign_session, verify_session, session_from_headers, SESSION_COOKIE

SECRET = "test-secret"


def test_session_roundtrip():
    token = sign_session(12345, SECRET)
    assert verify_session(token, SECRET) == 12345


def test_session_tampered_signature_rejected():
    token = sign_session(12345, SECRET)
    bad = token[:-2] + ("aa" if not token.endswith("aa") else "bb")
    assert verify_session(bad, SECRET) is None


def test_session_wrong_secret_rejected():
    assert verify_session(sign_session(1, SECRET), "other-secret") is None


def test_session_garbage_rejected():
    assert verify_session("not-a-token", SECRET) is None
    assert verify_session("", SECRET) is None


def test_session_expired_rejected(monkeypatch):
    token = sign_session(7, SECRET)
    future = int(time.time()) + 31 * 24 * 3600
    monkeypatch.setattr(time, "time", lambda: future)
    assert verify_session(token, SECRET) is None


def test_cookie_header_parsing():
    token = sign_session(99, SECRET)
    header = "other=1; %s=%s; theme=ink" % (SESSION_COOKIE, token)
    assert session_from_headers(header, SECRET) == 99
    assert session_from_headers("other=1", SECRET) is None
    assert session_from_headers("", SECRET) is None
