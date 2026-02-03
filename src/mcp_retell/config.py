"""Pydantic Settings configuration for Retell MCP server."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Retell AI API configuration.

    Reads from environment variables with RETELL_ prefix or .env file.
    """

    api_key: str = Field(default="", description="Retell API key")
    base_url: str = Field(
        default="https://api.retellai.com",
        description="Retell API base URL",
    )

    model_config = SettingsConfigDict(
        env_prefix="RETELL_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


def get_settings() -> Settings:
    """Get configuration from environment variables or .env file."""
    return Settings()
