from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Financial Engine"
    app_env: str = "development"
    debug: bool = True
    secret_key: str = "change-me-to-a-long-random-shared-secret-across-all-apps"
    database_url: str = "postgresql://stem:stem_secret@localhost:5432/financial_engine"
    iam_url: str = "http://localhost:8001"
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    app_slug: str = "financial-engine"

    @property
    def cors_origins_list(self) -> List[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
