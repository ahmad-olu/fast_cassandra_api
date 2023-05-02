import os
from pydantic import BaseSettings, Field
from functools import lru_cache


if os.getenv("CQLENG_ALLOW_SCHEMA_MANAGEMENT") is None:
    os.environ["CQLENG_ALLOW_SCHEMA_MANAGEMENT"] = "1"

class Settings(BaseSettings):
    secret_key: str = Field(..., env= 'SECRET_KEY')
    algorithm: str = Field(..., env= 'ALGORITHM')
    access_token_expire_minutes: int = Field(..., env= 'ACCESS_TOKEN_EXPIRE_MINUTES')
    astra_db_client_id: str = Field(..., env ='ASTRA_DB_CLIENT_ID')
    astra_db_client_secret: str = Field(..., env ='ASTRA_DB_CLIENT_SECRET')
    astra_db_app_token: str = Field(..., env ='ASTRA_DB_APP_TOKEN')
    environment_representation: int =Field(..., env="ENVIRONMENT_REPRESENTATION")

    class Config:
        env_file = ".env"

@lru_cache
def get_settings():
    return Settings()


