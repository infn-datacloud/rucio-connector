from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    RUCIO_HOST: str
    AUTH_HOST: str
    ACCOUNT: str
    USERNAME: str
    PASSWORD: str

    class Config:
        env_file = ".env"

# LRU-cached getter
@lru_cache()
def get_settings() -> Settings:
    return Settings()
