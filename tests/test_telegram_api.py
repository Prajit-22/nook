from telegram_api import (
    build_send_payload, command_of, parse_update, split_message, verify_secret,
)


def make_update(chat_id=42, text="hello"):
    return {"update_id": 1, "message": {"message_id": 1, "chat": {"id": chat_id}, "text": text}}


def test_parse_update_extracts_chat_and_text():
    update = parse_update(make_update(42, "  hi there  "))
    assert update.chat_id == 42
    assert update.text == "hi there"


def test_parse_update_ignores_non_message_payloads():
    assert parse_update({}) is None
    assert parse_update({"edited_message": {"chat": {"id": 1}, "text": "x"}}) is None
    assert parse_update({"message": {"chat": {"id": 1}}}) is None  # no text (photo etc.)
    assert parse_update({"message": {"chat": {}, "text": "x"}}) is None  # no chat id
    assert parse_update("not a dict") is None


def test_parse_update_accepts_caption():
    body = {"message": {"chat": {"id": 7}, "caption": "look at this"}}
    update = parse_update(body)
    assert update.chat_id == 7 and update.text == "look at this"


def test_verify_secret():
    assert verify_secret("s3cret", "s3cret")
    assert not verify_secret("wrong", "s3cret")
    assert not verify_secret(None, "s3cret")
    assert not verify_secret("s3cret", "")  # unconfigured secret rejects everything


def test_command_of():
    assert command_of("/jobs") == ("jobs", "")
    assert command_of("/forget 12") == ("forget", "12")
    assert command_of("/ask@NookBot what is rag?") == ("ask", "what is rag?")
    assert command_of("plain text") == (None, "plain text")


def test_split_message_short_text_untouched():
    assert split_message("short") == ["short"]


def test_split_message_respects_limit_and_boundaries():
    text = "\n".join(f"line {i} " + "word " * 20 for i in range(60))
    parts = split_message(text, limit=500)
    assert all(len(p) <= 500 for p in parts)
    assert "".join(parts).replace("\n", "").replace(" ", "") == text.replace("\n", "").replace(" ", "")


def test_split_message_hard_cuts_one_giant_word():
    parts = split_message("x" * 9000, limit=4096)
    assert all(len(p) <= 4096 for p in parts)
    assert "".join(parts) == "x" * 9000


def test_build_send_payload_is_plain_text():
    payload = build_send_payload(1, "check https://example.com")
    assert payload == {"chat_id": 1, "text": "check https://example.com"}
