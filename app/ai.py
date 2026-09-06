from typing import Any
import httpx
from .config import settings

SYSTEM = """You are RoboLab Core, a professional robotics engineering assistant. Produce structured, testable engineering work. State assumptions, constraints, risks, and verification steps. Never invent unavailable measurements or claim hardware was tested when it was not."""

class AIError(RuntimeError):
    pass

async def generate(prompt: str, context: dict[str, Any] | None = None) -> str:
    if not settings.ai_api_key or not settings.ai_base_url or not settings.ai_model:
        return local_fallback(prompt)
    payload = {
        "model": settings.ai_model,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": prompt + (f"\nProject context: {context}" if context else "")},
        ],
        "temperature": 0.15,
    }
    headers = {"Authorization": f"Bearer {settings.ai_api_key}", "Content-Type": "application/json"}
    try:
        async with httpx.AsyncClient(timeout=90) as client:
            response = await client.post(settings.ai_base_url.rstrip("/") + "/chat/completions", json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
    except Exception as exc:
        raise AIError(f"AI provider unavailable: {exc}") from exc


def local_fallback(prompt: str) -> str:
    return (
        "RoboLab Core is running in deterministic offline mode.\n\n"
        "Request: " + prompt.strip() + "\n\n"
        "Next steps:\n"
        "1. Define the target board/controller and power source.\n"
        "2. Identify sensors, actuators, interfaces, and voltage/current requirements.\n"
        "3. Generate implementation and wiring only after constraints are explicit.\n"
        "4. Verify pin conflicts, power paths, dependencies, and failure states before deployment."
    )
