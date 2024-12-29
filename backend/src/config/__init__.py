from functools import lru_cache
import os

from pydantic import Field, PostgresDsn, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):  # type: ignore
    database_url: PostgresDsn
    debug: bool = Field(default=False)
    prompts: str = Field(description="path to the agents prompts")

    @field_validator("database_url")
    def check_db_name(cls, v):
        assert v.path and len(v.path) > 1, "database must be provided"
        return v

    @field_validator("debug")
    def check_debug(cls, v):
        assert isinstance(v, bool), "debug must be a boolean"
        return v


@lru_cache
def get_settings() -> Settings:
    env = {}
    for variable in Settings.model_fields:
        env[variable] = os.environ.get(variable.upper())
    settings = Settings(**env)  # type: ignore
    return settings
