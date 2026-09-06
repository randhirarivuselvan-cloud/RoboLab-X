from __future__ import annotations

import json
from typing import Any
import httpx
from .config import get_settings

class ProviderError(RuntimeError):
    pass

async def generate_with_provider(system: str, user: str) -> dict[str, Any]:
    s = get_settings()
    if s.ai_provider == "local":
        return {"mode": "local", "text": "External inference is disabled; use the deterministic engineering pipeline."}
    if not s.ai_base_url or not s.ai_api_key or not s.ai_model:
        raise ProviderError("AI provider is selected but AI_BASE_URL, AI_MODEL or AI_API_KEY is missing")
    url = s.ai_base_url.rstrip("/") + "/chat/completions"
    headers = {"Authorization": f"Bearer {s.ai_api_key}", "Content-Type": "application/json"}
    payload = {
        "model": s.ai_model,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        "temperature": 0.15,
        "response_format": {"type": "json_object"},
    }
    try:
        async with httpx.AsyncClient(timeout=90) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
        text = data["choices"][0]["message"]["content"]
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            parsed = {"text": text}
        return {"mode": "provider", "model": s.ai_model, "result": parsed}
    except (httpx.HTTPError, KeyError, IndexError, TypeError) as exc:
        raise ProviderError(f"AI provider request failed: {exc}") from exc
