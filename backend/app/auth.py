from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

SESSION_TTL_SECONDS = 60 * 60 * 24 * 30


def _secret() -> str:
    secret = os.getenv("SESSION_SECRET", "")
    if len(secret) < 32:
        if os.getenv("ENVIRONMENT", "production") == "production":
            raise RuntimeError("SESSION_SECRET must be configured with at least 32 characters")
        secret = "dev-only-robolab-x-session-secret-change-me"
    return secret


def _serializer() -> URLSafeTimedSerializer:
    return URLSafeTimedSerializer(_secret(), salt="robolab-x-session-v1")


def issue_session(user: dict[str, Any]) -> str:
    payload = {
        "sub": user["id"],
        "mode": user["mode"],
        "name": user.get("name", "Engineer"),
        "email": user.get("email"),
        "pro": bool(user.get("pro", False)),
        "iat": datetime.now(timezone.utc).isoformat(),
    }
    return _serializer().dumps(payload)


def verify_session(token: str) -> dict[str, Any]:
    try:
        return _serializer().loads(token, max_age=SESSION_TTL_SECONDS)
    except SignatureExpired as exc:
        raise ValueError("Session expired") from exc
    except BadSignature as exc:
        raise ValueError("Invalid session") from exc


def create_guest() -> dict[str, Any]:
    user = {
        "id": f"guest-{uuid4()}",
        "mode": "guest",
        "name": "Guest Engineer",
        "email": None,
        "pro": False,
    }
    return {"token": issue_session(user), "user": user}


def verify_google_id_token(raw_token: str) -> dict[str, Any]:
    client_id = os.getenv("GOOGLE_CLIENT_ID", "").strip()
    if not client_id:
        raise RuntimeError("GOOGLE_CLIENT_ID is not configured")
    try:
        claims = id_token.verify_oauth2_token(raw_token, google_requests.Request(), client_id)
    except Exception as exc:
        raise ValueError("Google authentication failed") from exc

    issuer = claims.get("iss")
    if issuer not in {"accounts.google.com", "https://accounts.google.com"}:
        raise ValueError("Invalid Google token issuer")
    if not claims.get("email_verified", False):
        raise ValueError("Google account email is not verified")

    user = {
        "id": f"google-{claims['sub']}",
        "mode": "google",
        "name": claims.get("name") or claims.get("email") or "Engineer",
        "email": claims.get("email"),
        "picture": claims.get("picture"),
        "pro": False,
    }
    return {"token": issue_session(user), "user": user}
