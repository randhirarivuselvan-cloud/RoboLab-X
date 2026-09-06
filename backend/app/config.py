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
    rate_limit_per_minute: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))

@lru_cache
def get_settings() -> Settings:
    return Settings()
