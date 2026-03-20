from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import os

class Settings(BaseSettings):
    BOT_TOKEN: Optional[str] = None
    LMS_API_URL: str = "http://localhost:42002"
    LMS_API_KEY: str = "alex"
    
    # LLM Settings
    LLM_API_KEY: Optional[str] = "alex_qwen"
    LLM_API_BASE_URL: str = "http://localhost:42005"
    LLM_API_MODEL: str = "coder-model"

    model_config = SettingsConfigDict(
        env_file=(
            ".env.bot.secret", 
            ".env.bot.example",
            "../.env.bot.secret",
            "../.env.bot.example"
        ),
        env_file_encoding="utf-8",
        extra="ignore",
        env_nested_delimiter="__"
    )

settings = Settings()
