"""
Configuration module for ReLaunchAI backend.
Handles environment variables and application settings.
"""

import os
from dotenv import load_dotenv
# from pydantic_settings import BaseSettings
from pydantic import BaseSettings
from pydantic import Field

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # SambaNova API Configuration
    sambanova_api_key: str = Field(default="", alias="SAMBANOVA_API_KEY")
    sambanova_model: str = Field(default="Meta-Llama-3.1-8B-Instruct", alias="SAMBANOVA_MODEL")
    sambanova_base_url: str = Field(default="https://api.sambanova.ai/v1", alias="SAMBANOVA_BASE_URL")
    
    # Application Settings
    app_name: str = Field(default="ReLaunchAI", alias="APP_NAME")
    app_version: str = Field(default="1.0.0", alias="APP_VERSION")
    debug: bool = Field(default=False, alias="DEBUG")
    
    # API Settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        populate_by_name = True


# Global settings instance
settings = Settings()


def get_ai_client():
    """Initialize and return SambaNova AI client."""
    from sambanova import SambaNova
    
    if not settings.sambanova_api_key or settings.sambanova_api_key == "your_sambanova_api_key_here":
        raise ValueError("SambaNova API key not configured. Please set SAMBANOVA_API_KEY in .env file.")
    
    # Clean base_url (remove trailing spaces)
    base_url = settings.sambanova_base_url.strip()
    
    return SambaNova(
        api_key=settings.sambanova_api_key,
        base_url=base_url
    )
