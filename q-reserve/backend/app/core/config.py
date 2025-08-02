from typing import List, Optional
from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://qreserve:password@localhost:5432/qreserve"
    redis_url: str = "redis://localhost:6379"
    
    # JWT
    secret_key: str = "your-super-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # Email
    smtp_host: str = "localhost"
    smtp_port: int = 587
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None
    from_email: str = "noreply@qreserve.com"
    from_name: str = "q-reserve"
    
    # File Storage
    upload_dir: str = "uploads"
    max_file_size: int = 10485760  # 10MB
    allowed_extensions: str = "jpg,jpeg,png,gif,pdf,doc,docx,txt"
    
    # Application
    debug: bool = True
    environment: str = "development"
    base_url: str = "http://localhost:8000"
    
    # Security
    cors_origins: str = "http://localhost:8000,http://127.0.0.1:8000"
    rate_limit_per_minute: int = 60
    
    # Celery
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/0"
    
    @validator("cors_origins")
    def parse_cors_origins(cls, v):
        return [origin.strip() for origin in v.split(",")]
    
    @validator("allowed_extensions")
    def parse_allowed_extensions(cls, v):
        return [ext.strip().lower() for ext in v.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings() 