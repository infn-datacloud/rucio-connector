import logging
from pydantic import Field, BeforeValidator, AnyHttpUrl
from functools import lru_cache
from pydantic_settings import BaseSettings
from typing import Annotated, List
from enum import Enum
from fastapi import Depends


class AuthenticationMethodsEnum(str, Enum):
    """Enumeration of supported authentication methods."""

    local = "local"


class AuthorizationMethodsEnum(str, Enum):
    """Enumeration of supported authorization methods."""

    opa = "opa"


class LogLevelEnum(int, Enum):
    """Enumeration of supported logging levels."""

    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


def get_level(value: int | str | LogLevelEnum) -> int:
    """Convert a string, integer, or LogLevelEnum value to a logging level integer.

    Args:
        value: The log level as a string (case-insensitive), integer, or LogLevelEnum.

    Returns:
        int: The corresponding logging level integer.

    """
    if isinstance(value, str):
        return LogLevelEnum.__getitem__(value.upper())
    return value


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
    AUTHN_MODE: Annotated[
        AuthenticationMethodsEnum | None,
        Field(
            default=None,
            description="Authorization method to use. Allowed values: local",
        ),
    ]
    AUTHZ_MODE: Annotated[
        AuthorizationMethodsEnum | None,
        Field(
            default=None,
            description="Authorization method to use. Allowed values: opa",
        ),
    ]
    TRUSTED_IDP_LIST: Annotated[
        list[AnyHttpUrl],
        Field(
            default_factory=list,
            description="List of the application trusted identity providers",
        ),
    ]
    LOG_LEVEL: Annotated[
        LogLevelEnum,
        Field(default=LogLevelEnum.INFO, description="Logs level"),
        BeforeValidator(get_level),
    ]

    class Config:
        env_file = ".env"


# LRU-cached getter
@lru_cache()
def get_settings() -> Settings:
    return Settings()


SettingsDep = Annotated[Settings, Depends(get_settings)]
