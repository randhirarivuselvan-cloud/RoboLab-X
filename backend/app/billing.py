from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any

from google.oauth2 import service_account
from googleapiclient.discovery import build

ALLOWED_PRODUCTS = {"robolab_pro_monthly", "robolab_pro_annual"}
ENTITLED_STATES = {
    "SUBSCRIPTION_STATE_ACTIVE",
    "SUBSCRIPTION_STATE_IN_GRACE_PERIOD",
    "SUBSCRIPTION_STATE_CANCELED",
}


def _credentials():
    raw = os.getenv("GOOGLE_PLAY_SERVICE_ACCOUNT_JSON", "").strip()
    if not raw:
        raise RuntimeError("GOOGLE_PLAY_SERVICE_ACCOUNT_JSON is not configured")
    try:
        info = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError("GOOGLE_PLAY_SERVICE_ACCOUNT_JSON is invalid JSON") from exc
    return service_account.Credentials.from_service_account_info(
        info,
        scopes=["https://www.googleapis.com/auth/androidpublisher"],
    )


def _parse_time(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def verify_subscription(purchase_token: str, product_id: str) -> dict[str, Any]:
    if product_id not in ALLOWED_PRODUCTS:
        raise ValueError("Unknown RoboLab-X subscription product")
    package_name = os.getenv("ANDROID_PACKAGE_NAME", "com.synapsex.robotics.robolab_x").strip()
    if not package_name:
        raise RuntimeError("ANDROID_PACKAGE_NAME is not configured")

    service = build("androidpublisher", "v3", credentials=_credentials(), cache_discovery=False)
    try:
        data = (
            service.purchases()
            .subscriptionsv2()
            .get(packageName=package_name, token=purchase_token)
            .execute()
        )
    except Exception as exc:
        raise ValueError("Google Play could not verify this subscription") from exc

    state = data.get("subscriptionState")
    line_items = data.get("lineItems") or []
    matching = [item for item in line_items if item.get("productId") == product_id]
    if not matching:
        raise ValueError("Purchase token does not match the requested RoboLab-X product")

    now = datetime.now(timezone.utc)
    expiries = [_parse_time(item.get("expiryTime")) for item in matching]
    valid_expiries = [expiry for expiry in expiries if expiry and expiry > now]
    entitled = state in ENTITLED_STATES and bool(valid_expiries)
    if not entitled:
        raise ValueError("RoboLab-X Pro subscription is not currently entitled")

    expiry = max(valid_expiries)
    return {
        "verified": True,
        "product_id": product_id,
        "package_name": package_name,
        "subscription_state": state,
        "expires_at": expiry.isoformat(),
        "order_id": data.get("latestOrderId"),
    }
