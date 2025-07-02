"""Main entry point for the Rucio Connector API.

This module sets up the FastAPI application, configures middleware, authentication,
and provides endpoints to interact with Rucio for retrieving RSEs.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Security
from fastapi.middleware.cors import CORSMiddleware

from api.rucio import get_rses
from auth import check_authorization, configure_flaat
from config import get_settings
from logger import get_logger

settings = get_settings()

title = "Rucio Connector API"
summary = "Rucio Connector REST API"
description = "This API provides endpoints to interact with Rucio, a data management "
"system for scientific data. It allows users to retrieve RSEs (Rucio Storage Elements) "
"for specific datasets identified by their scope and name."
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
    description="Retrieve a list of RSEs for a given DID.",
    dependencies=[Security(check_authorization)],
)
async def get_rses_endpoint(did_scope: str, did_name: str):
    """Asynchronously retrieve the list of RSEs associated with a given DID.

    Use scope and name to define the target DID.

    Args:
        did_scope (str): The scope of the data identifier.
        did_name (str): The name of the data identifier.

    Returns:
        list: A list of RSEs associated with the specified DID.

    Example:
        rses = await get_rses_endpoint("scope", "name")

    """
    rses = get_rses(did_scope, did_name)

    return rses
