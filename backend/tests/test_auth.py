from app.auth import create_guest, verify_session


def test_guest_session_round_trip(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "test")
    monkeypatch.setenv("SESSION_SECRET", "test-session-secret-that-is-at-least-thirty-two-characters")
    issued = create_guest()
    assert issued["user"]["mode"] == "guest"
    claims = verify_session(issued["token"])
    assert claims["mode"] == "guest"
    assert claims["sub"].startswith("guest-")


def test_guest_is_not_pro_by_default(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "test")
    monkeypatch.setenv("SESSION_SECRET", "test-session-secret-that-is-at-least-thirty-two-characters")
    issued = create_guest()
    claims = verify_session(issued["token"])
    assert claims["pro"] is False
