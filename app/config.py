from pydantic_settings import BaseSettings
import os
from pathlib import Path

class Settings(BaseSettings):
    database_url: str = "sqlite:///./test.db"
    secret_key: str = "changeme"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    class Config:
        env_file = os.path.join(Path(__file__).parent.parent, ".env")

settings = Settings()