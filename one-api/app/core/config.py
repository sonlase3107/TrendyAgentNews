from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    app_name: str = "ONE API"
    app_version: str = "0.1.0"
    environment: str = "development"
    db_path: str = "one_api.db"

    model_config = SettingsConfigDict(env_prefix="ONE_API_", extra="ignore")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached settings instance for the app lifecycle."""
    return Settings()
