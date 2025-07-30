from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from .logger_config import logger
import pathlib


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    # Define your settings here
    LIVEKIT_URL: Optional[str]
    LIVEKIT_API_KEY: Optional[str]
    LIVEKIT_API_SECRET: Optional[str]
    OPENAI_API_KEY: Optional[str]
    DEEPGRAM_API_KEY: Optional[str]
    CARTESIA_API_KEY: Optional[str]

env_file_path = pathlib.Path(__file__).parent / ".env"
settings = Settings(_env_file=env_file_path, _env_file_encoding="utf-8")
logger.info("Settings loaded from %s", env_file_path)
