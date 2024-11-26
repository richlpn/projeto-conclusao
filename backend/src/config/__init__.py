from functools import lru_cache

from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):  # type: ignore
    database_url: PostgresDsn


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    return settings
