from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

   # Async version (used by FastAPI + SQLAlchemy)
    DATABASE_URL: str = "postgresql+asyncpg://postgres:amey@localhost:5433/AI_Job_Application_Tracker"
    # Sync version (used by Alembic migrations only)
    DATABASE_URL_SYNC: str = "postgresql+psycopg2://postgres:amey@localhost:5433/AI_Job_Application_Tracker"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Auth
    SECRET_KEY: str 
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Groq AI
    GROQ_API_KEY: str
    GROQ_MODEL_EXTRACTION: str = "llama-3.1-8b-instant"
    GROQ_MODEL_REASONING: str = "llama-3.3-70b-versatile"

    # Email
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""

    # App
    ENVIRONMENT: str = "development"
    MAX_UPLOAD_SIZE_MB: int = 10
    AI_MAX_RETRIES: int = 3

    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT == "development"

    @property
    def max_upload_size_bytes(self) -> int:
        return self.MAX_UPLOAD_SIZE_MB * 1024 * 1024


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()