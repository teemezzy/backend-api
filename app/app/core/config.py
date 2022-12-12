from typing import List

from pydantic import AnyHttpUrl, BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    JWT_SECRET_KEY: str
    ENCODING_KEY: str
    ENVIRONMENT: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 31
    DASHBOARD_HOST: AnyHttpUrl
    
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
     
     
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_INSTANCE_NAME: str
    
    FIRST_USER_EMAIL: str
    FIRST_USER_PASSWORD: str
    
    LOG_LEVEL: str = "INFO"
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
