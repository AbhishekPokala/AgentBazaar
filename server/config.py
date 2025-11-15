from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Database
    DATABASE_URL: str
    
    # API Keys
    ANTHROPIC_API_KEY: Optional[str] = None
    
    # Agent Service URLs
    SUMMARIZER_URL: str = "http://localhost:8001"
    TRANSLATOR_URL: str = "http://localhost:8002"
    SEARCH_URL: str = "http://localhost:8003"
    MOCK_BUSY_URL: str = "http://localhost:8004"
    MOCK_HIGHPRICE_URL: str = "http://localhost:8005"
    MOCK_NEGOTIATOR_URL: str = "http://localhost:8006"
    
    # HubChat
    HUBCHAT_ENABLED: bool = True
    
    # Server
    SERVER_PORT: int = 8000
    CORS_ORIGINS: str = "http://localhost:5000"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
