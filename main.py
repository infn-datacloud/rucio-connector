from fastapi import FastAPI, Security
from api.rucio import get_rses
from fastapi.middleware.cors import CORSMiddleware
from config import get_settings
from contextlib import asynccontextmanager
from auth import configure_flaat, check_authorization
from logger import get_logger

settings = get_settings()

title = "Rucio Connector API"
summary = "Rucio Connector REST API"
description = "This API provides endpoints to interact with Rucio, a data management system for scientific data. It allows users to retrieve RSEs (Rucio Storage Elements) for specific datasets identified by their scope and name."
version = "0.1.0"
docs_url = "/docs"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI application lifespan context manager.

    This function is called at application startup and shutdown. It performs:
    - Initializes the application logger and attaches it to the request state.
    - Configures authentication/authorization (Flaat).

    Args:
        app: The FastAPI application instance.

    Yields:
        dict: A dictionary with the logger instance, available in the request state.

    """
    logger = get_logger(settings)
    configure_flaat(settings, logger)
    yield {"logger": logger}


# Create FastAPI app
app = FastAPI(
    title=title,
    summary=summary,
    description=description,
    version=version,
    docs_url=docs_url,
    lifespan=lifespan,
)

# Allow specific origin
origins = settings.ALLOWED_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] to allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/rses",
    summary="Retrieve RSEs",
    description="Retrieve a list of RSEs for a given dataset.",
    dependencies=[Security(check_authorization)],
)
async def get_rses_endpoint(did_scope: str, did_name: str):
    """
    Endpoint to retrieve RSEs for a given did scope and name.
    """

    rses = get_rses(did_scope, did_name)

    return rses


# print(get_rses('user.atroja', 'test_TPC'))
