from pydantic import Field
from functools import lru_cache
from pydantic_settings import BaseSettings
from typing import Annotated, List


class Settings(BaseSettings):
    RUCIO_HOST: Annotated[
        str,
        Field(
            default="",
            description="Rucio host URL to connect to the Rucio API",
        ),
    ]
    AUTH_HOST: Annotated[
        str,
        Field(
            default="",
            description="Rucio authentication host URL",
        ),
    ]
    ACCOUNT: Annotated[
        str,
        Field(
            default="",
            description="Rucio account name",
        ),
    ]
    USERNAME: Annotated[
        str,
        Field(
            default="",
            description="Rucio username",
        ),
    ]
    PASSWORD: Annotated[
        str,
        Field(
            default="",
            description="Rucio password",
        ),
    ]
    ALLOWED_ORIGINS: Annotated[
        List[str],
        Field(
            default=["https://127.0.0.1:5000", "https://localhost:5000"],
            description="List of allowed CORS origins",
        ),
    ]

    class Config:
        env_file = ".env"


# LRU-cached getter
@lru_cache()
def get_settings() -> Settings:
    return Settings()
