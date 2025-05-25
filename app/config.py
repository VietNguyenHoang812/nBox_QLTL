from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # PostgreSQL connection settings
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "9010"
    POSTGRES_DB: str = "file_storage"
    
    # Directory to store uploaded files
    UPLOAD_DIR: str = "./uploads"
    
    @property
    def DATABASE_URL(self) -> str:
        """Construct the database URL from settings."""
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    class Config:
        env_file = ".env"


settings = Settings()