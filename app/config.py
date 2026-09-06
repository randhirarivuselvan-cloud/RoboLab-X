from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "RoboLab X"
    environment: str = "production"
    api_prefix: str = "/api"
    ai_provider: str = "openai_compatible"
    ai_base_url: str = ""
    ai_model: str = ""
    ai_api_key: str = ""
    allowed_origins: str = "*"
    rate_limit: str = "30/minute"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore")

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
