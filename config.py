from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Optional: Load .env early (especially useful for debugging or non-ASGI contexts)
load_dotenv()

class Settings(BaseSettings):
    RUCIO_HOST: str
    AUTH_HOST: str
    ACCOUNT: str
    USERNAME: str
    PASSWORD: str

    class Config:
        env_file = ".env"

settings = Settings()