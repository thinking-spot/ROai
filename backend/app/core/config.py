"""
Application configuration using Pydantic Settings
"""
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field, validator


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """

    # Application
    APP_NAME: str = "AI ROI Analytics Platform"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    # API
    API_V1_PREFIX: str = "/api/v1"
    SECRET_KEY: str = Field(..., min_length=32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 5
    DATABASE_MAX_OVERFLOW: int = 10

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_CACHE_TTL: int = 3600

    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]

    @validator("ALLOWED_ORIGINS", pre=True)
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            # Handle both JSON array string and comma-separated string
            if v.startswith("["):
                import json
                return json.loads(v)
            return [origin.strip() for origin in v.split(",")]
        return v

    # Google OAuth & API
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = ""

    # Microsoft OAuth & API
    MICROSOFT_CLIENT_ID: str = ""
    MICROSOFT_CLIENT_SECRET: str = ""
    MICROSOFT_TENANT_ID: str = ""
    MICROSOFT_REDIRECT_URI: str = ""

    # OpenAI
    OPENAI_API_KEY: str = ""

    # Anthropic
    ANTHROPIC_API_KEY: str = ""

    # Jira
    JIRA_API_TOKEN: str = ""

    # GitHub
    GITHUB_TOKEN: str = ""

    # Salesforce
    SALESFORCE_CLIENT_ID: str = ""
    SALESFORCE_CLIENT_SECRET: str = ""

    # Zendesk
    ZENDESK_SUBDOMAIN: str = ""
    ZENDESK_EMAIL: str = ""
    ZENDESK_API_TOKEN: str = ""

    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"

    # Email
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    EMAILS_FROM_EMAIL: str = ""
    EMAILS_FROM_NAME: str = ""

    # Analytics Settings
    METRICS_RETENTION_DAYS: int = 90
    ATTRIBUTION_CONFIDENCE_THRESHOLD: float = 0.95
    MIN_SAMPLE_SIZE: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()
