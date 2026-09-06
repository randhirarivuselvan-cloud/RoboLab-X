from __future__ import annotations

import json
from typing import Any
import httpx
from .config import get_settings

class ProviderError(RuntimeError):
    pass

MODEL_ENV = {
    "systems": "architect_model", "electronics": "circuit_model", "power": "circuit_model",
    "embedded": "code_model", "firmware": "code_model", "cpp": "code_model", "python": "code_model",
    "cad": "cad_model", "simulation": "cad_model", "verification": "verifier_model",
    "testing": "verifier_model", "auditor": "auditor_model", "lead": "architect_model",
}

GUARDRAILS = """You are an engineering specialist inside RoboLab-X. Be rigorous, skeptical and testable. Never invent datasheet values, pinouts, measurements, certifications or test results. Clearly label assumptions and estimates. For physical systems, check voltage, current, polarity, thermal limits, mechanical limits, signal compatibility and fault behavior. Challenge the design and report contradictions instead of agreeing automatically. Return valid JSON when requested."""

def _model_for(role: str, fallback: str) -> str:
    s = get_settings()
    attr = MODEL_ENV.get(role.lower())
    return (getattr(s, attr, "") if attr else "") or fallback

async def generate_with_provider(system: str, user: str, role: str = "lead") -> dict[str, Any]:
    s = get_settings()
    if s.ai_provider == "local":
        return {"mode": "local", "text": "External inference is disabled; deterministic engineering pipeline retained."}
    if not s.ai_base_url or not s.ai_api_key or not s.ai_model:
        raise ProviderError("AI provider configuration is incomplete")
    model = _model_for(role, s.ai_model)
    payload = {
        "model": model,
        "messages": [{"role": "system", "content": GUARDRAILS + "\n\n" + system}, {"role": "user", "content": user}],
        "temperature": 0.10,
        "top_p": 0.90,
        "response_format": {"type": "json_object"},
    }
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(90.0, connect=10.0)) as client:
            response = await client.post(s.ai_base_url.rstrip("/") + "/chat/completions", headers={"Authorization": f"Bearer {s.ai_api_key}", "Content-Type": "application/json"}, json=payload)
            response.raise_for_status()
            data = response.json()
        text = data["choices"][0]["message"]["content"]
        try:
            result = json.loads(text)
        except json.JSONDecodeError:
            result = {"text": text}
        return {"mode": "provider", "model": model, "role": role, "result": result}
    except (httpx.HTTPError, KeyError, IndexError, TypeError, ValueError) as exc:
        raise ProviderError(f"AI provider request failed: {exc}") from exc
