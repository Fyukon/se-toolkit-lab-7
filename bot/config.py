from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import os

class Settings(BaseSettings):
    BOT_TOKEN: Optional[str] = None
    LMS_API_URL: str = "http://localhost:8000"
    LMS_API_KEY: str = "placeholder_key"
    LLM_API_KEY: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=(
            ".env.bot.secret", 
            ".env.bot.example",
            "../.env.bot.secret",
            "../.env.bot.example"
        ),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
