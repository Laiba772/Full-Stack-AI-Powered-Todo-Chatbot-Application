# config.py
"""Configuration management using Pydantic BaseSettings."""
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    database_url: str

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # JWT Authentication
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 15  # Short-lived access tokens
    jwt_refresh_expiration_hours: int = 168  # Longer refresh tokens
    bcrypt_rounds: int = 12

    # Security
    access_token_cookie_name: str = "access_token"
    refresh_token_cookie_name: str = "refresh_token"
    csrf_token_header_name: str = "x-csrf-token"
    csrf_secret: str = ""

    # Rate Limiting
    rate_limit_requests: int = 100
    rate_limit_window: int = 3600  # in seconds

    # Debug
    debug: bool = False

    # Logging
    log_level: str = "info"

    # CORS
    cors_origins: list[str] = ["http://localhost:3000"]

    # OpenAI
    openai_api_key: str
    openai_model: str = "gpt-3.5-turbo"
    openai_agent_model: str = "gpt-4-turbo-preview"  # Model for AI agent
    openai_agent_max_tokens: int = 4096 # Max tokens for AI agent response
    ai_agent_system_prompt: str = (
        "You are a helpful AI assistant. Your primary goal is to assist users with their tasks. "
        "Be concise and respond directly to the user's request. "
        "If you need more information, ask clarifying questions."
    )

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "ignore"
    }


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
# Global settings instance
settings = get_settings()
