from __future__ import annotations

from pathlib import Path
from functools import lru_cache
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    data_dir: Path = Field(default=Path("./data"))
    log_level: str = Field(default="INFO")
    ntp_server: str = Field(default="pool.ntp.org")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
