from functools import lru_cache
import os
from pydantic import BaseModel

class Settings(BaseModel):
    app_name: str = "RoboLab-X"
    environment: str = os.getenv("ENVIRONMENT", "production")
    cors_origins: str = os.getenv("CORS_ORIGINS", "*")
    ai_provider: str = os.getenv("AI_PROVIDER", "local")
    ai_base_url: str = os.getenv("AI_BASE_URL", "")
    ai_model: str = os.getenv("AI_MODEL", "")
    ai_api_key: str = os.getenv("AI_API_KEY", "")
    # Optional specialist overrides. Keep secrets server-side only.
    architect_model: str = os.getenv("ARCHITECT_MODEL", "")
    circuit_model: str = os.getenv("CIRCUIT_MODEL", "")
    code_model: str = os.getenv("CODE_MODEL", "")
    cad_model: str = os.getenv("CAD_MODEL", "")
    verifier_model: str = os.getenv("VERIFIER_MODEL", "")
    compiler_model: str = os.getenv("COMPILER_MODEL", "")
    auditor_model: str = os.getenv("AUDITOR_MODEL", "")
    pro_beta_enabled: bool = os.getenv("PRO_BETA_ENABLED", "true").lower() in {"1", "true", "yes", "on"}
    rate_limit_per_minute: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))

@lru_cache
def get_settings() -> Settings:
    return Settings()
