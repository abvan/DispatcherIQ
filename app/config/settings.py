"""
Application configuration and environment variables
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # API Settings
    app_name: str = "DispatcherIQ"
    app_version: str = "0.1.0"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    
    # LLM Settings
    llm_provider: str = "openai"  # or "anthropic", "cohere", etc.
    openai_api_key: Optional[str] = None
    model_name: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 2048
    
    # Langraph Settings
    checkpointer_type: str = "memory"  # or "postgres", "sqlite"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
