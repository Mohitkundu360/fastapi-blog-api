from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""

    # Database
    database_url: str = "sqlite:///./blog.db"

    # JWT
    secret_key: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # App
    app_name: str = "Blog API"
    debug: bool = True

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    """Get cached settings"""
    return Settings()