from functools import lru_cache
import os

from pydantic import PostgresDsn, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):  # type: ignore
    database_url: PostgresDsn

    @field_validator("database_url")
    def check_db_name(cls, v):
        assert v.path and len(v.path) > 1, "database must be provided"
        return v


@lru_cache
def get_settings() -> Settings:
    settings = Settings(os.getenv("POSTGRES_DB"))  # type: ignore
    return settings
